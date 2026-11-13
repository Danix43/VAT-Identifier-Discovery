# Scopul: Daca poate fi construit un dataset cu numerele de TVA al firmelor din UK?

## Research

### Puncte de pornire

### Ideea 1

- Dateset-ul pus la dispozitie de [Companies House](https://download.companieshouse.gov.uk/en_output.html) contine date generale despre firme, fara sa includa un website sau un numar VAT. Poate fi folosit pentru a construi o baza initiala, care poate fi procesata mai departe.
- Cautarea fiecarei companii din dataset-ul CH printr-un motor de cautare poate fi atat de durata, cat si foarte costisitoare, daca se considera un API.
  - Considerand 8.000.000 de query-uri (exista aproximativ 4.000.000 de companii, cu 2 incercari de cautare), iar API-ul de la Google cere 5 USD per 1000 de query-uri, egaleaza un cost de 40k USD aproximativ.
- Considerand un scenariu ideal, unde fiecare afacere are un website functional si este gasit, site-ul trebuie cautat pentru numarul VAT, daca acesta exista.
  - O problema evidenta este structura website-urilor, care difera si pentru care programul trebuie adaptat.
  - O varianta cu sanse crescute de reusita este localizarea numarului prin `Regex`, daca numarul exista oriunde pe pagina initiala.
  - Daca nu este gasit pe pagina initiala, trebuie cautat in paginile de `Contact`, `Terms and Conditions`, `Privacy Policy`, etc

### Ideea 2

- Numarul VAT urmeaza o structura predictibila, si care poate fi verificata.
  - 9 cifre, care pot fi precedate de `GB`
- Astfel, pot fi generate toate combinatiile valide. Codurile valide pot fi dupa verificate prin API-ul [HMRC](https://developer.service.hmrc.gov.uk/api-documentation/docs/api/service/vat-registered-companies-api/2.0), care ofera date ale companiei precum nume si adresa.
  - Varianta aceasta este predispusa la costuri mari, in special datorita nevoii folosirii API-ului extern pentru verificare numerelor generate.
- Dar acesta varianta **poate** creea o lista completa cu toate afacerile existente si valide.

### General Notes

- Nu exista, pentru UK cel putin, o baza universala si accesibila liber care sa contina date ale companiilor impreuna cu VAT number
- Nu exista un consensus in ceea ce priveste afisarea numarului VAT pe site-uri
- Pe site-ul [UK Registery](https://find-and-update.company-information.service.gov.uk/) nu este afisat numarul VAT

## Proof of Concept

## [Strategia 1](./strat1.py)

### Functionare

---

#### START -> Genereaza CRN numbers -> Cauta numerele generate in Uk Registery -> Cauta site-ul daca exista o companie valida -> Scrap the site pentru VAT number -> Verifica VAT number pe HMRC -> Salveaza rezultatele -> END

---

1. Genereaza Company Registragion Numbers (CRNs); 8 chars long, poate incepe cu 1 sau 0
2. Cauta pe baza CRN in [UK Registery](https://find-and-update.company-information.service.gov.uk/) pentru datele companiei
3. Scrap the site pentru datele companiei (Nume, adresa)
4. Cauta site-ul companiei
5. Daca exista site-ul cauta VAT number-ul
6. Verifica VAT number prin aplicatia [HMRC](https://www.gov.uk/check-uk-vat-number)
7. Rezultatul cautarii este salvat intr-un fisier

### Notes

- Numele companiei trebuie sa contina tipul ei - Limited, LTD = Limited Company
  - Asta poate fi utila in cazul unei sortari dupa tipul de firma necesar
- Poate realiza o lista mult mai completa a companiilor
- Este mult mai cost intensive si este mai predispusa la rezultate inconcludente

## [Strategia 2](./strat2.py)

### Functionare

---

#### START -> Genereaza VAT numbers -> Verifica numerele generate pe site-ul HMRC -> salveaza rezultatele -> END

---

1. Genereaza VAT numbers;
    1. poate contine sau nu GB, urmate de 9 cifre
    2. VAT numbers-urile generate trebuiesc validate
2. Verifica numerele valide cu [HMRC](https://www.gov.uk/check-uk-vat-number)
    1. Site-ul HMRC ofera numele si adresa companiei
3. Salveaza rezultatele intr-un fisier

### Notes

- Strategia asta gaseste doar companiile care un VAT number valabil

### Probleme gasite

1. Website-ul HMRC poate aplica restrictii pentru volume mari de requests, este nevoie de un API care ridica costuri
2. API HMRC pentru verificarea VAT number nu este fezabil un test app. Este disponibil doar un sandbox limitat
3. Majoritatea VAT number generate sunt valide, insa nu duc spre nicio companie

## Real world application

Cea mai buna varianta, in perspectiva mea, utilizarea unor API-uri existente, precum HMRC, prin care sunt cautate numere VAT generate. Varianta de web crawling poate fi mult mai costisitoare si cu o rata de fail mult mai ridicata decat costul pentru API acces.
