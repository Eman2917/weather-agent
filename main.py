import requests
from fpdf import FPDF

def get_coords(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    r = requests.get(url, params={"name": city, "count": 1, "language": "en", "format": "json"})
    data = r.json()
    if "results" not in data:
        return None
    res = data["results"][0]
    return res["latitude"], res["longitude"], res["name"]

def predict_storm_dict(city):
    coords = get_coords(city)
    if not coords:
        return None
    lat, lon, name = coords

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,pressure_msl,wind_speed_10m,wind_direction_10m,wind_gusts_10m,is_day",
        "hourly": "temperature_2m,precipitation_probability,precipitation,wind_speed_10m,wind_gusts_10m,visibility",
        "daily": "temperature_2m_max,temperature_2m_min,uv_index_max,precipitation_probability_max",
        "timezone": "auto",
        "forecast_days": 7
    }
    r = requests.get(url, params=params)
    data = r.json()

    current = data["current"]
    hourly = data["hourly"]
    daily = data["daily"]

    idx = 0
    for i, t in enumerate(hourly["time"]):
        if t[:13] == current["time"][:13]:
            idx = i
            break

    next_rain = hourly["precipitation_probability"][idx:idx+6]
    next_wind = hourly["wind_speed_10m"][idx:idx+6]
    next_gust = hourly["wind_gusts_10m"][idx:idx+6]
    next_precip = hourly["precipitation"][idx:idx+6]

    max_rain = max([x for x in next_rain if x is not None], default=0)
    max_wind = max(next_wind)
    max_gust = max(next_gust)
    total_precip = sum([x for x in next_precip if x is not None])

    if max_gust > 55 or (max_wind > 40 and max_rain > 70):
        level, msg, color = "STORM ALERT", "Severe thunderstorm expected.", "red"
    elif total_precip > 2 or max_rain > 70:
        level, msg, color = "MODERATE ALERT", "Heavy rain expected.", "orange"
    elif max_rain > 40:
        level, msg, color = "LIGHT RAIN", "Light rain possible.", "orange"
    else:
        level, msg, color = "NO STORM - SAFE", "Weather is normal.", "green"

    return {
        "name": name, "current": current, "hourly": hourly, "daily": daily,
        "level": level, "msg": msg, "color": color,
        "max_rain_chance": int(max_rain), "max_wind": float(max_wind)
    }

def create_pdf(city, live_text, pred_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, f"Weather Report - {city}", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, live_text)
    pdf.multi_cell(0, 10, pred_text)
    filename = f"{city}_report.pdf"
    pdf.output(filename)
    return filename
