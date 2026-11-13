import json
import csv
from helpers import mock_hmrc_response, generate_vat_number, Company

if __name__ == "__main__":
    # Step 1
    vat_numbers = generate_vat_number(add_gb_prefix=True)

    total_vat_numbers_made = len(vat_numbers)
    valid_companies = []

    # Step 2
    for company in vat_numbers:

        # this should mock the response from the hmrc api with our vat number
        hmrc_response = json.loads(mock_hmrc_response(company.vat_number))

        # the api found the company and returned it's details
        if hmrc_response["code"] == "FOUND":
            company.name = hmrc_response["name"]
            company.address = Company.Address(
                hmrc_response["address"]["streetName"],
                hmrc_response["address"]["number"],
            )

            valid_companies.append(company)
            print(company)
        else:
            # the api didn't found a registered company with this vat_number
            continue

    # show stats
    print("")
    print(f"total numbers generated: {total_vat_numbers_made}")
    print(f"valid vat numbers : {len(valid_companies)}")
    print(f"invalid vat numbers: {total_vat_numbers_made - len(valid_companies)}")

    # Step 3
    headers = ["name", "vat_number", "street", "street_number"]

    with open("valid_companies_strat2.py", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        writer.writeheader()

        for row in valid_companies:
            writer.writerow(
                {
                    "name": row.name,
                    "vat_number": row.vat_number,
                    "street": row.address.street_name,
                    "street_number": row.address.number,
                }
            )
