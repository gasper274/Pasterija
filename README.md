# Pasterija

Naredila bova spletno trgovino, ki se ukvarja s prodajo testenin in prodajo že narejenih jedi s testeninami. Stran bo omogočala registracijo uporabnika, omogočeno dodajanje novih izdelkov v bazo, uporabnik bo lahko oddal naročilo. Naredila bova tudi statistiko glede na posamezen mesec.

Imela bova naslednje tabele:

1. Uporabniki
 - vsebovala bo informacije o uporabnikih (ime, priimek, email, geslo...)

2. Izdelki
 - vsebovala bo infromacije o izdelkih v ponudbi (naziv, opis, cena...)

3. Kategorija
 - skupine izdelkov

4. Naročila
 - podatki o naročilih

5. Postavke naročil
 - povezovalna tabela izdelkov in naročili z informacijo o količini in skupni ceni naročila

6. Dostava
 - vsebuje podatke o dostavi

Povezave tabel:
 
Uporabniki -- Naročila: en uporabnik lahko odda več naročil (1:N)
Naročila -- Postavke naročil: eno naročilo lahko ima več postavk (1:N)
Postavke naročil -- Izdelki: ena postavka se veže na en izdelek, isti izdelek lahko nastopa v več postavkah) (N:1)
Izdelki -- Kategorije: več izdelkov ima isto kategorijo (N:1)
Naročilo -- Dostava: eno naročilo ima eno dostavo (1:1)
