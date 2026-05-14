import logging
import os
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

OUTPUT_PATH = os.path.join("output", "leads.xlsx")


def export_leads(df: pd.DataFrame):
    """Save cleaned leads DataFrame to Excel file."""
    os.makedirs("output", exist_ok=True)
    try:
        df.to_excel(OUTPUT_PATH, index=False, engine="openpyxl")
        logging.info(f"leads.xlsx saved to {OUTPUT_PATH} ({len(df)} rows)")
    except IOError as e:
        logging.error(f"Failed to write Excel file: {e}")