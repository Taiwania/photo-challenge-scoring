import re
import datetime
import urllib.request
import json
import urllib.parse
from collections import defaultdict

# Constants
API_URL = "https://commons.wikimedia.org/w/api.php"
REGISTRATION_THRESHOLD_DAYS = 10
EDIT_COUNT_THRESHOLD = 50

def parse_challenge_date(content):
    # Pattern: ... midnight UTC on 31 December 2025 ...
    # Also handle typo: 31 Jaunary 2026
    # Allow variable whitespace between words
    match = re.search(r'midnight\s+UTC\s+on\s+(\d+)\s+([a-zA-Z]+)\s+(\d+)', content)
    if match:
        day = int(match.group(1))
        month_str = match.group(2)
        year = int(match.group(3))
        
        # Handle known typos and standard months
        month_map = {
            'January': 1, 'Jaunary': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
            'October': 10, 'November': 11, 'December': 12
        }
        
        month = month_map.get(month_str, 0)
        if month == 0:
            raise ValueError(f"Unknown month '{month_str}' in date string.")
            
        return datetime.datetime(year, month, day, 23, 59, 59)
    
    raise ValueError("Could not parse challenge end date from content.")

def make_api_query(params):
    params['format'] = 'json'
    url = f"{API_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'CommonsPhotoChallengeScoringBot/1.0.1 (https://commons.wikimedia.org/wiki/User:Taiwania_Justo; taiwaniajusto@gmail.com)'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"API Error: {e}")
        return {}

def get_image_authors(filenames):
    authors = {}
    # Batch requests (max 50 per request usually)
    chunk_size = 50
    chunks = [filenames[i:i + chunk_size] for i in range(0, len(filenames), chunk_size)]
    
    for chunk in chunks:
        titles = "|".join([f"File:{f}" for f in chunk])
        params = {
            "action": "query",
            "prop": "imageinfo",
            "iiprop": "user|timestamp",
            "titles": titles
        }
        data = make_api_query(params)
        pages = data.get('query', {}).get('pages', {})
        for page_id, page in pages.items():
            if 'imageinfo' in page:
                 # Usually the first one is the latest (current) revision, which is what we want for Uploader? 
                 # Actually for challenges usually it's the uploader of the *entry*, which is the initial revision or the one who nominated it.
                 # Taking the latest 'user' from imageinfo is usually the last uploader/overwriter. 
                 # Ideally we want the first revision user? Or assume current file version uploader is the participant.
                 # Let's use the 'user' from the imageinfo, which defaults to latest version. 
                 # Given it's a photo challenge, the file is likely uploaded by the author.
                 authors[page['title'].replace("File:", "")] = page['imageinfo'][0]['user']
            elif 'missing' in page:
                 print(f"Warning: File missing: {page.get('title')}")
    return authors

def get_voter_eligibility(voters, participants, challenge_end_date):
    # Eligibility: 
    # 1. Registered > 10 days before challenge end
    # 2. Edit count > 50
    # OR
    # 3. Is a participant (in the authors list)
    
    eligibility = {}
    users_to_check = [v for v in voters if v not in participants]
    
    # Check participants are automatically eligible
    for p in participants:
         eligibility[p] = {'eligible': True, 'reason': 'Participant'}

    if not users_to_check:
        return eligibility

    chunk_size = 50
    chunks = [users_to_check[i:i + chunk_size] for i in range(0, len(users_to_check), chunk_size)]
    
    cutoff_date = challenge_end_date - datetime.timedelta(days=REGISTRATION_THRESHOLD_DAYS)
    cutoff_str = cutoff_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    for chunk in chunks:
        ususers = "|".join(chunk)
        params = {
            "action": "query",
            "list": "users",
            "usprop": "editcount|registration",
            "ususers": ususers
        }
        data = make_api_query(params)
        users = data.get('query', {}).get('users', [])
        
        for u in users:
            name = u.get('name')
            if 'missing' in u:
                eligibility[name] = {'eligible': False, 'reason': 'User not found'}
                continue
            
            editcount = u.get('editcount', 0)
            registration = u.get('registration')
            
            is_eligible = False
            reason = []
            
            if editcount >= EDIT_COUNT_THRESHOLD:
                # Check registration
                if registration:
                    # simplistic check: comparison of ISO strings works for YYYY-MM-DD
                    if registration < cutoff_str:
                         is_eligible = True
                    else:
                         reason.append(f"Registered after {cutoff_str} ({registration})")
                else:
                    # If registration is null (very old users), assume eligible if edit count is high?
                    # API returns null for very old users (pre-2005). Treat as eligible.
                    is_eligible = True
            else:
                reason.append(f"Edit count {editcount} < {EDIT_COUNT_THRESHOLD}")
            
            if not is_eligible:
                 # Check if reason is empty (meaning edit count was fine but reg was failing, or vice versa)
                 if not reason: reason.append("Unknown criteria failure")
                 
            eligibility[name] = {'eligible': is_eligible, 'reason': "; ".join(reason)}
            
    return eligibility


