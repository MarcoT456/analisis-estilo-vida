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

# ==============================================================================
# DICCIONARIO ETIQUETAS - Humanización de Variables
# ==============================================================================
ETIQUETAS = {
    'city_name': '🏙️ Ciudad',
    'country': '🌍 Región',
    'population_density': '👥 Densidad Poblacional',
    'avg_income': '💰 Ingreso Mensual ($)',
    'internet_penetration': '📶 Conectividad Digital (%)',
    'avg_rent': '🏠 Renta Promedio ($)',
    'air_quality_index': '🌬️ Índice Calidad del Aire',
    'public_transport_score': '🚇 Transporte Público',
    'happiness_score': '😊 Nivel de Felicidad',
    'green_space_ratio': '🌳 Espacios Verdes (%)',
    'life_expectancy': '❤️ Esperanza de Vida'
}

# Diccionario inverso para obtener la clave técnica desde la etiqueta
ETIQUETAS_INV = {v: k for k, v in ETIQUETAS.items()}

# ==============================================================================
# PALETA DE COLORES PERSONALIZADA
# ==============================================================================
COLORES_PERSONALIZADOS = [
    '#2E86AB',  # Azul profundo
    '#A23B72',  # Magenta
    '#F18F01',  # Naranja cálido
    '#C73E1D',  # Rojo coral
    '#5C4D7D',  # Púrpura
    '#95C623',  # Verde lima
]

SECUENCIA_COLORES = px.colors.qualitative.Set2

# ==============================================================================
# DICCIONARIO DE COORDENADAS REGIONALES (Para el mapa)
# ==============================================================================
REGION_COORDS = {
    'Europe': {'lat': 54.5, 'lon': 15.2},
    'Asia': {'lat': 34.0, 'lon': 100.6},
    'North America': {'lat': 54.5, 'lon': -105.2},
    'South America': {'lat': -8.7, 'lon': -55.5},
    'Africa': {'lat': -8.7, 'lon': 34.5},
    'Oceania': {'lat': -25.2, 'lon': 133.7}
}

