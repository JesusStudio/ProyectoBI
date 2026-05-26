♻️ EcoBI – Plataforma de Gestión de Residuos Sólidos

Sistema de analítica y visualización de datos para la gestión de residuos sólidos urbanos, desarrollado con procesos ETL, modelado dimensional, base de datos SQL Server, scripts de predicción en Python y dashboard interactivo en Power BI.

📌 Descripción del Proyecto

EcoBI es una solución de Business Intelligence enfocada en el monitoreo y análisis de residuos sólidos.

El proyecto integra:

📂 Base de datos relacional en SQL Server
🔄 Procesos ETL
🏛️ Modelo dimensional tipo Data Warehouse
📊 Dashboard ejecutivo en Power BI
🤖 Modelos predictivos en Python

Archivo:

BD_Scripts/01_crear_bd_oltp.sql

Contiene:

Creación de tablas transaccionales
Relaciones entre entidades
Estructura operacional del sistema
2️⃣ DataMart

Archivo:

BD_Scripts/02_crear_datamart.sql

Incluye:

Modelo estrella
Tablas de hechos
Dimensiones
Optimización para análisis BI
3️⃣ Procesos ETL

Archivo:

BD_Scripts/03_etl_cursores.sql

Funciones:

Extracción de datos
Transformación
Limpieza
Carga al DataMart
4️⃣ Datos Simulados

Archivo:

BD_Scripts/04_insert_datos_simulados.sql

Genera:

Datos de prueba
Registros operativos
Información histórica simulada
🧠 Scripts Python
📌 Predicción de Toneladas

Archivo:

PYTHON/prediccion_toneladas.py

Realiza:

Análisis histórico
Predicción de toneladas recolectadas
Visualización de tendencias
📌 Predicción de Saturación

Archivo:

PYTHON/prediccion_saturacion.py

Permite:

Analizar niveles de saturación
Identificar posibles desbordes
Generar predicciones futuras
📌 Predicción de Quejas

Archivo:

PYTHON/prediccion_quejas.py

Incluye:

Predicción de incidencias
Detección de aumento de reclamos
Comportamiento temporal
📊 Dashboard Power BI

Archivo principal:

Frontend/Proyecto.pbix

Características:

KPIs ejecutivos
Predicciones visuales
Indicadores de residuos
Saturación promedio
Distancia promedio
Quejas registradas
Análisis por distrito
Tendencias temporales
🖼️ Vista del Dashboard

⚙️ Instalación y Configuración
1️⃣ Clonar el repositorio
git clone https://github.com/tuusuario/ecobi.git
cd ecobi
2️⃣ Configurar SQL Server

Ejecutar los scripts en este orden:

1. 01_crear_bd_oltp.sql
2. 04_insert_datos_simulados.sql
3. 02_crear_datamart.sql
4. 03_etl_cursores.sql
3️⃣ Crear entorno virtual
python -m venv venv

Activar entorno:

Windows
venv\Scripts\activate
Linux / Mac
source venv/bin/activate
4️⃣ Instalar dependencias
pip install pandas numpy matplotlib seaborn scikit-learn pyodbc
5️⃣ Configurar conexión SQL Server

Editar:

Backend/conexion_sqlserver.py

Configurar:

server = 'localhost'
database = 'EcoBI'
username = 'usuario'
password = 'password'
▶️ Ejecución
Ejecutar predicciones
python PYTHON/prediccion_toneladas.py
python PYTHON/prediccion_saturacion.py
python PYTHON/prediccion_quejas.py
Abrir dashboard

Abrir en Power BI:

Frontend/Proyecto.pbix
📈 Indicadores Principales

El dashboard incluye:

✅ Total de toneladas recolectadas
✅ Tiempo promedio de ruta
✅ Saturación promedio
✅ Total de quejas
✅ Distancia promedio
✅ Distribución por distrito
✅ Distribución por tipo de residuo
✅ Predicciones futuras
