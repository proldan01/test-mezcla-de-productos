"""
Optimización de Mezcla de Productos — Papelería MX
Teoría de Markowitz aplicada a portafolio de productos de papelería.
Ciudad de México · Ventas Nacionales
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Papelería MX · Optimización Markowitz",
    page_icon="📎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── SESSION STATE ────────────────────────────────────────────────────────────
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

# ─── CUSTOM CSS (Uiverse-inspired dark theme) ─────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a1628; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #0d1f2d 0%, #0f2335 60%, #091929 100%) !important;
    border-right: 1px solid rgba(42,157,143,0.2) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4) !important;
}

/* ── Uiverse-style glowing KPI cards ── */
.kpi-card {
    position: relative;
    background: #0f2335;
    border-radius: 16px;
    padding: 22px 16px 18px;
    text-align: center;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    border: 1px solid rgba(42,157,143,0.15);
    margin-bottom: 6px;
}
.kpi-card::before {
    content: '';
    position: absolute; inset: 0;
    background: linear-gradient(135deg, rgba(42,157,143,0.07) 0%, transparent 60%);
    pointer-events: none;
}
.kpi-card::after {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent 0%, #2a9d8f 40%, #e9c46a 70%, transparent 100%);
}
.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(42,157,143,0.22), 0 0 0 1px rgba(42,157,143,0.35);
}
.kpi-icon  { font-size: 1.65rem; margin-bottom: 6px; display: block; }
.kpi-value { font-size: 1.85rem; font-weight: 700; color: #2a9d8f; line-height: 1.15; }
.kpi-label {
    font-size: 0.7rem; color: #3e5e74;
    text-transform: uppercase; letter-spacing: 1.8px; margin-top: 5px;
}
.kpi-delta { font-size: 0.78rem; color: #e9c46a; font-weight: 500; margin-top: 6px; }

/* ── Uiverse-style toggle / action buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #264653, #2a9d8f) !important;
    color: #fff !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; letter-spacing: 0.5px !important;
    box-shadow: 0 0 14px rgba(42,157,143,0.35), inset 0 1px 0 rgba(255,255,255,0.08) !important;
    transition: all 0.22s !important; padding: 0.38rem 1rem !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 0 24px rgba(42,157,143,0.6) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Section headers ── */
.sec-hdr {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0; margin: 28px 0 14px;
    border-bottom: 1px solid rgba(42,157,143,0.16);
}
.sec-hdr-bar {
    width: 4px; height: 22px;
    background: linear-gradient(180deg, #2a9d8f, #e9c46a);
    border-radius: 2px; flex-shrink: 0;
}
.sec-hdr-text { font-size: 1.05rem; font-weight: 600; color: #bdd8e8; }
.sec-hdr-badge {
    margin-left: auto; padding: 3px 11px; border-radius: 20px;
    background: rgba(42,157,143,0.1); color: #2a9d8f;
    border: 1px solid rgba(42,157,143,0.28);
    font-size: 0.68rem; font-weight: 700; letter-spacing: 1.2px;
}

/* ── Hero block ── */
.hero-block {
    background: linear-gradient(135deg, rgba(42,157,143,0.09), rgba(233,196,106,0.03));
    border: 1px solid rgba(42,157,143,0.2);
    border-radius: 20px; padding: 28px 32px;
    margin-bottom: 22px; position: relative; overflow: hidden;
}
.hero-block::after {
    content: '📎'; position: absolute; right: 28px; top: 20px;
    font-size: 5rem; opacity: 0.055; pointer-events: none;
}
.hero-title {
    font-size: 1.8rem; font-weight: 700; margin: 0; line-height: 1.2;
    background: linear-gradient(135deg, #2a9d8f 30%, #e9c46a);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-subtitle { color: #3e5e74; font-size: 0.87rem; margin-top: 6px; }
.hero-tags { margin-top: 14px; display: flex; gap: 8px; flex-wrap: wrap; }
.hero-tag {
    padding: 4px 13px; border-radius: 20px; font-size: 0.7rem; font-weight: 500;
    background: rgba(42,157,143,0.1); color: #2a9d8f;
    border: 1px solid rgba(42,157,143,0.22);
}

/* ── Sidebar logo ── */
.sb-logo {
    background: linear-gradient(135deg, #1a3a4a, #2a9d8f);
    border-radius: 14px; padding: 18px; margin-bottom: 18px; text-align: center;
    box-shadow: 0 4px 22px rgba(42,157,143,0.28);
}
.sb-logo-main { font-size: 1.2rem; font-weight: 700; color: #fff; letter-spacing: 1px; }
.sb-logo-sub  {
    font-size: 0.62rem; color: #e9c46a;
    text-transform: uppercase; letter-spacing: 2.5px; margin-top: 4px;
}

/* ── Info / alert boxes ── */
.info-box {
    background: rgba(42,157,143,0.065);
    border: 1px solid rgba(42,157,143,0.2);
    border-left: 4px solid #2a9d8f;
    border-radius: 0 10px 10px 0;
    padding: 11px 15px; margin: 10px 0;
    font-size: 0.82rem; color: #6899aa; line-height: 1.55;
}
.gold-box {
    background: rgba(233,196,106,0.065);
    border: 1px solid rgba(233,196,106,0.2);
    border-left: 4px solid #e9c46a;
    border-radius: 0 10px 10px 0;
    padding: 11px 15px; margin: 10px 0;
    font-size: 0.82rem; color: #b8a460; line-height: 1.55;
}

/* ── Streamlit overrides ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stMetric"] {
    background: #0f2335 !important;
    border: 1px solid rgba(42,157,143,0.22) !important;
    border-radius: 14px !important; padding: 14px !important;
}
[data-testid="stMetricValue"] { color: #2a9d8f !important; font-size: 1.45rem !important; }
[data-testid="stMetricLabel"] { color: #3e5e74 !important; font-size: 0.74rem !important; }
div[data-testid="stExpander"] {
    background: rgba(15,35,53,0.65) !important;
    border: 1px solid rgba(42,157,143,0.16) !important;
    border-radius: 12px !important;
}
[data-testid="stExpander"] summary { color: #bdd8e8 !important; }
.stSlider > div > div > div > div { background: #2a9d8f !important; }
.stFileUploader {
    border: 2px dashed rgba(42,157,143,0.32) !important;
    border-radius: 12px !important; background: rgba(42,157,143,0.04) !important;
}
.stFileUploader:hover { border-color: rgba(42,157,143,0.6) !important; }
.stNumberInput input, .stTextInput input {
    background: #0f2335 !important; color: #bdd8e8 !important;
    border-color: rgba(42,157,143,0.28) !important; border-radius: 8px !important;
}
hr { border-color: rgba(42,157,143,0.14) !important; }
label { color: #6899aa !important; font-size: 0.82rem !important; }
.stDownloadButton > button {
    background: linear-gradient(135deg, #1a3a4a, #2a9d8f) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; box-shadow: 0 2px 14px rgba(42,157,143,0.3) !important;
}
</style>
"""

