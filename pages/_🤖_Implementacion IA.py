import streamlit as st
import google.generativeai as genai
import re

# --- Configuración de la API de Gemini ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except KeyError:
    st.error("Error: ¡Clave de API de Google no encontrada! Asegúrate de tener 'GOOGLE_API_KEY' en tu archivo .streamlit/secrets.toml.")
    st.stop() # Detiene la ejecución de la aplicación si no hay clave

# --- Función para listar y seleccionar el modelo adecuado de Gemini ---
@st.cache_resource
def get_available_gemini_model():
    try:
        models = genai.list_models()
        
        # Nombres de modelos preferidos, en orden de prioridad para texto
        preferred_model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro', 'models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']
        
        available_text_models = []
        for m in models:
            # Filtra por modelos que soportan 'generateContent' y que sean solo para texto.
            if ("generateContent" in m.supported_generation_methods and
                "embedding" not in m.name and # Excluir modelos de embedding
                "vision" not in m.name):      # Excluir modelos de visión explícitamente
                available_text_models.append(m.name)
        
        if not available_text_models:
            st.error("No se encontraron modelos de Gemini apropiados para generación de contenido (solo texto) en tu API Key/región.")
            st.stop()

        # Seleccionar el modelo más preferido que esté disponible
        for preferred_name in preferred_model_names:
            if preferred_name in available_text_models:
                return preferred_name
        
        # Si ninguno de los preferidos está disponible, toma el primero de la lista filtrada
        st.warning(f"Ninguno de los modelos preferidos se encontró. Usando el modelo '{available_text_models[0]}'.")
        return available_text_models[0]

    except Exception as e:
        st.error(f"Error al listar modelos de Gemini: {e}. Asegúrate de que tu clave de API sea válida y el servicio esté disponible.")
        st.stop()

# Obtener el nombre del modelo a usar y cargarlo
model_name = get_available_gemini_model()

@st.cache_resource
def load_gemini_model(name):
    return genai.GenerativeModel(name)

model = load_gemini_model(model_name)

# --- Funciones de Generación con Gemini ---

def generar_contenido_gemini(prompt, temperatura=0.7, max_salida_tokens=500): # Aumentado el default de tokens
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=max_salida_tokens,
                temperature=temperatura,
            )
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        st.error(f"Error al generar contenido con Gemini: {e}. Esto puede ocurrir si el contenido viola las políticas de seguridad o si el modelo falla. Intenta ajustar el prompt o las características.")
        return "No se pudo generar el contenido."

# --- Interfaz de Streamlit ---
st.title("Generador de Contenido de Marketing con IA")

## Descripción del Proyecto
st.markdown(f"""
Esta aplicación utiliza **Inteligencia Artificial de Google Gemini ({model_name})** para ayudarte a crear descripciones de productos detalladas y copys publicitarios persuasivos, adaptados a tu **público objetivo** y **tono de marketing** deseado.
""")

# --- Sección de Entrada de Producto ---

## 1. Información del Producto
nombre_generico_producto = st.text_input("Nombre Genérico del Producto (Ej: Cafetera, Smartphone)", "Cafetera")
marca_producto = st.text_input("Marca o Nombre Específico del Modelo (Ej: AromaMax Pro)", "AromaMax Pro")

caracteristicas = st.text_area("Características clave (separadas por comas o líneas)", "Prepara café en 30 segundos, Control por app móvil, Molinillo integrado, Diseño elegante, Capacidad para 10 tazas, Funciona con granos enteros o molidos")

# --- Sección de Opciones de Generación ---

## 2. Opciones de Generación
st.subheader("Generación de Copys para Anuncios y Descripciones")

### Define tu Público Objetivo
publico_objetivo = st.text_input(
    "¿Quién es tu público objetivo? (Ej: Jóvenes profesionales ocupados, amantes del café, familias, gamers, etc.)",
    "Amantes del café que valoran la comodidad y el diseño."
)

### Selecciona el Tono de Marketing
tonos_disponibles = [
    "Informativo (enfoque en datos y funcionalidades)",
    "Emocional (enfoque en sentimientos y experiencias)",
    "Urgente (enfoque en la escasez y la acción rápida)",
    "Innovador (enfoque en tecnología y el futuro)",
    "Divertido (enfoque en el humor y la ligereza)",
    "Lujoso (enfoque en la exclusividad y la calidad premium)",
    "Directo a la venta (énfasis en beneficios y cierre)"
]
tono_seleccionado = st.selectbox("Selecciona el Tono para los Copys Publicitarios y la Descripción:", tonos_disponibles)

