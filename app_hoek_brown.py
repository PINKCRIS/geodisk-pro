# -*- coding: utf-8 -*-
"""
GEOMECÁNICA DE MACIZOS ROCOSOS · Hoek-Brown (2002) / Mohr-Coulomb
=================================================================
Aplicación Streamlit que:
  1. Calcula propiedades físicas de la roca (densidades, porosidad, e, w, γ).
  2. Determina el GSI (matriz cualitativa, método cuantitativo RQD+JCond89 o directo).
  3. Selecciona el factor de perturbación D (guía de Hoek, Carranza-Torres & Corkum, 2002).
  4. Calcula mb, s, a, σt, σc, σcm, Erm y σ3max.
  5. Obtiene c' y φ' equivalentes de Mohr-Coulomb (fórmulas cerradas y ajuste numérico).
  6. Dibuja en tiempo real las envolventes HB y MC (τ–σn y σ1–σ3) con círculo de Mohr.

Ejecución:
    pip install streamlit numpy pandas plotly
    streamlit run app_hoek_brown.py

Referencias:
  - Hoek, Carranza-Torres & Corkum (2002). Hoek-Brown failure criterion – 2002 edition.
  - Hoek & Diederichs (2006). Empirical estimation of rock mass modulus.
  - Hoek, Carter & Diederichs (2013). Quantification of the GSI.
  - Balmer (1952). Envolvente de Mohr a partir de σ1(σ3).
"""

import inspect

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

G = 9.81          # m/s²
RHO_W = 1.0       # g/cm³

# ----------------------------------------------------------------------------
# DATOS DE REFERENCIA
# ----------------------------------------------------------------------------
MI_TABLA = {
    # Ígneas
    "Granito": 32, "Granodiorita": 29, "Diorita": 25, "Dolerita": 16, "Gabro": 27,
    "Norita": 20, "Andesita": 25, "Basalto": 25, "Riolita": 25, "Dacita": 25,
    "Obsidiana": 19, "Toba": 13, "Aglomerado": 19,
    # Metamórficas
    "Mármol": 9, "Cuarcita": 20, "Gneis": 28, "Esquisto": 12, "Filita": 7,
    "Pizarra": 7, "Corneana (hornfels)": 19, "Anfibolita": 26, "Migmatita": 29,
    "Metarenisca": 19,
    # Sedimentarias
    "Arenisca": 17, "Limolita": 7, "Arcillolita": 4, "Lutita (shale)": 6,
    "Marga": 7, "Conglomerado": 21, "Brecha": 19, "Grauvaca": 18,
    "Caliza cristalina": 12, "Caliza esparítica": 10, "Caliza micrítica": 8,
    "Dolomía": 9, "Yeso": 8, "Anhidrita": 12, "Tiza": 7,
}

ESTRUCTURAS = [
    ("Intacta o masiva", "Roca intacta o masiva, con pocas discontinuidades muy espaciadas"),
    ("En bloques", "Muy bien trabada, no perturbada; bloques cúbicos (3 familias ortogonales)"),
    ("Muy en bloques", "Trabada, parcialmente perturbada; bloques angulosos (4 o más familias)"),
    ("En bloques perturbada", "Plegada/fallada; bloques angulosos de muchas familias que se intersectan"),
    ("Desintegrada", "Mal trabada, muy fracturada; mezcla de fragmentos angulosos y redondeados"),
]
SUPERFICIES = [
    ("Muy buena", "Muy rugosa, fresca, sin meteorización"),
    ("Buena", "Rugosa, ligeramente meteorizada, con manchas de óxido"),
    ("Regular", "Lisa, moderadamente meteorizada o alterada"),
    ("Mala", "Espejos de falla, muy meteorizada, relleno compacto o fragmentos angulosos"),
    ("Muy mala", "Espejos de falla, muy meteorizada, relleno de arcilla blanda"),
]