# ─── CHART CONSTANTS ─────────────────────────────────────────────────────────
PAL = ["#2a9d8f", "#e9c46a", "#e76f51", "#5e9bae", "#f4a261", "#a8dadc", "#457b9d", "#62b5aa"]
BG  = "rgba(10,22,40,0)"
GRD = "rgba(42,157,143,0.1)"
FC  = "#3e5e74"


# ─── SIMULATED DATA ───────────────────────────────────────────────────────────
def _seasonal_series(rng, base, school, dec, noise, n=24):
    """Generate 24 months of margin data with stationery-specific seasonality."""
    vals = []
    for i in range(n):
        m = i % 12  # 0=Jan … 11=Dec
        s = 0.0
        # Back-to-school Mexico: Jul–Aug peak, Sep tail
        if m == 6: s += school * 0.55
        if m == 7: s += school * 1.00
        if m == 8: s += school * 0.65
        # January: new school cycle & corporate budgets
        if m == 0: s += school * 0.40
        # December: year-end corporate & gifts
        if m == 11: s += dec
        # June: mid-year corporate refresh
        if m == 5: s += dec * 0.28
        vals.append(round(max(base + s + rng.normal(0, noise), 0.50), 4))
    return vals


def get_sample_data() -> pd.DataFrame:
    """Simulated monthly margin data (%) for a Mexico City stationery company."""
    rng = np.random.default_rng(42)
    months = pd.date_range("2024-01", periods=24, freq="MS").strftime("%Y-%m").tolist()
    cfg = [
        # name,                        base,  school, dec,   noise
        ("Cuadernos y Libretas",        2.15,  0.80,   0.22,  0.17),
        ("Material Escolar",            2.38,  1.15,   0.12,  0.21),
        ("Material de Oficina",         2.60,  0.08,   0.32,  0.13),
        ("Artículos de Arte",           2.82,  0.18,   0.72,  0.19),
        ("Servicio de Impresión",       3.15,  0.00,   0.94,  0.14),
        ("Papelería Personalizada",     3.45,  0.12,   1.25,  0.17),
    ]
    data: dict = {"Mes": months}
    for name, base, school, dec, noise in cfg:
        data[name] = _seasonal_series(rng, base, school, dec, noise)
    return pd.DataFrame(data)


