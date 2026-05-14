import logging
import os
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)

RAW_OUTPUT_PATH = os.path.join("data", "raw", "leads_raw.xlsx")


def export_leads(df: pd.DataFrame):
    """Save cleaned leads DataFrame to raw Excel file."""
    os.makedirs(os.path.join("data", "raw"), exist_ok=True)
    try:
        df.to_excel(RAW_OUTPUT_PATH, index=False, engine="openpyxl")
        logging.info(
            f"leads_raw.xlsx saved to {RAW_OUTPUT_PATH} ({len(df)} rows)"
        )
    except IOError as e:
        logging.error(f"Failed to write Excel file: {e}")