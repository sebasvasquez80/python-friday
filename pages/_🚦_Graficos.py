import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(layout="wide")
st.title("Análisis de Ventas de Videojuegos")
st.markdown("""
Este proyecto analiza tendencias y patrones en la industria de videojuegos. A través de gráficos interactivos, podrás explorar:
- Ventas por género, plataforma, editor y año.
- Comparación entre regiones.
- Juegos más vendidos.
""")

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

df['Año'] = pd.to_numeric(df['Año'], errors='coerce') # Convierte no-números a NaN
df['Año'] = df['Año'].astype('Int64') # Usa el tipo entero que permite NaNs (Int64)

for col in ['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Ventas_OTRAS', 'Ventas_GLOBALES']:
    if col in df.columns:
        df[col] = df[col].fillna(0) # Rellena NaN con 0 en columnas de ventas

df['Editor'] = df['Editor'].fillna('Desconocido')
df['Género'] = df['Género'].fillna('Desconocido')

st.subheader("Vista previa del dataset")
st.dataframe(df.head(20))

tabs = st.tabs([
    "Vista General",
    "Análisis Regional",
    "Tendencias Anuales",
    "Exploración por Género",
    "Análisis de Editores",
    "Comparaciones Avanzadas"
])

with tabs[0]:
    st.header("Resumen y Top Globales")

    with st.expander("Ventas globales por género (Resumen)"):
        genero_ventas = df.groupby("Género")["Ventas_GLOBALES"].sum().reset_index()
        fig1 = px.bar(genero_ventas, x="Género", y="Ventas_GLOBALES", color="Género",
                      title="Ventas Globales Totales por Género")
        st.plotly_chart(fig1, use_container_width=True)

    with st.expander("Top 10 plataformas por ventas globales"):
        top_plataformas = df.groupby("Plataforma")["Ventas_GLOBALES"].sum().nlargest(10).reset_index()
        fig2 = px.bar(top_plataformas, x="Plataforma", y="Ventas_GLOBALES", color="Plataforma",
                      title="Top 10 Plataformas por Ventas Globales")
        st.plotly_chart(fig2, use_container_width=True)

    with st.expander("Top 10 juegos más vendidos globalmente"):
        top_juegos = df.sort_values("Ventas_GLOBALES", ascending=False).head(10)
        fig5 = px.bar(top_juegos, x="Nombre", y="Ventas_GLOBALES", color="Plataforma",
                      title="Top 10 Juegos Más Vendidos (Global)")
        st.plotly_chart(fig5, use_container_width=True)

    with st.expander("Distribución de Ventas por Género y Plataforma (Sunburst)"):
        fig11 = px.sunburst(df, path=["Género", "Plataforma"], values="Ventas_GLOBALES",
                            title="Distribución de Ventas por Género y Plataforma")
        st.plotly_chart(fig11, use_container_width=True)

with tabs[1]:
    st.header("Análisis Detallado de Ventas por Región")

    with st.expander("Distribución General de Ventas por Región"):
        ventas_regiones = df[["Ventas_NA", "Ventas_EU", "Ventas_JP", "Ventas_OTRAS"]].sum()
        fig_pie_regiones = px.pie(values=ventas_regiones, names=ventas_regiones.index,
                                  title="Proporción de Ventas Globales por Región")
        st.plotly_chart(fig_pie_regiones, use_container_width=True) 

    with st.expander("Ventas por Género en Norteamérica"):
        na_genero = df.groupby("Género")["Ventas_NA"].sum().reset_index()
        fig6 = px.bar(na_genero, x="Género", y="Ventas_NA", title="Ventas por Género en Norteamérica")
        st.plotly_chart(fig6, use_container_width=True)

    with st.expander("Ventas por Género en Japón"):
        jp_genero = df.groupby("Género")["Ventas_JP"].sum().reset_index()
        fig7 = px.bar(jp_genero, x="Género", y="Ventas_JP", title="Ventas por Género en Japón")
        st.plotly_chart(fig7, use_container_width=True)

    with st.expander("Comparativa Regional de un Género Específico"):
        genero_sel = st.selectbox("Selecciona un Género:", df["Género"].unique(), key="comp_gen_regional") # Clave única
        genero_df = df[df["Género"] == genero_sel]
        ventas_genero_region = genero_df[["Ventas_NA", "Ventas_EU", "Ventas_JP", "Ventas_OTRAS"]].sum()
        ventas_genero_region_df = ventas_genero_region.reset_index()
        ventas_genero_region_df.columns = ['Región', 'Ventas']

        fig8 = px.bar(ventas_genero_region_df, x='Región', y='Ventas',
                      title=f"Ventas por Región para el Género: {genero_sel}",
                      labels={'Región': 'Región', 'Ventas': 'Ventas'})
        st.plotly_chart(fig8, use_container_width=True)