# Valoraciones de JCond89 (Bieniawski, 1989) para GSI = 1.5·JCond89 + RQD/2
JCOND89 = {
    "Persistencia (longitud)": {"< 1 m": 6, "1–3 m": 4, "3–10 m": 2, "10–20 m": 1, "> 20 m": 0},
    "Apertura (separación)": {"Cerrada": 6, "< 0,1 mm": 5, "0,1–1 mm": 4, "1–5 mm": 1, "> 5 mm": 0},
    "Rugosidad": {"Muy rugosa": 6, "Rugosa": 5, "Ligeramente rugosa": 3, "Lisa": 1, "Espejo de falla": 0},
    "Relleno": {"Ninguno": 6, "Duro < 5 mm": 4, "Duro > 5 mm": 2, "Blando < 5 mm": 2, "Blando > 5 mm": 0},
    "Meteorización": {"Inalterada": 6, "Ligera": 5, "Moderada": 3, "Alta": 1, "Descompuesta": 0},
}

# Guía para D (Hoek et al., 2002)
TABLA_D = {
    "Voladura controlada de excelente calidad o excavación con TBM (túnel)": 0.0,
    "Excavación mecánica/manual en roca de mala calidad, sin voladura (túnel)": 0.0,
    "Excavación mecánica en terreno expansivo (squeezing) sin contrabóveda": 0.5,
    "Voladura de muy mala calidad en túnel de roca dura (daño local de 2–3 m)": 0.8,
    "Talud civil, voladura pequeña bien controlada": 0.7,
    "Talud civil, voladura deficiente": 1.0,
    "Mina a cielo abierto, voladura de producción": 1.0,
    "Mina a cielo abierto, excavación mecánica (ripping/dozing)": 0.7,
    "Personalizado": 0.0,
}


# ----------------------------------------------------------------------------
# FUNCIONES DE CÁLCULO (puras, sin Streamlit)
# ----------------------------------------------------------------------------
def gsi_matriz():
    """Valores centrales aproximados de GSI para cada celda de la matriz (5×5)."""
    m = np.zeros((5, 5))
    for i in range(5):
        for j in range(5):
            m[i, j] = max(5.0, 90.0 - 10.0 * i - 10.0 * j)
    return m


def parametros_hb(gsi, mi, d):
    """Parámetros del criterio generalizado de Hoek-Brown (edición 2002)."""
    mb = mi * np.exp((gsi - 100.0) / (28.0 - 14.0 * d))
    s = np.exp((gsi - 100.0) / (9.0 - 3.0 * d))
    a = 0.5 + (np.exp(-gsi / 15.0) - np.exp(-20.0 / 3.0)) / 6.0
    return mb, s, a


def sigma1_hb(sigma3, sci, mb, s, a):
    """σ1 = σ3 + σci (mb σ3/σci + s)^a"""
    x = np.maximum(mb * np.asarray(sigma3, dtype=float) / sci + s, 0.0)
    return sigma3 + sci * x ** a


def balmer(sigma3, sci, mb, s, a):
    """Envolvente de Mohr de HB (Balmer, 1952). Devuelve σn, τ, σ1."""
    sigma3 = np.asarray(sigma3, dtype=float)
    x = np.maximum(mb * sigma3 / sci + s, 1e-12)
    s1 = sigma3 + sci * x ** a
    dd = 1.0 + a * mb * x ** (a - 1.0)            # dσ1/dσ3
    sn = sigma3 + (s1 - sigma3) / (dd + 1.0)
    tau = (s1 - sigma3) * np.sqrt(dd) / (dd + 1.0)
    return sn, tau, s1


def resistencias_macizo(sci, mb, s, a):
    """σt, σc (uniaxial del macizo) y σcm (resistencia global del macizo)."""
    sigma_t = -s * sci / mb
    sigma_c = sci * s ** a
    sigma_cm = (sci * (mb + 4 * s - a * (mb - 8 * s)) * (mb / 4 + s) ** (a - 1)
                / (2 * (1 + a) * (2 + a)))
    return sigma_t, sigma_c, sigma_cm


def modulo_deformacion(gsi, d, ei=None):
    """Módulo de deformación del macizo Erm (MPa), Hoek & Diederichs (2006)."""
    if ei is None:
        return 1e5 * (1 - d / 2) / (1 + np.exp((75 + 25 * d - gsi) / 11))
    return ei * (0.02 + (1 - d / 2) / (1 + np.exp((60 + 15 * d - gsi) / 11)))


