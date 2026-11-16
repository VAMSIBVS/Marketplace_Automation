import os
from datetime import datetime

from openpyxl import Workbook
from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side,
)


def write_excel(report_rows, grand_total):

    os.makedirs("reports", exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    output_file = f"reports/marketplace_report_{today}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Overall Marketplaces"

    # -------------------------
    # Styles
    # -------------------------
    header_fill = PatternFill(
        fill_type="solid",
        start_color="A9D18E",
        end_color="A9D18E",
    )

    grand_fill = PatternFill(
        fill_type="solid",
        start_color="F4B183",
        end_color="F4B183",
    )

    thin_border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin"),
    )

    headers = [
        "Date",
        "Platform",
        "Revenue",
        "Revenue $",
        "Spend",
        "Spend $",
        "ROAS",
    ]

    # -------------------------
    # Header
    # -------------------------
    for col, header in enumerate(headers, start=1):

        cell = ws.cell(row=1, column=col)

        cell.value = header
        cell.font = Font(bold=True)
        cell.fill = header_fill
        cell.border = thin_border
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

    row = 2

    # -------------------------
    # Data Rows
    # -------------------------
    for item in report_rows:

        ws.cell(row=row, column=1).value = item["Date"]
        ws.cell(row=row, column=2).value = item["Platform"]
        ws.cell(row=row, column=3).value = item["Revenue"]
        ws.cell(row=row, column=4).value = item["Revenue $"]
        ws.cell(row=row, column=5).value = item["Spend"]
        ws.cell(row=row, column=6).value = item["Spend $"]
        ws.cell(row=row, column=7).value = item["ROAS"]

        for cell in ws[row]:
            cell.border = thin_border
            cell.alignment = Alignment(
                horizontal="center",
                vertical="center",
            )

        row += 1

    # -------------------------
    # Grand Total
    # -------------------------
    ws.cell(row=row, column=2).value = grand_total["Platform"]
    ws.cell(row=row, column=3).value = grand_total["Revenue"]
    ws.cell(row=row, column=4).value = grand_total["Revenue $"]
    ws.cell(row=row, column=5).value = grand_total["Spend"]
    ws.cell(row=row, column=6).value = grand_total["Spend $"]
    ws.cell(row=row, column=7).value = grand_total["ROAS"]

    for cell in ws[row]:
        cell.font = Font(bold=True)
        cell.fill = grand_fill
        cell.border = thin_border
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
        )

    # -------------------------
    # Auto Column Width
    # -------------------------
    for column_cells in ws.columns:

        length = max(len(str(cell.value or "")) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = length + 5

    wb.save(output_file)

    print("\n======================================")
    print("Report Generated Successfully")
    print(output_file)
    print("======================================")