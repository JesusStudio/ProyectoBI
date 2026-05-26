"""
=============================================================
  Data Mart – Residuos_DW
  Dimensiones y tabla de hechos como clases Python
  Equivalente a: 02_crear_datamart.sql
=============================================================
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


# ── DIMENSIONES ───────────────────────────────────────────────────

@dataclass
class Dim_Zona:
    Id_zona:  int
    distrito: str
    sector:   str


@dataclass
class Dim_Tiempo:
    Id_tiempo: int   # clave surrogate: yyyyMMdd  (ej. 20240102)
    fecha:     date
    dia:       int
    mes:       int
    anio:      int


@dataclass
class Dim_Camion:
    Id_camion: int
    placa:     str
    capacidad: float


@dataclass
class Dim_Contenedor:
    Id_contenedor: int
    ubicacion:     str
    capacidad:     float


@dataclass
class Dim_Tipo_Residuo:
    Id_tipo_residuo: int
    residuo:         str


# ── TABLA DE HECHOS ───────────────────────────────────────────────

@dataclass
class Fact_Recoleccion:
    Id_zona:               int
    Id_tiempo:             int
    Id_camion:             int
    Id_contenedor:         int
    Id_tipo_residuo:       int
    toneladas_recolectadas: float
    tiempo_recoleccion:    float
    nivel_saturacion:      float
    num_quejas:            int
    distancias_recorridas: float

    def __repr__(self):
        return (f"Fact(zona={self.Id_zona}, t={self.Id_tiempo}, "
                f"{self.toneladas_recolectadas}t, sat={self.nivel_saturacion}%)")


# ── Data Mart en memoria ──────────────────────────────────────────

class Residuos_DW:
    """
    Simula el Data Warehouse (Data Mart estrella) en memoria.
    """

    def __init__(self):
        self.dim_zona:        list[Dim_Zona]        = []
        self.dim_tiempo:      list[Dim_Tiempo]       = []
        self.dim_camion:      list[Dim_Camion]       = []
        self.dim_contenedor:  list[Dim_Contenedor]   = []
        self.dim_tipo_residuo:list[Dim_Tipo_Residuo] = []
        self.fact_recoleccion:list[Fact_Recoleccion] = []

    # ── Lookup helpers ────────────────────────────────────────────
    def get_dim_zona(self, Id_zona: int) -> Optional[Dim_Zona]:
        return next((z for z in self.dim_zona if z.Id_zona == Id_zona), None)

    def get_dim_tiempo(self, Id_tiempo: int) -> Optional[Dim_Tiempo]:
        return next((t for t in self.dim_tiempo if t.Id_tiempo == Id_tiempo), None)

    def get_dim_camion(self, Id_camion: int) -> Optional[Dim_Camion]:
        return next((c for c in self.dim_camion if c.Id_camion == Id_camion), None)

    def get_dim_tipo(self, Id_tipo_residuo: int) -> Optional[Dim_Tipo_Residuo]:
        return next((t for t in self.dim_tipo_residuo
                     if t.Id_tipo_residuo == Id_tipo_residuo), None)

    # ── Consultas analíticas ──────────────────────────────────────
    def total_toneladas_por_zona(self) -> dict:
        """Agrupa toneladas recolectadas por Id_zona."""
        resultado = {}
        for f in self.fact_recoleccion:
            resultado[f.Id_zona] = resultado.get(f.Id_zona, 0) + f.toneladas_recolectadas
        return dict(sorted(resultado.items()))

    def total_toneladas_por_mes(self) -> dict:
        """Agrupa toneladas recolectadas por mes (usa Dim_Tiempo)."""
        resultado = {}
        tiempo_map = {t.Id_tiempo: t.mes for t in self.dim_tiempo}
        for f in self.fact_recoleccion:
            mes = tiempo_map.get(f.Id_tiempo, 0)
            resultado[mes] = resultado.get(mes, 0) + f.toneladas_recolectadas
        return dict(sorted(resultado.items()))

    def total_quejas_por_tipo_residuo(self) -> dict:
        """Suma de quejas agrupadas por tipo de residuo."""
        resultado = {}
        tipo_map = {t.Id_tipo_residuo: t.residuo for t in self.dim_tipo_residuo}
        for f in self.fact_recoleccion:
            nombre = tipo_map.get(f.Id_tipo_residuo, f"Tipo {f.Id_tipo_residuo}")
            resultado[nombre] = resultado.get(nombre, 0) + f.num_quejas
        return dict(sorted(resultado.items(), key=lambda x: -x[1]))

    def promedio_saturacion_por_zona(self) -> dict:
        """Promedio de nivel de saturación por zona."""
        suma = {}; cnt = {}
        for f in self.fact_recoleccion:
            suma[f.Id_zona] = suma.get(f.Id_zona, 0) + f.nivel_saturacion
            cnt[f.Id_zona]  = cnt.get(f.Id_zona, 0) + 1
        return {z: round(suma[z] / cnt[z], 2) for z in sorted(suma)}

    def resumen(self):
        print("=== Residuos_DW – Resumen del Data Mart ===")
        print(f"  Dim_Zona        : {len(self.dim_zona):>5} registros")
        print(f"  Dim_Tiempo      : {len(self.dim_tiempo):>5} registros")
        print(f"  Dim_Camion      : {len(self.dim_camion):>5} registros")
        print(f"  Dim_Contenedor  : {len(self.dim_contenedor):>5} registros")
        print(f"  Dim_Tipo_Residuo: {len(self.dim_tipo_residuo):>5} registros")
        print(f"  Fact_Recoleccion: {len(self.fact_recoleccion):>5} registros")