def parse_mw_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    image_pattern = re.compile(r'===\s*(\d+)\.\s*(.*?)\s*===(.*?)(?====\s*\d+\. |$)', re.DOTALL)
    matches = image_pattern.findall(content)
    
    images = []
    
    for rank_idx, title, body in matches:
        file_match = re.search(r'\[\[File:(.*?)\|', body)
        filename = file_match.group(1).split('|')[0] if file_match else "Unknown"
        # Cleanup filename
        filename = filename.strip()
        
        vote_pattern = re.compile(r'\*\{\{([0-3])/3\*\}\} -- \[\[User:(.*?)\|.*?\]\] (.*? \(UTC\))')
        vote_matches = vote_pattern.findall(body)
        
        parsed_votes = []
        for vote_val, user, timestamp_str in vote_matches:
            try:
                # 14:16, 11 January 2026 (UTC)
                # Cleaning up potential non-breaking spaces or other junk
                timestamp_str = timestamp_str.replace("(UTC)", "").strip()
                # Parse logic
                # Try multiple formats if needed
                ts = datetime.datetime.strptime(timestamp_str, '%H:%M, %d %B %Y')
            except ValueError:
                ts = datetime.datetime.min # Graceful fallback
            
            parsed_votes.append({
                'user': user.strip(),
                'raw_score': int(vote_val),
                'time': ts,
                'original_text': f"{vote_val}/3*"
            })
            
        images.append({
            'id': rank_idx,
            'title': title,
            'filename': filename,
            'votes': parsed_votes,
            'author': "Unknown" # Will fetch later
        })
        
    return images

def calculate_scores(images, author_map, eligibility_map):
    # Set authors
    participants = set()
    for img in images:
        fn = img['filename']
        if fn in author_map:
            img['author'] = author_map[fn]
            participants.add(author_map[fn])
        else:
            img['author'] = "Unknown"

    # Flatten votes
    user_votes = defaultdict(list)
    
    for img in images:
        for v in img['votes']:
            voter = v['user']
            
            # Validation 1: Eligibility
            # Assume eligibility map covers everyone (we will ensure it does in main)
            is_eligible = eligibility_map.get(voter, {'eligible': False}).get('eligible', False)
            if not is_eligible:
                v['vote_obj'] = v
                v['effective_score'] = 0
                v['is_valid'] = False # Marked invalid, doesn't even count for support
                v['invalid_reason'] = "Ineligible voter"
                continue

            # Validation 2: Self-voting
            if img['author'] == voter:
                v['vote_obj'] = v
                v['effective_score'] = 0
                v['is_valid'] = False
                v['invalid_reason'] = "Self-voting"
                continue

            v['is_valid'] = True # Potentially valid, check duplicates next
            
            user_votes[voter].append({
                'img_filename': img['filename'],
                'raw_score': v['raw_score'],
                'time': v['time'],
                'vote_obj': v 
            })
            
    # Process duplicate rank handling for eligible votes
    for user, votes in user_votes.items():
        votes.sort(key=lambda x: x['time'])
        
        used_weights = set()
        
        for v in votes:
            score = v['raw_score']
            if score > 0:
                if score in used_weights:
                    # Downgrade to 0 (Support)
                    effective = 0
                    # It is still "valid" in the sense it counts for support
                else:
                    effective = score
                    used_weights.add(score)
            else:
                effective = 0
            
            # Store effective score
            v['vote_obj']['effective_score'] = effective

    # Tally
    results = []
    
    # Define sets for stats
    active_contributors = set()
    valid_voters = set()

    for img in images:
        score_sum = 0
        support_count = 0
        
        for v in img['votes']:
            if not v.get('is_valid', False):
                continue
                
            eff = v.get('effective_score', 0)
            score_sum += eff
            # all valid votes count for support (0* counts for Support)
            support_count += 1
            valid_voters.add(v['user'])
        
        results.append({
            'filename': img['filename'],
            'author': img['author'],
            'score': score_sum,
            'support': support_count
        })
        
        if img['author'] != "Unknown":
            active_contributors.add(img['author'])

    # Sort: Score DESC, Support DESC
    results.sort(key=lambda x: (-x['score'], -x['support']))
    
    stats = {
        'contributors': len(active_contributors),
        'voters': len(valid_voters),
        'images': len(images)
    }
    
    return results, stats

