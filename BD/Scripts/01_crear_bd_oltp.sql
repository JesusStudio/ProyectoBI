CREATE DATABASE Residuos_OLTP;
GO
USE Residuos_OLTP;
GO

CREATE TABLE Zona (
  Id_zona     INT PRIMARY KEY IDENTITY,
  distrito    VARCHAR(100),
  sector      VARCHAR(50)
);

CREATE TABLE Camion (
  Id_camion   INT PRIMARY KEY IDENTITY,
  placa       VARCHAR(20),
  capacidad   DECIMAL(5,2)
);

CREATE TABLE Contenedor (
  Id_contenedor INT PRIMARY KEY IDENTITY,
  ubicacion     VARCHAR(200),
  capacidad     DECIMAL(5,2),
  Id_zona       INT REFERENCES Zona(Id_zona)
);

CREATE TABLE TipoResiduo (
  Id_tipo_residuo INT PRIMARY KEY IDENTITY,
  residuo         VARCHAR(80)
);

CREATE TABLE Recoleccion (
  Id_recoleccion  INT PRIMARY KEY IDENTITY,
  Id_zona         INT REFERENCES Zona(Id_zona),
  Id_camion       INT REFERENCES Camion(Id_camion),
  Id_contenedor   INT REFERENCES Contenedor(Id_contenedor),
  Id_tipo_residuo INT REFERENCES TipoResiduo(Id_tipo_residuo),
  fecha           DATE,
  toneladas       DECIMAL(6,2),
  tiempo_min      DECIMAL(6,1),
  nivel_sat       DECIMAL(5,1),
  num_quejas      INT,
  distancia_km    DECIMAL(6,1)
);