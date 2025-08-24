# Pasterija

Naredila bova spletno trgovino, ki se ukvarja s prodajo testenin in prodajo že narejenih jedi s testeninami. Stran bo omogočala registracijo/prijavo uporabnika, dodajanje artiklov v košaričo in oddajanje naročila. Statistika je dostopna samo administratorju strani, uporabnisko ime: admin, geslo: admin zavihek statistika.

Imava 6 tabel:
<ol>
  <li>Uporabniki: informacije o uporabniku</li>
  <li>Izdelki: opis izdelka</li>
  <li>Kategorija: v katero kategorijo spada izdelek</li>
  <li>Naročila: vsebuje podatke naročila</li>
  <li>Postavke naročil: povezovalna tabela izdelkov in naročili z informacijo o količini in skupni ceni naročila </li>
  <li>Dostava: vsebuje mesto in postno številko naročila </li>
</ol> 

<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/ca7513e9-b1d4-40ab-839f-33c6be6e24a8" />

Povezave tabel:
<ul>
  <li>Uporabniki -- Naročila: en uporabnik lahko odda več naročil (1:N)</li>
  <li>Naročila -- Postavke naročil: eno naročilo lahko ima več postavk (1:N)</li>
  <li>Postavke naročil -- Izdelki: ena postavka se veže na en izdelek, isti izdelek lahko nastopa v več postavkah) (N:1)</li>
 <li>Izdelki -- Kategorije: več izdelkov ima isto kategorijo (N:1)</li>
 <li>Naročilo -- Dostava: eno naročilo ima eno dostavo (1:1)</li>
</ul>

