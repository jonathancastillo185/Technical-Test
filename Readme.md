# Prueba Técnica

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

- El script produce dos bases de datos, una correspondiente a películas y otra a series.
- Se registra el tiempo de ejecución de cada ejecución del script en el archivo "registro.txt".
- Se proporciona un notebook Jupyter en la carpeta "Notebook" con los pasos realizados y ejemplos de procesos para validar la veracidad de los resultados.
- El script principal que orquesta la obtención y procesamiento de la información se encuentra en la carpeta "Script". Las funciones utilizadas en el proceso ETL están almacenadas en la carpeta "Functions".

### Bases de datos:

![Alt text](/image/Peliculas.jpg)
