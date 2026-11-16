# Marketplace Report Automation 📊

An automated reporting pipeline that consolidates daily revenue and advertising spend across multiple e-commerce marketplaces (Amazon US, Amazon UK, Amazon AUS, Walmart, and eBay), calculates key performance metrics (including currency conversion to USD and ROAS), and exports styled Excel summary reports.

---

## 🚀 Overview

Tracking sales and advertising expenses across multiple global platforms often involves dealing with disjointed sources—CSVs, text summaries, and dashboard screenshots. 

**Marketplace Report Automation** streamlines this workflow:
1. **Reads heterogeneous source data** (CSVs and screenshot images via OCR).
2. **Fetches real-time exchange rates** (GBP/AUD to USD) to normalize financial performance.
3. **Calculates ROAS** (Return on Ad Spend) and grand totals.
4. **Generates publication-ready Excel reports** with custom styles and formatting.

---

## 🛠 Features

- **Multi-Platform Support**:
  - **Amazon US**: Screenshot OCR for Revenue, CSV for Campaign Spend.
  - **Amazon UK**: Screenshot OCR for Revenue, CSV for Campaign Spend (converted from GBP to USD).
  - **Amazon AUS**: Screenshot OCR for Revenue, CSV for Campaign Spend (converted from AUD to USD).
  - **Walmart**: CSV for Gross Merchandise Value (GMV), Screenshot OCR for Ad Spend.
  - **eBay**: Screenshot OCR for Total Sales and Ad Fees.
- **OCR Text Extraction**: Powered by `pytesseract` and `Pillow` to extract numerical revenue and spend values directly from dashboard screenshots (`.png`).
- **Live Currency Conversion**: Integrates with the open exchange rate API (`https://open.er-api.com`) to dynamically convert foreign currencies (GBP, AUD) into USD.
- **Performance Metrics**: Computes ROAS (`Revenue / Spend`) per marketplace and overall for the day.
- **Automated Excel Styling**: Formats tables with headers, totals, borders, and column alignments using `openpyxl`.

---

## 📁 Repository Structure

```text
Marketplace_Automation/
├── config.py             # Date configurations and directory path settings
├── calculations.py       # Currency conversion, exchange rate API, and ROAS calculations
├── excel_writer.py       # Excel workbook generation and openpyxl styling
├── main.py               # Main entry point orchestrating the workflow
├── readers.py            # Data ingestion: CSV parser and Tesseract OCR reader
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore file for Python environments and caches
├── data/                 # Dated folders containing daily input files (CSV, PNG, TXT)
│   ├── 2026-06-24/
│   ├── 2026-06-25/
│   └── ...
└── reports/              # Generated daily Excel reports
```

---

## ⚙️ Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR**:
   - For Windows: Download and install the Windows installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
   - Default configured path: `C:\Program Files\Tesseract-OCR\tesseract.exe` (can be customized in `readers.py`).

---

## 📦 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/VAMSIBVS/Marketplace_Automation.git
   cd Marketplace_Automation
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # Windows (CMD):
   .venv\Scripts\activate.bat
   # Linux/macOS:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚦 Usage

1. **Prepare Daily Data**:
   Place the daily files in `data/YYYY-MM-DD/` corresponding to today's date:
   - Amazon: `revenue_us.png`, `spends_us.csv`, `revenue_uk.png`, `spends_uk.csv`, `revenue_aust.png`, `spends_aust.csv`
   - Walmart: `revenue_walmart.csv`, `spends_walmart.png`
   - eBay: `revenue_ebay.png`, `spends_ebay.png`

2. **Run the Automation**:
   ```bash
   python main.py
   ```

3. **View the Report**:
   The generated report will be saved under the `reports/` directory:
   ```text
   reports/marketplace_report_YYYY-MM-DD.xlsx
   ```

---

## 📊 Sample Output Format

| Date | Platform | Revenue | Revenue $ | Spend | Spend $ | ROAS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| DD-MM-YYYY | Amazon USA | 1,250.00 | 1,250.00 | 300.00 | 300.00 | 4.17 |
| DD-MM-YYYY | Amazon UK | £950.00 | 1,206.50 | £210.00 | 266.70 | 4.52 |
| DD-MM-YYYY | Amazon AUS | A$1,800.00 | 1,188.00 | A$450.00 | 297.00 | 4.00 |
| DD-MM-YYYY | Walmart | 800.00 | 800.00 | 150.00 | 150.00 | 5.33 |
| DD-MM-YYYY | Ebay | 450.00 | 450.00 | 90.00 | 90.00 | 5.00 |
| | **Grand Total** | | **$4,894.50** | | **$1,103.70** | **4.43** |

---

## 👤 Author

- **Vamsi BVS** - [VAMSIBVS](https://github.com/VAMSIBVS)
