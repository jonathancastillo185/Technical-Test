import re
import time
import datetime
import requests
import pandas as pd
import multiprocessing
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from Function.funciones import movies_for_category, categories, print_process, movies, series_informacion, desempaquetado, generador_dummies

# -------------- Parametros --------------
ruta_base = r'.\\Bases_datos\\'

# ----------------------------------------

print_process("Comienzo del Script 'Scraping'")

comienzo_script = time.time()

categorias = categories()

num_nucleos = multiprocessing.cpu_count()
resultados_dict = {}
categorias_comienzo = time.time()

# Ejecutamos la captura de datos de manera paralela
with ThreadPoolExecutor(max_workers=num_nucleos) as executor:
    resultados = list(executor.map(movies_for_category, categorias))
    
    for categoria, resultado in zip(categorias, resultados):
        resultados_dict[categoria] = resultado

peliculas_total = []

for x,i in resultados_dict.items():
    for e in i:
        peliculas_total.append(e)

peliculas_total = set(peliculas_total)
categorias_fin = time.time()

print_process(f"La extraccion total de las categorias tubo una demora de {round((categorias_fin-categorias_comienzo),2)} segundos")

peliculas_total = [x for x in peliculas_total if "/content/" in x]

print_process("Comienzo del proceso de extraccion de informacion de cada iteracion (demora unos 6 minutos)")

# Crear un diccionario para almacenar los resultados
todo = {"titulo": [],"idioma" : [], "subtitulos" : [], "ano": [], "duracion_minutos": [], "categorias": [], "sinopsis": [], "tipo": [], "link": []}

comienzo_movies = time.time()

with ThreadPoolExecutor(max_workers=num_nucleos) as executor:
    # Ejecutar la función para cada categoría en paralelo
    resultados = list(executor.map(movies, peliculas_total))

    try:
        for resultado in resultados:
            for clave, valor in resultado.items():
                todo[clave].append(valor)
    except:
        print()

fin_movies = time.time()

print_process(f"El proceso de captura de la informacion de todo el contenido fue exsitoso, y demoro {round((fin_movies - comienzo_movies) / 60,2)} minutos")

# Convertimos la informacion extraida en un Dataframe
df = pd.DataFrame(todo)

# Exportamos el total de la informacion
df.to_csv("{}Peliculas_Series_Completo_Respaldo.csv".format(ruta_base) , index=False)

# Filtramos la informacion para separar las peliculas de series
peliculas = df.loc[df["tipo"] == "Pelicula"].reset_index(drop=True)
series = df.loc[df["tipo"] == "Serie"].reset_index(drop=True)

# Limpieza de informacion peliculas
peliculas["duracion_minutos"] = peliculas["duracion_minutos"].str.replace(" min","").astype(int)
peliculas.loc[peliculas["idioma"] == 'Non linguistic content', "idioma"] = "No contiene idioma"
peliculas["subtitulos"] = peliculas["subtitulos"].fillna("No contiene subtitutlos")

# Exportamos base de datos de Peliculas
peliculas.to_csv("{}Peliculas.csv".format(ruta_base),index=False)

# Generamos base de datos de peliculas con dummies para facilitar su etapa de analisis
peliculas_dummies = generador_dummies(peliculas)

# Exportamos base de datos de Peliculas con dummies
peliculas_dummies.to_csv("{}Peliculas_dummies.csv".format(ruta_base),index=False)

# Limpieza de series
series.drop(columns=['duracion_minutos'], inplace=True)
series.loc[series["idioma"] == 'Non linguistic content', "idioma"] = "No contiene idioma"
series["subtitulos"] = series["subtitulos"].fillna("No contiene subtitulos")

# Exportamos la base de datos de series
series.to_csv("{}series.csv".format(ruta_base),index=False)

# Comenzamos con el proceso de captura de informacion de cada serie
links_series = list(series["link"].values)
resultados_dict = {"titulo": [], "temporadas": [], "capitulos": [], "sinopsis" : [], "duracion_minutos" : []}

series_comienzo = time.time()

# Ejecutamos la captura en paralelo
with ThreadPoolExecutor(max_workers=num_nucleos) as executor:
    resultados_temporales = list(executor.map(series_informacion, links_series))

titulos, temporadas, capitulos, sinopsis, duracion_minutos = zip(*resultados_temporales)

resultados_dict["titulo"].extend(titulos)
resultados_dict["temporadas"].extend(temporadas)
resultados_dict["capitulos"].extend(capitulos)
resultados_dict["sinopsis"].extend(sinopsis)
resultados_dict["duracion_minutos"].extend(duracion_minutos)

series_fin = time.time()

print_process(f"La extraccion total de informacion de cada serie tuvo una demora de {round((series_fin-series_comienzo)/ 60, 2) } minutos")

series_meta = pd.DataFrame(desempaquetado(resultados_dict))

# Exportamos toda la informacion de series por separado
series_meta.to_csv("{}series_meta.csv".format(ruta_base), index=False)

# Exportamos la base de datos de serie con un merge de toda la informacion obtenida
series_todo = pd.merge(series,series_meta, on="titulo", how="inner")

series_todo.rename(columns={'sinopsis_y': 'sinopsis_capitulo'}, inplace=True)

series_todo.to_csv("{}series_completo.csv".format(ruta_base), index = False)

print_process(f"El script completo tubo una demora de {round((time.time()-comienzo_script),2)} minutos")

print_process(fin=False)