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


from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# -------------- PARAMETROS

espera = 10

# -------------- 


def inicio_driver():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    
    # En caso de querer ver el proceso con la ventana del navegador comentar la siguiente linea
    opts.add_argument("--headless")
    
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts)

    return driver
    
    
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
    comienzo = time.time()
    try:
        driver = inicio_driver()
        
        driver.get("https://filmzie.com/home")

        button = WebDriverWait(driver, espera).until(
            EC.presence_of_element_located((By.CLASS_NAME, "category-burger"))
        )

        button.click()

        menu_items = WebDriverWait(driver, espera).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".categories .category")))

        categorias = [x.text.lower().replace(" ","_").replace("-","_") for x in menu_items]

        fin = time.time()
        
        print_process("Categorias capturadas correctamente.")
        print_process(f"Categorias demoro {round((fin-comienzo),2)} segundos")
        
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
    links_element = driver.find_elements(By.CSS_SELECTOR, "a")

    link = [link.get_attribute("href") for link in links_element]
    
    return link


def movies_for_category(category):
    """
    Ingresa una categoría y esta función dirigirá a la URL específica de esta categoría 
    y devolverá la cantidad de títulos dentro de la misma.
    """
    comienzo = time.time()
    intentos = 5
    
    for intento in range(intentos):
        try:
            driver = inicio_driver()
            
            driver.get(f"https://filmzie.com/category/{category}")

            WebDriverWait(driver, espera).until(
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
                
                last_height = new_height

            # Obtener los títulos utilizando la función auxiliar
            titulos = get_titles(driver)
            
            fin = time.time()
            
            print_process(f"Todo el contenido de la categoria '{category}' fue capturado correctamente, demoro {round((fin-comienzo),2)} segundos")
            
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
            
            
def movies(url):
    try:
        # Realizar la solicitud GET a la página web
        response = requests.get(url)

        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Obtener el contenido HTML de la página
            html_content = response.content

            # Crear un objeto BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")
            
            diccionario_extraccion = {}
            
            try:
                diccionario_extraccion["titulo"] = soup.find(class_="fw-bold title").text
                diccionario_extraccion["ano"] = soup.find(class_="year").text
                diccionario_extraccion["duracion"] = soup.find(class_="duration").text
                diccionario_extraccion["categorias"] = soup.find(class_="category").text
                diccionario_extraccion["descripcion"] = soup.find(class_="fs-18").text
                diccionario_extraccion["tipo"] = "Pelicula"
                diccionario_extraccion["link"] = url

                
            except:
                diccionario_extraccion["titulo"] = soup.find(class_="fw-bold title").text
                diccionario_extraccion["ano"] = soup.find(class_="year").text
                diccionario_extraccion["duracion"] = "0 min"
                diccionario_extraccion["categorias"] = soup.find(class_="category").text
                diccionario_extraccion["descripcion"] = soup.find(class_="fs-18").text
                diccionario_extraccion["tipo"] = "Serie"
                diccionario_extraccion["link"] = url
                
            return diccionario_extraccion
        
        else:
            print(f"Error al cargar la url {url} :", response.status_code)
    except Exception as e:
        print("Se produjo un error durante la solicitud o el análisis de la página:", e)


def search(soup,*arg):
    """
        Primero ingresar componente de bs4 a analizar.
        luego Ingresar los valores a buscar anidados de la siguiente manera
        primer componente : "div/class"
        segundo componente : "p/class"
        y asi sucesivamente.
    """
    lista = [x.split("/") for x in arg]
    
    alm = soup
    
    for x in lista:

        alm = alm.find(x[0], class_=x[1])
    
    return alm.text
    
def get_images(soup,*arg):
    
    


def movies(url):
    for _ in range(2):  # Intentar dos veces
        try:
            # Realizar la solicitud GET a la página web
            response = requests.get(url)

            # Verificar si la solicitud fue exitosa (código de estado 200)
            if response.status_code == 200:
                # Obtener el contenido HTML de la página
                html_content = response.content

                # Crear un objeto BeautifulSoup
                soup = BeautifulSoup(html_content, "html.parser")

                # Crear un diccionario para almacenar los datos
                diccionario_extraccion = {}

                try:
                    try:
                        diccionario_extraccion["titulo"] = soup.find(class_="fw-bold title").text
                        diccionario_extraccion["idioma"] = search(soup,"div/audio fs-15 label margin-bottom-30","p/d-inline-block")
                        diccionario_extraccion["subtitulos"] = search(soup,"div/subtitle fs-15 label", "p/fw-bold")
                        diccionario_extraccion["ano"] = soup.find(class_="year").text
                        diccionario_extraccion["duracion_minutos"] = soup.find(class_="duration").text
                        diccionario_extraccion["categorias"] = soup.find(class_="category").text
                        diccionario_extraccion["sinopsis"] = soup.find(class_="fs-18").text
                        diccionario_extraccion["tipo"] = "Pelicula"
                        diccionario_extraccion["link"] = url
                    except:
                        diccionario_extraccion["titulo"] = soup.find(class_="fw-bold title").text
                        diccionario_extraccion["idioma"] = search(soup,"div/audio fs-15 label margin-bottom-30","p/d-inline-block")
                        diccionario_extraccion["subtitulos"] = search(soup,"div/subtitle fs-15 label", "p/fw-bold")
                        diccionario_extraccion["ano"] = soup.find(class_="year").text
                        diccionario_extraccion["duracion_minutos"] = "0 min"
                        diccionario_extraccion["categorias"] = soup.find(class_="category").text
                        diccionario_extraccion["sinopsis"] = soup.find(class_="fs-18").text
                        diccionario_extraccion["tipo"] = "Serie"
                        diccionario_extraccion["link"] = url
                except Exception as e:
                    # Si hay algún error al extraer los datos, imprimir el error y continuar con la siguiente iteración
                    print(f"Error al extraer los datos de la url {url} en el intento {_+1}: {e}")
                    continue
                
                return diccionario_extraccion

            else:
                print(f"Error al cargar la url {url} en el intento {_+1}: {response.status_code}")
        except Exception as e:
            print(f"Se produjo un error durante el intento {_+1} de la solicitud o el análisis de la página {url}: {e}")

    # Si todas las iteraciones fallan, retornar None
    return None