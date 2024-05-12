import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC

from concurrent.futures import ThreadPoolExecutor
import multiprocessing

from Functions.function import movies_for_category, categories

categorias = categories()


# Obtener la cantidad de núcleos disponibles en el sistema
num_nucleos = multiprocessing.cpu_count()

# Crear un diccionario para almacenar los resultados
resultados_dict = {}

with ThreadPoolExecutor(max_workers=num_nucleos) as executor:
    # Ejecutar la función para cada categoría en paralelo
    resultados = list(executor.map(movies_for_category, categorias))
    
    # Asignar los resultados al diccionario
    for categoria, resultado in zip(categorias, resultados):
        resultados_dict[categoria] = resultado