### Cantidad y Extensión
num_copys_generar = st.slider("Cantidad de Copys Publicitarios a Generar", 1, 5, 3)
longitud_copys = st.radio("Longitud de los Copys:", ["Cortos (frases directas)", "Medianos (1-2 párrafos)", "Largos (2-4 párrafos, con más detalle)"])


if st.button("Generar Contenido de Marketing", type="primary"):
    if nombre_generico_producto and marca_producto and caracteristicas and publico_objetivo:
        st.subheader("Resultados:")

        # --- Generar Descripción del Producto para E-commerce ---
        st.markdown("---")
        st.write("### Descripción del Producto para E-commerce:")
        with st.spinner("Generando descripción del producto con Gemini..."):
            prompt_descripcion = f"""
            Eres un experto en marketing digital y redacción de descripciones de productos para tiendas online (e-commerce).
            Tu objetivo es crear una descripción de producto atractiva, detallada, concisa, persuasiva y optimizada para la venta.
            Incluye un párrafo introductorio, un párrafo de beneficios/características clave, y una llamada a la acción (CTA) clara al final.

            Producto: '{nombre_generico_producto}'
            Marca/Modelo: '{marca_producto}'
            Características clave: {caracteristicas}
            Público Objetivo: {publico_objetivo}
            Tono de Marketing: {tono_seleccionado}

            Enfócate en cómo este producto resuelve un problema o mejora la vida del cliente.
            Asegúrate de que sea fácil de leer y escanear.
            """
            descripcion = generar_contenido_gemini(prompt_descripcion, max_salida_tokens=400) # Más tokens para descripción
            st.success("Descripción generada:")
            st.info(descripcion)

        # --- Generar Copys para Anuncios ---
        st.markdown("---")
        st.write(f"### Copys para Anuncios (Tono: *{tono_seleccionado.split(' ')[0]}*, Longitud: *{longitud_copys}*)")
        with st.spinner(f"Generando {num_copys_generar} copys con tono '{tono_seleccionado.split(' ')[0]}' y longitud '{longitud_copys}' con Gemini..."):
            
            # Ajustar max_salida_tokens y prompt para la longitud de los copys
            copy_max_tokens = 100 # Default para cortos
            if longitud_copys == "Medianos (1-2 párrafos)":
                copy_max_tokens = 200
            elif longitud_copys == "Largos (2-4 párrafos, con más detalle)":
                copy_max_tokens = 350 # Aumentado significativamente para copys largos

            prompt_copys = f"""
            Eres un copywriter publicitario experto. Tu objetivo es crear {num_copys_generar} copys distintos, persuasivos y optimizados para anuncios de marketing digital (ej. redes sociales, Google Ads).

            Producto: '{nombre_generico_producto}', modelo '{marca_producto}'.
            Características clave: {caracteristicas}
            Público Objetivo: {publico_objetivo}
            El tono para los copys debe ser: **{tono_seleccionado}**.
            La longitud de cada copy debe ser: **{longitud_copys}**.
            Cada copy debe ser conciso (dentro de la longitud especificada), persuasivo, enfocado en un beneficio clave o un llamado a la acción.
            Incluye un llamado a la acción claro al final de cada copy (ej. "¡Compra ahora!", "Descubre más", "Visita nuestra web").
            Formato: Lista numerada de copys.

            Ejemplo de formato de respuesta:
            1. [Copy 1 con CTA]
            2. [Copy 2 con CTA]
            """
            copys_texto_bruto = generar_contenido_gemini(prompt_copys, temperatura=0.9, max_salida_tokens=copy_max_tokens)

            copys_generados = [re.sub(r'^\s*\d+\.\s*', '', line).strip() for line in copys_texto_bruto.split('\n') if re.match(r'^\s*\d+\.', line.strip())]

            if copys_generados:
                for i, copy_text in enumerate(copys_generados[:num_copys_generar]):
                    st.success(f"Copy {i+1}:")
                    st.info(copy_text)
            else:
                st.warning("No se pudieron extraer los copys generados o Gemini no devolvió una lista numerada. Intenta ajustar el prompt o la longitud.")
                st.info(f"Salida bruta de Gemini (para depuración):\n{copys_texto_bruto}")

    else:
        st.warning("Por favor, ingresa toda la información del producto y el público objetivo para generar el contenido.")