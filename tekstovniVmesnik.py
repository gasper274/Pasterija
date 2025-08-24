import baza
from model import * 
from datetime import datetime

def kraj_dostave():

    kraj = Dostava.vse_dostave()
    for i in range(len(kraj)):
        print(f"{i+1}) {kraj[i].mesto} - ({kraj[i].postna_stevilka})")

def dobi_izdelke():
    """funkcija izpise ime in ceno izdelka"""
    izdelki = Izdelki.vsi_izdelki()
    for i in range(len(izdelki)):
        print(f"{i+1}. {izdelki[i].naziv}; ({izdelki[i].cena})")
    print("\n")


def prijava():
    """funkcija dobi od uporabnika podatke"""
    ime = input("Vnesi ime: ")
    geslo = input("Vnesi geslo: ")
    uporabniki = Uporabniki.dobi_uporabnika()
    for i in uporabniki:
        if i.ime == ime and i.geslo == geslo:
            print("Prijava uspešna.\n")
            return i.id
    print("Prijava neuspešna, poskusite ponovno.\n")
    return None


def registracija():
    """funckija dobi od uporabnika podatke"""
    ime = input("Vnesi ime: ")
    priimek = input("Vnesi priimek: ")
    email = input("Vnesi email: ")
    geslo = input("Vnesi geslo: ")
    uporabniki = Uporabniki.dobi_uporabnika()
    for i in uporabniki:
        if i.ime == ime and i.priimek == priimek and i.geslo == geslo and i.email == email:
            print("Registracija neuspešna. Poskusite ponovno.\n")
            return None
    print("Registracija uspešna!")
    return i.id
    


def kosarica(uporabnik):

    izdelki = Izdelki.vsi_izdelki()
    kraji = Dostava.vse_dostave()
    kosarica = []
    run = True

    while run:

        print("Dobrodošli v Košarici")
        print("=======================")
        print("1) Dodaj izdelek")
        print("2) Poglej košarico")
        print("3) Oddaj naročilo")
        print("4) Nazaj")

        stevilka = int(input("Vnesi številko: "))

        if stevilka == 1:
            dobi_izdelke()
            id_izdelka = int(input("Vnesi številko izdelka, ki ga želite dodati v košarico: ")) - 1
            if id_izdelka >= 0 and id_izdelka < len(izdelki):
                kosarica.append(izdelki[id_izdelka])
            else:
                print("Nepravilen vnos. Poskusite ponovno.")
        elif stevilka == 2:
            if len(kosarica) == 0:
                print("Košarica je prazna.")
            else:
                skupna_cena = sum([ime.cena for ime in kosarica])
                for ime in kosarica:
                    print(f"-> {ime.naziv} - ({ime.cena}€)")
                print(f"Skupna cena je: {skupna_cena}€")
        elif stevilka == 3:
            if len(kosarica) == 0:
                print("Košarica je prazna.")
            else:
                skupna_cena = sum([ime.cena for ime in kosarica])
                datum = datetime.now().strftime('%Y-%m-%d')
                kraj_dostave()
                dostava_id = int(input("Prosim, izberite številko kraja dostave: ")) - 1
                if dostava_id >= 0 and dostava_id < len(kraji):
                    Narocila.shrani_narocilo(int(uporabnik), skupna_cena, datum, dostava_id)
                else:
                    print("Vnesena nepravilna številka, poskusite ponovno.")

        elif stevilka == 4:
            run = False
        else:
            print("Vnesi številko od 1-4.")
    

def main_program():
    """vse glavno"""

    prijavljeni = None

    run = True
    while run:
        
        print("Dobrodošli v Pašteriji")
        print("=======================")
        print("1) Izdelki")
        print("2) Košarica")
        print("3) Prijava")
        print("4) Registracija")
        print("5) Izhod")
        stevilka = int(input("Vnesi številko: "))

        if stevilka == 1:
            dobi_izdelke()
        elif stevilka == 2:
            if prijavljeni == None:
                print("Prosimo prijavite se.\n")
            else:
                kosarica(prijavljeni)
        elif stevilka == 3:
            prijavljeni = prijava()
        elif stevilka == 4:
            prijavljeni = registracija()
        elif stevilka == 5:
            run = False
        else:
            print("Vnesi številko od 1-5.")



if __name__=="__main__":
    main_program()

    
    