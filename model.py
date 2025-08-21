import sqlite3
import baza

conn = sqlite3.connect("shop.sqlite3")

baza.pripravi_bazo(conn)


class Izdelki:
    
    def __init__(self, id, naziv, opis, cena, kategorija_id):
        self.id = id
        self.naziv = naziv
        self.opis = opis
        self.cena = cena
        self.kategorija_id = kategorija_id
    
    
    @staticmethod
    def vsi_izdelki():
        with conn:
            cursor = conn.execute("""
                SELECT * from izdelki
                """)
            podatki = list(cursor.fetchall())
            return [Izdelki(*pod) for pod in podatki]

class Dostava:
    
    def __init__(self, id, mesto, postna_stevilka):
        self.id = id
        self.mesto = mesto
        self.postna_stevilka = postna_stevilka
    
    @staticmethod
    def vse_dostave():
        with conn:
            cursor = conn.execute("""
                SELECT * from dostava
                """)
            podatki = list(cursor.fetchall())
            return [Dostava(*pod) for pod in podatki]

class Kategorije:
    
    def __init__(self, id, naziv):
        self.id = id
        self.naziv = naziv
    
    @staticmethod
    def vse_kategorije():
        with conn:
            cursor = conn.execute("""
                SELECT * from kategorije
                """)
            podatki = list(cursor.fetchall())
            return [Kategorije(*pod) for pod in podatki]

class Narocila:
    
    def __init__(self, id, uporabnik_id, skupna_cena, datum, dostava_id):
        self.id = id
        self.uporabnik_id = uporabnik_id
        self.skupna_cena = skupna_cena
        self.datum = datum
        self.dostava_id = dostava_id
    
    @staticmethod
    def vsa_narocila():
        with conn:
            cursor = conn.execute("""
                SELECT * from narocila
                """)
            podatki = list(cursor.fetchall())
            return [Narocila(*pod) for pod in podatki]
    
    @staticmethod
    def shrani_narocilo(uporabnik_id, skupna_cena, datum, dostava_id):
        """vstavi narocilo v bazo"""
        with conn:
            cursor = conn.execute(
                """INSERT INTO narocila (uporabnik_id, skupna_cena, datum, dostava_id) VALUES (?, ?, ?, ?)""", 
                (uporabnik_id, skupna_cena, datum, dostava_id)
            )

class PostavkeNarocil:
    
    def __init__(self, id, narocilo_id, izdelek_id, kolicina, skupna_cena):
        self.id = id
        self.narocilo_id = narocilo_id
        self.izdelek_id = izdelek_id
        self.kolicina = kolicina
        self.skupna_cena = skupna_cena
    
    @staticmethod
    def vse_postavkeNarocil():
        with conn:
            cursor = conn.execute("""
                SELECT * from postavke_narocil
                """)
            podatki = list(cursor.fetchall())
            return [PostavkeNarocil(*pod) for pod in podatki]

class Uporabniki:
    
    def __init__(self, id=None, ime=None, priimek=None, email=None, geslo=None):
        self.id = id
        self.ime = ime
        self.priimek = priimek
        self.email = email
        self.geslo = geslo
    
    @staticmethod
    def dobi_uporabnika():
         with conn:
             cursor = conn.execute("""SELECT * FROM uporabniki""")
             podatki = list(cursor.fetchall())
             return [Uporabniki(*pod) for pod in podatki]
    
    @staticmethod
    def shrani_uporabnika(ime, priimek, email, geslo):
        """vstavi uporabnike v bazo"""
        with conn:
            cursor = conn.execute(
                """INSERT INTO uporabniki (ime, priimek, email, geslo) VALUES (?, ?, ?, ?)""", 
                (ime, priimek, email, geslo)
            )

class Statistika:
    @staticmethod
    def dobi_statistiko():
        with conn:
            # Skupno število naročil
            cursor = conn.execute("SELECT COUNT(*) FROM narocila")
            st_narocil = cursor.fetchone()[0]

            # Skupna vrednost naročil
            cursor = conn.execute("SELECT SUM(skupna_cena) FROM narocila")
            skupna_vrednost = round(cursor.fetchone()[0] or 0, 2)

            # Število registriranih uporabnikov
            cursor = conn.execute("SELECT COUNT(*) FROM uporabniki")
            st_uporabnikov = cursor.fetchone()[0]

            # Najbolj priljubljena kategorija
            cursor = conn.execute("""
                SELECT k.naziv, COUNT(p.id) as st_postavk
                FROM kategorije k
                JOIN izdelki i ON i.kategorija_id = k.id
                JOIN postavke_narocil p ON p.izdelek_id = i.id
                GROUP BY k.id, k.naziv
                ORDER BY st_postavk DESC
                LIMIT 1
            """)
            priljubljena_kategorija = cursor.fetchone()
            priljubljena_kategorija = priljubljena_kategorija[0] if priljubljena_kategorija else "Ni podatkov"

            return {
                'st_narocil': st_narocil,
                'skupna_vrednost': skupna_vrednost,
                'st_uporabnikov': st_uporabnikov,
                'priljubljena_kategorija': priljubljena_kategorija
            }
            
        