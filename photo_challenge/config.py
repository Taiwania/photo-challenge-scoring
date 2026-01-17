import os

# Constants
API_URL = "https://commons.wikimedia.org/w/api.php"
REGISTRATION_THRESHOLD_DAYS = 10
EDIT_COUNT_THRESHOLD = 50

def load_env():
    """Load .env manually to avoid dependencies"""
    # Assuming the package is one level deep (photo_challenge/), so we go up one level to find .env
    # Current file: .../photo_challenge/config.py
    # .env: .../.env
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    # Handle lines that might not have = or handle empty values
                    parts = line.strip().split('=', 1)
                    if len(parts) == 2:
                        key, val = parts
                        os.environ[key] = val
