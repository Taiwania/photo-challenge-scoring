import urllib.request
import urllib.parse
import json
import os
import datetime
from . import config

def make_api_query(params):
    params['format'] = 'json'
    url = f"{config.API_URL}?{urllib.parse.urlencode(params)}"
    
    bot_username = os.getenv('COMMONS_BOT_USERNAME', 'Anonymous')
    bot_email = os.getenv('COMMONS_BOT_EMAIL', 'anonymous@example.com')
    user_agent = f'CommonsPhotoChallengeScoringBot/1.0.1 (https://commons.wikimedia.org/wiki/User:{bot_username}; {bot_email})'
    
    req = urllib.request.Request(url, headers={'User-Agent': user_agent})
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
                 # Usually the first one is the latest (current) revision
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
    
    cutoff_date = challenge_end_date - datetime.timedelta(days=config.REGISTRATION_THRESHOLD_DAYS)
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
            
            if editcount >= config.EDIT_COUNT_THRESHOLD:
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
                reason.append(f"Edit count {editcount} < {config.EDIT_COUNT_THRESHOLD}")
            
            if not is_eligible:
                 # Check if reason is empty (meaning edit count was fine but reg was failing, or vice versa)
                 if not reason: reason.append("Unknown criteria failure")
                 
            eligibility[name] = {'eligible': is_eligible, 'reason': "; ".join(reason)}
            
    return eligibility
