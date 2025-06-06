import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# --- TU API Key de OpenWeatherMap ---
# ¡IMPORTANTE! Reemplaza 'TU_API_KEY_AQUI' con la clave que obtuviste de OpenWeatherMap.
# Para esta demostración, la ponemos aquí directamente.
# En un proyecto real, se recomienda usar Streamlit secrets (.streamlit/secrets.toml) para mayor seguridad.
OPENWEATHER_API_KEY = "e7d9ee85aa20d4d42484e78fbb095b2d" # <<== ¡PEGA TU CLAVE AQUÍ!

# --- URL base de la API de OpenWeatherMap ---
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# --- Función para obtener datos del clima (con cache) ---
# El ttl=60 significa que la API solo se llamará cada 60 segundos por ciudad,
# incluso si el usuario presiona el botón antes, a menos que el botón fuerce un re-ejecute total.
@st.cache_data(ttl=60)
def get_weather_data(city_name: str, api_key: str):
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric", # Para obtener temperaturas en grados Celsius
        "lang": "es"       # Para descripciones en español
    }
    try:
        response = requests.get(OPENWEATHER_BASE_URL, params=params)
        response.raise_for_status() # Lanza un error para códigos de estado HTTP 4xx/5xx
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos del clima para '{city_name}': {e}")
        st.error("Asegúrate de que la ciudad sea válida y tu API Key de OpenWeatherMap esté correcta y activa.")
        return None

# --- Cuerpo de la Aplicación Streamlit ---
st.title("☀️ Dashboard de Clima Global (Actualización Manual)")
st.markdown("Consulta el clima actual de diversas ciudades y actualiza los datos con un botón.")

# Lista de ciudades para seleccionar (puedes ampliarla)
cities = [
    "Medellín", "Bogotá", "Cali", "Barranquilla", "Cartagena",
    "Londres", "Nueva York", "París", "Tokio", "Sídney", "Buenos Aires", "Madrid", "Ciudad de México"
]

# Usamos st.session_state para almacenar la última ciudad seleccionada y controlar el refresco
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = cities[0] # Valor por defecto

selected_city_from_widget = st.selectbox("Selecciona una Ciudad:", cities, key="city_selector")

# Si la ciudad seleccionada ha cambiado, actualizamos el estado de la sesión
if selected_city_from_widget != st.session_state.selected_city:
    st.session_state.selected_city = selected_city_from_widget
    # Forzamos un re-ejecute completo para cargar los datos de la nueva ciudad
    # y así el botón de actualizar funcione sobre ella
    st.rerun() # <== ¡CAMBIO AQUÍ!

# --- Botón de Actualizar Datos ---
if st.button("Actualizar Datos"):
    # Cuando se presiona el botón, invalida el caché de la función get_weather_data
    # Esto fuerza una nueva llamada a la API la próxima vez que se ejecute la función
    st.cache_data.clear() # ¡Importante para forzar el refresco!
    st.rerun() # <== ¡CAMBIO AQUÍ!

# Condición para avisar si la clave no se ha reemplazado
if OPENWEATHER_API_KEY == "TU_API_KEY_AQUI":
    st.warning("¡ATENCIÓN! Por favor, reemplaza 'TU_API_KEY_AQUI' en el código por tu clave real de OpenWeatherMap. "
               "Puedes obtenerla registrándote gratuitamente en openweathermap.org.")
elif st.session_state.selected_city: # Usamos la ciudad del estado de la sesión
    weather_data = get_weather_data(st.session_state.selected_city, OPENWEATHER_API_KEY)
    
    if weather_data:
        # Extraer datos clave para mostrar
        temp_celsius = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description'].capitalize()
        lat = weather_data['coord']['lat']
        lon = weather_data['coord']['lon']
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"

        st.markdown(f"### Clima Actual en {st.session_state.selected_city}")
        
        # Diseño en columnas para la información principal
        col_icon, col_metrics = st.columns([1, 3])
        with col_icon:
            st.image(icon_url, width=80)
        with col_metrics:
            st.metric(label="Temperatura", value=f"{temp_celsius:.1f} °C")
            st.metric(label="Humedad", value=f"{humidity}%")
            st.write(f"**Condición:** {description}")
        
        st.info(f"Datos mostrados a las: {pd.to_datetime('now').strftime('%H:%M:%S')}")

        # --- Mapa de la ciudad ---
        st.subheader("Ubicación en el Mapa")
        # Crear un DataFrame para st.map con latitud y longitud
        map_df = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(map_df, zoom=10) # Zoom ajustado para ver la ciudad
        
        # --- Gráfico de datos actuales (ejemplo: humedad) ---
        st.subheader("Visualización de Datos")
        current_data = pd.DataFrame({
            'Métrica': ['Temperatura (°C)', 'Humedad (%)'],
            'Valor': [temp_celsius, humidity]
        })
        fig_metrics = px.bar(
            current_data,
            x='Métrica',
            y='Valor',
            title=f'Métricas Actuales en {st.session_state.selected_city}',
            color='Métrica',
            template="plotly_white",
            height=300
        )
        st.plotly_chart(fig_metrics, use_container_width=True)

    else:
        st.warning(f"No se pudieron cargar los datos del clima para '{st.session_state.selected_city}'.")