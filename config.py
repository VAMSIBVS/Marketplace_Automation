from pathlib import Path
from datetime import datetime

TODAY = datetime.now().strftime("%Y-%m-%d")
REPORT_DATE = datetime.now().date()

BASE_DIR = Path(__file__).resolve().parent
DATA_FOLDER = BASE_DIR / "data" / TODAY
REPORTS_FOLDER = BASE_DIR / "reports"
REPORTS_FOLDER.mkdir(exist_ok=True)

OUTPUT_FILE = REPORTS_FOLDER / f"overall_marketplaces_{TODAY}.xlsx"