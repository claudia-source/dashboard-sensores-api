import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import random
from datetime import datetime

app = dash.Dash(__name__)

# -------------------------
# BASE DE DATOS SIMULADA
# -------------------------
data = []

# 👇 MUCHOS IDS POR TIPO 
sensores = {
    1: "temperatura",
    2: "temperatura",
    3: "temperatura",
    4: "presion",
    5: "presion",
    6: "presion",
    7: "velocidad",
    8: "velocidad"
}

def generar_datos():
    global data

    nuevos = []

    for sensor_id, tipo in sensores.items():

        if tipo == "temperatura":
            valor = random.uniform(10, 45)
        elif tipo == "presion":
            valor = random.uniform(950, 1050)
        else:
            valor = random.uniform(40, 120)

        nuevos.append({
            "sensor_id": str(sensor_id),
            "type": tipo,
            "value": round(valor, 2),
            "timestamp": datetime.now().isoformat()
        })

    data.extend(nuevos)

    # mantener historial (esto da MOVIMIENTO)
    if len(data) > 300:
        data[:] = data[-300:]


# -------------------------
# SEMÁFORO (CORRECTO)
# -------------------------
def semaforo(tipo, valor):

    if tipo == "temperatura":
        if valor < 0 or valor > 50:
            return "PELIGRO", "red"
        elif valor < 10 or valor > 40:
            return "ALERTA", "orange"
        else:
            return "NORMAL", "green"

    if tipo == "presion":
        if valor < 900 or valor > 1100:
            return "PELIGRO", "red"
        elif valor < 950 or valor > 1050:
            return "ALERTA", "orange"
        else:
            return "NORMAL", "green"

    if tipo == "velocidad":
        if valor > 120:
            return "PELIGRO", "red"
        elif valor > 80:
            return "ALERTA", "orange"
        else:
            return "NORMAL", "green"

    return "NORMAL", "green"


# -------------------------
# LAYOUT
# -------------------------
app.layout = html.Div([

    html.H1("📊 Dashboard", style={"textAlign": "center"}),

    dcc.Dropdown(id="tipo", placeholder="Tipo sensor"),
    dcc.Dropdown(id="sensor_id", placeholder="Sensor ID"),

    dcc.RangeSlider(id="slider"),

    html.Div(id="kpis"),

    dcc.Graph(id="grafico"),

    html.Div(id="hora"),

    dcc.Interval(id="interval", interval=1000, n_intervals=0)

])


# -------------------------
# CONTROLES
# -------------------------
@app.callback(
    Output("tipo", "options"),
    Output("sensor_id", "options"),
    Output("slider", "min"),
    Output("slider", "max"),
    Output("slider", "value"),
    Input("interval", "n_intervals"),
    Input("tipo", "value")  # 👈 IMPORTANTE
)
def controles(n, tipo):

    generar_datos()

    df = pd.DataFrame(data)

    if df.empty:
        return [], [], 0, 0, [0, 0]

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna()

    # 🔹 TIPOS
    tipos = [{"label": t, "value": t} for t in df["type"].unique()]

    # 🔹 FILTRAR POR TIPO (AQUÍ ESTÁ LA CLAVE)
    if tipo:
        df_filtrado = df[df["type"] == tipo]
    else:
        df_filtrado = df

    # 🔹 IDS CORRECTOS
    ids = [{"label": str(i), "value": str(i)} for i in df["sensor_id"].unique()]

    df["ts"] = df["timestamp"].astype("int64") // 10**9

    return tipos, ids, df["ts"].min(), df["ts"].max(), [df["ts"].min(), df["ts"].max()]

# -------------------------
# DASHBOARD
# -------------------------
@app.callback(
    Output("grafico", "figure"),
    Output("kpis", "children"),
    Input("tipo", "value"),
    Input("sensor_id", "value"),
    Input("slider", "value"),
    Input("interval", "n_intervals")
)
def dashboard(tipo, sensor_id, rango, n):

    df = pd.DataFrame(data)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if df.empty:
        return {}, "Sin datos"

    if tipo:
        df = df[df["type"] == tipo]

    if sensor_id is not None:
        df["sensor_id"] = df["sensor_id"].astype(str)
        df = df[df["sensor_id"] == str(sensor_id)]

    df["ts"] = df["timestamp"].astype("int64") // 10**9

    if rango:
        df = df[(df["ts"] >= rango[0]) & (df["ts"] <= rango[1])]

    if df.empty:
        return {}, "Sin datos"

    df = df.sort_values("timestamp")

    # 🔥 AQUÍ ESTÁ LA CLAVE DEL MOVIMIENTO
    fig = px.line(
        df,
        x="timestamp",
        y="value",
        color="sensor_id"
    )

    fig.update_traces(
    mode="lines+markers",
    line=dict(width=3, shape="spline"),  # 👈 curvas suaves (se ve más dinámico)
    marker=dict(size=6)
)

    fig.update_layout(
    transition_duration=800
)


    # 🔥 SEMÁFORO DINÁMICO (ÚLTIMO VALOR)
    ultimo = df.iloc[-1]
    estado, color = semaforo(ultimo["type"], ultimo["value"])

    promedio = df["value"].mean()
    minimo = df["value"].min()
    maximo = df["value"].max()

    kpis = html.Div([
        html.H3(f"Promedio: {promedio:.2f}"),
        html.H3(f"Mínimo: {minimo}"),
        html.H3(f"Máximo: {maximo}"),
        html.H3(f"Estado: {estado}", style={"color": color})
    ])

    return fig, kpis


# -------------------------
# HORA
# -------------------------
@app.callback(
    Output("hora", "children"),
    Input("interval", "n_intervals")
)
def hora(n):
    return f"Hora actual: {datetime.now().strftime('%H:%M:%S')}"


# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)