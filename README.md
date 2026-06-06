# Papelería MX — Optimización de Mezcla de Productos

Dashboard ejecutivo que aplica la **Teoría de Markowitz** para determinar la combinación
óptima de productos de papelería que maximiza el margen con el menor riesgo operativo.

## Demo

Desarrollado para el **Módulo 9 — Diplomado de AI en Análisis Financiero**.

## Funcionalidades

- **Modelo Markowitz + Monte Carlo** — frontera eficiente e índice Sharpe
- **Panel dinámico** — botón ocultar/mostrar sidebar
- **6 líneas de producto** simuladas (papelería CDMX)
- **Mapa territorial** — burbujas de ventas en los 32 estados de México
- **Estacionalidad** — picos regreso a clases y corporativos
- **Carga de Excel propio** — o usa datos simulados incluidos
- **Exportación** — descarga resultados en Excel multi-hoja

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run app.py
```

## Datos de ejemplo

El archivo `mezcla_productos_ejemplo.xlsx` contiene:

| Hoja                  | Contenido                                     |
|-----------------------|-----------------------------------------------|
| Márgenes Mensuales    | 24 meses (2024-2025) × 6 productos            |
| Ventas Territorial    | Ventas anuales simuladas por estado (32 est.) |

Para regenerar los datos simulados:

```bash
python generate_excel.py
```

## Formato Excel personalizado

| Columna | Contenido                               |
|---------|-----------------------------------------|
| Col 1   | Fecha (YYYY-MM)                         |
| Col 2+  | Margen mensual (%) por cada producto    |

## Productos simulados

| Línea                   | Margen Base | Temporada alta       |
|-------------------------|-------------|----------------------|
| Cuadernos y Libretas    | ~2.1%       | Jul–Ago (escolar)    |
| Material Escolar        | ~2.4%       | Jul–Ago (escolar)    |
| Material de Oficina     | ~2.6%       | Ene, Dic             |
| Artículos de Arte       | ~2.8%       | Dic                  |
| Servicio de Impresión   | ~3.2%       | Dic, Jun             |
| Papelería Personalizada | ~3.5%       | Dic, Jun             |

## Despliegue en Streamlit Cloud

1. Sube el repositorio a GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io) → New app
3. Selecciona el repo, branch `main`, archivo `app.py`
4. La app carga datos simulados automáticamente (sin necesidad de subir Excel)

## Tecnologías

`Streamlit` · `Plotly` · `Pandas` · `NumPy` · `openpyxl`
