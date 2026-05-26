"""
=============================================================
  ETL – Residuos_OLTP  →  Residuos_DW
  Proceso Extract – Transform – Load en Python puro
  Equivalente a: 03_etl_cursores.sql
=============================================================
"""

from datetime import date
from typing import TYPE_CHECKING

from .oltp_modelo import Residuos_OLTP   # type: ignore
from .datamart_modelo import (            # type: ignore
    Residuos_DW,
    Dim_Zona, Dim_Tiempo, Dim_Camion,
    Dim_Contenedor, Dim_Tipo_Residuo,
    Fact_Recoleccion,
)


# ── Utilidad de fecha ─────────────────────────────────────────────

def fecha_a_id(f: date) -> int:
    """Convierte date → int yyyyMMdd  (igual que FORMAT(fecha,'yyyyMMdd'))."""
    return int(f.strftime("%Y%m%d"))


# ── ETL principal ─────────────────────────────────────────────────

def ejecutar_etl(oltp: Residuos_OLTP, dw: Residuos_DW) -> None:
    """
    Carga todas las dimensiones y la tabla de hechos
    desde la BD OLTP hacia el Data Mart (DW).
    """

    print("── ETL iniciado ──────────────────────────────────")

    # ── 1. Dim_Zona ──────────────────────────────────────────────
    for z in oltp.zona:
        dw.dim_zona.append(Dim_Zona(z.Id_zona, z.distrito, z.sector))
    print(f"  [OK] Dim_Zona        → {len(dw.dim_zona)} filas")

    # ── 2. Dim_Tiempo (fechas distintas de Recoleccion) ──────────
    fechas_unicas = {r.fecha for r in oltp.recoleccion}
    for f in sorted(fechas_unicas):
        dw.dim_tiempo.append(
            Dim_Tiempo(
                Id_tiempo = fecha_a_id(f),
                fecha     = f,
                dia       = f.day,
                mes       = f.month,
                anio      = f.year,
            )
        )
    print(f"  [OK] Dim_Tiempo      → {len(dw.dim_tiempo)} filas")

    # ── 3. Dim_Camion ─────────────────────────────────────────────
    for c in oltp.camion:
        dw.dim_camion.append(Dim_Camion(c.Id_camion, c.placa, c.capacidad))
    print(f"  [OK] Dim_Camion      → {len(dw.dim_camion)} filas")

    # ── 4. Dim_Contenedor ────────────────────────────────────────
    for c in oltp.contenedor:
        dw.dim_contenedor.append(
            Dim_Contenedor(c.Id_contenedor, c.ubicacion, c.capacidad)
        )
    print(f"  [OK] Dim_Contenedor  → {len(dw.dim_contenedor)} filas")

    # ── 5. Dim_Tipo_Residuo ──────────────────────────────────────
    for t in oltp.tipo_residuo:
        dw.dim_tipo_residuo.append(
            Dim_Tipo_Residuo(t.Id_tipo_residuo, t.residuo)
        )
    print(f"  [OK] Dim_Tipo_Residuo→ {len(dw.dim_tipo_residuo)} filas")

    # ── 6. Fact_Recoleccion ──────────────────────────────────────
    for r in oltp.recoleccion:
        dw.fact_recoleccion.append(
            Fact_Recoleccion(
                Id_zona               = r.Id_zona,
                Id_tiempo             = fecha_a_id(r.fecha),
                Id_camion             = r.Id_camion,
                Id_contenedor         = r.Id_contenedor,
                Id_tipo_residuo       = r.Id_tipo_residuo,
                toneladas_recolectadas= r.toneladas,
                tiempo_recoleccion    = r.tiempo_min,
                nivel_saturacion      = r.nivel_sat,
                num_quejas            = r.num_quejas,
                distancias_recorridas = r.distancia_km,
            )
        )
    print(f"  [OK] Fact_Recoleccion→ {len(dw.fact_recoleccion)} filas")
    print("── ETL completado ────────────────────────────────")
