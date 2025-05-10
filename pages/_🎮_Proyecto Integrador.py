import streamlit as st
import pandas as pd

st.title("Proyecto integrador")

st.header("Descripción del proyecto")

st.markdown("""En este proyecto, desvelaremos patrones y tendencias clave en la industria mediante la exploración de diversas estadísticas de ventas. Desde analizar los géneros más populares y las plataformas con mayor demanda hasta identificar los títulos más exitosos a lo largo del tiempo, utilizaremos herramientas de análisis de datos para ofrecerte una visión profunda del mercado global de videojuegos.""")

df = pd.read_csv("./assets/vgsales.csv")

df.rename(columns={
    'Name': 'Nombre',
    'Platform': 'Plataforma',
    'Year': 'Año',
    'Genre': 'Género',
    'Publisher': 'Editor',
    'NA_Sales': 'Ventas_NA',
    'EU_Sales': 'Ventas_EU',
    'JP_Sales': 'Ventas_JP',
    'Other_Sales': 'Ventas_OTRAS',
    'Global_Sales': 'Ventas_GLOBALES'
}, inplace=True)

# Mostrar tabla completa o una parte
st.subheader("Vista previa del dataset")
st.dataframe(df.head(20)) 

# 📊 Exploración de datos
st.header("Exploración de Datos del Dataset")

st.subheader("Dimensiones del dataset (filas, columnas)")
st.write(df.shape)

st.subheader("Nombres de las columnas")
st.write(df.columns.tolist())

st.subheader("Tipos de datos por columna")
st.write(df.dtypes)

st.subheader("Primeros registros")
st.write(df.head())

st.subheader("Últimos registros")
st.write(df.tail())

st.subheader("Cantidad total de juegos registrados")
st.write(len(df))

st.subheader("Juegos más vendidos globalmente")
st.write(df[['Nombre', 'Ventas_GLOBALES']].sort_values('Ventas_GLOBALES', ascending=False).head(3))

st.subheader("Consolas (plataformas) disponibles sin repetir")
st.write(sorted(df['Plataforma'].unique()))

st.subheader("Cantidad de juegos por plataforma")
st.write(df['Plataforma'].value_counts())

st.subheader("Géneros disponibles sin repetir")
st.write(sorted(df['Género'].unique()))

st.subheader("Cantidad de juegos por género")
st.write(df['Género'].value_counts())

st.subheader("Editoriales (publishers) más comunes")
st.write(df['Editor'].value_counts().head(10))

st.subheader("Cantidad de juegos por editorial (top 10)")
st.write(df['Editor'].value_counts().head(10))

st.subheader("Años con más lanzamientos")
st.write(df['Año'].value_counts().sort_index(ascending=True).tail(10))

st.subheader("Año mínimo y máximo de lanzamiento")
st.write(f"Año mínimo: {int(df['Año'].min())}, Año máximo: {int(df['Año'].max())}")

st.subheader("Ventas globales promedio por género")
st.write(df.groupby('Género')['Ventas_GLOBALES'].mean().sort_values(ascending=False))

st.subheader("Ventas globales promedio por plataforma")
st.write(df.groupby('Plataforma')['Ventas_GLOBALES'].mean().sort_values(ascending=False))

st.header("Filtros del dataset")

if 'platform_filter' not in st.session_state:
    st.session_state['platform_filter'] = False

if st.button(" 🕹️ Filtrar por plataforma"):
    st.session_state['platform_filter'] = not st.session_state['platform_filter']
if st.session_state['platform_filter']:
    st.subheader("Filtrar por plataforma")
    plataformas = df['Plataforma'].unique()  
    plataforma_seleccionada = st.selectbox("Filtrar por plataforma", opciones := sorted(plataformas))
    df_filtrado = df[df['Plataforma'] == plataforma_seleccionada]
    st.subheader(f"Juegos para la plataforma: {plataforma_seleccionada}")
    st.dataframe(df_filtrado)

if 'mostrar_global_20m' not in st.session_state:
    st.session_state['mostrar_global_20m'] = False
if 'mostrar_nintendo_wii' not in st.session_state:
    st.session_state['mostrar_nintendo_wii'] = False
if 'mostrar_nintendo_sony' not in st.session_state:
    st.session_state['mostrar_nintendo_sony'] = False
if 'mostrar_accion_x360' not in st.session_state:
    st.session_state['mostrar_accion_x360'] = False
if 'mostrar_modernas' not in st.session_state:
    st.session_state['mostrar_modernas'] = False
if 'mostrar_jp_1m' not in st.session_state:
    st.session_state['mostrar_jp_1m'] = False
