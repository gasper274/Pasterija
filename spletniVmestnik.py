from bottle import run, route, template, get, post, request, response, redirect
from model import * 

secret = "nepovem"

@route("/")
def home():
    """izpise vse podatke"""
    ime = request.get_cookie("ime", secret=secret)
    return template('home.html', ime=ime)
@route("/prijava")
def prijava():
    return template("prijava.html")

@route("/prijava", method="POST")
def prijava_post():
    """User login authentication"""
    ime = request.forms.get("ime")
    geslo = request.forms.get("geslo")

    uporabniki = Uporabniki.dobi_uporabnika()

    for uporabnik in uporabniki:
        if uporabnik.ime == ime and uporabnik.geslo == geslo:
            # Set the session cookie
            response.set_cookie("ime", ime, secret=secret)
            redirect("/")  

    return "<h1>Nepravilno ime ali geslo</h1>"
        

@route("/odjava", method="POST")
def odjava():
    response.delete_cookie("ime")
    redirect("/")

@route("/registracija")
def registracija():
    return template("registracija.html")

@route("/registracija", method="POST")
def registracija_post():
    id = request.forms.id
    ime = request.forms.ime
    priimek = request.forms.priimek
    email = request.forms.email
    geslo = request.forms.geslo
    
    #dobimo tabelo emailov
    dobi_email = Uporabniki.dobi_uporabnika()
    tabela_mailov = [podatek.email for podatek in dobi_email]
    if email in tabela_mailov:
        return "<h1>email je ze v rabi</h1>"
    else:
        Uporabniki.shrani_uporabnika(ime, priimek, email, geslo)
        
        response.set_cookie("ime", ime, secret=secret)
        # Redirect to home page
        redirect("/")


@route("/kosarica")
def kosarica():
    """izpise vse podatke"""
    return "<h1>Kosarica</h1>"

@route("/izdelki")
def izdelki():
    """izpise vse podatke"""
    slovar_izdelkov = {
        1:[],
        2:[],
        3:[]
    }
    izdelki = Izdelki.vsi_izdelki()
    for i in izdelki:
        slovar_izdelkov[i.kategorija_id].append(i.naziv)
    #preimenujem keys
    slovar_izdelkov["Tipi špagetov"] = slovar_izdelkov.pop(1)
    slovar_izdelkov["Omake/Zacimbe"] = slovar_izdelkov.pop(2)
    slovar_izdelkov["Jedi"] = slovar_izdelkov.pop(3)
     
    return template("izdelki.html", slovar_izdelkov=slovar_izdelkov)

if __name__ == "__main__":
    run(host='localhost', port=8080, debug=True, reloader=True)