def sigma3max_hoek(sigma_cm, gamma, h, tipo):
    """σ3max (MPa) para el ajuste MC. γ en kN/m³ y H en m."""
    gh = max(gamma * h / 1000.0, 1e-6)      # MPa
    if tipo == "Túnel":
        ratio = 0.47 * (sigma_cm / gh) ** (-0.94)
    else:                                    # talud
        ratio = 0.72 * (sigma_cm / gh) ** (-0.91)
    return ratio * sigma_cm


def mc_equivalente(sci, mb, s, a, s3max):
    """c' (MPa) y φ' (°) equivalentes, fórmulas cerradas de Hoek et al. (2002)."""
    s3n = s3max / sci
    k = (s + mb * s3n) ** (a - 1.0)
    phi = np.arcsin(6 * a * mb * k / (2 * (1 + a) * (2 + a) + 6 * a * mb * k))
    c = (sci * ((1 + 2 * a) * s + (1 - a) * mb * s3n) * k
         / ((1 + a) * (2 + a) * np.sqrt(1 + 6 * a * mb * k / ((1 + a) * (2 + a)))))
    return float(c), float(np.degrees(phi))


def mc_ajuste_numerico(sci, mb, s, a, s3max, n=80):
    """Regresión lineal σ1–σ3 de HB en el rango σt < σ3 < σ3max (ajuste numérico)."""
    sigma_t = -s * sci / mb
    s3 = np.linspace(sigma_t, s3max, n)
    s1 = sigma1_hb(s3, sci, mb, s, a)
    k, b = np.polyfit(s3, s1, 1)
    sin_phi = np.clip((k - 1.0) / (k + 1.0), 0.0, 0.999)
    phi = np.arcsin(sin_phi)
    c = b * (1 - sin_phi) / (2 * np.cos(phi))
    return float(c), float(np.degrees(phi))


# ----------------------------------------------------------------------------
# UTILIDADES DE INTERFAZ
# ----------------------------------------------------------------------------
_TIENE_WIDTH = "width" in inspect.signature(st.plotly_chart).parameters


def mostrar(fig, key=None):
    """Compatibilidad entre versiones de Streamlit para ancho completo."""
    if _TIENE_WIDTH:
        st.plotly_chart(fig, width="stretch", key=key)
    else:
        st.plotly_chart(fig, use_container_width=True, key=key)


def entradas_sidebar():
    st.sidebar.header("🪨 Roca intacta")
    sci = st.sidebar.number_input("σci – resistencia a compresión uniaxial (MPa)",
                                  1.0, 500.0, 80.0, 1.0)
    opciones = list(MI_TABLA) + ["Personalizado"]
    roca = st.sidebar.selectbox("Tipo de roca (para mi)", opciones,
                                index=opciones.index("Granito"))
    mi_def = float(MI_TABLA.get(roca, 15))
    mi = st.sidebar.number_input("mi – constante de la roca intacta", 1.0, 50.0, mi_def, 0.5,
                                 key=f"mi_{roca}")
    mr = st.sidebar.slider("MR – relación de módulo (Ei = MR·σci)", 100, 1000, 350, 10)

    st.sidebar.header("🏗️ Obra / confinamiento")
    tipo = st.sidebar.radio("Tipo de obra para σ3max", ["Talud", "Túnel", "Manual"], horizontal=True)
    h, s3max_manual = 100.0, 1.0
    if tipo == "Talud":
        h = st.sidebar.number_input("Altura del talud H (m)", 1.0, 1500.0, 100.0, 5.0)
    elif tipo == "Túnel":
        h = st.sidebar.number_input("Profundidad del túnel H (m)", 1.0, 3000.0, 300.0, 10.0)
    else:
        s3max_manual = st.sidebar.number_input("σ3max (MPa)", 0.01, 200.0, 1.0, 0.05)
    return dict(sci=sci, mi=mi, mr=mr, tipo=tipo, h=h, s3max_manual=s3max_manual, roca=roca)


