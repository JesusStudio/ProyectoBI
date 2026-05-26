USE Residuos_DW;
GO

INSERT INTO Dim_Zona
SELECT Id_zona, distrito, sector
FROM Residuos_OLTP.dbo.Zona;

INSERT INTO Dim_Tiempo
SELECT CONVERT(INT, FORMAT(fecha,'yyyyMMdd')),
       fecha,
       DAY(fecha), MONTH(fecha), YEAR(fecha)
FROM (SELECT DISTINCT fecha FROM Residuos_OLTP.dbo.Recoleccion) f;

INSERT INTO Dim_Camion
SELECT Id_camion, placa, capacidad
FROM Residuos_OLTP.dbo.Camion;

INSERT INTO Dim_Contenedor
SELECT Id_contenedor, ubicacion, capacidad
FROM Residuos_OLTP.dbo.Contenedor;

INSERT INTO Dim_Tipo_Residuo
SELECT Id_tipo_residuo, residuo
FROM Residuos_OLTP.dbo.TipoResiduo;

INSERT INTO Fact_Recoleccion
SELECT r.Id_zona,
  CONVERT(INT, FORMAT(r.fecha,'yyyyMMdd')),
  r.Id_camion, r.Id_contenedor, r.Id_tipo_residuo,
  r.toneladas, r.tiempo_min,
  r.nivel_sat, r.num_quejas, r.distancia_km
FROM Residuos_OLTP.dbo.Recoleccion r;