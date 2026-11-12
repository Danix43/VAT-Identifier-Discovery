import random
import requests

SAMPLE_SIZE = 10000


def generate_vat_number(size=SAMPLE_SIZE, add_gb_prefix=False):
    GB_PREFIX = "GB"

    vat_numbers = []
    seen = set()
    while len(vat_numbers) < size:
        number = f"{random.randrange(10**9):09d}"
        if number not in seen and check_checksum_vat(number):
            if add_gb_prefix:
                number = "".join([GB_PREFIX, str(number)])
            seen.add(number)
            vat_numbers.append(number)
    return vat_numbers


def check_checksum_vat(number: str) -> bool:
    number = number.strip().upper()
    # filtering for prefix
    if number.startswith("GB"):
        number = number[2:]
    if len(number) != 9 or not number.isascii() or not number.isdigit():
        return False

    weights = (8, 7, 6, 5, 4, 3, 2, 10, 1)
    remainder = sum(weight * int(digit) for weight, digit in zip(weights, number)) % 97

    if int(number[:3]) < 100:
        return remainder == 0
    # legacy checksum check
    return remainder in (0, 42, 55)


def request_hmrc(vat_number):
    pass


def save_hmrc_response():
    pass


if __name__ == "__main__":
    vat_numbers = generate_vat_number(add_gb_prefix=True)

    print(f"made: {len(vat_numbers)} vat numbers")
    for number in vat_numbers:
        print(f"number: {number}, is valid: {check_checksum_vat(number)}")