def get_territorial_data() -> pd.DataFrame:
    """Simulated annual sales by Mexican state (Papelería MX national distribution)."""
    rows = [
        ("Ciudad de México",     4_850_000, 19.43,  -99.13,  "CDMX"),
        ("Estado de México",     2_950_000, 19.35,  -99.65,  "MEX"),
        ("Jalisco",              1_820_000, 20.66, -103.35,  "JAL"),
        ("Nuevo León",           1_640_000, 25.69, -100.32,  "NL"),
        ("Puebla",               1_230_000, 19.04,  -98.21,  "PUE"),
        ("Guanajuato",             980_000, 21.02, -101.26,  "GTO"),
        ("Querétaro",              870_000, 20.59, -100.39,  "QRO"),
        ("Veracruz",               750_000, 19.17,  -96.13,  "VER"),
        ("Baja California",        640_000, 30.84, -115.28,  "BC"),
        ("Sonora",                 520_000, 29.07, -110.96,  "SON"),
        ("Chihuahua",              490_000, 28.64, -106.09,  "CHIH"),
        ("Tamaulipas",             450_000, 24.27,  -98.84,  "TAMS"),
        ("Coahuila",               420_000, 27.07, -101.71,  "COAH"),
        ("Hidalgo",                380_000, 20.43,  -99.00,  "HGO"),
        ("Morelos",                310_000, 18.68,  -99.10,  "MOR"),
        ("San Luis Potosí",        290_000, 22.16, -100.99,  "SLP"),
        ("Aguascalientes",         270_000, 21.88, -102.29,  "AGS"),
        ("Michoacán",              250_000, 19.71, -101.19,  "MICH"),
        ("Sinaloa",                230_000, 24.80, -107.39,  "SIN"),
        ("Yucatán",                210_000, 20.97,  -89.59,  "YUC"),
        ("Tlaxcala",               180_000, 19.32,  -98.24,  "TLAX"),
        ("Guerrero",               160_000, 17.55,  -99.50,  "GRO"),
        ("Oaxaca",                 150_000, 17.07,  -96.72,  "OAX"),
        ("Nayarit",                130_000, 21.75, -104.85,  "NAY"),
        ("Colima",                 110_000, 19.24, -103.72,  "COL"),
        ("Durango",                100_000, 24.02, -104.66,  "DGO"),
        ("Tabasco",                 95_000, 17.99,  -92.93,  "TAB"),
        ("Chiapas",                 80_000, 16.75,  -93.11,  "CHIS"),
        ("Zacatecas",               75_000, 22.77, -102.58,  "ZAC"),
        ("Campeche",                60_000, 19.84,  -90.53,  "CAMP"),
        ("Quintana Roo",            55_000, 19.18,  -88.48,  "QROO"),
        ("Baja California Sur",     45_000, 26.04, -111.66,  "BCS"),
    ]
    df = pd.DataFrame(rows, columns=["Estado", "Ventas", "lat", "lon", "abbr"])
    df["Part_%"]     = (df["Ventas"] / df["Ventas"].sum() * 100).round(2)
    df["Ventas_fmt"] = df["Ventas"].apply(lambda x: f"${x:,.0f}")
    return df.sort_values("Ventas", ascending=False).reset_index(drop=True)


