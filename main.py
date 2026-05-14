import logging
from pipeline import collect_leads, clean_leads, export_leads

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


def run_pipeline():
    """Collect → Clean → Export. Full lead generation pipeline."""
    logging.info("Pipeline started")

    raw_profiles = collect_leads(count=150)
    cleaned_df = clean_leads(raw_profiles)
    export_leads(cleaned_df)

    logging.info("Pipeline finished. Check data/raw/leads_raw.xlsx")


if __name__ == "__main__":
    run_pipeline()