with tabs[2]:
    st.header("Tendencias y Evolución Anual")

    with st.expander("Evolución de Ventas Globales por Año"):
        ventas_anuales = df.groupby("Año")["Ventas_GLOBALES"].sum().reset_index()
        fig_anual_global = px.line(ventas_anuales, x="Año", y="Ventas_GLOBALES", markers=True,
                                  title="Tendencia de Ventas Globales a lo Largo del Tiempo") # Renombrado fig4 a fig_anual_global
        st.plotly_chart(fig_anual_global, use_container_width=True)

    with st.expander("Número de Juegos Lanzados por Año"):
        conteo_anual = df["Año"].value_counts().reset_index()
        conteo_anual.columns = ['Año', 'Cantidad']
        conteo_anual = conteo_anual.sort_values("Año", ascending=True)

        fig_juegos_anual = px.bar(conteo_anual, x="Año", y="Cantidad",
                                 title="Número de Juegos Lanzados por Año")
        st.plotly_chart(fig_juegos_anual, use_container_width=True)

    with st.expander("Tendencia de un Género Específico a lo Largo de los Años"):
        genero_anual_sel = st.selectbox("Selecciona un Género:", df["Género"].unique(), key="tend_gen_anual") # Clave única
        df_gen_anual = df[df["Género"] == genero_anual_sel]
        ventas_gen_anual = df_gen_anual.groupby("Año")["Ventas_GLOBALES"].sum().reset_index()
        fig14 = px.line(ventas_gen_anual, x="Año", y="Ventas_GLOBALES", markers=True,
                        title=f"Tendencia de Ventas Globales para {genero_anual_sel} por Año")
        st.plotly_chart(fig14, use_container_width=True)


    with st.expander("Heatmap de Ventas por Año y Plataforma (Top 10 Plataformas)"):
        top_plats = df["Plataforma"].value_counts().head(10).index
        heat_df = df[df["Plataforma"].isin(top_plats)]
        
        pivot = heat_df.pivot_table(values="Ventas_GLOBALES", index="Plataforma", columns="Año", aggfunc="sum").fillna(0)
        fig12 = px.imshow(pivot, labels=dict(color="Ventas Globales"),
                          title="Heatmap de Ventas por Plataforma y Año")
        st.plotly_chart(fig12, use_container_width=True)

with tabs[3]:
    st.header("Exploración Detallada por Género")

    generos = df['Género'].unique()
    genero_seleccionado_tab3 = st.selectbox(
        "Selecciona un Género para analizar:",
        sorted(generos),
        key='selectbox_genero_exploracion_tab3' 
    )

    df_genero_filtrado = df[df['Género'] == genero_seleccionado_tab3]

    with st.expander(f"**Ventas Totales del Género: {genero_seleccionado_tab3}**"):
        total_ventas_genero = df_genero_filtrado["Ventas_GLOBALES"].sum()
        st.metric(label=f"Ventas Globales Totales para {genero_seleccionado_tab3}",
                  value=f"{total_ventas_genero:,.2f} millones $")

        ventas_por_plataforma_genero = df_genero_filtrado.groupby("Plataforma")["Ventas_GLOBALES"].sum().reset_index()
        ventas_por_plataforma_genero = ventas_por_plataforma_genero.sort_values("Ventas_GLOBALES", ascending=False)
        fig_ventas_genero_plataforma = px.bar(
            ventas_por_plataforma_genero.head(10), 
            x="Ventas_GLOBALES",
            y="Plataforma",
            orientation='h', 
            title=f"Ventas Globales por Plataforma para el Género: {genero_seleccionado_tab3} (Top 10 Plataformas)",
            labels={"Ventas_GLOBALES": "Ventas Globales (millones)", "Plataforma": "Plataforma"},
            color="Plataforma" 
        )
        fig_ventas_genero_plataforma.update_layout(yaxis={'categoryorder':'total ascending'}) 
        st.plotly_chart(fig_ventas_genero_plataforma, use_container_width=True)

    with st.expander(f"**Top 10 Juegos del Género: {genero_seleccionado_tab3}**"):
        if not df_genero_filtrado.empty: 
            top_10_juegos_genero = df_genero_filtrado.sort_values(
                "Ventas_GLOBALES", ascending=False
            ).head(10)[["Nombre", "Plataforma", "Año", "Ventas_GLOBALES"]]

            st.dataframe(top_10_juegos_genero, hide_index=True) 

            fig_top_10_juegos = px.bar(
                top_10_juegos_genero,
                x="Ventas_GLOBALES",
                y="Nombre",
                orientation='h',
                title=f"Top 10 Juegos Más Vendidos en el Género: {genero_seleccionado_tab3}",
                labels={"Ventas_GLOBALES": "Ventas Globales (millones)", "Nombre": "Nombre del Juego"},
                color="Plataforma" 
            )
            fig_top_10_juegos.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_top_10_juegos, use_container_width=True)
        else:
            st.warning(f"No hay datos de juegos disponibles para el género: {genero_seleccionado_tab3}.")

