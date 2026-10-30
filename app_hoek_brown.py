import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMA OSCURO
# ---------------------------------------------------------
st.set_page_config(
    page_title="GeoDisk Pro | Selector Circular Multicapa",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #00f2fe !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161f30;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
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
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1e293b;
    }
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
# 2. PANEL LATERAL: DISCO SELECTOR MULTICAPA (ENTRADAS)
# ---------------------------------------------------------
st.sidebar.title("🎛️ Geo-Slide Selector")
st.sidebar.markdown("**UNAM - Ingeniería de Minas**")
st.sidebar.markdown("---")

st.sidebar.subheader("🔵 Layer 1: Calidad de Macizo (GSI)")
gsi = st.sidebar.slider("GSI (Índice de Resistencia Geológica)", 10, 90, 55, 1)
sigci = st.sidebar.slider("σci - Resistencia Intacta (MPa)", 1.0, 250.0, 65.0, 1.0)
mi = st.sidebar.slider("mi (Constante Roca Intacta)", 5.0, 35.0, 15.0, 1.0)

st.sidebar.subheader("⚪ Layer 2: Parámetros de Discontinuidad")
jcs = st.sidebar.slider("JCS - Resistencia de Juntas (MPa)", 20.0, 250.0, 100.0, 5.0)
jrc = st.sidebar.slider("JRC (Rugosidad de la Junta)", 0.0, 20.0, 8.0, 0.5)
apertura = st.sidebar.selectbox("Apertura / Relleno", ["Cerrada (< 0.1 mm)", "Normal (0.5 - 5 mm)", "Relleno Suave (> 5 mm)"])

st.sidebar.subheader("⚫ Layer 3: Propiedades Físico-Mecánicas")
D = st.sidebar.slider("Factor de Perturbación (D)", 0.0, 1.0, 0.0, 0.05)
peso_especifico = st.sidebar.slider("Peso Específico γ (kN/m³)", 20.0, 30.0, 26.5, 0.1)

# ---------------------------------------------------------
# 3. CÁLCULOS GEOMECÁNICOS (HOEK-BROWN 2002)
# ---------------------------------------------------------
mb = mi * np.exp((gsi - 100) / (28 - 14 * D))
s = np.exp((gsi - 100) / (9 - 3 * D)) if gsi >= 25 else 0.0
a = 0.5 + (1/6) * (np.exp(-gsi/15) - np.exp(-20/3))

sig_t = - (s * sigci) / mb
sig_cm = sigci * ((mb + 4*s - a*(mb - 8*s)) * (mb/4 + s)**(a - 1)) / (2*(1 + a)*(2 + a))
Erm = 25.0 * (0.02 + (1 - D/2)/(1 + np.exp((60 + 15*D - gsi)/11)))

# ---------------------------------------------------------
# 4. ENCABEZADO Y VISUALIZACIÓN DEL DISCO INTERACTIVO
# ---------------------------------------------------------
st.title("⚙️ GEODISK PRO : Disco Selector Multicapa Interactivo")
st.caption("Simulador geomecánico basado en el criterio de Hoek-Brown y análisis multicapa de discontinuidades.")

tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Disco Selector & Resultados", 
    "📈 Envolvente & Círculo de Mohr", 
    "🧪 Animación de Carga & Ruptura", 
    "📑 Memoria de Cálculo"
])

with tab1:
    col_d1, col_d2 = st.columns([1.2, 1])
    
    with col_d1:
        st.subheader("🔄 Representación Circular Multicapa")
        st.markdown("""
        <div class='custom-card'>
        <b>Funcionamiento del Disco:</b> Al mover los parámetros en el panel lateral, las capas virtuales del disco 
        interactúan para calcular de forma dinámica la resistencia global del macizo rocoso de la región Moquegua.
        </div>
        """, unsafe_allow_html=True)
        
        # Gráfico polar simulando el disco selector multicapa
        fig_disk = go.Figure(go.Barpolar(
            r=[gsi, jcs, jrc*5, sigci/2.5],
            theta=['Layer 1: GSI', 'Layer 2: JCS', 'Layer 2: JRC (x5)', 'Layer 3: σci (scaled)'],
            marker=dict(color=['#00f2fe', '#0072ff', '#ff007f', '#ffea00'], line=dict(color="#ffffff", width=1)),
            opacity=0.85
        ))
        fig_disk.update_layout(
            template="plotly_dark",
            title="Diagrama Multicapa Concéntrico del Disco",
            polar=dict(bgcolor="#0f172a", radialaxis=dict(visible=True, range=[0, 100])),
            paper_bgcolor="#0b0f19",
            height=400
        )
        st.plotly_chart(fig_disk, use_container_width=True)

    with col_d2:
        st.subheader("⚡ Parámetros Resultantes del Disco")
        
        st.metric(label="Resistencia Global del Macizo (σcm)", value=f"{sig_cm:.2f} MPa", delta="Sostenimiento Sugerido")
        st.metric(label="Módulo de Deformación (Erm)", value=f"{Erm:.2f} GPa", delta="Macizo Rocoso")
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Constante mb", f"{mb:.3f}")
        col_m2.metric("Constante s", f"{s:.5f}")
        
        st.markdown(f"""
        * **Apertura de Juntas:** {apertura}
        * **Peso Específico (γ):** {peso_especifico} kN/m³
        * **Resistencia a la Tracción (σt):** {sig_t:.3f} MPa
        """)

