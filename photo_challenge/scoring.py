from collections import defaultdict

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