if 'mostrar_global_5m_ocultar' not in st.session_state:
    st.session_state['mostrar_global_5m_ocultar'] = False
if 'mostrar_anio_2010' not in st.session_state:
    st.session_state['mostrar_anio_2010'] = False
if 'mostrar_no_deportes_carreras' not in st.session_state:
    st.session_state['mostrar_no_deportes_carreras'] = False
if 'mostrar_nintendo_na_2m' not in st.session_state:
    st.session_state['mostrar_nintendo_na_2m'] = False

# Filtro 1: Ventas globales mayores a 20 millones
if st.button("🔝 Juegos con ventas globales > 20M"):
    st.session_state['mostrar_global_20m'] = not st.session_state['mostrar_global_20m']
if st.session_state['mostrar_global_20m']:
    st.dataframe(df[df['Ventas_GLOBALES'] > 20])

# Filtro 2: Juegos de Nintendo en Wii
if st.button("🎮 Juegos de Nintendo en Wii"):
    st.session_state['mostrar_nintendo_wii'] = not st.session_state['mostrar_nintendo_wii']
if st.session_state['mostrar_nintendo_wii']:
    filtro = df[(df['Editor'] == 'Nintendo') & (df['Plataforma'] == 'Wii')]
    st.dataframe(filtro)

# Filtro 3: Juegos publicados por Nintendo o Sony
if st.button("🆚 Juegos publicados por Nintendo o Sony"):
    st.session_state['mostrar_nintendo_sony'] = not st.session_state['mostrar_nintendo_sony']
if st.session_state['mostrar_nintendo_sony']:
    filtro = df[(df['Editor'] == 'Nintendo') | (df['Editor'] == 'Sony Computer Entertainment')]
    st.dataframe(filtro)

# Filtro 4: Juegos de acción en Xbox 360
if st.button("⚔️ Juegos de acción en Xbox 360"):
    st.session_state['mostrar_accion_x360'] = not st.session_state['mostrar_accion_x360']
if st.session_state['mostrar_accion_x360']:
    st.dataframe(df.query("Género == 'Action' and Plataforma == 'X360'"))

# Filtro 5: Juegos en plataformas modernas
plataformas_deseadas = ['PS4', 'XOne', 'PC']
if st.button("🖥️ Juegos en plataformas modernas (PS4, XOne, PC)"):
    st.session_state['mostrar_modernas'] = not st.session_state['mostrar_modernas']
if st.session_state['mostrar_modernas']:
    st.dataframe(df[df['Plataforma'].isin(plataformas_deseadas)])

# Filtro 6: Ventas en Japón mayores a 1 millón (usa where)
if st.button("🗾 Juegos con >1M ventas en Japón"):
    st.session_state['mostrar_jp_1m'] = not st.session_state['mostrar_jp_1m']
if st.session_state['mostrar_jp_1m']:
    st.dataframe(df.where(df['Ventas_JP'] > 1).dropna())

# Filtro 7: Ocultar juegos con ventas globales < 5M (mask)
if st.button("🙈 Ocultar juegos con <5M en ventas globales"):
    st.session_state['mostrar_global_5m_ocultar'] = not st.session_state['mostrar_global_5m_ocultar']
if st.session_state['mostrar_global_5m_ocultar']:
    st.dataframe(df.mask(df['Ventas_GLOBALES'] < 5))

# Filtro 8: Juegos desde 2010 en adelante
if st.button("📅 Juegos lanzados desde 2010"):
    st.session_state['mostrar_anio_2010'] = not st.session_state['mostrar_anio_2010']
if st.session_state['mostrar_anio_2010']:
    st.dataframe(df[df['Año'] >= 2010])

# Filtro 9: Juegos que no son de deportes ni carreras
if st.button("🚫 Juegos que NO son de deportes ni carreras"):
    st.session_state['mostrar_no_deportes_carreras'] = not st.session_state['mostrar_no_deportes_carreras']
if st.session_state['mostrar_no_deportes_carreras']:
    st.dataframe(df[~df['Género'].isin(['Sports', 'Racing'])])

# Filtro 10: Juegos de Nintendo con buenas ventas en NA
if st.button("🏙️ Juegos de Nintendo con >2M ventas en Norteamerica (NA)"):
    st.session_state['mostrar_nintendo_na_2m'] = not st.session_state['mostrar_nintendo_na_2m']
if st.session_state['mostrar_nintendo_na_2m']:
    filtro = df[(df['Editor'] == 'Nintendo') & (df['Ventas_NA'] > 2)]
    st.dataframe(filtro)