# ----------------------------------------------------------------------------
# PESTAÑA 1 · PROPIEDADES FÍSICAS
# ----------------------------------------------------------------------------
def tab_propiedades():
    st.subheader("Propiedades físicas de la roca")
    modo = st.radio("Método de cálculo",
                    ["Ensayo de laboratorio (masas)", "Índices (Gs, n)"], horizontal=True)
    c1, c2 = st.columns(2)

    with c2:
        sr = st.slider("Grado de saturación natural Sr (%)", 0, 100, 50) / 100.0

    with c1:
        if modo.startswith("Ensayo"):
            m_seca = st.number_input("Masa seca Md (g)", 0.1, 100000.0, 250.0, 1.0)
            m_sat = st.number_input("Masa saturada superficie seca Msat (g)", 0.1, 100000.0, 253.0, 1.0)
            m_sum = st.number_input("Masa sumergida Msub (g)", 0.0, 100000.0, 157.0, 1.0)
            if not (m_sat >= m_seca and m_sat > m_sum):
                st.error("Se requiere Msat ≥ Md y Msat > Msub.")
                st.stop()
            vb = (m_sat - m_sum) / RHO_W                  # cm³
            rho_d = m_seca / vb
            n = (m_sat - m_seca) / (m_sat - m_sum)
            gs = rho_d / (RHO_W * (1 - n))
        else:
            gs = st.number_input("Gravedad específica de sólidos Gs", 1.5, 5.0, 2.70, 0.01)
            n = st.slider("Porosidad n (%)", 0.0, 50.0, 1.0, 0.1) / 100.0
            rho_d = gs * RHO_W * (1 - n)

    rho_sat = rho_d + n * RHO_W
    rho_nat = rho_d + sr * n * RHO_W
    e = n / (1 - n)
    w = sr * n * RHO_W / rho_d
    gam_d, gam_nat, gam_sat = rho_d * G, rho_nat * G, rho_sat * G
    gam_sum = gam_sat - G * RHO_W

    m = st.columns(4)
    m[0].metric("ρ seca", f"{rho_d:.3f} g/cm³")
    m[1].metric("ρ natural", f"{rho_nat:.3f} g/cm³")
    m[2].metric("ρ saturada", f"{rho_sat:.3f} g/cm³")
    m[3].metric("γ natural", f"{gam_nat:.2f} kN/m³")
    m = st.columns(4)
    m[0].metric("Porosidad n", f"{n * 100:.2f} %")
    m[1].metric("Índice de vacíos e", f"{e:.4f}")
    m[2].metric("Humedad natural w", f"{w * 100:.3f} %")
    m[3].metric("Gs", f"{gs:.3f}")

    usar_manual = st.checkbox("Usar un peso unitario manual para el cálculo de σ3max", False)
    gamma = gam_nat
    if usar_manual:
        gamma = st.number_input("γ (kN/m³)", 10.0, 40.0, float(round(gam_nat, 2)), 0.1)

    with st.expander("Ver tabla completa"):
        df = pd.DataFrame([
            ("Densidad seca ρd", rho_d, "g/cm³"), ("Densidad natural ρ", rho_nat, "g/cm³"),
            ("Densidad saturada ρsat", rho_sat, "g/cm³"),
            ("Peso unitario seco γd", gam_d, "kN/m³"), ("Peso unitario natural γ", gam_nat, "kN/m³"),
            ("Peso unitario saturado γsat", gam_sat, "kN/m³"),
            ("Peso unitario sumergido γ'", gam_sum, "kN/m³"),
            ("Porosidad n", n * 100, "%"), ("Índice de vacíos e", e, "–"),
            ("Humedad natural w", w * 100, "%"), ("Saturación Sr", sr * 100, "%"),
            ("Gravedad específica Gs", gs, "–"),
        ], columns=["Propiedad", "Valor", "Unidad"])
        df["Valor"] = df["Valor"].round(4)
        st.dataframe(df, hide_index=True)

    return dict(rho_d=rho_d, rho_nat=rho_nat, rho_sat=rho_sat, n=n, e=e, w=w,
                gs=gs, gamma=gamma, gamma_nat=gam_nat)


# ----------------------------------------------------------------------------
# PESTAÑA 2 · GSI
# ----------------------------------------------------------------------------
def figura_matriz_gsi(mat, i_sel, j_sel):
    fig = go.Figure(go.Heatmap(
        z=mat, x=[s[0] for s in SUPERFICIES], y=[e[0] for e in ESTRUCTURAS],
        colorscale="RdYlGn", zmin=0, zmax=100, text=mat.astype(int), texttemplate="%{text}",
        colorbar=dict(title="GSI"),
        hovertemplate="Estructura: %{y}<br>Superficie: %{x}<br>GSI ≈ %{z}<extra></extra>"))
    fig.add_shape(type="rect", x0=j_sel - 0.5, x1=j_sel + 0.5, y0=i_sel - 0.5, y1=i_sel + 0.5,
                  line=dict(color="black", width=4))
    fig.update_yaxes(autorange="reversed", title="Estructura del macizo")
    fig.update_xaxes(title="Condición de la superficie de las discontinuidades", side="top")
    fig.update_layout(height=430, margin=dict(l=10, r=10, t=70, b=10), template="plotly_white")
    return fig


