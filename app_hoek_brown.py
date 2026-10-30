import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y TEMA OSCURO
# ---------------------------------------------------------
st.set_page_config(
    page_title="GeoDisk Pro | Disco Selector Circular",
    page_icon="⛏️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #00f2fe !important;
    }
    .custom-card {
        background: #161f30;
        border-left: 4px solid #00f2fe;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #161f30;
        padding: 8px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        background-color: #0f172a;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%) !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. ENCABEZADO PRINCIPAL
# ---------------------------------------------------------
st.title("⚙️ GEODISK PRO : Multi-Layer Circular Geological Selector")
st.markdown("##### *Escuela Profesional de Ingeniería de Minas - UNAM | Disco Selector Multicapa Interactivo*")
st.markdown("---")

# ---------------------------------------------------------
# 3. CONTROLES DEL DISCO CIRCULAR (ORGANIZADO EN 3 CAPAS)
# ---------------------------------------------------------
col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

with col_ctrl1:
    st.markdown("### 🟢 Layer 1: Calidad")
    gsi = st.slider("GSI (Índice Geológico)", 10, 90, 55, 1)
    sigci = st.slider("σci Resistencia Intacta (MPa)", 1.0, 250.0, 65.0, 1.0)

with col_ctrl2:
    st.markdown("### 🟡 Layer 2: Discontinuidades")
    jcs = st.slider("JCS Resistencia Juntas (MPa)", 20.0, 250.0, 100.0, 5.0)
    jrc = st.slider("JRC Rugosidad de Junta", 0.0, 20.0, 8.0, 0.5)

with col_ctrl3:
    st.markdown("### 🔴 Layer 3: Físico-Mecánicas")
    D = st.slider("Factor de Perturbación (D)", 0.0, 1.0, 0.0, 0.05)
    mi = st.slider("Constante mi (Roca)", 5.0, 35.0, 15.0, 1.0)

# ---------------------------------------------------------
# CÁLCULOS GEOMECÁNICOS (HOEK-BROWN 2002)
# ---------------------------------------------------------
mb = mi * np.exp((gsi - 100) / (28 - 14 * D))
s = np.exp((gsi - 100) / (9 - 3 * D)) if gsi >= 25 else 0.0
a = 0.5 + (1/6) * (np.exp(-gsi/15) - np.exp(-20/3))

sig_t = - (s * sigci) / mb
sig_cm = sigci * ((mb + 4*s - a*(mb - 8*s)) * (mb/4 + s)**(a - 1)) / (2*(1 + a)*(2 + a))
Erm = 25.0 * (0.02 + (1 - D/2)/(1 + np.exp((60 + 15*D - gsi)/11)))

# ---------------------------------------------------------
# 4. PESTAÑAS DINÁMICAS CON EL DISCO CENTRAL
# ---------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🎯 Disco Selector & Resultados en Vivo", 
    "📈 Envolvente de Falla & Mohr", 
    "🧪 Simulación de Carga & Ruptura"
])

with tab1:
    col_vis1, col_vis2 = st.columns([1.3, 1])
    
    with col_vis1:
        st.subheader("🔄 Visualización Circular Multicapa del Disco")
        
        # Gráfico polar interactivo simulando el disco giratorio multicapa
        fig_disk = go.Figure()
        
        # Anillos concéntricos del disco
        fig_disk.add_trace(go.Barpolar(
            r=[gsi, jcs, jrc*10, sigci/2.5],
            theta=['Layer 1: GSI', 'Layer 2: JCS', 'Layer 2: JRC (scaled)', 'Layer 3: σci (scaled)'],
            marker=dict(
                color=['#00f2fe', '#0072ff', '#ffea00', '#ff007f'],
                line=dict(color="#ffffff", width=1.5)
            ),
            opacity=0.9,
            name="Capas del Disco"
        ))
        
        fig_disk.update_layout(
            template="plotly_dark",
            polar=dict(
                bgcolor="#0f172a",
                radialaxis=dict(visible=True, range=[0, 100], color="#94a3b8"),
                angularaxis=dict(color="#ffffff", rotation=90, direction="clockwise")
            ),
            paper_bgcolor="#0b0f19",
            height=450,
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_disk, use_container_width=True)

    with col_vis2:
        st.subheader("⚡ Resultados Geomecánicos del Disco")
        
        st.markdown("""
        <div class='custom-card'>
        <b>Estado del Macizo:</b> Los datos seleccionados en las capas del disco interactúan para arrojar 
        los siguientes parámetros de resistencia y deformabilidad:
        </div>
        """, unsafe_allow_html=True)
        
        st.metric(label="Resistencia Global del Macizo (σcm)", value=f"{sig_cm:.2f} MPa")
        st.metric(label="Módulo de Deformación (Erm)", value=f"{Erm:.2f} GPa")
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("mb", f"{mb:.3f}")
        col_m2.metric("s", f"{s:.5f}")
        
        st.markdown(f"**Resistencia a la Tracción ($\sigma_t$):** `{sig_t:.3f} MPa`")

with tab2:
    st.subheader("📊 Envolvente de Falla Hoek-Brown & Círculo de Mohr")
    sig3_max = st.slider("Confinamiento Máximo σ3 (MPa)", 1.0, 50.0, 15.0)
    
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
        height=450, paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a"
    )
    st.plotly_chart(fig_mohr, use_container_width=True)

with tab3:
    st.subheader("🧪 Simulación de Carga y Dilatancia del Testigo")
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
        fig_st.update_layout(template="plotly_dark", title="Curva Esfuerzo-Deformación", paper_bgcolor="#0b0f19", plot_bgcolor="#0f172a", height=380)
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