# ─── MARKOWITZ ENGINE ─────────────────────────────────────────────────────────
def run_markowitz(returns_df: pd.DataFrame, n_sims: int, budget: float,
                  w_min: float, w_max: float):
    n = returns_df.shape[1]
    # Guard: ensure feasible constraint region
    if w_min * n > 1.0:
        w_min = round(1.0 / n - 0.005, 3)
    if w_max < 1.0 / n:
        w_max = round(1.0 / n + 0.005, 3)

    mu  = returns_df.mean()
    cov = returns_df.cov()

    rets, risks, sharpes, wlist = [], [], [], []
    for _ in range(n_sims):
        w = np.random.dirichlet(np.ones(n))
        # Project onto [w_min, w_max] simplex (clip + renormalize)
        w = np.clip(w, w_min, w_max)
        w /= w.sum()
        r  = float(np.dot(w, mu))
        s  = float(np.sqrt(w @ cov.values @ w))
        sh = r / s if s > 0 else 0.0
        rets.append(r); risks.append(s); sharpes.append(sh); wlist.append(w)

    sim_df = pd.DataFrame({"Margen (%)": rets, "Riesgo": risks, "Sharpe": sharpes})
    best   = int(sim_df["Sharpe"].idxmax())
    bw     = wlist[best]

    allocation = pd.DataFrame({
        "Producto":          returns_df.columns.tolist(),
        "Peso Óptimo (%)":   (bw * 100).round(2),
        "Presupuesto (MXN)": (bw * budget).round(0),
        "Margen Esp. (%)":   (mu.values * 100).round(2),
        "Riesgo Indiv.":     np.sqrt(np.diag(cov.values)).round(4),
    })

    metrics = {
        "margen": sim_df.loc[best, "Margen (%)"],
        "riesgo": sim_df.loc[best, "Riesgo"],
        "sharpe": sim_df.loc[best, "Sharpe"],
    }
    return sim_df, allocation, metrics, cov, mu


# ─── CHART HELPERS ────────────────────────────────────────────────────────────
def _layout(**kw):
    return dict(
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(family="Inter", color=FC),
        margin=dict(l=10, r=10, t=48, b=10),
        **kw,
    )


def chart_frontier(sim_df, metrics):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=sim_df["Riesgo"], y=sim_df["Margen (%)"],
        mode="markers",
        marker=dict(
            color=sim_df["Sharpe"],
            colorscale=[[0,"#112233"],[0.5,"#2a9d8f"],[1,"#e9c46a"]],
            size=4, opacity=0.6,
            colorbar=dict(title="Sharpe", thickness=11, x=1.01,
                          tickfont=dict(color=FC, size=9)),
            showscale=True,
        ),
        name="Portafolios",
        hovertemplate="Riesgo: %{x:.4f}<br>Margen: %{y:.4f}<br>Sharpe: %{marker.color:.3f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[metrics["riesgo"]], y=[metrics["margen"]],
        mode="markers",
        marker=dict(symbol="star", size=20, color="#e9c46a",
                    line=dict(color="white", width=1.5)),
        name="★ Portafolio Óptimo",
        hovertemplate="ÓPTIMO<br>Riesgo: %{x:.4f}<br>Margen: %{y:.4f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Frontera Eficiente de Markowitz", font=dict(size=14, color="#bdd8e8")),
        xaxis=dict(title="Riesgo (σ)", gridcolor=GRD, color=FC, zeroline=False),
        yaxis=dict(title="Margen Esperado (%)", gridcolor=GRD, color=FC, zeroline=False),
        legend=dict(font=dict(color="#bdd8e8"), bgcolor="rgba(0,0,0,0)"),
        height=430, **_layout(),
    )
    return fig


def chart_pie(allocation):
    fig = go.Figure(go.Pie(
        labels=allocation["Producto"],
        values=allocation["Peso Óptimo (%)"],
        hole=0.54,
        textinfo="label+percent",
        textfont=dict(size=10),
        marker=dict(colors=PAL, line=dict(color="#0a1628", width=2)),
        hovertemplate="%{label}<br>Peso: %{value:.2f}%<br>$%{customdata:,.0f}<extra></extra>",
        customdata=allocation["Presupuesto (MXN)"],
    ))
    fig.add_annotation(text="Portafolio<br>Óptimo", x=0.5, y=0.5,
                       font=dict(size=12, color="#bdd8e8"), showarrow=False)
    fig.update_layout(
        title=dict(text="Asignación Óptima", font=dict(size=14, color="#bdd8e8")),
        legend=dict(font=dict(color="#bdd8e8", size=9), bgcolor="rgba(0,0,0,0)"),
        height=430, **_layout(),
    )
    return fig