def tab_gsi():
    st.subheader("Índice de resistencia geológica (GSI)")
    metodo = st.radio("Método", ["Matriz cualitativa (Hoek & Marinos)",
                                 "Cuantitativo (RQD + JCond89)", "Valor directo"], horizontal=True)
    if metodo.startswith("Matriz"):
        mat = gsi_matriz()
        c1, c2 = st.columns([1, 1.4])
        with c1:
            i = st.selectbox("Estructura del macizo", range(5),
                             format_func=lambda k: ESTRUCTURAS[k][0], index=2)
            st.caption(ESTRUCTURAS[i][1])
            j = st.selectbox("Condición de las discontinuidades", range(5),
                             format_func=lambda k: SUPERFICIES[k][0], index=1)
            st.caption(SUPERFICIES[j][1])
            ajuste = st.slider("Ajuste fino dentro de la celda (puntos)", -5.0, 5.0, 0.0, 0.5)
            gsi = float(np.clip(mat[i, j] + ajuste, 0, 100))
            st.metric("GSI adoptado", f"{gsi:.1f}")
            st.caption("Los valores de la matriz son centros de celda aproximados del gráfico original.")
        with c2:
            mostrar(figura_matriz_gsi(mat, i, j), key="matriz_gsi")
    elif metodo.startswith("Cuantitativo"):
        c1, c2 = st.columns(2)
        with c1:
            rqd = st.slider("RQD (%)", 0, 100, 75)
            st.caption("Si solo tienes Jv: RQD ≈ 115 − 3,3·Jv (acotado a 0–100).")
        total = 0
        with c2:
            for nombre, tabla in JCOND89.items():
                op = st.selectbox(nombre, list(tabla), index=1, key=f"jc_{nombre}")
                total += tabla[op]
        gsi = float(np.clip(1.5 * total + rqd / 2.0, 0, 100))
        st.info(f"JCond89 = {total} · GSI = 1,5·{total} + {rqd}/2 = **{gsi:.1f}**")
    else:
        gsi = st.slider("GSI", 5.0, 100.0, 60.0, 0.5)
    return gsi


# ----------------------------------------------------------------------------
# PESTAÑA 3 · FACTOR D
# ----------------------------------------------------------------------------
def tab_perturbacion():
    st.subheader("Factor de perturbación D")
    opcion = st.selectbox("Condición de excavación (Hoek et al., 2002)", list(TABLA_D))
    d = st.slider("D", 0.0, 1.0, float(TABLA_D[opcion]), 0.05, key=f"d_{opcion}")
    st.caption("D = 0: macizo sin perturbar · D = 1: macizo muy perturbado (voladura de producción).")
    return float(d)


