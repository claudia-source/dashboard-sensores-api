# 📊 Dashboard de Sensores

Proyecto desarrollado con Flask y Dash para la visualización interactiva de sensores en tiempo real.

---

# 🚀 Tecnologías utilizadas

- Python
- Flask
- Dash
- Plotly
- Pandas

---

# 📁 Estructura del proyecto

```bash
dashboard_sensores/
│
├── API.py
├── Dashboard.py
├── sensores.json
├── requirements.txt
├── README.md
└── capturas/
⚙️ Instalación
1. Clonar repositorio
git clone https://github.com/claudia-source/dashboard-sensores-ap
2. Entrar a la carpeta
cd dashboard_sensores
3. Instalar dependencias
pip install -r requirements.txt

▶️ Ejecutar API
python API.py

Servidor:

http://127.0.0.1:5000
▶️ Ejecutar Dashboard

En otra terminal:

python Dashboard.py

Dashboard:

http://127.0.0.1:8050

📌 Funcionalidades
API Flask
GET /sensors
GET /sensors/<id>
POST /sensors
PUT /sensors/<id>
DELETE /sensors/<id>
Dashboard Dash
Visualización en tiempo real
Filtros por tipo
Filtros por sensor_id
Líneas dinámicas
Indicadores KPI
Semáforo inteligente
Actualización automática cada 2 segundos

# 📸 Capturas

Las capturas de funcionamiento del dashboard y las pruebas en Postman se encuentran en la carpeta:

```bash
capturas/

📊 Sección del Dashboard


## 📊 Dashboard funcionando

dashboard_general.png
dashboard_tipo.png
dashboard_id.png

Pruebas de la API
📥 GET sensores temperatura
GET_sensor_temperatura.png
📥 GET sensor por ID
GET_by_ID_para_sensor_temperatura.png
📤 POST sensor temperatura
POST_sensor_temperatura.png
⚠️ POST fuera de rango
POST_sensor_temperatura_fuera_de_rango.png
🔄 PUT sensor
PUT_sensor.png
❌ DELETE sensor
DELETE_sensor_temperatura.png

## 📊 Pruebas API - Presión

### 📥 GET sensores presión
GET_sensor_presion.png
### 📥 GET sensor por ID (presión)
GET_sensores_por_ID_de_presion.png
### 📤 POST sensor presión
POST_sensor_presion.png
### ⚠️ POST presión fuera de rango
POST_sensor_presion_fuera_de_rango.png
### 🔄 PUT sensor presión
PUT_sensor_presion.png
### ❌ DELETE sensor presión
DELETE_sensor_presion.png

## 🚀 Pruebas API - Velocidad

### 📥 GET sensores velocidad
GET_sensor_velocidad.png
### 📤 POST sensor velocidad
POST_sensor_velocidad.png
### ⚠️ POST velocidad fuera de rango
POST_sensor_velocidad_fuera_de_rango.png
### 🔄 PUT sensor velocidad
PUT_sensor_velocidad.png
### ❌ DELETE sensor velocidad
DELETE_sensor_velocidad.png

## 👩‍💻 Autor
Claudia Liliana Cabrera Cabezas