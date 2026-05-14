import requests
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {}
if GITHUB_TOKEN and GITHUB_TOKEN != "your_github_personal_access_token_here":
    HEADERS["Authorization"] = f"token {GITHUB_TOKEN}"


def fetch_usernames(count=40):
    """Search GitHub for users with 5+ repos in India."""
    usernames = []
    per_page = 30
    pages_needed = -(-count // per_page)  # ceiling division

    for page in range(1, pages_needed + 1):
        url = "https://api.github.com/search/users"
        params = {
            "q": "location:india repos:>5",
            "per_page": per_page,
            "page": page,
        }
        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            items = response.json().get("items", [])
            usernames.extend([u["login"] for u in items])
            logging.info(f"Page {page}: fetched {len(items)} usernames")
        except requests.RequestException as e:
            logging.error(f"Failed to fetch usernames on page {page}: {e}")
            break

    # TODO: add pagination to fetch beyond 150 results if needed
    return usernames[:count]


def fetch_profile(username):
    """Fetch full profile data for a single GitHub user."""
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        return {
            "Name": data.get("name"),
            "Email": data.get("email"),
            "Website": data.get("blog"),
            "Location": data.get("location"),
            "GitHub Profile": data.get("html_url"),
        }
    except requests.RequestException as e:
        logging.warning(f"Could not fetch profile for {username}: {e}")
        return None


def collect_leads(count=40):
    """Run full collection: search → profiles → raw list of dicts."""
    logging.info("Starting lead collection from GitHub API")
    usernames = fetch_usernames(count)
    raw_profiles = []

    for username in usernames:
        profile = fetch_profile(username)
        if profile:
            raw_profiles.append(profile)
        time.sleep(0.5)

    logging.info(f"Collection complete. {len(raw_profiles)} raw profiles fetched.")
    return raw_profiles