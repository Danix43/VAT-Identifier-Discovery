import random
import json
import re
from bs4 import BeautifulSoup

SAMPLE_SIZE = 50000
MOCK_NAMES = [
    "Amber Finch Supplies Ltd",
    "Blue Oak Components Ltd",
    "Bracken Bell Trading Ltd",
    "Copper Kite Logistics Ltd",
    "Foxglove Works Ltd",
    "Green Lantern Packaging Ltd",
    "Juniper Bridge Services Ltd",
    "Little Harbour Manufacturing Ltd",
    "Silver Thistle Foods Ltd",
    "Westmere Digital Ltd",
    "Amber Badger Textiles Ltd",
    "Bramble Fox Engineering Ltd",
    "Cloudberry Works Ltd",
    "Dappled Heron Consulting Ltd",
    "Ember Fern Foods Ltd",
    "Fablewood Trading Ltd",
    "Golden Acorn Services Ltd",
    "Hollowbrook Supplies Ltd",
    "Ivory Kite Packaging Ltd",
    "Kingfisher Vale Logistics Ltd",
    "Larkspur Lantern Media Ltd",
    "Mossy Compass Manufacturing Ltd",
    "Northwind Pebble Design Ltd",
    "Orchard Moon Technologies Ltd",
    "Pinecone Harbour Retail Ltd",
    "Quiet Meadow Components Ltd",
    "Riverstone Badger Foods Ltd",
    "Sunbeam Thistle Services Ltd",
    "Velvet Acorn Digital Ltd",
    "Wandering Wren Distribution Ltd",
]
MOCK_STREET_NAMES = [
    "Willowbank Road",
    "Ashcombe Lane",
    "Cedar Grove",
    "Hawthorn Street",
    "Millstream Avenue",
    "Foxglove Way",
    "Meadowgate Road",
    "Bracken Close",
    "Wrenfield Drive",
    "Old Foundry Street",
]


def generate_crn(size=SAMPLE_SIZE):
    crn_numbers = []
    unique = set()

    prefix_numbers = [0, 1]
    while len(crn_numbers) < size:
        pre_char = random.choice(prefix_numbers)
        number = f"{pre_char}{random.randrange(10**7):07d}"
        if number not in unique:
            unique.add(number)
            crn_numbers.append(number)
    return crn_numbers


def mock_uk_registery_api(company_number):
    return json.dumps(
        {
            "company_name": random.choice(MOCK_NAMES),
            "company_number": company_number,
            "address": {
                "streetName": random.choice(MOCK_STREET_NAMES),
                "number": random.randint(0, 100),
            },
        }
    )


def make_website(company_details):
    has_vat_number = random.choice([True, False])

    return f"""
        <!doctype html>
        <body>
            <h1>This is the website for the {company_details.name}</h1>
            <h3>We are at {company_details.address}</h3>
            <h3>Come visit us!</h3>
        <footer>
            <div class="bussiness-details">
                <h4>Here are all the legal stuff</h4>
                <p class="company-name">{company_details.name}</p>
                <p class="company-number">{company_details.number}</p>
                <p class="company-address">{company_details.address}</p>
                {f'<p class="company-vat-number">{f"{random.randrange(10**9):09d}"}</p>' if has_vat_number else ""}
            </div>
        </footer>
        </body>
"""


def search_website(company_name, list):
    return list[company_name]


def search_vat_number(html_doc):
    page_text = BeautifulSoup(html_doc, "html.parser").get_text(" ", strip=True)

    # search based on regex, may return false responses
    # still better than doc traversing in this case
    VAT_NUMBER_PATTERN = re.compile(
        r"(?<![A-Z0-9])(?:GB)?\d{9}(?![A-Z0-9])",
    )

    match = VAT_NUMBER_PATTERN.search(page_text)
    if match is None:
        return False, ""
    return True, match.group().upper()