def chart_correlation(cov):
    std  = np.sqrt(np.diag(cov.values))
    corr = cov.values / np.outer(std, std)
    lbl  = [c[:13] + "…" if len(c) > 13 else c for c in cov.columns]
    fig  = go.Figure(go.Heatmap(
        z=np.round(corr, 2), x=lbl, y=lbl,
        colorscale=[[0,"#0f2335"],[0.5,"rgba(42,157,143,0.35)"],[1,"#e9c46a"]],
        zmin=-1, zmax=1,
        text=np.round(corr, 2), texttemplate="%{text}",
        textfont=dict(size=11),
        hovertemplate="%{y} × %{x}: %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        title=dict(text="Matriz de Correlación", font=dict(size=14, color="#bdd8e8")),
        height=390, **_layout(),
    )
    return fig


def chart_risk_return(mu, cov):
    stds = np.sqrt(np.diag(cov.values))
    fig  = go.Figure()
    for i, (prod, ret) in enumerate(mu.items()):
        c = PAL[i % len(PAL)]
        lbl = prod[:11] + ("…" if len(prod) > 11 else "")
        fig.add_trace(go.Scatter(
            x=[stds[i]], y=[ret], mode="markers+text",
            text=[lbl], textposition="top center",
            textfont=dict(size=9.5, color=c),
            marker=dict(size=18, color=c, opacity=0.88, line=dict(color="white", width=1.5)),
            hovertemplate=f"<b>{prod}</b><br>Margen: {ret:.4f}%<br>Riesgo: {stds[i]:.4f}<extra></extra>",
            showlegend=False,
        ))
    fig.update_layout(
        title=dict(text="Perfil Riesgo-Margen por Producto", font=dict(size=14, color="#bdd8e8")),
        xaxis=dict(title="Riesgo (σ)", gridcolor=GRD, color=FC, zeroline=False),
        yaxis=dict(title="Margen Esperado (%)", gridcolor=GRD, color=FC, zeroline=False),
        height=390, **_layout(),
    )
    return fig


def chart_seasonality(returns_df):
    mn  = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    tmp = returns_df.copy()
    tmp["_m"] = [i % 12 for i in range(len(tmp))]
    avg = tmp.groupby("_m")[returns_df.columns].mean()
    avg.index = mn
    fig = go.Figure()
    for col, c in zip(returns_df.columns, PAL):
        fig.add_trace(go.Scatter(
            x=avg.index, y=avg[col], mode="lines+markers",
            name=col[:18] + ("…" if len(col) > 18 else ""),
            line=dict(color=c, width=2.5), marker=dict(size=7),
            hovertemplate=f"{col}<br>%{{x}}: %{{y:.3f}}%<extra></extra>",
        ))
    fig.update_layout(
        title=dict(text="Estacionalidad del Margen (Promedio Mensual)", font=dict(size=14, color="#bdd8e8")),
        xaxis=dict(title="Mes", gridcolor=GRD, color=FC),
        yaxis=dict(title="Margen Promedio (%)", gridcolor=GRD, color=FC),
        legend=dict(font=dict(color="#bdd8e8", size=9), bgcolor="rgba(0,0,0,0)"),
        hovermode="x unified",
        height=380, **_layout(),
    )
    return fig


def chart_map(terr_df):
    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lat=terr_df["lat"], lon=terr_df["lon"],
        text=terr_df["Estado"],
        customdata=np.stack([terr_df["Ventas_fmt"], terr_df["Part_%"].astype(str)], axis=-1),
        hovertemplate="<b>%{text}</b><br>Ventas: %{customdata[0]}<br>Part.: %{customdata[1]}%<extra></extra>",
        mode="markers",
        marker=dict(
            size=terr_df["Ventas"] / terr_df["Ventas"].max() * 50 + 6,
            color=terr_df["Ventas"],
            colorscale=[[0,"#0f2335"],[0.3,"#2a9d8f"],[1,"#e9c46a"]],
            opacity=0.85,
            colorbar=dict(title=dict(text="Ventas MXN", font=dict(size=10)),
                          thickness=11, x=1.0, tickfont=dict(color=FC, size=9)),
            line=dict(color="rgba(255,255,255,0.25)", width=1),
            showscale=True,
        ),
    ))
    fig.add_trace(go.Scattergeo(
        lat=terr_df["lat"], lon=terr_df["lon"],
        text=terr_df["abbr"], mode="text",
        textfont=dict(size=7.5, color="rgba(255,255,255,0.4)"),
        showlegend=False, hoverinfo="skip",
    ))
    fig.update_geos(
        scope="north america",
        center=dict(lat=23.6, lon=-102.5),
        projection_scale=4.8,
        lataxis_range=[14, 33], lonaxis_range=[-120, -85],
        showland=True,       landcolor="rgba(10,22,40,0.9)",
        showocean=True,      oceancolor="rgba(8,18,35,0.7)",
        showcoastlines=True, coastlinecolor="rgba(42,157,143,0.38)",
        showframe=False,     bgcolor="rgba(0,0,0,0)",
        showborder=True,     bordercolor="rgba(42,157,143,0.22)",
        showsubunits=True,   subunitcolor="rgba(42,157,143,0.15)",
    )
    fig.update_layout(
        title=dict(text="Mapa de Ventas Territoriales — México (32 estados)", font=dict(size=14, color="#bdd8e8")),
        geo=dict(bgcolor="rgba(0,0,0,0)"),
        height=500, **_layout(margin=dict(l=0, r=0, t=48, b=0)),
    )
    return fig


