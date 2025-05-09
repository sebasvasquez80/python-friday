# Proyecto Integrador - Análisis de Ventas de Videojuegos

Este proyecto es una aplicación web interactiva desarrollada con Streamlit que permite explorar y analizar un conjunto de datos sobre ventas de videojuegos. A través de esta herramienta, los usuarios pueden descubrir patrones y tendencias clave en la industria de los videojuegos, como los géneros más populares, las plataformas con mayor demanda y los títulos más exitosos a lo largo del tiempo.

## Descripción del Proyecto

En este proyecto, se utiliza un enfoque basado en datos para analizar estadísticas de ventas globales de videojuegos. Los usuarios pueden aplicar diversos filtros para explorar el dataset y obtener información valiosa sobre:

- Juegos con ventas globales destacadas.
- Juegos específicos de plataformas o géneros.
- Comparaciones entre editores como Nintendo y Sony.
- Juegos lanzados en plataformas modernas como PS4, Xbox One y PC.
- Juegos con ventas significativas en regiones específicas como Japón o Norteamérica.

El objetivo es proporcionar una visión profunda del mercado global de videojuegos mediante herramientas de análisis de datos.

## Dataset

El dataset utilizado en esta aplicación proviene de Kaggle y está disponible en el siguiente enlace:  
[Video Game Sales Dataset](https://www.kaggle.com/datasets/gregorut/videogamesales)

Este dataset contiene información sobre ventas de videojuegos, incluyendo columnas como:

- Nombre del juego
- Plataforma
- Año de lanzamiento
- Género
- Editor
- Ventas en diferentes regiones (Norteamérica, Europa, Japón, otras regiones)
- Ventas globales

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona o descarga este repositorio en tu computadora.
2. Crea un entorno virtual (opcional pero recomendado):
   ```sh
   python -m venv .venv
   ```
3. Activa el entorno virtual:
   - En Windows:
     ```sh
     .venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
4. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar la aplicación, utiliza el siguiente comando en la terminal:

```sh
streamlit run pages/12_🎮_Proyecto\ integrador.py
```

La aplicación estará disponible en tu navegador en `http://localhost:8501`.

## Funcionalidades Principales

La aplicación incluye los siguientes filtros interactivos para explorar el dataset:

1. **Filtrar por plataforma**: Permite seleccionar una plataforma específica y visualizar los juegos disponibles para ella.
2. **Juegos con ventas globales > 20M**: Muestra los juegos con ventas globales superiores a 20 millones.
3. **Juegos de Nintendo en Wii**: Filtra los juegos publicados por Nintendo en la plataforma Wii.
4. **Juegos publicados por Nintendo o Sony**: Muestra los juegos publicados por estos dos editores.
5. **Juegos de acción en Xbox 360**: Filtra los juegos del género "Acción" en la plataforma Xbox 360.
6. **Juegos en plataformas modernas (PS4, Xbox One, PC)**: Muestra los juegos disponibles en estas plataformas.
7. **Juegos con >1M ventas en Japón**: Filtra los juegos con ventas superiores a 1 millón en Japón.
8. **Ocultar juegos con <5M en ventas globales**: Oculta los juegos con ventas globales inferiores a 5 millones.
9. **Juegos lanzados desde 2010**: Muestra los juegos lanzados a partir del año 2010.
10. **Juegos que NO son de deportes ni carreras**: Excluye los juegos de los géneros "Deportes" y "Carreras".
11. **Juegos de Nintendo con >2M ventas en Norteamérica**: Filtra los juegos de Nintendo con ventas superiores a 2 millones en Norteamérica.

## Estructura del Proyecto

```
├── .streamlit/            # Configuración de Streamlit
│   └── config.toml        # Archivo de configuración (tema, servidor, etc.)
├── assets/                # Recursos estáticos
│   └── vgsales.csv        # Dataset de ventas de videojuegos
├── pages/                 # Páginas de la aplicación
│   └── 12_🎮_Proyecto integrador.py  # Página del proyecto integrador
├── .gitignore             # Archivos ignorados por Git
├── README.md              # Este archivo
└── requirements.txt       # Dependencias del proyecto
```

## Dependencias Principales

- **streamlit**: Framework para crear aplicaciones web interactivas.
- **pandas**: Manipulación y análisis de datos.

Consulta el archivo [`requirements.txt`](requirements.txt) para ver la lista completa de dependencias.

## Consejos para el Desarrollo

- Utiliza la función [`st.help()`](https://docs.streamlit.io/library/api-reference) para obtener ayuda sobre cualquier función de Streamlit.
- Consulta la [documentación oficial de Streamlit](https://docs.streamlit.io/) para más información.
- Utiliza [`st.write()`](https://docs.streamlit.io/library/api-reference/write-magic/st.write) para depurar variables durante el desarrollo.z