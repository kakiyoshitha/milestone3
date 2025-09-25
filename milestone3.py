# Milestone 3: Weeks 5–6
# Module: Alert Logic & Trend Visualization

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# -------------------------
# 1. AQI Calculation Logic
# -------------------------
def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "green"
    elif aqi <= 100:
        return "Moderate", "orange"
    elif aqi <= 150:
        return "Unhealthy for Sensitive", "red"
    elif aqi <= 200:
        return "Unhealthy", "purple"
    else:
        return "Very Unhealthy", "maroon"

# -------------------------
# 2. Simulated Data
# -------------------------
# Current AQI
current_aqi = 78
category, color = get_aqi_category(current_aqi)

# 7-day forecast AQI
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
forecast_aqi = [45, 52, 78, 112, 105, 85, 60]
forecast_df = pd.DataFrame({"Day": days, "AQI": forecast_aqi})

# Pollutant concentrations for 24h
hours = np.arange(0, 25, 2)
pollutants = pd.DataFrame({
    "Hour": hours,
    "PM2.5": np.random.randint(20, 60, len(hours)),
    "PM10": np.random.randint(30, 70, len(hours)),
    "O3": np.random.randint(15, 55, len(hours))
})

# Active alerts (generate based on thresholds)
alerts = []
if current_aqi > 100:
    alerts.append(("Unhealthy for Sensitive Groups", "Tomorrow, 10:00 AM"))
if pollutants["O3"].max() > 50:
    alerts.append(("High Ozone Levels Expected", "Friday, 2:00 PM"))
if current_aqi > 50:
    alerts.append(("Moderate Air Quality", "Today, 8:00 AM"))

# -------------------------
# 3. Build Dashboard
# -------------------------
app = Dash(__name__)

app.layout = html.Div(style={"backgroundColor": "#fafafa", "padding": "20px"}, children=[
    html.H1("Air Quality Alert System", style={"textAlign": "center", "color": "#b85c00"}),
    html.H3("Milestone 3: Working Application (Weeks 5–6)", style={"textAlign": "center"}),

    html.Div([
        # Left: Current AQI Gauge
        html.Div([
            html.H4("Current Air Quality", style={"textAlign": "center"}),
            dcc.Graph(
                figure=go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=current_aqi,
                    title={"text": f"AQI ({category})"},
                    gauge={
                        "axis": {"range": [0, 200]},
                        "bar": {"color": color},
                        "steps": [
                            {"range": [0, 50], "color": "lightgreen"},
                            {"range": [51, 100], "color": "orange"},
                            {"range": [101, 150], "color": "red"},
                            {"range": [151, 200], "color": "purple"},
                        ],
                    }
                ))
            , style={"height": "300px"})
        ], style={"width": "45%", "display": "inline-block", "verticalAlign": "top"}),

        # Right: 7-Day Forecast
        html.Div([
            html.H4("7-Day Forecast", style={"textAlign": "center"}),
            dcc.Graph(
                figure=go.Figure(data=[
                    go.Bar(
                        x=forecast_df["Day"],
                        y=forecast_df["AQI"],
                        marker_color=["green" if x <= 50 else
                                      "orange" if x <= 100 else
                                      "red" if x <= 150 else "purple"
                                      for x in forecast_df["AQI"]],
                        text=forecast_df["AQI"],
                        textposition="auto"
                    )
                ]).update_layout(yaxis_title="AQI", xaxis_title="Day")
            , style={"height": "300px"})
        ], style={"width": "50%", "display": "inline-block", "marginLeft": "20px"})
    ]),

    html.Br(),

    # Pollutant Concentrations
    html.Div([
        html.H4("Pollutant Concentrations", style={"textAlign": "center"}),
        dcc.Graph(
            figure=go.Figure()
            .add_trace(go.Scatter(x=pollutants["Hour"], y=pollutants["PM2.5"], mode="lines+markers", name="PM2.5"))
            .add_trace(go.Scatter(x=pollutants["Hour"], y=pollutants["PM10"], mode="lines+markers", name="PM10"))
            .add_trace(go.Scatter(x=pollutants["Hour"], y=pollutants["O3"], mode="lines+markers", name="O3"))
            .update_layout(xaxis_title="Hour of Day", yaxis_title="Concentration (µg/m³)")
        )
    ], style={"width": "70%", "margin": "auto"}),

    html.Br(),

    # Active Alerts
    html.Div([
        html.H4("Active Alerts", style={"textAlign": "center"}),
        html.Ul([
            html.Li(f"{alert[0]} – {alert[1]}", style={"color": "red", "fontWeight": "bold"})
            for alert in alerts
        ])
    ], style={"width": "60%", "margin": "auto", "padding": "20px", "backgroundColor": "#fff3cd",
              "borderRadius": "10px", "boxShadow": "0px 2px 5px rgba(0,0,0,0.2)"})
])

# -------------------------
# 4. Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
