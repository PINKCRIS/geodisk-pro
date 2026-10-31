import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Laboratorio del Macizo Rocoso",
    page_icon="⛏️",
    layout="wide"
)

# Estilos CSS personalizados para darle una apariencia de cuaderno de campo profesional
st.markdown("""
    <style>
    .main-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #12191c;
    }
    .sub-header {
        font-size: 0.9rem;
        color: #56666c;
        margin-bottom: 20px;
    }
    .metric-card {
        background-color: #fbfcfc;
        border: 1px solid #cdd7d9;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Encabezado principal
st.markdown('<p class="main-header">⛏️ Laboratorio del Macizo Rocoso</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Cuaderno Geomecánico Digital &bull; Hoek-Brown & Clasificaciones Empíricas</p>', unsafe_allow_html=True)

# Sección de pestañas para organizar los módulos
tab1, tab2, tab3, tab4 = st.tabs(["RQD", "RMR (Bieniawski)", "Q de Barton", "Hoek-Brown"])

with tab1:
    st.subheader("Evaluación de RQD (Rock Quality Designation)")
    st.write("Ingrese las longitudes de los fragmentos de testigo mayores a 10 cm recuperados en la maniobra.")
    
    longitud_recuperada = st.number_input("Longitud total de fragmentos >= 10 cm (cm)", min_value=0.0, value=85.0, step=1.0)
    longitud_total = st.number_input("Longitud total del vano / perforación (cm)", min_value=0.1, value=100.0, step=1.0)
    
    if longitud_total > 0:
        rqd = (longitud_recuperada / longitud_total) * 100
        st.metric(label="Valor RQD (%)", value=f"{rqd:.2f}%")
        
        # Calificación del RQD según Deere
        if rqd < 25:
            calif = "Muy Pobre"
        elif rqd < 50:
            calif = "Pobre"
        elif rqd < 75:
            calif = "Regular"
        elif rqd < 90:
            calif = "Bueno"
        else:
            calif = "Excelente"
        st.info(f"Calidad del macizo rocoso (Deere): **{calif}**")

with tab2:
    st.subheader("Clasificación RMR (Bieniawski, 1989)")
    
    col1, col2 = st.columns(2)
    with col1:
        resistencia = st.selectbox("1. Resistencia Compresiva Uniaxial (UCS)", [
            "> 250 MPa (15 pts)", "100 - 250 MPa (12 pts)", "50 - 100 MPa (7 pts)", 
            "25 - 50 MPa (4 pts)", "5 - 25 MPa (2 pts)", "1 - 5 MPa (1 pt)", "< 1 MPa (0 pts)"
        ])
        rqd_val = st.selectbox("2. Valor RQD", [
            "90% - 100% (20 pts)", "75% - 90% (17 pts)", "50% - 75% (13 pts)", 
            "25% - 50% (8 pts)", "< 25% (3 pts)"
        ])
        espaciado = st.selectbox("3. Espaciado de discontinuidades", [
            "> 2 m (20 pts)", "0.6 - 2 m (15 pts)", "200 - 600 mm (10 pts)", 
            "60 - 200 mm (8 pts)", "< 60 mm (5 pts)"
        ])
    
    with col2:
        condicion = st.selectbox("4. Condición de las discontinuidades", [
            "Muy buenas: superficies muy rugosas, cerradas (30 pts)",
            "Buenas: ligeramente rugosas, separación < 1mm (25 pts)",
            "Regulares: superficies lisas, separación 1-5mm (20 pts)",
            "Malas: slickensided o relleno blando > 5mm (10 pts)",
            "Muy malas: relleno blando continuo > 5mm (0 pts)"
        ])
        agua = st.selectbox("5. Presencia de agua subterránea", [
            "Completamente seco (15 pts)", "Húmedo (10 pts)", "Goteo (7 pts)", 
            "Flujo moderado (4 pts)", "Flujo severo (0 pts)"
        ])
        ajuste_orientacion = st.slider("6. Ajuste por orientación de juntas", -60, 0, -5)

    # Lógica de asignación de puntos aproximada para demostración en vivo
    pts_res = {" > 250 MPa (15 pts)": 15, "100 - 250 MPa (12 pts)": 12, "50 - 100 MPa (7 pts)": 7, "25 - 50 MPa (4 pts)": 4, "5 - 25 MPa (2 pts)": 2, "1 - 5 MPa (1 pt)": 1, "< 1 MPa (0 pts)": 0}
    pts_rqd = {"90% - 100% (20 pts)": 20, "75% - 90% (17 pts)": 17, "50% - 75% (13 pts)": 13, "25% - 50% (8 pts)": 8, "< 25% (3 pts)": 3}
    pts_esp = {" > 2 m (20 pts)": 20, "0.6 - 2 m (15 pts)": 15, "200 - 600 mm (10 pts)": 10, "60 - 200 mm (8 pts)": 8, "< 60 mm (5 pts)": 5}
    pts_con = {
        "Muy buenas: superficies muy rugosas, cerradas (30 pts)": 30,
        "Buenas: ligeramente rugosas, separación < 1mm (25 pts)": 25,
        "Regulares: superficies lisas, separación 1-5mm (20 pts)": 20,
        "Malas: slickensided o relleno blando > 5mm (10 pts)": 10,
        "Muy malas: relleno blando continuo > 5mm (0 pts)": 0
    }
    pts_agu = {"Completamente seco (15 pts)": 15, "Húmedo (10 pts)": 10, "Goteo (7 pts)": 7, "Flujo moderado (4 pts)": 4, "Flujo severo (0 pts)": 0}

    rmr_total = pts_res[resistencia] + pts_rqd[rqd_val] + pts_esp[espaciado] + pts_con[condicion] + pts_agu[agua] + ajuste_orientacion
    st.markdown("---")
    st.metric(label="RMR Básico Modificado", value=f"{rmr_total} pts")

with tab3:
    st.subheader("Sistema Q de Barton")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        rqd_q = st.number_input("RQD", 0.0, 100.0, 75.0)
        jn = st.number_input("Jn (Índice de familias de juntas)", 0.5, 20.0, 9.0)
        jr = st.number_input("Jr (Índice de rugosidad)", 0.5, 20.0, 1.5)
    with col_q2:
        ja = st.number_input("Ja (Índice de alteración)", 0.75, 20.0, 1.0)
        jw = st.number_input("Jw (Factor de reducción por agua)", 0.05, 1.0, 1.0)
        srf = st.number_input("SRF (Factor de reducción de esfuerzo)", 0.5, 400.0, 2.5)

    if jn > 0 and ja > 0 and srf > 0:
        q_val = (rqd_q / jn) * (jr / ja) * (jw / srf)
        st.metric(label="Valor Q de Barton", value=f"{q_val:.3f}")

with tab4:
    st.subheader("Criterio de Hoek-Brown (Generalized, 2002)")
    sig_ci = st.number_input("Resistencia a la compresión de la roca intacta (sig_ci en MPa)", value=80.0)
    mi = st.number_input("Constante de la roca intacta (mi)", value=10.0)
    gsi = st.slider("Índice de Resistencia Geológica (GSI)", 10, 100, 65)
    
    # Cálculo simplificado de parámetros Hoek-Brown
    import math
    if gsi >= 45:
        s = math.exp((gsi - 100) / 9)
        a = 0.5
        mb = mi * math.exp((gsi - 100) / 28)
    else:
        s = math.exp((gsi - 100) / 9)
        a = 0.65 - (gsi / 200)
        mb = mi * math.exp((gsi - 100) / 28)

    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    c1.metric("Parámetro mb", f"{mb:.3f}")
    c2.metric("Parámetro s", f"{s:.5f}")
    c3.metric("Parámetro a", f"{a:.4f}")
