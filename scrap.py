import requests
from bs4 import BeautifulSoup

# URL del sitio web
url = "https://tienda.durigutti.com/"

# Realizar una solicitud GET al sitio web
response = requests.get(url)

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
        print(link.get("href"))
else:
    print("Error al obtener la página:", response.status_code)
    
