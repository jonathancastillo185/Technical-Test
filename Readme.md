<center><h1>Prueba Técnica</h1></center>

## Objetivo

El objetivo de esta prueba técnica es obtener todas las películas y series, incluyendo su metadata: título, año, sinopsis, enlace y duración (solo para películas). La información recopilada debe ser almacenada en una base de datos o en archivos `.json` o `.csv` de forma automática. Se debe proporcionar un ejemplo de la salida generada en el repositorio.

### Plus

- Obtener los episodios de cada serie y su metadata.
- Obtener información adicional/metadata para cada contenido si es posible.
- Identificar el modelo de negocio, el cual es "modelo de suscripción".
- Asegurar que el tiempo de ejecución sea menor a 2 horas.
- Realizar análisis y/o limpieza de la metadata.
- Incluir cualquier otro aspecto relevante que se considere necesario.

## Instalación

1. Clona este repositorio:

    ```bash
    git clone https://github.com/jonathancastillo185/Technical-Test
    ```

2. Navega al directorio del proyecto:

    ```bash
    cd Technical-Test
    ```

3. Crea y activa un entorno virtual (se recomienda usar `venv`):

    ```bash
    python -m venv venv
    ```

    En Windows:

    ```bash
    venv\Scripts\activate
    ```

    En macOS y Linux:

    ```bash
    source venv/bin/activate
    ```

4. Instala las dependencias del proyecto desde el archivo `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```

## Resultados

- El script produce dos bases de datos principales, una correspondiente a [películas](/Bases_datos/Peliculas.csv) y otra a [series](/Bases_datos/series.csv), luego se utiliza la informacion de las mísmas para obtener mas información necesaría.
- Se registra el tiempo de ejecución de cada ejecución del script en el archivo ["registro.txt"](/registro.txt) .
- Se proporciona un [Jupyter Notebook](/Scraping.ipynb) en la carpeta llamada Notebook con los pasos realizados y ejemplos de procesos para validar la veracidad de los resultados.
- El script principal que orquesta la obtención y procesamiento de la información se encuentra en la carpeta script el archivo llamado ["Scraping.py"](/Script/Scraping.py). Las funciones utilizadas en el proceso ETL están almacenadas en la carpeta Functions el archivo llamado ["Function.py"](/Script/Function/funciones.py).
- En la extraccion si un request falla se reintenta las veces establecidas antes de devolver un error, esto se ve reflejado en impresiones de pantalla por medio de la terminal.
- El tiempo total de ejecucion es de 12 minutos (en el archivo llamado "registro.txt" se almacena el tiempo de cada proceso).

### Bases de datos:

A continuacion se adjuntan capturas de pantalla de como se visualiza la informacion extraida de ambos tipos.

<center><h2>Peliculas</h2></center>
<center>
<img src="images\Peliculas.png" alt="Imagen de películas">
</center>

<center><h2>Peliculas Dummies</h2></center>
<center>
<img src="images\peliculas_dummies.png" alt="Imagen de películas">
</center>

<center><h2>Series</h2></center>
<center>
<img src="images\Series_1.png" alt="Imagen de películas">
</center>

<center><h2>Series meta</h2></center>
<center>
<img src="images\series_meta.png" alt="Imagen de películas">
</center>

<center><h2>Series completo</h2></center>
<center>
<img src="images\series_completo.png" alt="Imagen de películas">
</center>

<center><h2>Video demostracion de ejecucion del Script</h2></center>

<center>

[![Video Demo](https://img.youtube.com/vi/dj9wanx66lE/0.jpg)](https://www.youtube.com/watch?v=dj9wanx66lE)

</center>

