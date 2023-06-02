## import
import urllib.request, urllib.error, urllib.parse, re, time


## encoder requete url => not working
def url_encode(nom):
    liste=nom.split(" ")
    input=''
    for i in range(0,len(liste)):
        if i!=len(liste)-1:
            input=(input+liste[i]+'+')
        else:
            input=(input+liste[i])
    titre=" ".join(liste)
    return(input,titre)

## envoyer requete url
def url_request(site, input):
    url=''
    if site=='Altf4':
        url = 'https://www.altf4online.com/products/search?q='+input+'&c=1'
    elif site == 'CardBrawlers':
        url = 'https://cardbrawlers.com/search?type=product&options%5Bprefix%5D=last&q='+input
    else:
        return("error")
    reponse = urllib.request.urlopen(url)
    contenu_web = reponse.read().decode('UTF-8')
    return(contenu_web.split("\n"))


## suppression des lignes vides
def clean_liste(liste):
    a1=[]
    for l in liste:
        if re.search("\\S",l):
            a1.append(l)
    return(a1)

## recherche des cartes trouvées par Altf4
def search_cards(clean_liste,titre):
    # compteur name
    cn=0
    # token
    t=[]
    for i in clean_liste:
        # recherche des cartes trouvées
        name=re.search("<div class=.h4 grid-view-item__title.>",i)
        if name:
            if re.search("<div class=.h4 grid-view-item__title.>"+titre,i):
                t.append(cn)
                #print("<h4 class=.name small-12 medium-4. itemprop=.name. title=."+titre)
            cn+=1
    return(t)


## calcul prix
def calcul_prix(clean_liste,t):
    # compteur price
    cp=0
    #liste des prix
    p=[]
    #liste des quantités
    qt=[]
    for i in range(0,len(clean_liste)):
        price=((re.search("<select name=.id. data-section=.template..\d{1,}..content. class=.product-form..variants no-js.>",clean_liste[i-1]) and re.search("<option  selected=.selected.  value=.\d{1,}. data-available=.[1-9]. data-price=..\d{1,}.\d{1,}",clean_liste[i])))
        noprice=(re.search("<select name=.id. data-section=.template--\d{1,}__content. class=.product-form__variants no-js.>",clean_liste[i-1]) and re.search("<option  selected=.selected.  value=.\d{1,}. data-available=.0. data-price=..\d{1,}.\d{1,}",clean_liste[i]))
        if price or noprice:
            #print("ok")
            if cp in t:
                #print("ok bis")
                if price:
                    test=(re.search("data-price=..\d{1,}.\d{1,}",price.group(0)).group(0))
                    #print((re.search("\d{1,}.\d{1,}",test).group(0)))
                    p.append(float(re.search("\d{1,}.\d{1,}",test).group(0)))
                    q=[*(re.search("<select name=.id. data-section=.template--\d{1,}",clean_liste[i-1]).group(0))]
                    #print(q[len(q)-1])
                    qt.append(int(q[len(q)-1]))
                #elif noprice:
                    #print("no stock")
            cp+=1
    return(p,qt)


## decklist
def DecklistCB(path):
    decklist1 = open(path,'r')
    lines = decklist1.readlines()
    tableau=[]
    for l in lines:
        l=l.strip('\n')
        l=l.split(" ")
        l=' '.join(l[1:])
        time.sleep(1)
        input2=urllib.parse.quote_plus(l)
        cl=clean_liste(url_request('CardBrawlers',input2))
        list_prices=calcul_prix(cl,search_cards(cl,l))
        if list_prices!=([], []):
            items = list(zip(list_prices[0], list_prices[1]))
            items.sort(key=lambda x: x[0])
            sorted_prices, sorted_quantities = zip(*items)
            tableau.append([l,sorted_quantities[0],sorted_prices[0]])
        else:
            tableau.append([l,0,100000])
    return(tableau)


## decklist
def DecklistOnlyCB(path):
    decklist1 = open(path,'r')
    lines = decklist1.readlines()
    total=0
    tableau=[]
    for l in lines:
        l=l.strip('\n')
        l=l.split(" ")
        qt_wanted=int(l[0])
        #print(qt_wanted)
        qt_wanted_bis=qt_wanted
        l=' '.join(l[1:])
        #pour ne pas surcharger le site de requetes
        time.sleep(1)
        input2=urllib.parse.quote_plus(l)
        #print(input2)
        liste=l.split(" ")

        cl=clean_liste(url_request('CardBrawlers',input2))
        list_prices=calcul_prix(cl,search_cards(cl,l))
        #print(list_prices)
        if list_prices!=([], []):
            items = list(zip(list_prices[0], list_prices[1]))
            items.sort(key=lambda x: x[0])
            #print(items)
            prix=0
            sorted_prices, sorted_quantities = zip(*items)
            if qt_wanted >= sum(sorted_quantities) :
                #print(l,": quantités disponibles: ",sum(sorted_quantities))
                #print("Acheter toutes les copies disponibles pour: ",sum(sorted_prices))
                #print("________________________________________________________________")
                prix=sum(price * quantity for price, quantity in zip(sorted_prices, sorted_quantities))
                tableau.append([l,qt_wanted_bis,sum(sorted_quantities),prix])
            else:
                for i in range(sum((sorted_quantities))):
                    if qt_wanted>0:
                        if sorted_quantities[i]<=qt_wanted:
                            prix+=sorted_quantities[i]*sorted_prices[i]
                            qt_wanted=qt_wanted-sorted_quantities[i]
                        else:
                            prix+=qt_wanted*sorted_prices[i]
                            qt_wanted=0
                #print(qt_wanted_bis,'x',l,':',prix,'CAD$')
                #print("________________________________________________________________")
                tableau.append([l,qt_wanted_bis,qt_wanted_bis,prix])
            total+=prix
        else:
            #print(l,": out of stock")
            #print("________________________________________________________________")
            tableau.append([l,qt_wanted_bis,0,0])
    print("------tableau cardbrawlers loaded------")
    return(tableau,total)
















