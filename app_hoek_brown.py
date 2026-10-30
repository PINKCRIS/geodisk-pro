import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMA OSCURO FUTURISTA
# ---------------------------------------------------------
st.set_page_config(
    page_title="GeoDisk Pro | Geomecánica Avanzada",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Personalizados para Interfaz Oscura Dinámica
st.markdown("""
    <style>
    /* Fondo principal negro profundo */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Contenedores y Tarjetas */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #00f2fe !important;
    }
    
    .css-1r650a2, .stMarkdownContainer {
        color: #cbd5e1;
    }

    /* Pestañas Personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161f30;
        padding: 8px;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        background-color: #0f172a;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
        color: #ffffff !important;
        box-shadow: 0px 4px 15px rgba(0, 198, 255, 0.4);
    }
    
    /* Paneles de Control lateral */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1e293b;
    }
    
    /* Cuadros de Alerta / Info */
    .custom-card {
        background: #1e293b;
        border-left: 4px solid #00f2fe;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. PANEL LATERAL: PARÁMETROS DE ENTRADA
# ---------------------------------------------------------
st.sidebar.title("🎛️ Parámetros de Entrada")
st.sidebar.markdown("---")

st.sidebar.subheader(" Matriz Rocosa e Intacta")
sigci = st.sidebar.slider("Resistencia Uniaxial intacta σci (MPa)", 1.0, 250.0, 65.0, 1.0)
mi = st.sidebar.slider("Constante mi (Roca Intacta)", 5.0, 35.0, 15.0, 1.0)

st.sidebar.subheader(" Macizo Rocoso (GSI y Perturbación)")
gsi = st.sidebar.slider("Índice de Resistencia Geológica (GSI)", 10, 90, 55, 1)
D = st.sidebar.slider("Factor de Perturbación (D)", 0.0, 1.0, 0.0, 0.05)
Ei = st.sidebar.number_input("Módulo Intacto Ei (GPa)", value=25.0, step=1.0)

# ---------------------------------------------------------
# 3. CÁLCULOS MATEMÁTICOS (HOEK-BROWN 2002)
# ---------------------------------------------------------
mb = mi * np.exp((gsi - 100) / (28 - 14 * D))
s = np.exp((gsi - 100) / (9 - 3 * D)) if gsi >= 25 else 0.0
a = 0.5 + (1/6) * (np.exp(-gsi/15) - np.exp(-20/3))

# Resistencia a la Tracción
sig_t = - (s * sigci) / mb

# Resistencia Global y Módulo Reducido (Erm)
sig_cm = sigci * ((mb + 4*s - a*(mb - 8*s)) * (mb/4 + s)**(a - 1)) / (2*(1 + a)*(2 + a))
Erm = Ei * (0.02 + (1 - D/2)/(1 + np.exp((60 + 15*D - gsi)/11)))

# ---------------------------------------------------------
# 4. ENCABEZADO Y PESTAÑAS PRINCIPALES
# ---------------------------------------------------------
st.title("⚡ GeoDisk Pro : Geomecánica y Fallo de Rocas")
st.caption("Plataforma interactiva para el análisis de envolventes de falla, ensayos de compresión y modos de ruptura.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Envolvente & Círculo de Mohr", 
    "🧪 Animación de Carga & Dilatancia", 
    "⚡ Modos de Ruptura de la Roca", 
    "📑 Fórmulas & Tablas Detalladas"
])

# ---------------------------------------------------------
# PESTAÑA 1: ENV
# ---------------------------------------------------------
with tab1:
    st.subheader("📊 Envolvente de Falla Hoek-Brown & Círculo de Mohr")
    
    col_sig3, col_m1, col_m2, col_m3 = st.columns(4)
    sig3_max = col_sig3.slider("σ3 Máximo (MPa)", 1.0, 50.0, 15.0)
    col_m1.metric("Constante mb", f"{mb:.3f}")
    col_m2.metric("Constante s", f"{s:.5f}")
    col_m3.metric("Exponente a", f"{a:.3f}")
    
    # Generación de curva Hoek-Brown
    sig3_vals = np.linspace(sig_t, sig3_max, 200)
    sig1_vals = np.zeros_like(sig3_vals)
    for i, s3 in enumerate(sig3_vals):
        if s3 >= sig_t:
            term = mb * (s3 / sigci) + s
            sig1_vals[i] = s3 + sigci * (term**a if term > 0 else 0)
        else:
            sig1_vals[i] = np.nan

    # Gráfico interactivo con Plotly
    fig = go.Figure()
    
    # Curva HB
    fig.add_trace(go.Scatter(
        x=sig3_vals, y=sig1_vals,
        mode='lines', name='Envolvente Hoek-Brown',
        line=dict(color='#00f2fe', width=3)
    ))
    
    # Círculo de Mohr para un σ3 seleccionado
    s3_eval = sig3_max / 2
    s1_eval = s3_eval + sigci * ((mb * (s3_eval / sigci) + s)**a)
    center = (s1_eval + s3_eval) / 2
    radius = (s1_eval - s3_eval) / 2
    theta = np.linspace(0, np.pi, 100)
    circle_x = center + radius * np.cos(theta)
    circle_y = radius * np.sin(theta)
    
    fig.add_trace(go.Scatter(
        x=circle_x, y=circle_y,
        mode='lines', name=f'Círculo de Mohr (σ3={s3_eval:.1f} MPa)',
        line=dict(color='#ff007f', width=2, dash='dash')
    ))

    fig.update_layout(
        template="plotly_dark",
        title="Envolvente de Falla en el Espacio de Esfuerzos Principales (σ3 - σ1)",
        xaxis_title="Esfuerzo Principal Menor σ3 (MPa)",
        yaxis_title="Esfuerzo Principal Mayor σ1 (MPa)",
        height=520,
        paper_bgcolor="#0b0f19",
        plot_bgcolor="#0f172a",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 2: SIMULACIÓN DE CARGA Y DILATANCIA
# ---------------------------------------------------------
with tab2:
    st.subheader("🧪 Simulación de Carga Uniaxial / Triaxial y Dilatancia")
    
    st.markdown("""
    <div class='custom-card'>
    <b>Proceso de Fallo y Dilatancia:</b> Durante el ensayo de compresión, la roca pasa por una fase elástica lineal,
    seguida de microagrietamiento e iniciación de grietas (micro-cracking). A esfuerzo pico, las grietas se interconectan provocando 
    un incremento acelerado de volumen no elástico llamado <b>Dilatancia (ΔV/V)</b>.
    </div>
    """, unsafe_allow_html=True)
    
    col_sim1, col_sim2 = st.columns([1, 1])
    
    with col_sim1:
        carga_pct = st.slider("Simular Carga Aplicada (% respecto al Pico σci)", 10, 150, 85, 5)
        
        # Curva Esfuerzo-Deformación Teórica
        def_axial = np.linspace(0, 3.0, 100)
        # Curva con ablandamiento post-pico
        esfuerzo = sigci * (def_axial / 1.0) * np.exp(1 - (def_axial / 1.0))
        dilatancia = np.where(def_axial < 0.7, -0.1 * def_axial, 0.4 * (def_axial - 0.7)**2 - 0.07)
        
        idx_curr = int((carga_pct / 150) * 99)
        
        fig_stress = make_subplots(specs=[[{"secondary_y": True}]])
        fig_stress.add_trace(go.Scatter(x=def_axial, y=esfuerzo, name="Esfuerzo σ1 (MPa)", line=dict(color="#00f2fe", width=3)))
        fig_stress.add_trace(go.Scatter(x=def_axial, y=dilatancia, name="Dilatancia ΔV/V (%)", line=dict(color="#ffea00", width=2, dash="dash")), secondary_y=True)
        
        # Marcador del punto de carga actual
        fig_stress.add_trace(go.Scatter(x=[def_axial[idx_curr]], y=[esfuerzo[idx_curr]], mode="markers", marker=dict(color="#ff007f", size=12), name="Carga Actual"))
        
        fig_stress.update_layout(template="plotly_dark", title="Curva Esfuerzo - Deformación Axial y Volumétrica", paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a", height=400)
        st.plotly_chart(fig_stress, use_container_width=True)

    with col_sim2:
        st.write("#### 🧱 Respuesta Mecánica del Testigo de Roca")
        
        # Deformación visual interactiva
        def_val = def_axial[idx_curr]
        scale_y = 1.0 - 0.15 * (def_val / 3.0)
        scale_x = 1.0 + (dilatancia[idx_curr] if dilatancia[idx_curr] > 0 else 0) * 0.2
        
        # Testigo en Plotly 2D
        rock_x = [-0.5 * scale_x, 0.5 * scale_x, 0.5 * scale_x, -0.5 * scale_x, -0.5 * scale_x]
        rock_y = [-1.0 * scale_y, -1.0 * scale_y, 1.0 * scale_y, 1.0 * scale_y, -1.0 * scale_y]
        
        fig_rock = go.Figure()
        fig_rock.add_trace(go.Scatter(x=rock_x, y=rock_y, fill="fill", fillcolor="#334155", line=dict(color="#00f2fe", width=3), name="Testigo"))
        
        # Si sobrepasa el pico, mostrar planos de falla
        if carga_pct >= 100:
            fig_rock.add_trace(go.Scatter(x=[-0.4*scale_x, 0.4*scale_x], y=[-0.8*scale_y, 0.8*scale_y], mode="lines", line=dict(color="#ff007f", width=4), name="Plano de Cizalla"))
        
        fig_rock.update_layout(
            template="plotly_dark",
            title=f"Estado del Testigo de Roca ({carga_pct}% de Carga)",
            xaxis=dict(range=[-1.5, 1.5], visible=False),
            yaxis=dict(range=[-1.5, 1.5], visible=False),
            height=400,
            paper_bgcolor="#0b0f19",
            plot_bgcolor="#0f172a"
        )
        st.plotly_chart(fig_rock, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 3: COMPORTAMIENTO Y MODOS DE RUPTURA
# ---------------------------------------------------------
with tab3:
    st.subheader("⚡ Comportamiento de la Roca y Modos de Ruptura")
    st.caption("Selecciona un modo de falla para analizar su origen físico, condiciones de ocurrencia e inclinación del plano.")

    modo = st.radio(
        "Selecciona el Modo de Ruptura a Inspeccionar:",
        ["Tracción Directa (Splitting)", "Cizalladura o Corte (Shear Failure)", "Flexión o Pandeo (Bending/Buckling)"],
        horizontal=True
    )
    
    col_m_desc, col_m_vis = st.columns([1.2, 1])
    
    with col_m_desc:
        if modo == "Tracción Directa (Splitting)":
            st.markdown("""
            ### 💥 Tracción Directa (Tensile Splitting / Spalling)
            * **¿Cuándo ocurre?**: Se produce bajo confinamiento nulo o muy bajo ($\sigma_3 \approx 0$) y altas cargas axiales de compresión.
            * **Mecanismo**: Las microgrietas orientadas en la dirección de la carga axial se propagan y unen, haciendo que la roca se divida en "columnas" o lajas paralelas a la fuerza.
            * **Límite Teórico**: Ocurre cuando el esfuerzo de tracción inducido transversalmente supera la resistencia a la tracción ($\sigma_t$) de la roca intacta.
            """)
        elif modo == "Cizalladura o Corte (Shear Failure)":
            st.markdown("""
            ### ✂️ Cizalladura o Corte (Shear Failure)
            * **¿Cuándo ocurre?**: Es el modo dominante en presencia de confinamiento moderado a alto ($\sigma_3 > 0$).
            * **Mecanismo**: La falla desliza a lo largo de uno o dos planos inclinados predefinidos por el ángulo de fricción interna del material ($\phi$).
            * **Ángulo de Falla**: El plano se orienta teóricamente a un ángulo $\theta = 45^\circ + \phi/2$ respecto al plano del esfuerzo principal menor $\sigma_3$.
            """)
        else:
            st.markdown("""
            ### 🔄 Flexión o Pandeo (Bending / Buckling)
            * **¿Cuándo ocurre?**: Típico en macizos rocosos estratificados, foliados o profundamente discontinuos (p. ej., pizarras, filitas) sometidos a cargas paralelas a los planos de debilidad.
            * **Mecanismo**: Las capas delgadas sufren flexión lateral por inestabilidad elástica hasta romperse por esfuerzo de tracción en la cara convexa de la curvatura.
            """)

    with col_m_vis:
        fig_mode = go.Figure()
        
        # Esquema de fractura según modo
        if modo == "Tracción Directa (Splitting)":
            fig_mode.add_trace(go.Scatter(x=[-0.5, 0.5, 0.5, -0.5, -0.5], y=[-1, -1, 1, 1, -1], fill="fill", fillcolor="#1e293b", line=dict(color="#00f2fe")))
            fig_mode.add_trace(go.Scatter(x=[0, 0], y=[-0.9, 0.9], mode="lines", line=dict(color="#ff007f", width=4, dash="dot"), name="Grieta Vertical"))
            fig_mode.add_trace(go.Scatter(x=[-0.2, -0.2], y=[-0.9, 0.9], mode="lines", line=dict(color="#ff007f", width=4, dash="dot")))
        elif modo == "Cizalladura o Corte (Shear Failure)":
            fig_mode.add_trace(go.Scatter(x=[-0.5, 0.5, 0.5, -0.5, -0.5], y=[-1, -1, 1, 1, -1], fill="fill", fillcolor="#1e293b", line=dict(color="#00f2fe")))
            fig_mode.add_trace(go.Scatter(x=[-0.4, 0.4], y=[-0.8, 0.8], mode="lines", line=dict(color="#ffea00", width=5), name="Plano de Corte θ"))
        else:
            # Curvatura por flexión
            y_curv = np.linspace(-1, 1, 50)
            x_curv = 0.2 * np.sin(np.pi * y_curv)
            fig_mode.add_trace(go.Scatter(x=x_curv, y=y_curv, mode="lines", line=dict(color="#00f2fe", width=4), name="Capas Pandedas"))
            fig_mode.add_trace(go.Scatter(x=x_curv+0.2, y=y_curv, mode="lines", line=dict(color="#ff007f", width=3, dash="dash")))

        fig_mode.update_layout(
            template="plotly_dark", title="Diagrama Vectorial del Modo de Ruptura",
            xaxis=dict(range=[-1, 1], visible=False), yaxis=dict(range=[-1.2, 1.2], visible=False),
            height=350, paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a"
        )
        st.plotly_chart(fig_mode, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 4: FÓRMULAS Y RESULTADOS DETALLADOS
# ---------------------------------------------------------
with tab4:
    st.subheader("📋 Memoria de Cálculo & Fórmulas Hoek-Brown (2002)")
    
    col_f1, col_f2 = st.columns(2)
    
    with col_f1:
        st.markdown("#### 📐 Ecuaciones Principales")
        st.latex(r"\sigma_1' = \sigma_3' + \sigma_{ci} \left( m_b \frac{\sigma_3'}{\sigma_{ci}} + s \right)^a")
        st.latex(r"m_b = m_i \cdot \exp\left( \frac{GSI - 100}{28 - 14D} \right)")
        st.latex(r"s = \exp\left( \frac{GSI - 100}{9 - 3D} \right)")
        st.latex(r"a = \frac{1}{2} + \frac{1}{6} \left( e^{-GSI/15} - e^{-20/3} \right)")

    with col_f2:
        st.markdown("#### 📊 Resumen de Resultados Calculados")
        st.table({
            "Parámetro Geomecánico": [
                "Resistencia Intacta (σci)",
                "Constante mb",
                "Constante s",
                "Exponente a",
                "Resistencia a la Tracción (σt)",
                "Resistencia Global del Macizo (σcm)",
                "Módulo del Macizo Rocoso (Erm)"
            ],
            "Valor Obtenido": [
                f"{sigci:.2f} MPa",
                f"{mb:.4f}",
                f"{s:.6f}",
                f"{a:.4f}",
                f"{sig_t:.3f} MPa",
                f"{sig_cm:.2f} MPa",
                f"{Erm:.2f} GPa"
            ]
        })
