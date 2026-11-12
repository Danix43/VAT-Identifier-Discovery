# Scopul: Daca poate fi construit un dataset cu numerele de TVA al firmelor din UK?

## General Notes

- Nu exista, pentru UK, o baza universala si accesibila liber care sa contina date ale companiilor impreuna cu VAT number
- Nu exista un consensus in ceea ce priveste afisarea numarului VAT pe site-uri
- Pe site-ul [UK Registery](https://find-and-update.company-information.service.gov.uk/) nu este afisat numarul VAT
- Numarul VAT poate fi generat si verificat relativ rapid, fiind un cod de 9 cifre

## Strat 1

### Notes

- Poate realiza o lista mult mai completa ale companiilor
- Este mult mai cost intensive si este mai predispusa la rezultate inconcludente

### Functionare

1. Genereaza Company Registragion Numbers (CRNs); 8 chars long, poate incepe cu 1 sau 0
2. Cauta pe baza CRN in [UK Registery](https://find-and-update.company-information.service.gov.uk/) pentru datele companiei
3. Scrap the site pentru datele companiei (Nume, adresa)
    1. Numele companiei trebuie sa contina tipul ei - Limited, LTD = Limited Company
4. Cauta site-ul companiei
5. Daca exista site-ul cauta VAT number-ul
6. Verifica VAT number prin aplicatia [HMRC](https://www.gov.uk/check-uk-vat-number)
7. Rezultatul cautarii salveaza-l intr-un fisier

## Strat 2

### Notes

- Strategia asta gaseste doar companiile care un VAT number valabil

### Probleme gasite

1. Website-ul HMRC poate aplica restrictii pentru volume mari, este nevoie de un API
2. Majoritatea VAT number generate sunt valide, insa nu duc spre nicio companie

### Functionare

1. Genereaza VAT numbers;
    1. poate contine sau nu GB, urmate de 9 cifre
    2. VAT numbers-urile generate trebuiesc validate
2. Verifica numerele valide cu [HMRC](https://www.gov.uk/check-uk-vat-number)
    1. Site-ul HMRC ofera numele si adresa companiei
3. Salveaza rezultatele intr-un fisier

## Tasks

- Exploreaza variante deja existente
- NIF-ul companiei trebuie sa fie valid, verificabil de [HMRC](https://www.gov.uk/check-uk-vat-numbers), indiferent daca e valabil sau nu
- Verifica daca poate fi aplicat pentru alte tari

## Test Sample

TODO: adauga o companie sample valida si una invalida
