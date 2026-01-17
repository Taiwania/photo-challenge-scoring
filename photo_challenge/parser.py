import re
import datetime

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
