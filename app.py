import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="City Lifestyle Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stAlert {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- FUNCIÓN DE CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Cargar el dataset desde el archivo local
    try:
        df = pd.read_csv("city_lifestyle_dataset.csv")
        return df
    except FileNotFoundError:
        st.error("No se encontró el archivo 'city_lifestyle_dataset.csv'. Asegúrate de que está en la misma carpeta.")
        return None

df = load_data()

# --- DICCIONARIO DE COORDENADAS REGIONALES (Aproximadas) ---
# Usado para el mapa de burbujas por región
REGION_COORDS = {
    'Europe': {'lat': 54.5, 'lon': 15.2},
    'Asia': {'lat': 34.0, 'lon': 100.6},
    'North America': {'lat': 54.5, 'lon': -105.2},
    'South America': {'lat': -8.7, 'lon': -55.5},
    'Africa': {'lat': -8.7, 'lon': 34.5},
    'Oceania': {'lat': -25.2, 'lon': 133.7}
}

# --- FUNCIÓN "PLAIN LANGUAGE" PARA CORRELACIONES ---
def interpreter_correlacion(valor_corr, var_x, var_y):
    """Traduce un valor numérico de correlación a lenguaje natural."""
    abs_corr = abs(valor_corr)
    
    # Determinar fuerza
    if abs_corr < 0.2:
        fuerza = "No hay una relación clara"
        explicacion = f"Los datos sugieren que '{var_x}' y '{var_y}' no están conectados significativamente."
    elif abs_corr < 0.5:
        fuerza = "Relación Moderada"
        tipo = "sube" if valor_corr > 0 else "baja"
        explicacion = f"Existe una cierta tendencia: A veces, cuando aumenta '{var_x}', también {tipo} '{var_y}'."
    else:
        fuerza = "🔥 Relación Fuerte y Clara"
        tipo = "AUMENTA" if valor_corr > 0 else "DISMINUYE"
        explicacion = f"Patrón Evidente: Generalmente, si una ciudad tiene mayor '{var_x}', su '{var_y}' {tipo} notablemente."
        
    return fuerza, explicacion

# --- BARRA LATERAL (SIDEBAR) ---
st.sidebar.header("🎛️ Panel de Control")