# ==============================================================================
# ESTILOS CSS PERSONALIZADOS
# ==============================================================================
st.markdown("""
<style>
    .main .block-container {
        padding-top: 1.5rem;
    }
    .winner-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 25px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.4);
        margin-bottom: 20px;
    }
    .winner-title {
        font-size: 1.3rem;
        margin-bottom: 5px;
        opacity: 0.9;
    }
    .winner-city {
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .runner-up-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: #f0f2f6;
        border-radius: 10px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# FUNCIÓN DE CARGA DE DATOS
# ==============================================================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("city_lifestyle_dataset.csv")
        return df
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'city_lifestyle_dataset.csv'. Asegúrate de que está en la misma carpeta.")
        return None

df = load_data()

# ==============================================================================
# FUNCIÓN DE INTERPRETACIÓN DE CORRELACIONES (Estilo Consultor)
# ==============================================================================
def interpretar_correlacion(valor_corr, var_x, var_y):
    """Traduce un valor numérico de correlación a lenguaje de consultor."""
    abs_corr = abs(valor_corr)
    
    # Obtener nombres amigables
    nombre_x = ETIQUETAS.get(var_x, var_x)
    nombre_y = ETIQUETAS.get(var_y, var_y)
    
    if abs_corr < 0.2:
        icono = "🔍"
        titulo = "Relación No Significativa"
        texto = f"""
        Tras analizar los datos, **no encontramos una conexión clara** entre {nombre_x} y {nombre_y}.
        
        *En otras palabras:* Conocer el valor de una variable no nos ayuda a predecir la otra. 
        Son factores independientes en estas ciudades.
        """
        tipo_alerta = "info"
        
    elif abs_corr < 0.5:
        icono = "📊"
        direccion = "positiva" if valor_corr > 0 else "negativa"
        verbo = "tiende a aumentar" if valor_corr > 0 else "tiende a disminuir"
        titulo = f"Tendencia Moderada ({direccion.title()})"
        texto = f"""
        Detectamos una **relación moderada**: cuando {nombre_x} es mayor, {nombre_y} {verbo}.
        
        *Esto sugiere que:* Existe cierta conexión, aunque hay otros factores en juego. 
        Un análisis más profundo podría revelar variables intermedias.
        """
        tipo_alerta = "warning"
        
    else:
        icono = "🔥"
        direccion = "positiva" if valor_corr > 0 else "inversa"
        verbo = "AUMENTA significativamente" if valor_corr > 0 else "DISMINUYE notablemente"
        titulo = f"¡Patrón Fuerte Detectado! ({direccion.title()})"
        texto = f"""
        **Hallazgo importante:** Existe una correlación fuerte entre estas variables.
        
        Cuando una ciudad tiene mayor {nombre_x}, su {nombre_y} {verbo}.
        
        *Un dato interesante:* Este patrón se mantiene consistente en {abs_corr*100:.0f}% de los casos analizados.
        Esto podría indicar una relación causal o factores compartidos.
        """
        tipo_alerta = "success"
    
    return icono, titulo, texto, tipo_alerta

# ==============================================================================
# BARRA LATERAL (SIDEBAR)
# ==============================================================================
st.sidebar.header("🎛️ Panel de Control")

if df is not None:
    # Filtro por Región
    regiones_disponibles = sorted(df['country'].unique())
    regiones_seleccionadas = st.sidebar.multiselect(
        f"Filtrar por {ETIQUETAS['country']}:",
        options=regiones_disponibles,
        default=regiones_disponibles
    )
    
    # Aplicar filtro
    df_filtered = df[df['country'].isin(regiones_seleccionadas)]
    
    st.sidebar.markdown("---")
    st.sidebar.success(f"📍 Mostrando **{len(df_filtered)}** de {len(df)} ciudades")
    
    # ==============================================================================
    # HEADER PRINCIPAL
    # ==============================================================================
    st.title("🌍 Explorador de Estilos de Vida Urbanos")
    st.markdown("*Descubre patrones ocultos sobre cómo vivimos, cuánto ganamos y qué tan felices somos alrededor del mundo.*")
    
    # ==============================================================================
    # NAVEGACIÓN POR PESTAÑAS
    # ==============================================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "🌍 El Mapa Mundial", 
        "📊 Comparador", 
        "💡 Descubrimientos", 
        "🎯 Tu Ciudad Ideal"
    ])
    
    # ==========================================================================
    # PESTAÑA 1: EL MAPA MUNDIAL
    # ==========================================================================
    with tab1:
        st.header("🗺️ Panorama Global")
        st.markdown("Una vista de pájaro sobre el bienestar mundial")
        
        # KPIs en tarjetas
        with st.container(border=True):
            st.subheader("📈 Métricas Clave")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    ETIQUETAS['happiness_score'], 
                    f"{df_filtered['happiness_score'].mean():.1f}/10",
                    delta=f"{df_filtered['happiness_score'].mean() - df['happiness_score'].mean():.2f} vs global"
                )
            with col2:
                st.metric(
                    ETIQUETAS['avg_income'], 
                    f"${df_filtered['avg_income'].mean():,.0f}"
                )
            with col3:
                st.metric(
                    ETIQUETAS['avg_rent'], 
                    f"${df_filtered['avg_rent'].mean():,.0f}"
                )
            with col4:
                st.metric(
                    "🏙️ Ciudades Analizadas", 
                    len(df_filtered)
                )
        
        st.markdown("")
        
        # Mapa Mundial
        with st.container(border=True):
            st.subheader("🌐 Mapa de Felicidad por Región")
            
            # Preparar datos para el mapa
            df_region = df_filtered.groupby('country').agg({
                'happiness_score': 'mean',
                'population_density': 'mean',
                'city_name': 'count'
            }).reset_index()
            
            df_region['lat'] = df_region['country'].map(lambda x: REGION_COORDS.get(x, {}).get('lat'))
            df_region['lon'] = df_region['country'].map(lambda x: REGION_COORDS.get(x, {}).get('lon'))
            
            fig_map = px.scatter_geo(
                df_region,
                lat='lat',
                lon='lon',
                size='city_name',
                color='happiness_score',
                hover_name='country',
                projection="natural earth",
                color_continuous_scale='Viridis',
                size_max=35,
                labels={
                    'happiness_score': ETIQUETAS['happiness_score'],
                    'city_name': '🏙️ N° Ciudades'
                }
            )
            fig_map.update_layout(
                height=500, 
                margin={"r":0,"t":10,"l":0,"b":0},
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor="lightgray",
                    projection_type='natural earth'
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)
            st.caption("💡 El tamaño de cada burbuja representa la cantidad de ciudades analizadas en esa región.")

    # ==========================================================================
    # PESTAÑA 2: COMPARADOR
    # ==========================================================================
    with tab2:
        st.header("📊 Centro de Comparaciones")
        st.markdown("Analiza y compara métricas entre ciudades y regiones")
        
        col_left, col_right = st.columns(2)
        
        # Box Plot - Comparación por Región
        with col_left:
            with st.container(border=True):
                st.subheader("📦 Distribución por Región")
                
                opciones_metricas = ['happiness_score', 'avg_rent', 'avg_income', 'air_quality_index', 
                                     'internet_penetration', 'public_transport_score']
                etiquetas_metricas = [ETIQUETAS[m] for m in opciones_metricas]
                
                metrica_seleccionada_label = st.selectbox(
                    "Selecciona una métrica:",
                    options=etiquetas_metricas,
                    index=0,
                    key="box_metric"
                )
                metrica_seleccionada = ETIQUETAS_INV[metrica_seleccionada_label]
                
                fig_box = px.box(
                    df_filtered, 
                    x='country', 
                    y=metrica_seleccionada, 
                    points="outliers",
                    color='country',
                    color_discrete_sequence=COLORES_PERSONALIZADOS,
                    labels={
                        'country': ETIQUETAS['country'],
                        metrica_seleccionada: metrica_seleccionada_label
                    }
                )
                fig_box.update_layout(
                    height=450, 
                    showlegend=False,
                    title=f"Variabilidad de {metrica_seleccionada_label}"
                )
                st.plotly_chart(fig_box, use_container_width=True)
        
        # Ranking - Top Ciudades
        with col_right:
            with st.container(border=True):
                st.subheader("🏆 Ranking de Ciudades")
                
                opciones_ranking = ['happiness_score', 'avg_income', 'public_transport_score', 
                                    'internet_penetration', 'green_space_ratio']
                etiquetas_ranking = [ETIQUETAS[m] for m in opciones_ranking]
                
                ranking_label = st.selectbox(
                    "¿Qué quieres rankear?",
                    options=etiquetas_ranking,
                    index=0,
                    key="ranking_metric"
                )
                ranking_metric = ETIQUETAS_INV[ranking_label]
                
                col_slider, col_check = st.columns([2, 1])
                with col_slider:
                    top_n = st.slider("N° de ciudades", 5, 15, 10, key="top_n")
                with col_check:
                    ascending = st.checkbox("Mostrar peores", value=False)
                
                df_sorted = df_filtered.sort_values(by=ranking_metric, ascending=ascending).head(top_n)
                
                fig_bar = px.bar(
                    df_sorted, 
                    x=ranking_metric, 
                    y='city_name', 
                    orientation='h', 
                    color='country',
                    color_discrete_sequence=COLORES_PERSONALIZADOS,
                    labels={
                        ranking_metric: ranking_label,
                        'city_name': ETIQUETAS['city_name'],
                        'country': ETIQUETAS['country']
                    }
                )
                fig_bar.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    height=450,
                    title=f"{'Bottom' if ascending else 'Top'} {top_n} - {ranking_label}"
                )
                st.plotly_chart(fig_bar, use_container_width=True)

    # ==========================================================================
    # PESTAÑA 3: DESCUBRIMIENTOS
    # ==========================================================================
    with tab3:
        st.header("💡 Centro de Descubrimientos")
        st.markdown("Explora relaciones ocultas y encuentra patrones en los datos")
        
        with st.container(border=True):
            st.subheader("🔍 Explorador de Relaciones")
            st.info("💡 Selecciona dos variables para descubrir si están conectadas y cómo se influyen mutuamente.")
            
            # Selectores de variables
            opciones_x = ['avg_income', 'avg_rent', 'population_density', 'internet_penetration', 'green_space_ratio']
            opciones_y = ['happiness_score', 'air_quality_index', 'public_transport_score', 'avg_rent']
            opciones_size = ['population_density', 'avg_income', 'happiness_score']
            
            c1, c2, c3 = st.columns(3)
            with c1:
                x_label = st.selectbox(
                    "📌 Variable X (Causa potencial):",
                    options=[ETIQUETAS[m] for m in opciones_x],
                    index=0
                )
                x_axis = ETIQUETAS_INV[x_label]
            with c2:
                y_label = st.selectbox(
                    "📌 Variable Y (Efecto):",
                    options=[ETIQUETAS[m] for m in opciones_y],
                    index=0
                )
                y_axis = ETIQUETAS_INV[y_label]
            with c3:
                size_label = st.selectbox(
                    "📌 Tamaño de burbuja:",
                    options=[ETIQUETAS[m] for m in opciones_size],
                    index=0
                )
                size_var = ETIQUETAS_INV[size_label]
            
            # Gráfico de Dispersión
            fig_scatter = px.scatter(
                df_filtered, 
                x=x_axis, 
                y=y_axis, 
                size=size_var, 
                color='country',
                hover_name='city_name', 
                trendline="ols",
                color_discrete_sequence=COLORES_PERSONALIZADOS,
                labels={
                    x_axis: x_label,
                    y_axis: y_label,
                    size_var: size_label,
                    'country': ETIQUETAS['country']
                }
            )
            fig_scatter.update_layout(height=500)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Interpretación Automática
        if len(df_filtered) > 1:
            corr_val = df_filtered[x_axis].corr(df_filtered[y_axis])
            icono, titulo, texto, tipo_alerta = interpretar_correlacion(corr_val, x_axis, y_axis)
            
            with st.container(border=True):
                st.subheader(f"{icono} Análisis: {titulo}")
                st.markdown(f"**Coeficiente de Correlación:** `{corr_val:.3f}`")
                
                if tipo_alerta == "success":
                    st.success(texto)
                elif tipo_alerta == "warning":
                    st.warning(texto)
                else:
                    st.info(texto)

    # ==========================================================================
    # PESTAÑA 4: TU CIUDAD IDEAL
    # ==========================================================================
    with tab4:
        st.header("🎯 Encuentra Tu Ciudad Ideal")
        st.markdown("*Ajusta tus prioridades y descubre qué ciudades son perfectas para ti*")
        
        with st.container(border=True):
            st.subheader("⚙️ Define Tus Prioridades")
            st.caption("Mueve los deslizadores para indicar qué tan importante es cada categoría para ti (0 = no importa, 10 = crucial)")
            
            col_pref1, col_pref2, col_pref3 = st.columns(3)
            
            with col_pref1:
                st.markdown("**💰 Factor Económico**")
                st.caption("Ingreso alto + Renta accesible")
                w_econ = st.slider("Importancia", 0, 10, 5, key="w_econ", label_visibility="collapsed")
                
            with col_pref2:
                st.markdown("**🌿 Factor Bienestar**")
                st.caption("Felicidad + Aire limpio + Áreas verdes")
                w_wellbeing = st.slider("Importancia", 0, 10, 8, key="w_well", label_visibility="collapsed")
                
            with col_pref3:
                st.markdown("**📶 Factor Conectividad**")
                st.caption("Internet + Transporte público")
                w_tech = st.slider("Importancia", 0, 10, 5, key="w_tech", label_visibility="collapsed")
        
        if st.button("🔮 Encontrar Mi Ciudad Ideal", type="primary", use_container_width=True):
            # Algoritmo de Recomendación
            df_rec = df_filtered.copy()
            
            cols_to_norm = ['avg_income', 'avg_rent', 'happiness_score', 'air_quality_index', 
                            'green_space_ratio', 'internet_penetration', 'public_transport_score']
            
            for col in cols_to_norm:
                min_v = df_rec[col].min()
                max_v = df_rec[col].max()
                if max_v - min_v == 0:
                    df_rec[f'norm_{col}'] = 0
                else:
                    df_rec[f'norm_{col}'] = (df_rec[col] - min_v) / (max_v - min_v)
            
            # Invertir Renta y AQI (menor es mejor)
            df_rec['norm_avg_rent'] = 1 - df_rec['norm_avg_rent']
            df_rec['norm_air_quality_index'] = 1 - df_rec['norm_air_quality_index']
            
            # Calcular Scores
            score_econ = (df_rec['norm_avg_income'] + df_rec['norm_avg_rent']) / 2
            score_well = (df_rec['norm_happiness_score'] + df_rec['norm_air_quality_index'] + df_rec['norm_green_space_ratio']) / 3
            score_tech = (df_rec['norm_internet_penetration'] + df_rec['norm_public_transport_score']) / 2
            
            df_rec['match_score'] = (score_econ * w_econ) + (score_well * w_wellbeing) + (score_tech * w_tech)
            
            top_matches = df_rec.sort_values('match_score', ascending=False).head(5)
            
            st.balloons()
            st.markdown("---")
            
            # Ciudad Ganadora - Tarjeta Principal
            winner = top_matches.iloc[0]
            match_percent = int((winner['match_score'] / df_rec['match_score'].max()) * 100)
            
            st.markdown(f"""
            <div class="winner-card">
                <div class="winner-title">🥇 TU MATCH PERFECTO</div>
                <div class="winner-city">{winner['city_name']}, {winner['country']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Métricas de la ciudad ganadora
            with st.container(border=True):
                st.subheader(f"📊 Perfil de {winner['city_name']}")
                
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric(ETIQUETAS['happiness_score'], f"{winner['happiness_score']:.1f}/10")
                with m2:
                    st.metric(ETIQUETAS['avg_income'], f"${winner['avg_income']:,.0f}")
                with m3:
                    st.metric(ETIQUETAS['avg_rent'], f"${winner['avg_rent']:,.0f}")
                
                m4, m5, m6 = st.columns(3)
                with m4:
                    st.metric(ETIQUETAS['internet_penetration'], f"{winner['internet_penetration']:.0f}%")
                with m5:
                    st.metric(ETIQUETAS['green_space_ratio'], f"{winner['green_space_ratio']:.1f}%")
                with m6:
                    st.metric(ETIQUETAS['public_transport_score'], f"{winner['public_transport_score']:.0f}/100")
                
                st.markdown(f"**🎯 Compatibilidad:** ")
                st.progress(match_percent / 100)
                st.caption(f"{match_percent}% de coincidencia con tus preferencias")
            
            # Otras recomendaciones
            if len(top_matches) > 1:
                st.markdown("### 🏅 Otras Excelentes Opciones")
                
                cols = st.columns(min(4, len(top_matches) - 1))
                for i, (_, row) in enumerate(top_matches.iloc[1:].iterrows()):
                    if i < 4:
                        with cols[i]:
                            with st.container(border=True):
                                match_pct = int((row['match_score'] / df_rec['match_score'].max()) * 100)
                                st.markdown(f"**#{i+2} {row['city_name']}**")
                                st.caption(f"📍 {row['country']}")
                                st.metric(ETIQUETAS['happiness_score'], f"{row['happiness_score']:.1f}")
                                st.progress(match_pct / 100)
                                st.caption(f"{match_pct}% match")

else:
    st.error("❌ Error al cargar los datos. Verifica que el archivo CSV existe.")