# ----------------------------------------------------------------------------
# PESTAÑA 4 · PARÁMETROS
# ----------------------------------------------------------------------------
def tab_parametros(P):
    st.subheader("Parámetros de Hoek-Brown y resistencia del macizo")
    c = st.columns(3)
    c[0].metric("mb", f"{P['mb']:.4f}")
    c[1].metric("s", f"{P['s']:.6f}")
    c[2].metric("a", f"{P['a']:.4f}")
    c = st.columns(4)
    c[0].metric("σt (tracción)", f"{P['sigma_t']:.4f} MPa")
    c[1].metric("σc (uniaxial macizo)", f"{P['sigma_c']:.3f} MPa")
    c[2].metric("σcm (global)", f"{P['sigma_cm']:.2f} MPa")
    c[3].metric("Erm", f"{P['erm'] / 1000:.2f} GPa")
    c = st.columns(4)
    c[0].metric("σ3max", f"{P['s3max']:.3f} MPa")
    c[1].metric("c' (MC, fórmula)", f"{P['c_cf']:.3f} MPa")
    c[2].metric("φ' (MC, fórmula)", f"{P['phi_cf']:.2f} °")
    c[3].metric("σcm/σci", f"{P['sigma_cm'] / P['sci']:.3f}")

    with st.expander("Ecuaciones utilizadas"):
        st.latex(r"m_b = m_i \exp\left(\frac{GSI-100}{28-14D}\right),\quad "
                 r"s = \exp\left(\frac{GSI-100}{9-3D}\right)")
        st.latex(r"a = \tfrac12 + \tfrac16\left(e^{-GSI/15} - e^{-20/3}\right)")
        st.latex(r"\sigma_1 = \sigma_3 + \sigma_{ci}\left(m_b\frac{\sigma_3}{\sigma_{ci}} + s\right)^a")
        st.latex(r"\sigma_t = -\frac{s\,\sigma_{ci}}{m_b},\quad \sigma_c = \sigma_{ci}\,s^a")
        st.latex(r"\sigma_{cm} = \sigma_{ci}\,\frac{m_b + 4s - a(m_b - 8s)\,(m_b/4 + s)^{a-1}}"
                 r"{2(1+a)(2+a)}")
        st.latex(r"E_{rm} = E_i\left(0.02 + \frac{1-D/2}{1+e^{(60+15D-GSI)/11}}\right)")
        st.latex(r"\sigma_n = \sigma_3 + \frac{\sigma_1-\sigma_3}{\partial\sigma_1/\partial\sigma_3 + 1},\quad "
                 r"\tau = (\sigma_1-\sigma_3)\frac{\sqrt{\partial\sigma_1/\partial\sigma_3}}"
                 r"{\partial\sigma_1/\partial\sigma_3 + 1}")
        st.latex(r"\phi' = \sin^{-1}\frac{6\,a\,m_b(s+m_b\sigma_{3n})^{a-1}}"
                 r"{2(1+a)(2+a)+6\,a\,m_b(s+m_b\sigma_{3n})^{a-1}}")
        st.latex(r"c' = \frac{\sigma_{ci}\left[(1+2a)s+(1-a)m_b\sigma_{3n}\right](s+m_b\sigma_{3n})^{a-1}}"
                 r"{(1+a)(2+a)\sqrt{1+\dfrac{6\,a\,m_b(s+m_b\sigma_{3n})^{a-1}}{(1+a)(2+a)}}}")
        st.latex(r"\frac{\sigma_{3max}}{\sigma_{cm}} = 0.72\left(\frac{\sigma_{cm}}{\gamma H}\right)^{-0.91}"
                 r"\ \text{(taludes)},\quad "
                 r"0.47\left(\frac{\sigma_{cm}}{\gamma H}\right)^{-0.94}\ \text{(túneles)}")


