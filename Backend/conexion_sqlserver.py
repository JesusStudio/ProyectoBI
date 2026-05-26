import pyodbc
import pandas as pd

def conectar():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost;"
        "DATABASE=DM_ResiduosLimaNorte;"
        "Trusted_Connection=yes;"
    )
    return conn

def leer_fact():
    conn = conectar()
    query = """
        SELECT f.toneladas_recolectadas,
            f.tiempo_recoleccion,
            f.nivel_saturacion,
            f.num_quejas,
            f.distancias_recorridas,
            z.distrito, t.residuo
        FROM Fact_Recoleccion f
        JOIN Dim_Zona z ON f.Id_zona = z.Id_zona
        JOIN Dim_Tipo_Residuo t ON f.Id_tipo_residuo = t.Id_tipo_residuo
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

if __name__ == "__main__":
    df = leer_fact()
    print(f"Datos cargados: {len(df)} filas")
    print(df.head())