if df is not None:
    # Filtro por Región (Country)
    regiones_disponibles = sorted(df['country'].unique())
    regiones_seleccionadas = st.sidebar.multiselect(
        "Filtrar por Región:",
        options=regiones_disponibles,
        default=regiones_disponibles
    )
    
    # Aplicar filtro
    df_filtered = df[df['country'].isin(regiones_seleccionadas)]
    
    st.sidebar.markdown("---")
    st.sidebar.info(f"Mostrando **{len(df_filtered)}** ciudades de {len(df)} totales.")

    # --- BODY PRINCIPAL ---
    st.title("🌍 Análisis de Estilos de Vida Urbano")
    st.markdown("Descubre patrones ocultos sobre cómo vivimos, cuánto ganamos y qué tan felices somos alrededor del mundo.")

    # ==========================================
    # SECCIÓN A: ANALÍTICA DESCRIPTIVA
    # ==========================================
    st.header("1. Panorama Actual (Descriptivo)")
    
    # 1. KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Felicidad Promedio", f"{df_filtered['happiness_score'].mean():.2f}/10")
    with col2:
        st.metric("Ingreso Promedio", f"${df_filtered['avg_income'].mean():,.0f}")
    with col3:
        st.metric("Renta Promedio", f"${df_filtered['avg_rent'].mean():,.0f}")
    with col4:
        st.metric("Ciudades Analizadas", len(df_filtered))

    st.markdown("---")

    # 2. Mapa Mundial de Regiones
    col_mapa, col_box = st.columns([2, 1])
    
    with col_mapa:
        st.subheader("🗺️ Mapa Global de Felicidad")
        # Preparar datos para el mapa (agrupados por región)
        df_region = df_filtered.groupby('country').agg({
            'happiness_score': 'mean',
            'population_density': 'mean',
            'city_name': 'count'
        }).reset_index()
        
        # Asignar coordenadas manuales
        df_region['lat'] = df_region['country'].map(lambda x: REGION_COORDS.get(x, {}).get('lat'))
        df_region['lon'] = df_region['country'].map(lambda x: REGION_COORDS.get(x, {}).get('lon'))
        
        # Crear mapa
        fig_map = px.scatter_geo(
            df_region,
            lat='lat',
            lon='lon',
            size='city_name', # Tamaño = cantidad de ciudades en la muestra
            color='happiness_score',
            hover_name='country',
            projection="natural earth",
            color_continuous_scale=px.colors.sequential.Viridis,
            size_max=30,
            title="Felicidad Promedio por Región (Tamaño = N° Ciudades)"
        )
        fig_map.update_layout(height=400, margin={"r":0,"t":30,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with col_box:
        st.subheader("📊 Variedad de Opciones")
        metric_box = st.selectbox("Comparar regiones por:", 
                                ['happiness_score', 'avg_rent', 'avg_income', 'air_quality_index'], 
                                index=0)
        
        fig_box = px.box(df_filtered, x='country', y=metric_box, points="outliers", 
                         title=f"Distribución de {metric_box}")
        fig_box.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

    # 3. Rankings
    st.subheader("🏆 Top Rankings")
    col_rank_opt, col_rank_chart = st.columns([1, 3])
    
    with col_rank_opt:
        ranking_metric = st.selectbox("¿Qué quieres rankear?", 
                                     ['happiness_score', 'avg_income', 'public_transport_score', 'internet_penetration'])
        top_n = st.slider("Número de ciudades", 5, 20, 10)
        ascending = st.checkbox("Mostrar los peores (Ascendente)", value=False)
    
    with col_rank_chart:
        df_sorted = df_filtered.sort_values(by=ranking_metric, ascending=ascending).head(top_n)
        fig_bar = px.bar(df_sorted, x=ranking_metric, y='city_name', orientation='h', color='country',
                         title=f"Top {top_n} Ciudades - {ranking_metric}")
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================
    # SECCIÓN B: ANALÍTICA INTERPRETATIVA
    # ==========================================
    st.markdown("---")
    st.header("2. Interpretación y Descubrimiento (El 'Por Qué')")
    st.info("💡 Esta sección te ayuda a entender las relaciones ocultas en los datos usando un lenguaje sencillo.")

    # 1. Explorador de Relaciones
    st.subheader("🔍 Explorador de Tendencias")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        x_axis = st.selectbox("Eje X (Causa Potencial):", 
                             ['avg_income', 'avg_rent', 'population_density', 'internet_penetration'], index=0)
    with c2:
        y_axis = st.selectbox("Eje Y (Efecto):", 
                             ['happiness_score', 'life_expectancy', 'air_quality_index', 'public_transport_score'], index=0)
    with c3:
        size_var = st.selectbox("Tamaño de burbuja:", ['population_density', 'avg_income'], index=0)

    # Gráfico de Dispersión
    fig_scatter = px.scatter(df_filtered, x=x_axis, y=y_axis, size=size_var, color='country',
                             hover_name='city_name', trendline="ols", 
                             title=f"Relación: {x_axis} vs {y_axis}")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # INTERPRETACIÓN AUTOMÁTICA (PLAIN LANGUAGE)
    if len(df_filtered) > 1:
        corr_val = df_filtered[x_axis].corr(df_filtered[y_axis])
        fuerza_txt, explicacion_txt = interpreter_correlacion(corr_val, x_axis, y_axis)
        
        st.success(f"""
        **Análisis Automático:** {fuerza_txt} (Correlación: {corr_val:.2f})  
        👉 {explicacion_txt}
        """)

    st.markdown("---")

    # 2. Buscador de Ciudad Ideal
    st.subheader("✨ Encuentra tu Ciudad Ideal")
    st.markdown("Ajusta tus preferencias y el algoritmo encontrará las mejores coincidencias para ti.")
    
    # Inputs de usuario (Sliders)
    col_pref1, col_pref2, col_pref3 = st.columns(3)
    
    with col_pref1:
        w_econ = st.slider("Importancia Económica (Renta baja/Ingreso alto)", 0, 10, 5)
    with col_pref2:
        w_wellbeing = st.slider("Importancia Bienestar (Felicidad/Aire/Verde)", 0, 10, 8)
    with col_pref3:
        w_tech = st.slider("Importancia Conexión (Internet/Transporte)", 0, 10, 5)
    
    if st.button("🔍 Calcular Recomendaciones"):
        # Algoritmo de Recomendación Simple (Normalización Min-Max y Puntuación Ponderada)
        df_rec = df_filtered.copy()
        
        # Normalizar columnas (0 a 1)
        # Para Renta, menor es mejor -> 1 - normalizado
        cols_to_norm = ['avg_income', 'avg_rent', 'happiness_score', 'air_quality_index', 
                        'green_space_ratio', 'internet_penetration', 'public_transport_score']
        
        for col in cols_to_norm:
            min_v = df_rec[col].min()
            max_v = df_rec[col].max()
            if max_v - min_v == 0:
                df_rec[f'norm_{col}'] = 0
            else:
                df_rec[f'norm_{col}'] = (df_rec[col] - min_v) / (max_v - min_v)
        
        # Invertir Renta (Menos es mejor) y Aire (Depende del índice, asumiremos AQI alto = Malo, entonces invertimos)
        # Nota: En dataset, AQI alto suele ser malo.
        df_rec['norm_avg_rent'] = 1 - df_rec['norm_avg_rent']
        df_rec['norm_air_quality_index'] = 1 - df_rec['norm_air_quality_index'] 
        
        # Calcular Score
        # Econ = Ingreso + Renta(invertido)
        # Bienestar = Felicidad + Aire(invertido) + Verde
        # Tech = Internet + Transporte
        
        score_econ = (df_rec['norm_avg_income'] + df_rec['norm_avg_rent']) / 2
        score_well = (df_rec['norm_happiness_score'] + df_rec['norm_air_quality_index'] + df_rec['norm_green_space_ratio']) / 3
        score_tech = (df_rec['norm_internet_penetration'] + df_rec['norm_public_transport_score']) / 2
        
        df_rec['match_score'] = (score_econ * w_econ) + (score_well * w_wellbeing) + (score_tech * w_tech)
        
        # Mostrar Top 3
        top_matches = df_rec.sort_values('match_score', ascending=False).head(5)
        
        st.balloons()
        st.subheader("🎉 ¡Tus Ciudades Ideales!")
        
        # Mostrar resultados en tarjetas bonitas
        for i, (index, row) in enumerate(top_matches.iterrows()):
            with st.container():
                st.markdown(f"### #{i+1} {row['city_name']}, {row['country']}")
                c_a, c_b, c_c = st.columns(3)
                c_a.metric("Felicidad", row['happiness_score'])
                c_b.metric("Renta", f"${row['avg_rent']}")
                c_c.metric("Score Tech", f"{row['public_transport_score']}/100")
                st.progress(int((row['match_score'] / df_rec['match_score'].max()) * 100))
                st.markdown("---")

else:
    st.error("Error al cargar los datos.")
