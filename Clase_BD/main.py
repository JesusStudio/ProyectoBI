"""
=============================================================
  main.py  –  Punto de entrada de la carpeta Clase_BD
  Ejecuta: carga de datos → ETL → consultas analíticas
=============================================================
  Uso:
      python main.py
  (desde la carpeta que CONTIENE a Clase_BD, o bien
   cd Clase_BD && python main.py  si ajustas los imports)
=============================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Clase_BD.oltp_modelo   import Residuos_OLTP
from Clase_BD.datamart_modelo import Residuos_DW
from Clase_BD.datos_simulados   import cargar_datos
from Clase_BD.etl               import ejecutar_etl


def main():
    # ── 1. Crear BD OLTP en memoria ──────────────────────────────
    oltp = Residuos_OLTP()
    cargar_datos(oltp)
    oltp.resumen()
    print()

    # ── 2. Crear Data Mart en memoria ─────────────────────────────
    dw = Residuos_DW()
    ejecutar_etl(oltp, dw)
    print()
    dw.resumen()
    print()

    # ── 3. Consultas analíticas de ejemplo ────────────────────────
    print("=== Consultas sobre el Data Mart ===\n")

    print("▸ Toneladas recolectadas por zona:")
    for zona_id, total in dw.total_toneladas_por_zona().items():
        zona = dw.get_dim_zona(zona_id)
        nombre = f"{zona.distrito} – {zona.sector}" if zona else f"Zona {zona_id}"
        print(f"   Zona {zona_id:>2} ({nombre:<35}): {total:>8.2f} t")

    print("\n▸ Toneladas recolectadas por mes (2024):")
    meses = ["","Ene","Feb","Mar","Abr","May","Jun",
             "Jul","Ago","Sep","Oct","Nov","Dic"]
    for mes, total in dw.total_toneladas_por_mes().items():
        print(f"   {meses[mes]}: {total:>8.2f} t")

    print("\n▸ Quejas totales por tipo de residuo:")
    for tipo, total in dw.total_quejas_por_tipo_residuo().items():
        print(f"   {tipo:<20}: {total:>5} quejas")

    print("\n▸ Promedio de saturación (%) por zona:")
    for zona_id, prom in dw.promedio_saturacion_por_zona().items():
        print(f"   Zona {zona_id:>2}: {prom:>6.2f}%")


if __name__ == "__main__":
    main()
