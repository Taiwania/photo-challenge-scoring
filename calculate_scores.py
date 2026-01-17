import argparse
import os
from photo_challenge import config, parser as pc_parser, api, scoring, report

def main():
    arg_parser = argparse.ArgumentParser(description="Calculate Commons Photo Challenge Scores")
    arg_parser.add_argument("input_file", help="Path to the input MediaWiki file (e.g., imports/file.mw)")
    arg_parser.add_argument("--output-dir", default="exports", help="Directory to save the output file")
    
    args = arg_parser.parse_args()
    
    # Load environment variables
    config.load_env()

    # Derive output filename
    base_name = os.path.splitext(os.path.basename(args.input_file))[0]
    output_filename = f"{base_name}-scoring.mw"
    output_path = os.path.join(args.output_dir, output_filename)
    
    print(f"Processing {args.input_file}...")
    
    mw_path = args.input_file
    
    # Read content primarily for date parsing
    with open(mw_path, 'r', encoding='utf-8') as f:
        raw_content = f.read()
        
    try:
        challenge_end_date = pc_parser.parse_challenge_date(raw_content)
        print(f"Challenge End Date: {challenge_end_date}")
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return
    
    images = pc_parser.parse_mw_file(mw_path)
    
    # 1. Collect all filenames
    filenames = [img['filename'] for img in images]
    print(f"Found {len(images)} images.")
    print("Fetching image authors...")
    authors = api.get_image_authors(filenames)
    
    # 2. Collect all voters
    all_voters = set()
    for img in images:
        for v in img['votes']:
            all_voters.add(v['user'])
            
    participants = set(authors.values())
    
    print(f"Checking eligibility for {len(all_voters)} voters...")
    eligibility = api.get_voter_eligibility(list(all_voters), participants, challenge_end_date)
    
    # 3. Calculate
    final_scores, stats = scoring.calculate_scores(images, authors, eligibility)
    
    # 4. Generate Output
    mw_report = report.generate_mw_table(final_scores, stats)
    
    # Write to export
    os.makedirs(args.output_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(mw_report)
        
    print(f"Done. Export written to {output_path}")

if __name__ == "__main__":
    main()