# ----------------------------------------------------------------------------
# PESTAÑA 5 · ENVOLVENTES
# ----------------------------------------------------------------------------
def tab_envolventes(P):
    st.subheader("Envolventes de falla en tiempo real")
    sci, mb, s, a = P["sci"], P["mb"], P["s"], P["a"]
    sigma_t, s3max = P["sigma_t"], P["s3max"]
    c_cf, phi_cf = P["c_cf"], P["phi_cf"]
    c_nm, phi_nm = P["c_num"], P["phi_num"]

    k1, k2, k3, k4 = st.columns(4)
    ext = k1.slider("Rango de σ3 (× σ3max)", 1.0, 10.0, 3.0, 0.5)
    pct = k2.slider("Posición del círculo de Mohr (%)", 0, 100, 40)
    ver_circulo = k3.checkbox("Círculo de Mohr + tangencia", True)
    ver_num = k4.checkbox("Ajuste numérico MC", True)

    s3_top = ext * s3max
    s3 = np.linspace(sigma_t, s3_top, 600)
    sn, tau, s1 = balmer(s3, sci, mb, s, a)
    mask = s3 <= s3max

    s3c = sigma_t + pct / 100.0 * (s3_top - sigma_t)
    snc, tauc, s1c = balmer(np.array([s3c]), sci, mb, s, a)
    snc, tauc, s1c = float(snc[0]), float(tauc[0]), float(s1c[0])

    tan_f = np.tan(np.radians(phi_cf))
    sin_f = np.sin(np.radians(phi_cf))
    cos_f = np.cos(np.radians(phi_cf))

    # ---------------- τ–σn ----------------
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=sn, y=tau, mode="lines", name="Hoek-Brown",
                              line=dict(color="crimson", width=3)))
    fig1.add_trace(go.Scatter(x=sn[mask], y=tau[mask], mode="lines", name="Rango de ajuste (σt–σ3max)",
                              line=dict(color="rgba(220,20,60,0.25)", width=12), hoverinfo="skip"))
    x_min = -c_cf / tan_f if tan_f > 1e-9 else 0.0
    xs = np.array([x_min, float(np.max(sn)) * 1.05])
    fig1.add_trace(go.Scatter(x=xs, y=c_cf + xs * tan_f, mode="lines",
                              name=f"MC fórmula: c'={c_cf:.2f} MPa, φ'={phi_cf:.1f}°",
                              line=dict(color="royalblue", width=2.5)))
    if ver_num:
        tn = np.tan(np.radians(phi_nm))
        xn_min = -c_nm / tn if tn > 1e-9 else 0.0
        xn = np.array([xn_min, float(np.max(sn)) * 1.05])
        fig1.add_trace(go.Scatter(x=xn, y=c_nm + xn * tn, mode="lines",
                                  name=f"MC numérico: c'={c_nm:.2f} MPa, φ'={phi_nm:.1f}°",
                                  line=dict(color="seagreen", width=2, dash="dash")))
    if ver_circulo:
        th = np.linspace(0, np.pi, 200)
        cen, rad = (s1c + s3c) / 2.0, (s1c - s3c) / 2.0
        fig1.add_trace(go.Scatter(x=cen + rad * np.cos(th), y=rad * np.sin(th), mode="lines",
                                  name="Círculo de Mohr", line=dict(color="gray", width=2)))
        fig1.add_trace(go.Scatter(x=[snc], y=[tauc], mode="markers", name="Punto de tangencia",
                                  marker=dict(color="black", size=10, symbol="x")))
    fig1.update_xaxes(title="σn (MPa)", zeroline=True)
    fig1.update_yaxes(title="τ (MPa)", rangemode="tozero", scaleanchor="x", scaleratio=1)
    fig1.update_layout(title="Espacio τ–σn (envolvente de Mohr)", height=520, template="plotly_white",
                       legend=dict(orientation="h", y=-0.2), margin=dict(l=10, r=10, t=50, b=10))

    # ---------------- σ1–σ3 ----------------
    k = (1 + sin_f) / (1 - sin_f)
    sc_mc = 2 * c_cf * cos_f / (1 - sin_f)
    xs3 = np.array([sigma_t, s3_top])
    fig2 = go.Figure()
    fig2.add_vrect(x0=sigma_t, x1=s3max, fillcolor="orange", opacity=0.15, line_width=0,
                   annotation_text="Rango de ajuste", annotation_position="top left")
    fig2.add_trace(go.Scatter(x=s3, y=s1, mode="lines", name="Hoek-Brown",
                              line=dict(color="crimson", width=3)))
    fig2.add_trace(go.Scatter(x=xs3, y=sc_mc + k * xs3, mode="lines", name="MC fórmula",
                              line=dict(color="royalblue", width=2.5)))
    if ver_num:
        sn_f = np.sin(np.radians(phi_nm))
        k_n = (1 + sn_f) / (1 - sn_f)
        sc_n = 2 * c_nm * np.cos(np.radians(phi_nm)) / (1 - sn_f)
        fig2.add_trace(go.Scatter(x=xs3, y=sc_n + k_n * xs3, mode="lines", name="MC numérico",
                                  line=dict(color="seagreen", width=2, dash="dash")))
    if ver_circulo:
        fig2.add_trace(go.Scatter(x=[s3c], y=[s1c], mode="markers", name="Estado del círculo",
                                  marker=dict(color="black", size=10, symbol="x")))
    fig2.update_xaxes(title="σ3 (MPa)")
    fig2.update_yaxes(title="σ1 (MPa)")
    fig2.update_layout(title="Espacio σ1–σ3", height=520, template="plotly_white",
                       legend=dict(orientation="h", y=-0.2), margin=dict(l=10, r=10, t=50, b=10))

    g1, g2 = st.columns(2)
    with g1:
        mostrar(fig1, key="fig_tau_sn")
    with g2:
        mostrar(fig2, key="fig_s1_s3")

    st.caption(f"Círculo seleccionado: σ3 = {s3c:.3f} MPa · σ1 = {s1c:.3f} MPa · "
               f"tangencia en σn = {snc:.3f} MPa, τ = {tauc:.3f} MPa.")
    comp = pd.DataFrame({
        "Método": ["Fórmulas cerradas (Hoek 2002)", "Ajuste numérico (regresión σ1–σ3)"],
        "c' (MPa)": [round(c_cf, 4), round(c_nm, 4)],
        "φ' (°)": [round(phi_cf, 3), round(phi_nm, 3)],
    })
    st.dataframe(comp, hide_index=True)


