from datetime import datetime
import requests


# ---------------------------------------
# GET LIVE EXCHANGE RATES
# ---------------------------------------

def get_exchange_rates():

    url = "https://open.er-api.com/v6/latest/USD"

    response = requests.get(url)
    data = response.json()

    rates = data["rates"]

    return {
        "GBP_TO_USD": 1 / rates["GBP"],
        "AUD_TO_USD": 1 / rates["AUD"]
    }


# ---------------------------------------
# CALCULATE ROAS
# ---------------------------------------

def calculate_roas(revenue, spend):

    if spend == 0:
        return 0

    return round(revenue / spend, 2)


# ---------------------------------------
# BUILD REPORT
# ---------------------------------------

def build_report_data(data):

    report_rows = []

    total_revenue_usd = 0
    total_spend_usd = 0

    today = datetime.now().strftime("%d-%m-%Y")

    rates = get_exchange_rates()

    GBP_TO_USD = rates["GBP_TO_USD"]
    AUD_TO_USD = rates["AUD_TO_USD"]

    for platform, values in data.items():

        revenue = values["Revenue"]
        spend = values["Spend"]

        revenue_usd = revenue
        spend_usd = spend

        # -----------------------------
        # Currency Conversion
        # -----------------------------

        if platform == "Amazon UK":

            revenue_usd = round(revenue * GBP_TO_USD, 2)
            spend_usd = round(spend * GBP_TO_USD, 2)

        elif platform == "Amazon AUS":

            revenue_usd = round(revenue * AUD_TO_USD, 2)
            spend_usd = round(spend * AUD_TO_USD, 2)

        roas = calculate_roas(revenue_usd, spend_usd)

        report_rows.append({

            "Date": today,
            "Platform": platform,

            "Revenue": revenue,
            "Revenue $": revenue_usd,

            "Spend": spend,
            "Spend $": spend_usd,

            "ROAS": roas

        })

        total_revenue_usd += revenue_usd
        total_spend_usd += spend_usd

    grand_total = {

        "Date": "",

        "Platform": "Grand Total",

        "Revenue": "",
        "Revenue $": round(total_revenue_usd, 2),

        "Spend": "",
        "Spend $": round(total_spend_usd, 2),

        "ROAS": calculate_roas(
            total_revenue_usd,
            total_spend_usd
        )

    }

    return report_rows, grand_total