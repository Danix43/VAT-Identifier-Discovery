# Goal: Can a dataset be built with the VAT numbers of UK companies?

## Research

### Starting points

### Idea 1

- The dataset provided by [Companies House](https://download.companieshouse.gov.uk/en_output.html) contains general company data without a website or VAT number. It can be used to create an initial database that can be processed further.
- Searching each company in the CH dataset through a search engine can be both time-consuming and very expensive, especially when considering an API.
  - Considering 8,000,000 queries (there are approximately 4,000,000 companies, with 2 search attempts each), and the Google API charges $5 per 1,000 queries, this equals an estimated cost of around $40k.
- In an ideal scenario, where each business has a working website and is found, the site must be searched for the VAT number if it exists.
  - An obvious challenge is the varying structure of websites, which the program must adapt to.
  - A higher-success option is locating the number via `Regex` if the VAT number appears anywhere on the homepage.
  - If it is not found on the homepage, it must be searched for on the `Contact`, `Terms and Conditions`, `Privacy Policy`, etc. pages.

### Idea 2

- The VAT number follows a predictable structure that can be validated.
  - 9 digits, which may be preceded by `GB`
- Thus, all generated combinations can be validated. Valid codes can then be checked through the [HMRC](https://developer.service.hmrc.gov.uk/api-documentation/docs/api/service/vat-registered-companies-api/2.0) API, which provides company data such as name and address.
  - This variant is prone to high costs, especially due to the need to use an external API to verify generated numbers.
- But this approach can create a complete list of all existing and valid businesses.

### General Notes

- There is no universal, freely accessible database for the UK that contains company details together with VAT numbers.
- There is no consensus on how VAT numbers are displayed on websites.
- On the [UK Registry](https://find-and-update.company-information.service.gov.uk/) website, the VAT number is not displayed.

## Proof of Concept

## [Strategy 1](./strat1.py)

### How it works

---

#### START -> Generate CRN numbers -> Search generated numbers in the UK Registry -> Search for the website if a valid company exists -> Scrape the website for the VAT number -> Verify the VAT number in HMRC -> Save the results -> END

---

1. Generate Company Registration Numbers (CRNs); 8 characters long, may begin with 1 or 0
2. Search the CRN in the [UK Registry](https://find-and-update.company-information.service.gov.uk/) for the company details
3. Scrape the website for company details (name, address)
4. Search the company's website
5. If the website exists, look for the VAT number
6. Verify the VAT number via the [HMRC](https://www.gov.uk/check-uk-vat-number) application
7. The search result is saved to a file

### Notes

- The company name should include its type - Limited, LTD = Limited Company
  - This can be useful for sorting by company type when needed
- It can produce a much more complete list of companies
- It is more cost-intensive and more prone to inconclusive results

## [Strategy 2](./strat2.py)

### How it works

---

#### START -> Generate VAT numbers -> Verify generated numbers on the HMRC website -> save results -> END

---

1. Generate VAT numbers;
    1. may or may not include GB, followed by 9 digits
    2. Generated VAT numbers must be validated
2. Verify valid numbers with [HMRC](https://www.gov.uk/check-uk-vat-number)
    1. The HMRC website provides the company's name and address
3. Save the results to a file

### Notes

- This strategy only finds companies with a valid VAT number

### Problems found

1. The HMRC website may impose restrictions on large numbers of requests, requiring an API that raises costs
2. The HMRC VAT number verification API is not feasible for app testing. It is available only in a limited sandbox
3. Most generated VAT numbers are valid but do not correspond to any company

## Real world application

In my opinion, the best option is to use existing APIs such as HMRC to search generated VAT numbers. The web crawling approach can be much more costly and has a much higher failure rate than the API access cost.
