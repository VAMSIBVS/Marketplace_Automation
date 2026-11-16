from readers import load_all_reports
from calculations import build_report_data
from excel_writer import write_excel


def main():

    print("=" * 50)
    print("Marketplace Report Automation")
    print("=" * 50)

    # Step 1 - Read all reports
    data = load_all_reports()

    # Step 2 - Build report rows
    report_rows, grand_total = build_report_data(data)

    # Step 3 - Generate Excel
    write_excel(report_rows, grand_total)

    print("\nAutomation Completed Successfully!")


if __name__ == "__main__":
    main()