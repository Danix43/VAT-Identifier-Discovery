from helpers import (
    search_vat_number,
    make_website,
    search_website,
    generate_crn,
    mock_uk_registery_api,
    Company,
)
import csv

import json

if __name__ == "__main__":
    # Step 1
    crns = generate_crn()

    companies = []
    companies_with_vat = []
    website_collection = {}

    # map the crn to company details
    for crn in crns:
        # Step 2
        response = json.loads(mock_uk_registery_api(crn))

        # Step 3
        company = Company()
        company.name = response["company_name"]
        company.number = crn
        company.address = Company.Address(
            response["address"]["streetName"],
            response["address"]["number"],
        )

        companies.append(company)

        # map the company name to website
        website_collection[company.name] = make_website(company)

    # Step 4
    # simulate the search process
    for company in companies:
        # Step 5
        # ! in real world, this would query some api based on company name or number and return the webpage
        website_found = search_website(company.name, website_collection)

        # Step 6
        is_vat_number_found, vat_number = search_vat_number(website_found)
        if is_vat_number_found:
            # print(f"scraper found the vat number: {vat_number}")
            company.vat_number = vat_number
            companies_with_vat.append(company)
        else:
            # print("scraper didn't found the vat number")
            continue

    # stats
    print(f"found {len(companies)} companies in total")
    print(f"from those, {len(companies_with_vat)} had the vat number visible")
    print(
        f"didn't found the vat number for {len(companies) - len(companies_with_vat)} companies"
    )

    # Step 7
    # save to file
    headers = ["name", "vat_number", "company_number", "street", "street_number"]

    with open("valid_companies_strat1.csv", "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)

        writer.writeheader()

        for row in companies:
            writer.writerow(
                {
                    "name": row.name,
                    "vat_number": row.vat_number,
                    "company_number": row.number,
                    "street": row.address.street_name,
                    "street_number": row.address.number,
                }
            )
