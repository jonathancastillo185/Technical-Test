import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
import shutil
from bs4 import BeautifulSoup
import requests

def print_process(texto):
    terminal_width, _ = shutil.get_terminal_size()  # Obtener el ancho del terminal
    longitud_total = terminal_width - 2  # Longitud total de la línea (restando el espacio para los bordes)
    espacio_alrededor = (longitud_total - len(texto)) // 2  # Espacio alrededor del texto

    # Imprimir la línea con el texto centrado
    print("|" + "-" * espacio_alrededor + texto + "-" * espacio_alrededor + "|")


def categories():    
    """
        Con esta funcion extraemos todas las categorias de la pagina 'https://filmzie.com/home'
    """
    try:
        driver = webdriver.Chrome()
        
        driver.get("https://filmzie.com/home")

        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "category-burger"))
        )

        button.click()

        menu_items = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".categories .category")))

        categorias = [x.text.lower().replace(" ","_").replace("-","_") for x in menu_items]

        print_process("Categorias capturadas correctamente.")
        
        return categorias[1:]
    
    except:
        print("Error al inicializar el navegador:", e)
        return []
    
    finally:

        driver.quit()


def get_titles(driver):
    """
    Función auxiliar para obtener los títulos de una página web.
    """
    titulos_element = driver.find_elements(By.CSS_SELECTOR, "p.title")

    titulos = [titulo.text.lower().replace(" ", "-") for titulo in titulos_element]
    
    return titulos


def movies_for_category(category):
    """
    Ingresa una categoría y esta función dirigirá a la URL específica de esta categoría 
    y devolverá la cantidad de títulos dentro de la misma.
    """
    intentos = 5
    for intento in range(intentos):
        try:
            # Inicializar el navegador Chrome
            driver = webdriver.Chrome()
            
            # Abrir la página web
            driver.get(f"https://filmzie.com/category/{category}")

            # Esperar hasta que aparezca al menos un título
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "p.title"))
            )

            # Definir la altura inicial de la página
            last_height = driver.execute_script("return document.body.scrollHeight")

            # Realizar scroll hacia abajo hasta que la altura de la página ya no aumente
            while True:
                # Scroll hacia abajo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Esperar un poco para que carguen los nuevos elementos
                time.sleep(2)

                # Calcular la nueva altura de la página
                new_height = driver.execute_script("return document.body.scrollHeight")

                # Si la altura de la página ya no aumenta, salir del bucle
                if new_height == last_height:
                    break

                # Actualizar la altura de la página
                last_height = new_height

            # Obtener los títulos utilizando la función auxiliar
            titulos = get_titles(driver)
            
            print_process(f"Todas las peliculas de la categoria '{category}' capturadas correctamente.")
            
            return titulos

        except WebDriverException as e:
            print(f"Error al intentar obtener los títulos para la categoría {category}: {e}")
            if intento < intentos - 1:
                print(f"{category} Reintentando...")
                time.sleep(2)  # Esperar un poco antes de intentar nuevamente
            else:
                print(f"Se han agotado los {intentos} intentos. No se pueden obtener los títulos para la categoría {category}.")
                return []

        finally:
            # Cerrar el navegador
            driver.quit()
            
            
def movies(titulo):
    # URL de la página web a analizar
    url = f"https://filmzie.com/content/{titulo}"

    # Realizar la solicitud GET a la página web
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Obtener el contenido HTML de la página
        html_content = response.content

        # Crear un objeto BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        nombre_extraccion = ["titulo","ano","duracion","categorias","descripcion"]
        lista_extraccion = ["fw-bold title","year","duration","category","fs-18"]
        
        diccionario_extraccion = {}
        
        for nombre , clase in zip(nombre_extraccion,lista_extraccion):
            diccionario_extraccion[nombre] = soup.find(class_=clase).get_text()

        diccionario_extraccion["link"] = url

        print(diccionario_extraccion)
        # Ahora puedes usar el objeto soup para buscar y analizar el contenido HTML según sea necesario
        # Por ejemplo:
        # title = soup.title
        # print(title)
    else:
        print("Error al cargar la página:", response.status_code)