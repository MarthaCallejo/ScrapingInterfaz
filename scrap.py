import requests
from bs4 import BeautifulSoup

# URL del sitio web
url = "https://tienda.durigutti.com/"

# Realizar una solicitud GET al sitio web
def estraccion_links_menu(url):
    response = requests.get(url)
    lista_links = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        menu = soup.find(class_="sub-menu")
        links = menu.find_all("a")
        for link in links:
            direccion = link.get("href")
            print(direccion)
            lista_links.append(direccion) #A cada enlace que extrae la agrego a la lista
        print("--------------------------------")
        print(lista_links)
    else:
        print("Error al obtener la página:", response.status_code)
    
    return lista_links

lista_enlaces_menu = estraccion_links_menu(url)


def extraccion_links_vinos(lista_enlaces_menu):
    vinos_enlaces = []                   
    for enlace in lista_enlaces_menu:
        pagina_vinos = requests.get(enlace)
        sopa = BeautifulSoup(pagina_vinos.text, "html.parser")
        productos = sopa.find_all(class_="title-wrapper")
        for producto in productos:
            links_vinos = producto.find_all('a')
            print(producto.text.strip()) 
            for link in links_vinos:
                vinos_enlaces.append(link.get("href"))
                print(link.get("href"))
                print("--------------------")
        print("Seccion completada\n-----------------------------")
    print(vinos_enlaces)
    return vinos_enlaces

extraccion_links_vinos(lista_enlaces_menu)
    
