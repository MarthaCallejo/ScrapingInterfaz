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
            lista_links.append(direccion)  # A cada enlace que extrae lo agrego a la lista
    else:
        print("Error al obtener la página:", response.status_code)
    
    return lista_links

def extraccion_links_vinos(lista_enlaces_menu):
    vinos_enlaces = []
    for enlace in lista_enlaces_menu:
        pagina_vinos = requests.get(enlace)
        sopa = BeautifulSoup(pagina_vinos.text, "html.parser")
        productos = sopa.find_all(class_="title-wrapper")
        for producto in productos:
            links_vinos = producto.find_all('a')
            for link in links_vinos:
                vinos_enlaces.append(link.get("href"))
    return vinos_enlaces

def obtener_descripcion_producto(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        descripcion = soup.find(class_="product-short-description")
        if descripcion:
            return descripcion.text.strip()
        else:
            return "Descripción no encontrada"
    else:
        return "Error al obtener la página:", response.status_code

lista_enlaces_menu = estraccion_links_menu(url)
vinos_enlaces = extraccion_links_vinos(lista_enlaces_menu)

for vino_url in vinos_enlaces:
    descripcion = obtener_descripcion_producto(vino_url)
    print(f"Descripción del producto en {vino_url}:\n{descripcion}\n")
