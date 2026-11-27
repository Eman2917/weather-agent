# ===== FIXED: Sahi predict - code + precipitation + is_night alag alag =====
code = int(c.get("weather_code", 0))
# is_night pehle main.py se, warna is_day se
is_night = pred.get("is_night", int(c.get("is_day", 1)) == 0)
# Agar is_day bhi na ho to time se check karo
if "is_night" not in pred and "is_day" not in c:
    try:
        hh = int(str(c.get("time", "12:00"))[11:13])
        is_night = hh < 6 or hh >= 18
    except:
        is_night = False

precip = float(c.get("precipitation", 0) or 0)
rain_prob = int(pred.get("max_rain_chance", 0) or 0)

# Weather type - sab se pehle snowfall / storm / rain, phir clear / cloudy
if code in [71,73,75,77,85,86]:
    weather_type = "SNOW"; weather_label = "Snowy & Cold"
elif code in [95, 96, 99]:
    weather_type = "STORM"; weather_label = "Stormy & Thunder"
elif code in [51,53,55,61,63,65,66,67,80,81,82] or (precip > 0 and code not in [0,1,2]):
    weather_type = "RAIN"; weather_label = "Rainy Night" if is_night else "Rainy"
elif code in [0, 1]:
    weather_type = "CLEAR"
    weather_label = "Clear Night" if is_night else "Sunny"
else:
    # code 2, 3, 45, 48 = Cloudy / Fog - is me baarish nahi hai
    weather_type = "CLOUDY"
    weather_label = "Cloudy Night" if is_night else "Cloudy"