with tabs[4]:
    st.header("Análisis de Ventas por Editor")

    with st.expander("Top 10 Editores por Ventas Globales"):
        top_editores = df.groupby("Editor")["Ventas_GLOBALES"].sum().nlargest(10).reset_index()
        fig9 = px.bar(top_editores, x="Editor", y="Ventas_GLOBALES", color="Editor",
                      title="Top 10 Editores Globales")
        st.plotly_chart(fig9, use_container_width=True)

    with st.expander("Comparación de Ventas Globales de Editores Seleccionados"):
        editores_top = df.groupby('Editor')['Ventas_GLOBALES'].sum().sort_values(ascending=False).head(20).index.tolist()

        editores_seleccionados = st.multiselect("Selecciona Editores para comparar:", editores_top,
                                                default=editores_top[:5], key='multiselect_editores_comparacion')
        df_editores_filtrados = df[df['Editor'].isin(editores_seleccionados)]
        df_editor_ventas = df_editores_filtrados.groupby('Editor')['Ventas_GLOBALES'].sum().reset_index()
        fig_comp_editores = px.bar(df_editor_ventas, x='Editor', y='Ventas_GLOBALES',
                                  title="Ventas Globales de Editores Seleccionados")
        st.plotly_chart(fig_comp_editores, use_container_width=True)

with tabs[5]:
    st.header("Comparaciones y Relaciones entre Variables")

    with st.expander("Comparación de Ventas por Continente y Plataforma"):
        plataformas = st.multiselect("Selecciona Plataformas:", df['Plataforma'].unique(),
                                     default=['PS2', 'X360', 'Wii'], key='multiselect_plataformas_comparacion') # Clave única
        df_filtro_plataforma = df[df['Plataforma'].isin(plataformas)]
        ventas_por_plataforma_region = df_filtro_plataforma.groupby('Plataforma')[['Ventas_NA', 'Ventas_EU', 'Ventas_JP', 'Ventas_OTRAS']].sum().reset_index()
        ventas_por_plataforma_region = ventas_por_plataforma_region.melt(id_vars='Plataforma', var_name='Región', value_name='Ventas')
        fig_comp_plataforma_region = px.bar(ventas_por_plataforma_region, x='Plataforma', y='Ventas',
                                           color='Región', barmode='group',
                                           title="Ventas por Región y Plataforma Seleccionada")
        st.plotly_chart(fig_comp_plataforma_region, use_container_width=True)

    with st.expander("Comparación de Ventas entre Dos Regiones"):
        col1, col2 = st.columns(2)
        with col1:
            region1 = st.selectbox("Selecciona Región 1:", ["Ventas_NA", "Ventas_EU", "Ventas_JP", "Ventas_OTRAS"], key="reg1_comparacion") # Clave única
        with col2:
            region2 = st.selectbox("Selecciona Región 2:", ["Ventas_NA", "Ventas_EU", "Ventas_JP", "Ventas_OTRAS"], key="reg2_comparacion") # Clave única

        fig_scatter_regiones = px.scatter(df, x=region1, y=region2, color="Género",
                                         title=f"Comparativa de Ventas: {region1.replace('Ventas_', '')} vs {region2.replace('Ventas_', '')}",
                                         labels={region1: f"Ventas {region1.replace('Ventas_', '')}", region2: f"Ventas {region2.replace('Ventas_', '')}"})
        st.plotly_chart(fig_scatter_regiones, use_container_width=True)