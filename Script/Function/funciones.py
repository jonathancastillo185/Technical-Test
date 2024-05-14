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


import datetime
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# -------------- PARAMETROS

espera = 10

# -------------- 


def inicio_driver():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    
    # En caso de querer ver el proceso con la ventana del navegador comentar la siguiente linea
    # opts.add_argument("--headless")
    
    driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=opts)

    return driver
    

def print_process(texto,fin=True):
    """
    Con esta función imprimimos en terminal el proceso centrado con su duración,
    además de generar y agregar a un archivo de tipo texto (llamado registro.txt)
    el registro de su ejecución paso a paso con horario y duración de procesos.
    
    Args:
        *texto (str): Texto a imprimir.
        fin (bool): Indica si es el fin del proceso o no (por defecto es True).
    """
    
    terminal_width, _ = shutil.get_terminal_size() 
    longitud_total = terminal_width - 2 
    espacio_alrededor = (longitud_total - len(texto)) // 2

    print("|" + "-" * espacio_alrededor + texto + "-" * espacio_alrededor + "|")

    if fin:
        ahora = datetime.datetime.now()
        with open("registro.txt", "a") as f:
            f.write(f"{ahora.strftime('%d/%m/%Y %H:%M:%S')} - {texto}\n")
    else:
        ahora = datetime.datetime.now()
        with open("registro.txt", "a") as f:
            f.write(f"{ahora.strftime('%d/%m/%Y %H:%M:%S')} - {'-' * 20 + ' Fin del script ' + '-' * 20}\n")


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
        Obtiene los titulos de la pagina.
    """
    links_element = driver.find_elements(By.CSS_SELECTOR, "a")

    link = [link.get_attribute("href") for link in links_element]
    
    return link


def movies_for_category(category):
    """
    Ingresa una categoría y esta función dirigirá a la URL específica de esta categoría 
    y devolverá la cantidad de títulos dentro de la misma.
    
    Args:
    Str: nombre de la categoria
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
            
            
def search(soup, *arg):
    """
        Primero ingresar componente de bs4 a analizar.
        luego Ingresar los valores a buscar anidados.
        
        Args:
        primer componente : "div/class"
        segundo componente : "p/class"
        y asi sucesivamente.
    """
    try:
        lista = [x.split("/") for x in arg]
        alm = soup
        for x in lista:
            alm = alm.find(x[0], class_=x[1])
        
        return alm.text
    except:
        return None

def movies(url):
    """
    Esta función busca información sobre películas o series en una página web.

    Args:
    url (str): La URL de la página web que contiene la información de la película o serie.

    Returns:
    dict or None: Un diccionario con la información de la película o serie si se encuentra, o None si hay algún error.
    """
    for _ in range(4):  # Cantidad de intentos antes de devolver error
        try:
            response = requests.get(url)

            if response.status_code == 200:
                html_content = response.content

                soup = BeautifulSoup(html_content, "html.parser")

                diccionario_extraccion = {}

                try:
                    try:
                        diccionario_extraccion["titulo"] = soup.find(class_="fw-bold title").text
                        diccionario_extraccion["idioma"] = search(soup,"div/audio fs-15 label margin-bottom-30","p/d-inline-block")
                        diccionario_extraccion["subtitulos"] = search(soup,"div/subtitle fs-15 label", "span/")
                        diccionario_extraccion["ano"] = soup.find(class_="year").text
                        diccionario_extraccion["duracion_minutos"] = soup.find(class_="duration").text
                        diccionario_extraccion["categorias"] = soup.find(class_="category").text
                        diccionario_extraccion["sinopsis"] = soup.find(class_="fs-18").text
                        diccionario_extraccion["tipo"] = "Pelicula"
                        diccionario_extraccion["link"] = url
                    except:
                        diccionario_extraccion["titulo"] = soup.find(class_="fw-bold title").text
                        diccionario_extraccion["idioma"] = search(soup,"div/audio fs-15 label margin-bottom-30","p/d-inline-block")
                        diccionario_extraccion["subtitulos"] = search(soup,"div/subtitle fs-15 label", "span/")
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

    return None


def generador_dummies(df):
    """
    Esta función convierte las categorías en columnas binarias (dummies).

    Args:
    df (DataFrame): El DataFrame de pandas con una columna llamada 'categorias' que contiene listas de categorías.

    Returns:
    DataFrame: El DataFrame modificado con las columnas de categorías binarias.
    """
    df['categorias'] = df['categorias'].str.split(', ')

    all_categories = set([cat for sublist in df['categorias'].tolist() for cat in sublist])

    for category in all_categories:
        df[category] = df['categorias'].apply(lambda x: 1 if category in x else 0)

    df.drop(columns=['categorias'], inplace=True)

    return df




