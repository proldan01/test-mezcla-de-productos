"""
Genera el archivo mezcla_productos_ejemplo.xlsx con datos simulados
de una empresa de papelería en CDMX con distribución nacional.
Ejecutar una sola vez: python generate_excel.py
"""

import numpy as np
import pandas as pd
from pathlib import Path

OUTPUT = Path(__file__).parent / "mezcla_productos_ejemplo.xlsx"


def _seasonal_series(rng, base, school, dec, noise, n=24):
    vals = []
    for i in range(n):
        m = i % 12
        s = 0.0
        if m == 6: s += school * 0.55
        if m == 7: s += school * 1.00
        if m == 8: s += school * 0.65
        if m == 0: s += school * 0.40
        if m == 11: s += dec
        if m == 5: s += dec * 0.28
        vals.append(round(max(base + s + rng.normal(0, noise), 0.50), 4))
    return vals


def build_margins() -> pd.DataFrame:
    rng    = np.random.default_rng(42)
    months = pd.date_range("2024-01", periods=24, freq="MS").strftime("%Y-%m").tolist()
    cfg = [
        ("Cuadernos y Libretas",    2.15, 0.80, 0.22, 0.17),
        ("Material Escolar",        2.38, 1.15, 0.12, 0.21),
        ("Material de Oficina",     2.60, 0.08, 0.32, 0.13),
        ("Artículos de Arte",       2.82, 0.18, 0.72, 0.19),
        ("Servicio de Impresión",   3.15, 0.00, 0.94, 0.14),
        ("Papelería Personalizada", 3.45, 0.12, 1.25, 0.17),
    ]
    data: dict = {"Mes": months}
    for name, base, school, dec, noise in cfg:
        data[name] = _seasonal_series(rng, base, school, dec, noise)
    return pd.DataFrame(data)


def build_territorial() -> pd.DataFrame:
    rows = [
        ("Ciudad de México",    4_850_000),
        ("Estado de México",    2_950_000),
        ("Jalisco",             1_820_000),
        ("Nuevo León",          1_640_000),
        ("Puebla",              1_230_000),
        ("Guanajuato",            980_000),
        ("Querétaro",             870_000),
        ("Veracruz",              750_000),
        ("Baja California",       640_000),
        ("Sonora",                520_000),
        ("Chihuahua",             490_000),
        ("Tamaulipas",            450_000),
        ("Coahuila",              420_000),
        ("Hidalgo",               380_000),
        ("Morelos",               310_000),
        ("San Luis Potosí",       290_000),
        ("Aguascalientes",        270_000),
        ("Michoacán",             250_000),
        ("Sinaloa",               230_000),
        ("Yucatán",               210_000),
        ("Tlaxcala",              180_000),
        ("Guerrero",              160_000),
        ("Oaxaca",                150_000),
        ("Nayarit",               130_000),
        ("Colima",                110_000),
        ("Durango",               100_000),
        ("Tabasco",                95_000),
        ("Chiapas",                80_000),
        ("Zacatecas",              75_000),
        ("Campeche",               60_000),
        ("Quintana Roo",           55_000),
        ("Baja California Sur",    45_000),
    ]
    df = pd.DataFrame(rows, columns=["Estado", "Ventas_Anuales_MXN"])
    df["Participación_%"] = (df["Ventas_Anuales_MXN"] / df["Ventas_Anuales_MXN"].sum() * 100).round(2)
    return df


def main():
    margins    = build_margins()
    territorial = build_territorial()

    with pd.ExcelWriter(OUTPUT, engine="openpyxl") as writer:
        margins.to_excel(writer, index=False, sheet_name="Márgenes Mensuales")
        territorial.to_excel(writer, index=False, sheet_name="Ventas Territorial")

    print(f"OK  Archivo generado: {OUTPUT}")
    print(f"    Hoja 1 - Margenes Mensuales : {margins.shape[0]} filas x {margins.shape[1]} cols")
    print(f"    Hoja 2 - Ventas Territorial : {territorial.shape[0]} estados")


if __name__ == "__main__":
    main()