# ----------------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ----------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="Hoek-Brown · Mohr-Coulomb", page_icon="⛏️", layout="wide")
    st.title("⛏️ Geomecánica de macizos rocosos · Hoek-Brown y Mohr-Coulomb")
    st.caption("Propiedades físicas · GSI · factor D · parámetros HB · envolventes de falla interactivas")

    S = entradas_sidebar()
    resumen = st.container()
    tabs = st.tabs(["1 · Propiedades físicas", "2 · GSI", "3 · Factor D",
                    "4 · Parámetros HB", "5 · Envolventes"])

    with tabs[0]:
        fis = tab_propiedades()
    with tabs[1]:
        gsi = tab_gsi()
    with tabs[2]:
        d = tab_perturbacion()

    # ------------------------- cálculos -------------------------
    sci, mi = S["sci"], S["mi"]
    mb, s, a = parametros_hb(gsi, mi, d)
    sigma_t, sigma_c, sigma_cm = resistencias_macizo(sci, mb, s, a)
    erm = modulo_deformacion(gsi, d, ei=S["mr"] * sci)

    if S["tipo"] == "Manual":
        s3max = S["s3max_manual"]
    else:
        s3max = sigma3max_hoek(sigma_cm, fis["gamma"], S["h"], S["tipo"])

    c_cf, phi_cf = mc_equivalente(sci, mb, s, a, s3max)
    c_num, phi_num = mc_ajuste_numerico(sci, mb, s, a, s3max)

    P = dict(sci=sci, mi=mi, gsi=gsi, d=d, mb=mb, s=s, a=a, sigma_t=sigma_t, sigma_c=sigma_c,
             sigma_cm=sigma_cm, erm=erm, s3max=s3max, c_cf=c_cf, phi_cf=phi_cf,
             c_num=c_num, phi_num=phi_num)

    with resumen:
        m = st.columns(7)
        m[0].metric("GSI", f"{gsi:.1f}")
        m[1].metric("D", f"{d:.2f}")
        m[2].metric("mb", f"{mb:.3f}")
        m[3].metric("s", f"{s:.5f}")
        m[4].metric("a", f"{a:.4f}")
        m[5].metric("c' (MPa)", f"{c_cf:.3f}")
        m[6].metric("φ' (°)", f"{phi_cf:.2f}")

    with tabs[3]:
        tab_parametros(P)
        tabla = pd.DataFrame([
            ("σci", sci, "MPa"), ("mi", mi, "–"), ("GSI", gsi, "–"), ("D", d, "–"),
            ("mb", mb, "–"), ("s", s, "–"), ("a", a, "–"),
            ("σt", sigma_t, "MPa"), ("σc macizo", sigma_c, "MPa"), ("σcm", sigma_cm, "MPa"),
            ("Erm", erm, "MPa"), ("γ", fis["gamma"], "kN/m³"), ("σ3max", s3max, "MPa"),
            ("c' (fórmula)", c_cf, "MPa"), ("φ' (fórmula)", phi_cf, "°"),
            ("c' (numérico)", c_num, "MPa"), ("φ' (numérico)", phi_num, "°"),
            ("ρ natural", fis["rho_nat"], "g/cm³"), ("Porosidad n", fis["n"] * 100, "%"),
        ], columns=["Parámetro", "Valor", "Unidad"])
        st.download_button("⬇️ Descargar resultados (CSV)",
                           tabla.to_csv(index=False).encode("utf-8"),
                           file_name="resultados_hoek_brown.csv", mime="text/csv")

    with tabs[4]:
        tab_envolventes(P)


if __name__ == "__main__":
    main()