def chart_bar_territory(terr_df):
    top = terr_df.head(12).sort_values("Ventas")
    fig = go.Figure(go.Bar(
        x=top["Ventas"], y=top["Estado"],
        orientation="h",
        marker=dict(
            color=top["Ventas"],
            colorscale=[[0,"#0f2335"],[0.5,"#2a9d8f"],[1,"#e9c46a"]],
            line=dict(color="rgba(0,0,0,0)"),
        ),
        hovertemplate="%{y}: $%{x:,.0f}<extra></extra>",
        text=top["Ventas_fmt"], textposition="outside",
        textfont=dict(size=9.5, color=FC),
    ))
    fig.update_layout(
        title=dict(text="Top 12 Estados — Ventas Anuales", font=dict(size=14, color="#bdd8e8")),
        xaxis=dict(title="Ventas (MXN)", gridcolor=GRD, color=FC),
        yaxis=dict(color=FC),
        height=430, **_layout(),
    )
    return fig


# ─── SECTION HEADER ───────────────────────────────────────────────────────────
def sec(title: str, badge: str = ""):
    b = f'<div class="sec-hdr-badge">{badge}</div>' if badge else ""
    st.markdown(
        f'<div class="sec-hdr"><div class="sec-hdr-bar"></div>'
        f'<div class="sec-hdr-text">{title}</div>{b}</div>',
        unsafe_allow_html=True,
    )


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    st.markdown(CSS, unsafe_allow_html=True)

    # ── Sidebar toggle button (always visible, top-left) ──────────────────────
    tcol, _ = st.columns([1, 12])
    with tcol:
        lbl = "◀ Ocultar" if st.session_state.show_sidebar else "▶ Panel"
        if st.button(lbl, key="sb_toggle"):
            st.session_state.show_sidebar = not st.session_state.show_sidebar
            st.rerun()

    # Hide sidebar via CSS when collapsed
    if not st.session_state.show_sidebar:
        st.markdown(
            "<style>[data-testid='stSidebar']{display:none!important;}</style>",
            unsafe_allow_html=True,
        )

    # ── Sidebar content ───────────────────────────────────────────────────────
    if st.session_state.show_sidebar:
        with st.sidebar:
            st.markdown("""
            <div class="sb-logo">
                <div class="sb-logo-main">📎 Papelería MX</div>
                <div class="sb-logo-sub">Optimización de Portafolio</div>
            </div>""", unsafe_allow_html=True)

            st.markdown("#### ⚙️ Configuración")
            uploaded = st.file_uploader(
                "Cargar datos (.xlsx)",
                type=["xlsx"],
                help="Col 1 = Fechas · Siguientes = Márgenes mensuales (%) por producto",
            )

            st.divider()
            n_sims  = st.slider("Simulaciones Monte Carlo", 1_000, 50_000, 10_000, 1_000)
            budget  = st.number_input("Presupuesto Total (MXN)", 10_000, 10_000_000, 500_000, 10_000)

            st.divider()
            st.markdown("**Restricciones de Ponderación**")
            w_min = st.slider("Peso Mínimo / Producto", 0.00, 0.25, 0.05, 0.01, format="%.2f")
            w_max = st.slider("Peso Máximo / Producto", 0.15, 1.00, 0.60, 0.05, format="%.2f")

            st.divider()
            with st.expander("📖 Teoría de Markowitz"):
                st.markdown("""
                <div class="info-box">
                <b>Harry Markowitz (1952)</b> desarrolló la Teoría Moderna del Portafolio:
                diversificar entre activos con baja correlación reduce el riesgo sin
                sacrificar rendimiento.<br><br>
                <b>Frontera Eficiente:</b> portafolios que maximizan margen para cada
                nivel de riesgo dado.<br><br>
                <b>Índice de Sharpe = Margen / Riesgo</b><br>
                Mayor Sharpe → mejor relación riesgo-retorno.
                </div>""", unsafe_allow_html=True)

            with st.expander("🗺️ Cobertura Territorial"):
                st.markdown("""
                <div class="gold-box">
                Datos simulados de ventas anuales en los <b>32 estados</b> de México.
                Sede central en <b>CDMX</b>. Distribución nacional vía mayoristas
                y canales digitales.
                </div>""", unsafe_allow_html=True)

            st.markdown("---")
            st.markdown(
                "<small style='color:#2a4a5e'>Diplomado AI · Análisis Financiero<br>"
                "Módulo 9 · Optimización de Portafolio</small>",
                unsafe_allow_html=True,
            )
    else:
        # Fallback defaults when sidebar is hidden
        uploaded = None
        n_sims   = 10_000
        budget   = 500_000
        w_min    = 0.05
        w_max    = 0.60

    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="hero-block">
        <div class="hero-title">Optimización de Mezcla de Productos</div>
        <div class="hero-subtitle">
            Papelería MX · Sede CDMX · Distribución Nacional · Modelo Markowitz + Monte Carlo
        </div>
        <div class="hero-tags">
            <span class="hero-tag">📊 Markowitz</span>
            <span class="hero-tag">🎲 Monte Carlo</span>
            <span class="hero-tag">🗺️ 32 Estados</span>
            <span class="hero-tag">📎 6 Líneas de Producto</span>
            <span class="hero-tag">📅 24 Meses Históricos</span>
        </div>
    </div>""", unsafe_allow_html=True)

    # ── Load & validate data ──────────────────────────────────────────────────
    if uploaded is not None:
        df_raw = pd.read_excel(uploaded).dropna()
        src    = f"📂 {uploaded.name}"
    else:
        df_raw = get_sample_data()
        src    = "📊 Datos simulados — Papelería MX (CDMX)"

    returns_df = df_raw.iloc[:, 1:].apply(pd.to_numeric, errors="coerce").dropna()

    if returns_df.empty or returns_df.shape[1] < 2:
        st.error("El archivo cargado debe tener al menos 2 columnas de productos con datos numéricos.")
        return

    st.markdown(
        f'<div class="info-box">Fuente: <b>{src}</b> &nbsp;·&nbsp; '
        f'<b>{len(returns_df)}</b> períodos &nbsp;·&nbsp; '
        f'<b>{returns_df.shape[1]}</b> líneas de producto</div>',
        unsafe_allow_html=True,
    )

    # ── Run Markowitz optimization ────────────────────────────────────────────
    with st.spinner("Ejecutando optimización Monte Carlo…"):
        sim_df, allocation, metrics, cov, mu = run_markowitz(
            returns_df, n_sims, budget, w_min, w_max
        )

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    sec("Métricas del Portafolio Óptimo", "MARKOWITZ")
    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        ("📈", f"{metrics['margen']*100:.2f}%",  "Margen Esperado",   "Portafolio Óptimo", k1),
        ("⚖️", f"{metrics['riesgo']:.4f}",         "Riesgo (σ)",        "Mínimo Eficiente",  k2),
        ("⭐", f"{metrics['sharpe']:.3f}",          "Índice de Sharpe",  "Mayor Sharpe",      k3),
        ("💰", f"${budget:,.0f}",                   "Presupuesto (MXN)", "Asignación Óptima", k4),
    ]
    for icon, val, lbl, delta, col in kpis:
        with col:
            st.markdown(
                f'<div class="kpi-card">'
                f'<span class="kpi-icon">{icon}</span>'
                f'<div class="kpi-value">{val}</div>'
                f'<div class="kpi-label">{lbl}</div>'
                f'<div class="kpi-delta">{delta}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    # ── Frontier & Pie ────────────────────────────────────────────────────────
    sec("Frontera Eficiente & Asignación Óptima", "OPTIMIZACIÓN")
    c1, c2 = st.columns([3, 2])
    with c1:
        st.plotly_chart(chart_frontier(sim_df, metrics), use_container_width=True)
    with c2:
        st.plotly_chart(chart_pie(allocation), use_container_width=True)

    with st.expander("📋 Tabla de Asignación Óptima", expanded=True):
        disp = allocation.copy()
        disp["Peso Óptimo (%)"]   = disp["Peso Óptimo (%)"].map("{:.2f}%".format)
        disp["Presupuesto (MXN)"] = disp["Presupuesto (MXN)"].map("${:,.0f}".format)
        disp["Margen Esp. (%)"]   = disp["Margen Esp. (%)"].map("{:.2f}%".format)
        disp["Riesgo Indiv."]     = disp["Riesgo Indiv."].map("{:.4f}".format)
        st.dataframe(disp, use_container_width=True, hide_index=True)

    # ── Correlation & Risk-Return ─────────────────────────────────────────────
    sec("Análisis de Riesgo y Correlaciones", "DIAGNÓSTICO")
    c3, c4 = st.columns(2)
    with c3:
        st.plotly_chart(chart_correlation(cov), use_container_width=True)
    with c4:
        st.plotly_chart(chart_risk_return(mu, cov), use_container_width=True)

    # ── Seasonality ───────────────────────────────────────────────────────────
    sec("Estacionalidad de Márgenes", "TENDENCIAS")
    st.markdown(
        '<div class="gold-box">🗓️ Picos estacionales México: <b>Jul–Ago</b> (regreso a clases) · '
        '<b>Dic</b> (cierre corporativo) · <b>Ene</b> (presupuestos nuevos) · '
        '<b>Jun</b> (renovación corporativa mid-year)</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(chart_seasonality(returns_df), use_container_width=True)

    # ── Territorial map ───────────────────────────────────────────────────────
    sec("Cobertura Territorial Nacional", "GEOGRAFÍA")
    terr = get_territorial_data()
    cm1, cm2 = st.columns([3, 2])
    with cm1:
        st.plotly_chart(chart_map(terr), use_container_width=True)
    with cm2:
        st.plotly_chart(chart_bar_territory(terr), use_container_width=True)

    with st.expander("📊 Tabla Completa por Estado"):
        show_t = terr[["Estado", "Ventas_fmt", "Part_%"]].rename(
            columns={"Ventas_fmt": "Ventas Anuales", "Part_%": "Part. (%)"}
        )
        st.dataframe(show_t, use_container_width=True, hide_index=True)
        total    = terr["Ventas"].sum()
        top2_pct = terr[terr["Estado"].isin(
            ["Ciudad de México", "Estado de México"])]["Part_%"].sum()
        st.markdown(
            f'<div class="info-box">'
            f'<b>Total Nacional:</b> ${total:,.0f} MXN &nbsp;·&nbsp; '
            f'<b>CDMX + Edo. Méx.:</b> {top2_pct:.1f}% del total nacional</div>',
            unsafe_allow_html=True,
        )

    # ── Raw data + download ───────────────────────────────────────────────────
    with st.expander("📂 Datos Históricos de Márgenes"):
        st.dataframe(df_raw, use_container_width=True, hide_index=True)
        buf = io.BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as w:
            df_raw.to_excel(w, index=False, sheet_name="Márgenes Históricos")
            allocation.to_excel(w, index=False, sheet_name="Asignación Óptima")
            sim_df.head(5_000).to_excel(w, index=False, sheet_name="Simulaciones")
            terr[["Estado", "Ventas", "Part_%"]].to_excel(w, index=False, sheet_name="Territorial")
        st.download_button(
            "⬇️  Descargar Resultados Excel",
            data=buf.getvalue(),
            file_name="optimizacion_papeleria_mx.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


if __name__ == "__main__":
    main()
