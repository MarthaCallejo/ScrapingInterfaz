import requests
from bs4 import BeautifulSoup
import re

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

def obtener_titulo_producto(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titulo = soup.find('h1')
        if titulo:
            return titulo.text.strip()
        else:
            return "Titulo no encontrado"
    else:
        return "Error al obtener la página:", response.status_code
    
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

def obtener_precio_producto(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        price = soup.find(class_='price')
        if price:
            return price.text.strip()
        else:
            return "Precio no encontrada"
    else:
        return "Error al obtener la página:", response.status_code

lista_enlaces_menu = estraccion_links_menu(url)
vinos_enlaces = extraccion_links_vinos(lista_enlaces_menu)

def calculo_de_precio(descripcion,precio):
    numero_buscar = re.search(r'(\d+)\.(\d+)',precio)
    if numero_buscar:
        numero_uno = numero_buscar.group(1)
        numero_dos = numero_buscar.group(2)
        numero_completo = numero_uno + numero_dos
        numero_calcular = int(numero_completo)
    buscar_numero = re.search(r'x(\d+)', descripcion)
    if buscar_numero:
        numero = int(buscar_numero.group(1))
        if numero != 0:
            calculo = numero_calcular/numero
            precio = f"${calculo}"

    return precio

for vino_url in vinos_enlaces:
    titulo = obtener_titulo_producto(vino_url)
    descripcion = obtener_descripcion_producto(vino_url)
    precio = obtener_precio_producto(vino_url)
    precio_calculado = calculo_de_precio(descripcion,precio)
    print(f"Titulo del producto:\n{titulo}\n")
    print(f"Descripción del producto:\n{descripcion}\n")
    if precio_calculado == precio:
        print(f"Precio del producto:\n{precio}\n")
    else:
        print(f"Precio del producto por caja:\n{precio}\n")
        print(f"Precio por unidad:\n{precio_calculado}")
    print("-------------------------------------")