def season_click(driver, div):
    """
    Esta función hace clic en una temporada específica.

    Args:
    driver: El controlador del navegador.
    texto (str): El texto de la temporada en la que se hará clic.
    """
    try:
        season = driver.find_element(By.XPATH, f"/html/body/main/div/div/div[3]/div[2]/div[2]/div[1]/button")
        
        season.click()
        
        time.sleep(2)
        
        season_num = driver.find_element(By.XPATH, f"/html/body/main/div/div/div[3]/div[2]/div[2]/div[1]/div/button[{div}]")
        
        season_num.click()
        
        return True
    except:
        return False


def capitulo_click(driver, div):
    """
    Esta función hace clic en un elemento con el texto especificado.

    Args:
    driver: El controlador del navegador.
    texto (str): El texto del elemento en el que se hará clic.
    """
    try:
        capitulo = driver.find_element(By.XPATH, f"/html/body/main/div/div/div[3]/div[2]/div[2]/div[2]/div/div/div[{div}]/p")
        
        capitulo.click()
        
        return True
    except:
        return False


def series_informacion(url):    
    """
    Esta función extrae información sobre las temporadas y capítulos de una serie desde la URL proporcionada.
    
    Args:
    url (str): La URL de la serie en la página web.

    Returns:
    dict: Un diccionario con la información de la serie.
    """
    intentos = 3  # Número de intentos
    espera_1 = 10  # Tiempo de espera máximo en segundos
    serie = {}   # Diccionario para almacenar la información de la serie
        
    try:
        comienzo = time.time()

        driver = inicio_driver()
        
        # Intentamos obtener la página hasta 3 veces
        for _ in range(intentos):
            try:
                driver.get(url)
                time.sleep(3)
                break
            except WebDriverException as e:
                print(f"Error al cargar la página: {e}")
                print("Intentando nuevamente...")

        
        titulo = driver.find_element(By.XPATH, "/html/body/main/div/div/div[2]/div/div[2]/h1").text
        
        serie = {"titulo" : [], "temporada" : [], "capitulos" : [], "sinopsis" : [], "duracion_minutos" : []}

        button = WebDriverWait(driver, espera_1).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn.select-trigger.text-white.bg-transparent.fs-16"))
        )
        
        button.click()

        menu_temporadas = WebDriverWait(driver, espera_1).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".btn.fs-15.block.text-white > span"))
        )
        
        cant_temporadas = [x.text for x in menu_temporadas]
        
        button.click()
        cont_1 = 1
        
        time.sleep(2)
        
        for temporada in cant_temporadas:
            try:
                bloque_1 = season_click(driver, cont_1)
                time.sleep(2)
                if bloque_1 == True:
                    capitulos_temporada = WebDriverWait(driver, espera_1).until(
                        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".episode-title.fs-16.fw-bold"))
                    )
                    capitulos_temporada = [x.text for x in capitulos_temporada]

                    alm = {"titulo" : [],"temporada" : [],"capitulo" : [], "sinopsis" : [], "duracion_minutos" : []}
                    
                    cont_2 = 1

                    for capitulo in capitulos_temporada:
                        try:
                            bloque_2 = capitulo_click(driver, cont_2)
                            
                            if bloque_2 == True:
                                
                                sinopsis = driver.find_element(By.XPATH, "/html/body/main/div/div/div[3]/div[2]/div[2]/div[3]/div/div[1]/p[2]").text
                                duracion = driver.find_element(By.XPATH, "/html/body/main/div/div/div[2]/div/div[2]/div/p/span[3]").text

                                alm["titulo"].append(titulo)
                                alm["temporada"].append(temporada)
                                alm["capitulo"].append(capitulo)
                                alm["sinopsis"].append(sinopsis)
                                alm["duracion_minutos"].append(int(duracion.replace(" min","")))
                                
                            else:
                                break
                            cont_2 += 1
                            
                        except (TimeoutException, NoSuchElementException) as e:
                            print(f"No se pudo obtener información del capítulo {capitulo}: {e}")

                    serie["titulo"].append(alm["titulo"])
                    serie["temporada"].append(alm["temporada"])
                    serie["capitulos"].append(alm["capitulo"])
                    serie["sinopsis"].append(alm["sinopsis"])
                    serie["duracion_minutos"].append(alm["duracion_minutos"])
                else:
                    break
                cont_1 += 1
            except TimeoutException as e:
                print(f"No se pudo obtener información de la temporada {temporada}: {e}")

        driver.quit()

        tiempo_total = time.time() - comienzo
        print(f"Tiempo total de {titulo}: {round(tiempo_total,2)} segundos")

        return serie["titulo"], serie["temporada"], serie["capitulos"], serie["sinopsis"], serie["duracion_minutos"]

    except TimeoutException as e:
        
        driver.quit()
        
        return f"Error de procesamiento {url}"
    
    


def union_lista(lista):
    alm = []
    for x in lista:
        for i in x:
            for l in i:
                alm.append(l)
    return alm

def desempaquetado(df):
    total_informacion = {}

    for x in df.keys():
        total_informacion[x] = union_lista(df[x])
    return total_informacion