from model import *
from bottle import Bottle, run, template, request, redirect, response
from datetime import datetime

def preveri_registracija(ime,priimek,email):
    '''funkcija preverja ali je uporabnik že v bazi'''
    
    uporabniki = Uporabniki.dobi_uporabnika()
    tabela_uporabnikov = [(i.ime,i.priimek,i.email) for i in uporabniki]
    if (f'{ime}', f'{priimek}', f'{email}') in tabela_uporabnikov:
        return True
    else:
        return False

def preveri_prijava(ime,geslo):
    '''funckija preverja ali se lahko uporabnik prijavi'''
    uporabniki = Uporabniki.dobi_uporabnika()
    tabela_uporabnikov = [(i.ime,i.geslo) for i in uporabniki]
    if (f'{ime}', f'{geslo}') not in tabela_uporabnikov:
        return False
    else:
        return True
      
# def izdelki_po_kategorijah():
#     '''funkcija naredi slovar, kjer so kljuèi kategorije_id in vrednosti imena izdelkov'''
#     izdelki = Izdelki.vsi_izdelki()
#     kategorije = dict()
#     for st_kategorij in izdelki:
#         kategorije[st_kategorij.kategorija_id] = []
#     for i in izdelki:
#         kategorije[i.kategorija_id].append(i.naziv)
#     return kategorije

app = Bottle()

skrivnost = "ne-povem"

@app.route('/', method="GET")
def home_page():
    ime = request.get_cookie("uporabnik", secret=skrivnost)
    return template('homepage', ime=ime)

@app.route('/izdelki', method="GET")
def izdelki_page():
    izdelki = Izdelki.vsi_izdelki()
    uporabnik_id = request.get_cookie("uporabnik_id", secret=skrivnost)
    
    return template('izdelki', izdelki=izdelki, uporabnik_id=uporabnik_id)

@app.get('/kosarica')
def prikazi_kosarico():
    ime = request.get_cookie('uporabnik', secret=skrivnost)
    uporabnik_id = request.get_cookie('uporabnik_id', secret=skrivnost)
    
    if not ime:
        return redirect('/prijava')
    
    kosarica_ime = f'kosarica-{uporabnik_id}'
    kosarica = request.get_cookie(kosarica_ime, secret=skrivnost)
    if kosarica:
        nazivi = kosarica.split(',')
    else:
        nazivi = []
    
    dostave = Dostava.vse_dostave()
    
    vsi = Izdelki.vsi_izdelki()
    izdelki = []
    skupna_cena = 0
    
    for i in vsi:
        if i.naziv in nazivi:
            izdelki.append(i)
            skupna_cena += i.cena
            skupna_cena = round(skupna_cena,2)
            
    return template('kosarica', izdelki=izdelki, skupna_cena=skupna_cena, dostave=dostave)


@app.route('/dodaj-v-kosarico/<naziv>', method='POST')
def dodaj_v_kosarico(naziv):
    
    uporabnik_id = request.get_cookie('uporabnik_id', secret=skrivnost)
    kosarica_ime = f'kosarica-{uporabnik_id}'
    
    kosarica = request.get_cookie(kosarica_ime, secret=skrivnost)
    
    if kosarica:
        nazivi = kosarica.split(',')
    else:
        nazivi = []

    nazivi.append(naziv)
    nova_kosarica = ','.join(nazivi)
    response.set_cookie(kosarica_ime, nova_kosarica, secret=skrivnost, path='/')
    return redirect('/kosarica')

@app.route('/kosarica/pocisti')
def pocisti_kosarico():
    uporabnik_id = request.get_cookie('uporabnik_id', secret=skrivnost)
    kosarica_ime = f'kosarica-{uporabnik_id}'
    response.delete_cookie(kosarica_ime, path='/')
    return redirect('/kosarica')

@app.route('/izdelki-oddaj', method='POST')
def oddaj_narocilo():
    uporabnik_id = request.get_cookie('uporabnik_id', secret=skrivnost)
    kosarica_ime = f'kosarica-{uporabnik_id}'
    kosarica = request.get_cookie(kosarica_ime, secret=skrivnost)
    nazivi = kosarica.split(',') if kosarica else []

    vsi = Izdelki.vsi_izdelki()
    skupna_cena = round(sum(i.cena for i in vsi if i.naziv in nazivi), 2)
    datum = datetime.now().strftime('%Y-%m-%d')
    dostava_id = int(request.forms.get('dostava_id'))

    Narocila.shrani_narocilo(int(uporabnik_id), skupna_cena, datum, dostava_id)
    pocisti_kosarico()

    return redirect('/')
    

@app.route('/prijava', method="GET")
def prijava_page():
    return template('prijava')

@app.route('/prijava', method="POST")
def prijava_page():
    ime = request.forms.get('ime')
    geslo = request.forms.get('geslo')
    uporabniki = Uporabniki.dobi_uporabnika()
    for i in uporabniki:
        if i.ime == ime:
            uporabnik = i.id
            
    if preveri_prijava(ime,geslo) == True:
        response.set_cookie('uporabnik_id', str(uporabnik), secret=skrivnost, path='/')
        response.set_cookie('uporabnik', ime, secret=skrivnost, path='/')
        return redirect('/')
    else:
        return "<a href='/prijava'> Prijava ni uspela, prosimo poskusite znova</a>"

@app.route('/odjava')
def odjava():
    response.delete_cookie("uporabnik", path='/')
    return redirect('/')

@app.route('/registracija', method="GET")
def registracija_page():
    return template('registracija')

@app.route('/registracija', method="POST")
def registracija_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    email = request.forms.get('email')
    geslo = request.forms.get('geslo')
    
    
    if preveri_registracija(ime,priimek,email) == True:
        return "<a href='/registracija'> Uporabnik že obstaja, prosimo poskusite znova</a>"
    
    Uporabniki.shrani_uporabnika(ime,priimek,email,geslo)
    response.set_cookie('uporabnik', ime, secret=skrivnost, path='/')
    return redirect('/')

@app.route('/statistika', method="GET")
def statistika_admina():
    ime = request.get_cookie("uporabnik", secret=skrivnost)
    if ime != "admin":
        return redirect('/')
    try:
        statistika = Statistika.dobi_statistiko()
        return template('statistika', statistika=statistika, ime=ime)
    except RuntimeError as e:
        return template('statistika', statistika=None, napaka=str(e), ime=ime)
    
    
if __name__ == "__main__":
    app.run(host='localhost', port=8080, reloader=True, debug=True)


