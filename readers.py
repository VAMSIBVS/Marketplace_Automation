import re
import pandas as pd
import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

from PIL import Image
from pathlib import Path

from config import DATA_FOLDER


# ----------------------------------------------------
# FIND FILE
# ----------------------------------------------------

def find_file(filename):
    """
    Finds a file by exact name (case-insensitive).
    """

    for file in DATA_FOLDER.iterdir():
        if file.name.lower() == filename.lower():
            return file

    print("\nFiles found in folder:")
    for file in DATA_FOLDER.iterdir():
        print(" -", file.name)

    raise FileNotFoundError(f"{filename} not found.")

# ----------------------------------------------------
# CLEAN MONEY
# ----------------------------------------------------

def clean_money(value):

    if pd.isna(value):
        return 0.0

    value = str(value)

    value = value.replace("$", "")
    value = value.replace("£", "")
    value = value.replace(",", "")
    value = value.strip()

    if value == "":
        return 0.0

    return float(value)


# ----------------------------------------------------
# AMAZON REVENUE
# ----------------------------------------------------

def read_amazon_revenue(image_file):

    print(f"Reading {image_file.name}...")

    image = Image.open(image_file)

    text = pytesseract.image_to_string(image)

    print(text)

    match = re.search(r"\$?\s*([\d,]+\.\d{2})", text)

    if match:

        revenue = float(
            match.group(1).replace(",", "")
        )

        print(f"Amazon Revenue : {revenue}")

        return revenue

    print("Amazon revenue not found.")

    return 0.0

# ----------------------------------------------------
# AMAZON SPEND
# ----------------------------------------------------

def read_amazon_spend(csv_file):

    print(f"Reading {csv_file.name}...")

    df = pd.read_csv(csv_file)

    # find Total cost column automatically

    spend_column = None

    for column in df.columns:

        if "Total cost" in column:

            spend_column = column
            break

    if spend_column is None:

        raise Exception(
            f"Total cost column not found in {csv_file.name}"
        )

    df[spend_column] = (
        df[spend_column]
        .apply(clean_money)
    )

    spend = round(df[spend_column].sum(), 2)

    return spend
# ----------------------------------------------------
# WALMART REVENUE
# ----------------------------------------------------

def read_walmart_revenue(csv_file):

    print(f"Reading {csv_file.name}...")

    df = pd.read_csv(csv_file)

    # Find the GMV column automatically
    revenue_column = None

    for column in df.columns:

        if "gmv" in column.lower():

            revenue_column = column
            break

    if revenue_column is None:

        raise Exception(
            f"GMV column not found in {csv_file.name}"
        )

    revenue = clean_money(df[revenue_column].iloc[0])

    print(f"Walmart GMV : {revenue}")

    return revenue


# ----------------------------------------------------
# OCR FUNCTION
# ----------------------------------------------------

def read_value_from_png(image_file, keyword):

    print(f"Reading {image_file.name}...")

    image = Image.open(image_file)

    text = pytesseract.image_to_string(image)

    print(text)

    pattern = rf"{keyword}.*?\$?([\d,]+\.\d+)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:

        value = match.group(1).replace(",", "")

        print(f"{keyword}: {value}")

        return float(value)

    print(f"{keyword} not found")

    return 0.0
# ----------------------------------------------------
# WALMART SPEND
# ----------------------------------------------------

def read_walmart_spend(image_file):

    return read_value_from_png(
        image_file,
        "Ad Spend"
    )


# ----------------------------------------------------
# EBAY REVENUE
# ----------------------------------------------------

def read_ebay_revenue(image_file):

    return read_value_from_png(
        image_file,
        "Total Sales"
    )


# ----------------------------------------------------
# EBAY SPEND
# ----------------------------------------------------

def read_ebay_spend(image_file):

    return read_value_from_png(
        image_file,
        "Ad fees"
    )
# ----------------------------------------------------
# LOAD EVERYTHING
# ----------------------------------------------------

def load_all_reports():

    print("\nLooking for reports in:")
    print(DATA_FOLDER)

    # AMAZON

    us_revenue = read_amazon_revenue(
        find_file("revenue_us.png")
    )

    uk_revenue = read_amazon_revenue(
        find_file("revenue_uk.png")
    )

    aus_revenue = read_amazon_revenue(
        find_file("revenue_aust.png")
    )

    us_spend = read_amazon_spend(
        find_file("spends_us.csv")
    )

    uk_spend = read_amazon_spend(
        find_file("spends_uk.csv")
    )

    aus_spend = read_amazon_spend(
        find_file("spends_aust.csv")
    )


    # WALMART

    walmart_revenue = read_walmart_revenue(
        find_file("revenue_walmart.csv")
    )

    walmart_spend = read_walmart_spend(
        find_file("spends_walmart.png")
    )


    # EBAY

    ebay_revenue = read_ebay_revenue(
        find_file("revenue_ebay.png")
    )

    ebay_spend = read_ebay_spend(
        find_file("spends_ebay.png")
    )


    return {

        "Amazon USA": {
            "Revenue": us_revenue,
            "Spend": us_spend
        },

        "Amazon UK": {
            "Revenue": uk_revenue,
            "Spend": uk_spend
        },

        "Amazon AUS": {
            "Revenue": aus_revenue,
            "Spend": aus_spend
        },

        "Walmart": {
            "Revenue": walmart_revenue,
            "Spend": walmart_spend
        },

        "Ebay": {
            "Revenue": ebay_revenue,
            "Spend": ebay_spend
        }

    }