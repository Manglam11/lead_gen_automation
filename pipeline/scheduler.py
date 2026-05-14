import schedule
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)


def run_pipeline():
    """Import here to avoid circular imports at module level."""
    from pipeline.collector import collect_leads
    from pipeline.cleaner import clean_leads
    from pipeline.exporter import export_leads

    logging.info("Scheduled pipeline started")
    raw_profiles = collect_leads()
    cleaned_df = clean_leads(raw_profiles)
    export_leads(cleaned_df)
    logging.info("Scheduled pipeline complete")


def start_scheduler():
    """Run pipeline immediately, then every 6 hours."""
    run_pipeline()
    schedule.every(6).hours.do(run_pipeline)
    logging.info("Scheduler active — pipeline runs every 6 hours")

    while True:
        schedule.run_pending()
        time.sleep(60)