# ---------------------------------------------------------
# PESTAÑA 2: ENVOLVENTE Y MOHR
# ---------------------------------------------------------
with tab2:
    st.subheader("📊 Envolvente de Falla Hoek-Brown & Círculo de Mohr")
    sig3_max = st.slider("σ3 Máximo de Confinamiento (MPa)", 1.0, 50.0, 15.0)
    
    sig3_vals = np.linspace(sig_t, sig3_max, 200)
    sig1_vals = np.zeros_like(sig3_vals)
    for i, s3 in enumerate(sig3_vals):
        if s3 >= sig_t:
            term = mb * (s3 / sigci) + s
            sig1_vals[i] = s3 + sigci * (term**a if term > 0 else 0)
        else:
            sig1_vals[i] = np.nan

    fig_mohr = go.Figure()
    fig_mohr.add_trace(go.Scatter(x=sig3_vals, y=sig1_vals, mode='lines', name='Envolvente Hoek-Brown', line=dict(color='#00f2fe', width=3)))
    
    s3_eval = sig3_max / 2
    s1_eval = s3_eval + sigci * ((mb * (s3_eval / sigci) + s)**a)
    center = (s1_eval + s3_eval) / 2
    radius = (s1_eval - s3_eval) / 2
    theta = np.linspace(0, np.pi, 100)
    
    fig_mohr.add_trace(go.Scatter(
        x=center + radius * np.cos(theta), y=radius * np.sin(theta),
        mode='lines', name=f'Círculo de Mohr (σ3={s3_eval:.1f} MPa)',
        line=dict(color='#ff007f', width=2, dash='dash')
    ))

    fig_mohr.update_layout(
        template="plotly_dark",
        title="Espacio de Esfuerzos Principales (σ3 - σ1)",
        xaxis_title="Esfuerzo Principal Menor σ3 (MPa)",
        yaxis_title="Esfuerzo Principal Mayor σ1 (MPa)",
        height=480, paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a"
    )
    st.plotly_chart(fig_mohr, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 3: ANIMACIÓN DE CARGA Y MODOS DE RUPTURA
# ---------------------------------------------------------
with tab3:
    st.subheader("🧪 Simulación de Carga y Modos de Ruptura de la Roca")
    
    carga_pct = st.slider("Porcentaje de Carga Aplicada (% σci)", 10, 150, 80, 5)
    
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        def_axial = np.linspace(0, 3.0, 100)
        esfuerzo = sigci * (def_axial / 1.0) * np.exp(1 - (def_axial / 1.0))
        dilatancia = np.where(def_axial < 0.7, -0.1 * def_axial, 0.4 * (def_axial - 0.7)**2 - 0.07)
        idx_curr = int((carga_pct / 150) * 99)
        
        fig_st = make_subplots(specs=[[{"secondary_y": True}]])
        fig_st.add_trace(go.Scatter(x=def_axial, y=esfuerzo, name="Esfuerzo σ1", line=dict(color="#00f2fe", width=3)))
        fig_st.add_trace(go.Scatter(x=def_axial, y=dilatancia, name="Dilatancia ΔV/V", line=dict(color="#ffea00", width=2, dash="dash")), secondary_y=True)
        fig_st.add_trace(go.Scatter(x=[def_axial[idx_curr]], y=[esfuerzo[idx_curr]], mode="markers", marker=dict(color="#ff007f", size=12), name="Estado Actual"))
        fig_st.update_layout(template="plotly_dark", title="Curva Esfuerzo-Deformación y Dilatancia", paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a", height=380)
        st.plotly_chart(fig_st, use_container_width=True)

    with col_s2:
        st.write("#### 🧱 Deformación Visual del Testigo")
        scale_y = 1.0 - 0.15 * (def_axial[idx_curr] / 3.0)
        scale_x = 1.0 + max(0, dilatancia[idx_curr]) * 0.2
        
        fig_rock = go.Figure()
        fig_rock.add_trace(go.Scatter(
            x=[-0.5 * scale_x, 0.5 * scale_x, 0.5 * scale_x, -0.5 * scale_x, -0.5 * scale_x],
            y=[-1.0 * scale_y, -1.0 * scale_y, 1.0 * scale_y, 1.0 * scale_y, -1.0 * scale_y],
            fill="toself", fillcolor="#334155", line=dict(color="#00f2fe", width=3), name="Testigo"
        ))
        if carga_pct >= 100:
            fig_rock.add_trace(go.Scatter(x=[-0.4*scale_x, 0.4*scale_x], y=[-0.8*scale_y, 0.8*scale_y], mode="lines", line=dict(color="#ff007f", width=4), name="Plano de Cizalla"))
        
        fig_rock.update_layout(
            template="plotly_dark", title=f"Testigo de Roca ({carga_pct}% Carga)",
            xaxis=dict(range=[-1.5, 1.5], visible=False), yaxis=dict(range=[-1.5, 1.5], visible=False),
            height=380, paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a"
        )
        st.plotly_chart(fig_rock, use_container_width=True)

# ---------------------------------------------------------
# PESTAÑA 4: FÓRMULAS
# ---------------------------------------------------------
with tab4:
    st.subheader("📋 Memoria de Cálculo Detallada")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        st.latex(r"\sigma_1' = \sigma_3' + \sigma_{ci} \left( m_b \frac{\sigma_3'}{\sigma_{ci}} + s \right)^a")
        st.latex(r"m_b = m_i \cdot \exp\left( \frac{GSI - 100}{28 - 14D} \right)")
    with col_f2:
        st.table({
            "Parámetro": ["σci", "mb", "s", "a", "σt", "σcm", "Erm"],
            "Valor": [f"{sigci} MPa", f"{mb:.3f}", f"{s:.5f}", f"{a:.4f}", f"{sig_t:.3f} MPa", f"{sig_cm:.2f} MPa", f"{Erm:.2f} GPa"]
        })