def generate_mw_table(results, stats):
    out = []
    out.append(f"*Number of contributors: {stats['contributors']}")
    out.append(f"*Number of voters:       {stats['voters']}")
    out.append(f"*Number of images:       {stats['images']}")
    out.append("")
    out.append("The Score is the sum of the 3*/2*/1* votes. The Support is the count of 3*/2*/1* votes and 0* likes. In the event of a tie vote, the support decides the rank.")
    out.append("")
    out.append('{| class="sortable wikitable"')
    out.append('|-')
    out.append('! class="unsortable"| Image')
    out.append('! Author')
    out.append('! data-sort-type="number" | Rank')
    out.append('! data-sort-type="number" | Score')
    out.append('! data-sort-type="number" | Support')
    
    current_rank = 1
    for i, res in enumerate(results):
        rank = i + 1
        if i > 0:
            prev = results[i-1]
            if prev['score'] == res['score'] and prev['support'] == res['support']:
                rank = current_rank
            else:
                current_rank = rank
        else:
            current_rank = rank

        img_cell = f"[[File:{res['filename']}|120px]]"
        auth_cell = f"[[User:{res['author']}|{res['author']}]] ([[User talk:{res['author']}|<span class=\"signature-talk\">talk</span>]])" if res['author'] != "Unknown" else "Unknown"
        
        row = "|-\n"
        row += f"| {img_cell} || {auth_cell} || {current_rank} || {res['score']} || {res['support']}"
        out.append(row)
        
    out.append('|}')
    return "\n".join(out)

import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Calculate Commons Photo Challenge Scores")
    parser.add_argument("input_file", help="Path to the input MediaWiki file (e.g., imports/file.mw)")
    parser.add_argument("--output-dir", default="exports", help="Directory to save the output file")
    
    args = parser.parse_args()
    
    # Derive output filename
    base_name = os.path.splitext(os.path.basename(args.input_file))[0]
    output_filename = f"{base_name}-scoring.mw"
    output_path = os.path.join(args.output_dir, output_filename)
    
    print(f"Processing {args.input_file}...")
    
    mw_path = args.input_file
    
    # Read content primarily for date parsing
    with open(mw_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    challenge_end_date = parse_challenge_date(raw_content)
    print(f"Challenge End Date: {challenge_end_date}")
    
    images = parse_mw_file(mw_path)
    
    # 1. Collect all filenames
    filenames = [img['filename'] for img in images]
    print(f"Found {len(images)} images.")
    print("Fetching image authors...")
    authors = get_image_authors(filenames)
    
    # 2. Collect all voters
    all_voters = set()
    for img in images:
        for v in img['votes']:
            all_voters.add(v['user'])
            
    participants = set(authors.values())
    
    print(f"Checking eligibility for {len(all_voters)} voters...")
    eligibility = get_voter_eligibility(list(all_voters), participants, challenge_end_date)
    
    # 3. Calculate
    final_scores, stats = calculate_scores(images, authors, eligibility)
    
    # 4. Generate Output
    report = generate_mw_table(final_scores, stats)
    
    # Write to export
    os.makedirs(args.output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    print(f"Done. Export written to {output_path}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
