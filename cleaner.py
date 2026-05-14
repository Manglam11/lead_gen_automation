import re
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")


def extract_username(github_url):
    """Pull username from GitHub profile URL."""
    if isinstance(github_url, str) and github_url:
        return github_url.rstrip("/").split("/")[-1]
    return None


def is_valid_email(email):
    """Return True if email matches standard format."""
    if not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def clean_leads(raw_profiles):
    """Clean raw profile list and return a cleaned DataFrame."""
    df = pd.DataFrame(raw_profiles)
    logging.info(f"Raw entries received: {len(df)}")

    df.drop_duplicates(subset=["GitHub Profile"], inplace=True)
    logging.info(f"After removing duplicates: {len(df)}")

    # Strip whitespace from all string fields
    str_columns = ["Name", "Email", "Website", "Location"]
    for col in str_columns:
        df[col] = df[col].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    # Replace empty strings with None so fillna works correctly
    df.replace("", None, inplace=True)

    # Fill missing values
    df["Location"] = df["Location"].fillna("Not Specified")
    df["Website"] = df["Website"].fillna("N/A")
    df["Name"] = df["Name"].fillna(df["GitHub Profile"].apply(
        lambda x: extract_username(x) or "Unknown"
    ))

    # Bonus Feature A — email generation
    def resolve_email(row):
        if is_valid_email(row["Email"]):
            return row["Email"], "real"
        username = extract_username(row["GitHub Profile"])
        if username:
            logging.warning(
                f"No real email for {username}, generating fallback"
            )
            return f"{username}@github.com", "generated"
        return "N/A", "unavailable"

    df[["Email", "Email Source"]] = df.apply(
        resolve_email, axis=1, result_type="expand"
    )

    logging.info(f"Cleaning complete. {len(df)} leads ready for export.")
    return df