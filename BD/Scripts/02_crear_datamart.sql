CREATE DATABASE Residuos_DW;
GO
USE Residuos_DW;
GO

CREATE TABLE Dim_Zona (
  Id_zona   INT PRIMARY KEY,
  distrito  VARCHAR(100),
  sector    VARCHAR(50)
);
CREATE TABLE Dim_Tiempo (
  Id_tiempo INT PRIMARY KEY,
  fecha     DATE,
  dia       INT, mes INT, año INT
);
CREATE TABLE Dim_Camion (
  Id_camion INT PRIMARY KEY,
  placa     VARCHAR(20),
  capacidad DECIMAL(5,2)
);
CREATE TABLE Dim_Contenedor (
  Id_contenedor INT PRIMARY KEY,
  ubicacion     VARCHAR(200),
  capacidad     DECIMAL(5,2)
);
CREATE TABLE Dim_Tipo_Residuo (
  Id_tipo_residuo INT PRIMARY KEY,
  residuo         VARCHAR(80)
);

CREATE TABLE Fact_Recoleccion (
  Id_zona           INT REFERENCES Dim_Zona(Id_zona),
  Id_tiempo         INT REFERENCES Dim_Tiempo(Id_tiempo),
  Id_camion         INT REFERENCES Dim_Camion(Id_camion),
  Id_contenedor     INT REFERENCES Dim_Contenedor(Id_contenedor),
  Id_tipo_residuo   INT REFERENCES Dim_Tipo_Residuo(Id_tipo_residuo),
  toneladas_recolectadas DECIMAL(6,2),
  tiempo_recoleccion     DECIMAL(6,1),
  nivel_saturacion       DECIMAL(5,1),
  num_quejas             INT,
  distancias_recorridas  DECIMAL(6,1)
);