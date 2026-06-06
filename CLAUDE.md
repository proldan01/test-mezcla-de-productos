# CLAUDE.md — Papelería MX: Optimización de Mezcla de Productos

## Contexto del Proyecto

Aplicación Streamlit para el **Módulo 9 del Diplomado de AI en Análisis Financiero**.
Aplica la Teoría de Markowitz para optimizar el portafolio de productos de una empresa
de papelería con sede en Ciudad de México y distribución nacional.

## Estructura del Proyecto

```
pablo/
├── app.py                        # App principal Streamlit
├── mezcla_productos_ejemplo.xlsx # Datos simulados (2 hojas)
├── generate_excel.py             # Script para regenerar el Excel
├── requirements.txt              # Dependencias Python
├── CLAUDE.md                     # Este archivo
├── README.md                     # Documentación pública
└── .gitignore
```

## Líneas de Producto Simuladas

| Producto                  | Margen Base | Pico Estacional          |
|---------------------------|-------------|--------------------------|
| Cuadernos y Libretas      | 2.15%       | Jul–Ago (regreso clases) |
| Material Escolar          | 2.38%       | Jul–Ago (regreso clases) |
| Material de Oficina       | 2.60%       | Ene, Dic (corporativo)   |
| Artículos de Arte         | 2.82%       | Dic (regalos)            |
| Servicio de Impresión     | 3.15%       | Dic, Jun (corporativo)   |
| Papelería Personalizada   | 3.45%       | Dic, Jun (corporativo)   |

## Datos de Prueba

- `generate_excel.py` genera `mezcla_productos_ejemplo.xlsx` con:
  - **Hoja 1 — Márgenes Mensuales:** 24 meses (2024-01 a 2025-12), 6 productos
  - **Hoja 2 — Ventas Territorial:** 32 estados de México con ventas anuales simuladas

Regenerar: `python generate_excel.py`

## Arquitectura de la App

### Funciones principales en `app.py`

| Función               | Rol                                                    |
|-----------------------|--------------------------------------------------------|
| `get_sample_data()`   | Genera datos simulados (seed=42, reproducible)         |
| `get_territorial_data()` | Datos de ventas por estado (32 estados México)      |
| `run_markowitz()`     | Monte Carlo + optimización Markowitz                   |
| `chart_frontier()`    | Frontera eficiente (scatter Sharpe-coloreado)          |
| `chart_pie()`         | Donut de asignación óptima                             |
| `chart_correlation()` | Heatmap correlaciones (covarianza normalizada)         |
| `chart_risk_return()` | Scatter riesgo-retorno individual por producto         |
| `chart_seasonality()` | Líneas de estacionalidad mensual promedio              |
| `chart_map()`         | Bubble map geográfico México (Scattergeo)              |
| `chart_bar_territory()` | Barras horizontales top-12 estados                  |

### Panel Lateral (Sidebar)

El panel es dinámico con botón **◀ Ocultar / ▶ Panel** implementado con:
- `st.session_state.show_sidebar` (booleano)
- CSS `display:none` cuando está colapsado
- `st.rerun()` para re-renderizado inmediato

## Stack Tecnológico

- **Streamlit** ≥1.28 — framework web
- **Plotly** ≥5.17 — visualizaciones interactivas (incluye Scattergeo)
- **Pandas** ≥2.0 + **NumPy** ≥1.24 — análisis de datos
- **openpyxl** ≥3.1 — lectura/escritura Excel

## Diseño UI

Tema oscuro inspirado en Uiverse.io:
- Background: `#0a1628`
- Accent teal: `#2a9d8f`
- Accent gold: `#e9c46a`
- Font: Inter (Google Fonts)
- Efectos: glassmorphism, gradient-top-border en cards, glow hover

## Despliegue en Streamlit Cloud

1. Subir repo a GitHub (incluir todos los archivos excepto `.gitignore` targets)
2. Conectar en [share.streamlit.io](https://share.streamlit.io)
3. Configurar: `Main file = app.py`, Python 3.10+
4. El archivo Excel de ejemplo se carga automáticamente vía `get_sample_data()`
   (no requiere archivo externo para funcionar)

## Notas de Desarrollo

- La semilla `np.random.default_rng(42)` garantiza datos reproducibles
- `run_markowitz()` valida automáticamente las restricciones `w_min * n ≤ 1`
- El mapa territorial usa `go.Scattergeo` con `scope="north america"` — no requiere GeoJSON
- El Excel tiene 2 hojas; la app solo lee la primera (`iloc[:,1:]`)
