"""
=============================================================
  BD OLTP – Residuos_OLTP
  Modelos de tablas como clases Python (dataclasses)
  Equivalente a: 01_crear_bd_oltp.sql
=============================================================
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class Zona:
    Id_zona:  int
    distrito: str
    sector:   str

    def __repr__(self):
        return f"Zona({self.Id_zona}: {self.distrito} – {self.sector})"


@dataclass
class Camion:
    Id_camion: int
    placa:     str
    capacidad: float   # toneladas

    def __repr__(self):
        return f"Camion({self.Id_camion}: {self.placa}, cap={self.capacidad}t)"


@dataclass
class Contenedor:
    Id_contenedor: int
    ubicacion:     str
    capacidad:     float
    Id_zona:       int

    def __repr__(self):
        return f"Contenedor({self.Id_contenedor}: {self.ubicacion[:30]}...)"


@dataclass
class TipoResiduo:
    Id_tipo_residuo: int
    residuo:         str

    def __repr__(self):
        return f"TipoResiduo({self.Id_tipo_residuo}: {self.residuo})"


@dataclass
class Recoleccion:
    Id_recoleccion:  int
    Id_zona:         int
    Id_camion:       int
    Id_contenedor:   int
    Id_tipo_residuo: int
    fecha:           date
    toneladas:       float
    tiempo_min:      float
    nivel_sat:       float
    num_quejas:      int
    distancia_km:    float

    def __repr__(self):
        return (f"Recoleccion({self.Id_recoleccion}: zona={self.Id_zona}, "
                f"fecha={self.fecha}, {self.toneladas}t)")


# ── "Base de datos" en memoria (listas que actúan como tablas) ──
class Residuos_OLTP:
    """
    Simula la base de datos OLTP completa en memoria.
    Cada atributo es la 'tabla' (lista de objetos).
    """

    def __init__(self):
        self.zona:        list[Zona]        = []
        self.camion:      list[Camion]      = []
        self.contenedor:  list[Contenedor]  = []
        self.tipo_residuo:list[TipoResiduo] = []
        self.recoleccion: list[Recoleccion] = []
        self._next_ids = {
            "zona": 1, "camion": 1,
            "contenedor": 1, "tipo_residuo": 1, "recoleccion": 1
        }

    # ── helpers IDENTITY ──────────────────────────────────────────
    def _next(self, tabla: str) -> int:
        val = self._next_ids[tabla]
        self._next_ids[tabla] += 1
        return val

    # ── INSERT helpers ────────────────────────────────────────────
    def insert_zona(self, distrito: str, sector: str) -> Zona:
        z = Zona(self._next("zona"), distrito, sector)
        self.zona.append(z)
        return z

    def insert_camion(self, placa: str, capacidad: float) -> Camion:
        c = Camion(self._next("camion"), placa, capacidad)
        self.camion.append(c)
        return c

    def insert_contenedor(self, ubicacion: str, capacidad: float,
                          Id_zona: int) -> Contenedor:
        c = Contenedor(self._next("contenedor"), ubicacion, capacidad, Id_zona)
        self.contenedor.append(c)
        return c

    def insert_tipo_residuo(self, residuo: str) -> TipoResiduo:
        t = TipoResiduo(self._next("tipo_residuo"), residuo)
        self.tipo_residuo.append(t)
        return t

    def insert_recoleccion(self, Id_zona, Id_camion, Id_contenedor,
                           Id_tipo_residuo, fecha, toneladas,
                           tiempo_min, nivel_sat, num_quejas,
                           distancia_km) -> Recoleccion:
        r = Recoleccion(
            self._next("recoleccion"),
            Id_zona, Id_camion, Id_contenedor, Id_tipo_residuo,
            fecha, toneladas, tiempo_min, nivel_sat, num_quejas, distancia_km
        )
        self.recoleccion.append(r)
        return r

    # ── SELECT helpers ────────────────────────────────────────────
    def get_zona(self, Id_zona: int) -> Optional[Zona]:
        return next((z for z in self.zona if z.Id_zona == Id_zona), None)

    def get_camion(self, Id_camion: int) -> Optional[Camion]:
        return next((c for c in self.camion if c.Id_camion == Id_camion), None)

    def resumen(self):
        print("=== Residuos_OLTP – Resumen de tablas ===")
        print(f"  Zona        : {len(self.zona):>5} registros")
        print(f"  Camion      : {len(self.camion):>5} registros")
        print(f"  Contenedor  : {len(self.contenedor):>5} registros")
        print(f"  TipoResiduo : {len(self.tipo_residuo):>5} registros")
        print(f"  Recoleccion : {len(self.recoleccion):>5} registros")
