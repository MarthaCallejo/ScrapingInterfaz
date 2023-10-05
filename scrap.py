import requests
from bs4 import BeautifulSoup

# URL del sitio web
url = "https://tienda.durigutti.com/"

# Realizar una solicitud GET al sitio web
def estraccion_links_menu(url):
    response = requests.get(url)
    lista_links = []
    # Comprobar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Encontrar el menú con la clase "sub-menu"
        menu = soup.find(class_="sub-menu")
        
        # Buscar enlaces dentro del menú
        links = menu.find_all("a")
        
        
        # Imprimir los enlaces encontrados
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
    for enlace in lista_enlaces_menu:
        pagina_vinos = requests.get(enlace)

        sopa = BeautifulSoup(pagina_vinos.text, "html.parser")

        productos = sopa.find_all(class_="title-wrapper")
        
        for producto in productos:
            links_vinos = producto.find_all('a')
            print(producto.text.strip()) 
            for link in links_vinos:
                print(link.get("href"))
                print("--------------------")
        print("Seccion completada\n-----------------------------")

extraccion_links_vinos(lista_enlaces_menu)
    
