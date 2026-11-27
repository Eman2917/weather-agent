import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from main import predict_storm_dict, create_pdf

st.set_page_config(page_title="Storm Prediction Agent", page_icon="🌩️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
* { font-family: 'Poppins', 'Segoe UI', sans-serif !important; }
.stApp { background: #FFFFFF !important; }
.block-container { max-width: 1080px !important; padding-top: 12px !important; padding-bottom: 20px !important; }
h1, h2, h3, p, span, div, button, input { font-family: 'Poppins', 'Segoe UI', sans-serif !important; }
h1, h2, h3, p { color: #0F172A !important; }
.top-title { font-size: 22px; font-weight: 700; color: #0F172A !important; margin: 0; letter-spacing: -0.3px; }
.top-sub { font-size: 17px !important; font-weight: 600 !important; color: #38BDF8 !important; margin: 4px 0 16px 0 !important; letter-spacing: 0.3px; }
[data-testid="stTextInput"] input { background: #F1F5F9 !important; border: none !important; border-radius: 999px !important; height: 46px !important; font-size: 14px !important; font-weight: 400 !important; padding: 0 18px 0 18px !important; color: #0F172A !important; box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important; }
[data-testid="stTextInput"] input::placeholder { color: #94A3B8 !important; opacity: 1 !important; font-weight: 400 !important; }
[data-testid="stTextInput"] input:focus { outline: 2px solid #BAE6FD !important; background: #FFFFFF !important; box-shadow: 0 4px 16px rgba(56,189,248,0.15) !important; }
.hero { position: relative; border-radius: 22px; overflow: hidden; height: 342px; box-shadow: 0 10px 28px rgba(56,189,248,0.22); }
.hero-bg { position: absolute; inset: 0; background: linear-gradient(180deg, #3A7BD5 0%, #5AA0E0 28%, #8EC5F0 62%, #CDE6F8 100%); }
.hero-content { position: relative; z-index: 3; height: 100%; padding: 20px 24px 18px 24px; display: flex; flex-direction: column; justify-content: space-between; }
.hero-city { font-size: 26px; font-weight: 700; color: white !important; margin: 0; text-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.hero-feels { font-size: 12px; font-weight: 500; color: white !important; margin: 0; opacity: 0.95; }
.hero-center { text-align: center; margin-top: -8px; }
.hero-cond { font-size: 19px; font-weight: 500; color: white !important; margin: 0; text-shadow: 0 1px 6px rgba(0,0,0,0.15); }
.hero-range { font-size: 13px; font-weight: 400; color: rgba(255,255,255,0.92) !important; margin: 5px 0 0 0; }
.hero-temp { font-size: 88px; font-weight: 300; color: white !important; line-height: 1; margin: 4px 0 0 0; letter-spacing: -2px; text-shadow: 0 3px 14px rgba(0,0,0,0.12); }
.hero-temp span { font-size: 34px; font-weight: 300; }
.hero-bottom { display: flex; justify-content: space-between; align-items: center; }
.hero-bottom p { font-size: 12px; font-weight: 500; color: white !important; margin: 0; opacity: 0.95; }
.img-sun { position: absolute; top: 22px; right: 36px; width: 56px; height: 56px; background: radial-gradient(circle, #FFFFFF 0%, #FFFDE6 38%, #FFE88A 72%, rgba(255,232,138,0) 100%); border-radius: 50%; box-shadow: 0 0 16px 8px rgba(255,255,255,0.95), 0 0 42px 22px rgba(255,255,220,0.55), 0 0 85px 42px rgba(255,240,170,0.30); animation: sunPulse 3s ease-in-out infinite; z-index: 2; }
@keyframes sunPulse { 0%,100% { transform: scale(1); } 50% { transform: scale(1.07); } }
.img-moon { position: absolute; top: 22px; right: 36px; width: 56px; height: 56px; background: radial-gradient(circle at 35% 35%, #FFFFFF 0%, #E8EEF5 55%, #C8D2E0 100%); border-radius: 50%; box-shadow: 0 0 18px 8px rgba(255,255,255,0.85), 0 0 50px 25px rgba(200,210,255,0.35); z-index: 2; }
.img-moon::after { content: ''; position: absolute; width: 12px; height: 12px; background: #D5DCE8; border-radius: 50%; top: 12px; left: 14px; opacity: 0.7; box-shadow: 10px 16px 0 2px #D5DCE8; }
.star { position: absolute; width: 4px; height: 4px; background: white; border-radius: 50%; box-shadow: 0 0 6px white; animation: twinkle 1.8s ease-in-out infinite; }
@keyframes twinkle { 0%,100% { opacity: 0.3; transform: scale(0.7); } 50% { opacity: 1; transform: scale(1.2); } }
.img-cloud { position: absolute; width: 145px; height: 42px; background: rgba(255,255,255,0.92); border-radius: 50px; filter: blur(0.6px); }
.img-cloud::before { content: ''; position: absolute; width: 56px; height: 56px; background: rgba(255,255,255,0.92); border-radius: 50%; top: -27px; left: 25px; }
.img-cloud::after { content: ''; position: absolute; width: 38px; height: 38px; background: rgba(255,255,255,0.92); border-radius: 50%; top: -15px; left: 70px; }
.cloud1 { left: 7%; top: 108px; opacity: 0.55; animation: drift 6s ease-in-out infinite; }
.cloud2 { left: 54%; top: 152px; width: 105px; height: 32px; opacity: 0.45; animation: drift2 7s ease-in-out infinite; }
.cloud-dark { background: rgba(30,41,59,0.92); }
.cloud-dark::before { background: rgba(30,41,59,0.92); }
.cloud-dark::after { background: rgba(30,41,59,0.92); }
.cloud-night { background: rgba(148,163,184,0.85); }
.cloud-night::before { background: rgba(148,163,184,0.85); }
.cloud-night::after { background: rgba(148,163,184,0.85); }
@keyframes drift { 0%,100% { transform: translateX(0); } 50% { transform: translateX(16px); } }
@keyframes drift2 { 0%,100% { transform: translateX(0); } 50% { transform: translateX(-14px); } }
.rain-line { position: absolute; top: 70px; width: 1.6px; height: 36px; background: linear-gradient(to bottom, transparent, rgba(255,255,255,0.95)); border-radius: 2px; transform: rotate(10deg); animation: rainDrop 0.6s linear infinite; }
@keyframes rainDrop { 0% { transform: translateY(0) rotate(10deg); opacity: 0; } 20% { opacity: 1; } 100% { transform: translateY(275px) rotate(10deg); opacity: 0; } }
.bolt { position: absolute; left: 56%; top: 92px; width: 26px; height: 52px; background: #FFE600; clip-path: polygon(45% 0, 65% 0, 35% 45%, 55% 45%, 20% 100%, 40% 50%, 15% 50%); filter: drop-shadow(0 0 10px #FFE600); animation: boltFlash 1.4s ease-in-out infinite; z-index: 2; }
.flash-bg { position: absolute; inset: 0; animation: bgFlash 1.4s ease-in-out infinite; }
@keyframes boltFlash { 0%, 55%, 100% { opacity: 0; } 8%, 25% { opacity: 1; } }
@keyframes bgFlash { 0%, 55%, 100% { background: rgba(255,255,200,0); } 8%, 25% { background: rgba(255,255,200,0.35); } }
.snow-dot { position: absolute; width: 9px; height: 9px; background: white; border-radius: 50%; box-shadow: 0 0 10px white; animation: snowFall 3.2s linear infinite; z-index: 2; }
@keyframes snowFall { 0% { transform: translateY(-10px); opacity: 0; } 15% { opacity: 1; } 100% { transform: translateY(320px) translateX(18px); opacity: 0; } }
.alert-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 18px; padding: 18px 18px 16px 18px; box-shadow: 0 2px 12px rgba(0,0,0,0.04); min-height: 118px; }
.alert-card h4 { font-size: 14px; font-weight: 700; margin: 0; color: #0F172A !important; }
.alert-card p { font-size: 12.5px; font-weight: 400; line-height: 1.6; color: #64748B !important; margin: 8px 0 0 0; }
.alert-card .small { font-size: 11px; font-weight: 500; color: #94A3B8 !important; margin-top: 10px; }
.sec-title { font-size: 18px; font-weight: 700; color: #0F172A !important; margin: 22px 0 14px 0; }
.factor-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 18px; padding: 18px 16px 16px 16px; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.04); }
.factor-gauge { width: 92px; height: 92px; border-radius: 50%; margin: 0 auto 10px auto; display: flex; align-items: center; justify-content: center; }
.factor-inner { width: 66px; height: 66px; background: white; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.factor-val { font-size: 19px; font-weight: 700; color: #0F172A; line-height: 1; }
.factor-icon { font-size: 12px; margin-bottom: 2px; }
.factor-name { font-size: 13.5px; font-weight: 600; color: #334155 !important; margin: 0; }
.factor-sub { font-size: 12px; font-weight: 500; color: #64748B !important; margin: 3px 0 0 0; }
.fore-card { background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 16px; padding: 12px 8px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }
.fore-card p { margin: 0; }
.fore-day { font-size: 11px; font-weight: 500; color: #64748B !important; }
.fore-temp { font-size: 19px; font-weight: 700; color: #0F172A !important; margin: 5px 0 0 0 !important; }
.fore-rain { font-size: 11px; font-weight: 600; color: #38BDF8 !important; margin-top: 3px !important; }
.stButton button { background: #38BDF8 !important; color: white !important; border-radius: 999px !important; height: 42px !important; font-weight: 600 !important; font-size: 14px !important; border: none !important; letter-spacing: 0.2px; }
</style>
""", unsafe_allow_html=True)

st.markdown("<p class='top-title'>🌩️ Weather Analysis & Storm Prediction</p><p class='top-sub'>Live Weather Prediction</p>", unsafe_allow_html=True)

city = st.text_input("City", "Thimphu", label_visibility="collapsed", placeholder="🔍 Search city...")
search = bool(city and city.strip() != "")

if search:
    with st.spinner("Fetching live data..."):
        pred = predict_storm_dict(city)

    if not pred:
        st.error("City not found.")
    else:
        c = pred["current"]
        h = pred["hourly"]
        d = pred.get("daily", {"temperature_2m_min": [15,15,15,15], "temperature_2m_max": [26,26,26,26], "uv_index_max": [2,2,2,2], "time": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]})

        raw_msg = pred.get("msg", "")
        raw_level = pred.get("level", "")
        color = pred.get("color", "green")
        level, msg = raw_level, raw_msg

        feels = int(c["apparent_temperature"])
        humidity = int(c["relative_humidity_2m"])
        wind_speed = c["wind_speed_10m"]
        wind_dir = int(c.get("wind_direction_10m", 0))
        pressure = int(c["pressure_msl"])
        temp = float(c["temperature_2m"])
        uv = d["uv_index_max"][0] if "uv_index_max" in d else 1
        uv_val = round(float(uv), 1) if uv else 1
        vis_list = h.get("visibility", [3200])
        vis_km = round((vis_list[0] or 3200) / 1000, 1)
        dirs = ["N","NE","E","SE","S","SW","W","NW"]
        dir_name = dirs[round(wind_dir/45)%8]
        t_min = int(d["temperature_2m_min"][0])
        t_max = int(d["temperature_2m_max"][0])
        rain_chance = int(pred['max_rain_chance'])
        max_wind = float(pred['max_wind'])

        # ===== FIXED: Sahi predict - current time wala hour lo, purana hour nahi =====
        code = int(c.get("weather_code", 0))
        is_night = pred.get("is_night", int(c.get("is_day", 1)) == 0)
        if "is_night" not in pred and "is_day" not in c:
            try:
                hh = int(str(c.get("time", "12:00"))[11:13])
                is_night = hh < 6 or hh >= 18
            except:
                is_night = False

        precip = float(c.get("precipitation", 0) or 0)
        cloud = float(c.get("cloud_cover", 0) or 0)
        try:
            h_times = h.get("time", [])
            h_codes = h.get("weather_code", [])
            h_precip_prob = h.get("precipitation_probability", [])
            cur_time = str(c.get("time", ""))[:13]
            idx = 0
            for i, t in enumerate(h_times):
                if str(t)[:13] == cur_time:
                    idx = i
                    break
            if h_codes and code == 0:
                code = int(h_codes[idx] or 0)
            if h_precip_prob and h_precip_prob[idx] is not None:
                rain_prob_now = int(h_precip_prob[idx])
            else:
                rain_prob_now = int(pred.get("max_rain_chance", 0) or 0)
        except:
            rain_prob_now = int(pred.get("max_rain_chance", 0) or 0)

        # Weather type - pehle asli baarish / snowfall / storm, phir clear / cloudy
        # FIXED SNOW: sirf code pe depend nahi, snowfall + thand + baarish bhi check karo
        snowfall = float(c.get("snowfall", 0) or 0)
        if code in [71,73,75,77,85,86] or snowfall > 0 or (temp <= 1 and precip > 0):
            weather_type = "SNOW"; weather_label = "Snowy & Cold"
        elif code in [95, 96, 99]:
            weather_type = "STORM"; weather_label = "Stormy & Thunder"
        elif code in [51,53,55,61,63,65,66,67,80,81,82] or precip > 0:
            weather_type = "RAIN"; weather_label = "Rainy Night" if is_night else "Rainy"
        elif code in [0, 1] and cloud < 20 and precip == 0:
            weather_type = "CLEAR"
            weather_label = "Clear Night" if is_night else "Sunny"
        else:
            weather_type = "CLOUDY"
            weather_label = "Cloudy Night" if is_night else "Cloudy"

        # Sky background - raat ko hamesha dark
        if is_night:
            sky_bg = "<div class='hero-bg' style='background: linear-gradient(180deg,#0B1026 0%, #1B2A4A 45%, #3A4A6B 100%);'></div>"
        elif weather_type == "RAIN" or weather_type == "STORM":
            sky_bg = "<div class='hero-bg' style='background: linear-gradient(180deg,#2C3E50 0%, #4A6572 45%, #A8C5D6 100%);'></div>"
        elif weather_type == "SNOW":
            sky_bg = "<div class='hero-bg' style='background: linear-gradient(180deg,#8AB6D9 0%, #C5E1F2 60%, #F0F9FF 100%);'></div>"
        elif weather_type == "CLEAR":
            sky_bg = "<div class='hero-bg'></div>"
        else:
            sky_bg = "<div class='hero-bg' style='background: linear-gradient(180deg,#3E6EA5 0%, #7AA8CC 50%, #CDE6F8 100%);'></div>"

        # Animation - 5 Rules Final
        stars = "".join([f"<div class='star' style='left:{8+i*9}%; top:{20+i*12}px; animation-delay:{i*0.3}s;'></div>" for i in range(10)])

        # ===== FIXED: 5 Rules - Final Logic =====
        # 1. Snowfall -> sirf snowfall
        # 2. Baarish -> rain + badal + bijli (storm me)
        # 3. Sunny Day -> sun
        # 4. Raat -> chand
        # 5. Raat + Baarish -> sirf baarish, chand NAHI
        # 6. Cloudy Night -> chand + badal + taare
        if weather_type == "STORM":
            drops = "".join([f"<div class='rain-line' style='left:{5+i*9}%; animation-delay:{i*0.06}s;'></div>" for i in range(12)])
            anim = f"<div class='flash-bg'></div><div class='img-cloud cloud-dark cloud1'></div><div class='img-cloud cloud-dark cloud2'></div><div class='bolt'></div>{drops}"
        elif weather_type == "RAIN":
            drops = "".join([f"<div class='rain-line' style='left:{5+i*9}%; animation-delay:{i*0.08}s;'></div>" for i in range(12)])
            anim = f"<div class='img-cloud cloud-dark cloud1'></div><div class='img-cloud cloud-dark cloud2'></div>{drops}"
        elif weather_type == "SNOW":
            flakes = "".join([f"<div class='snow-dot' style='left:{3+i*3}%; top:{5+i*3}px; animation-delay:{i*0.25}s;'></div>" for i in range(30)])
            anim = f"<div class='img-cloud cloud1'></div><div class='img-cloud cloud2'></div>{flakes}"
        elif weather_type == "CLOUDY" and is_night:
            anim = f"<div class='img-moon'></div>{stars}<div class='img-cloud cloud-night cloud1'></div><div class='img-cloud cloud-night cloud2'></div><div class='img-cloud cloud-night' style='left:38%; top:88px; width:120px; height:34px; opacity:0.85;'></div>"
        elif weather_type == "CLOUDY":
            anim = "<div class='img-sun'></div><div class='img-cloud cloud1'></div><div class='img-cloud cloud2'></div>"
        elif is_night:
            anim = f"<div class='img-moon'></div><div class='img-cloud cloud1' style='opacity:0.25;'></div>{stars}"
        else:
            anim = "<div class='img-sun'></div><div class='img-cloud cloud1'></div><div class='img-cloud cloud2'></div>"

        if color == "red":
            alert_title, alert_msg2 = "🚨 STORM ALERT", "Severe thunderstorm expected. Take precautions and secure outdoor items."
        elif color == "orange":
            alert_title, alert_msg2 = "⚠️ MODERATE ALERT", msg
        else:
            alert_title, alert_msg2 = "✅ NO STORM - SAFE", msg

        # ===== ADVISORY CARD - DYNAMIC BY WEATHER =====
        if is_night and weather_type == "CLEAR":
            adv_title = "🌙 Clear Night"
            adv_msg = "It is a clear night. The sky is clear and the temperature may drop. Enjoy the calm night."
            adv_small = f"🌙 Clear Sky • Feels Like {feels}°C"
        elif weather_type == "CLEAR":
            adv_title = "☀️ Sun Advisory"
            adv_msg = "Sunny day ahead. Wear sunglasses, use sunscreen and stay hydrated."
            adv_small = f"☀️ UV Index {uv_val} • Clear Sky"
        elif weather_type == "RAIN":
            adv_title = "🌧️ Rain Advisory"
            adv_msg = "Rainfall is expected in the next few hours. Carry an umbrella if you are heading out."
            adv_small = f"⚡ Storm Indicators • Gusts {c['wind_gusts_10m']} km/h"
        elif weather_type == "STORM":
            adv_title = "⛈️ Storm Advisory"
            adv_msg = "Thunderstorm nearby. Stay indoors, avoid travelling and stay away from electric poles."
            adv_small = f"⚡ Storm Indicators • Gusts {c['wind_gusts_10m']} km/h"
        elif weather_type == "SNOW":
            adv_title = "❄️ Snow Advisory"
            adv_msg = "Snowfall is expected. Wear warm clothes and drive carefully on slippery roads."
            adv_small = f"❄️ Feels Like {feels}°C • Visibility {vis_km} km"
        else:
            adv_title = "☁️ Cloud Advisory"
            adv_msg = "It is cloudy today. Light rain is possible, so it is better to keep an umbrella with you."
            adv_small = f"☁️ Humidity {humidity}% • Rain {rain_chance}%"

        st.markdown(f"<div class='hero'>{sky_bg}{anim}<div class='hero-content'><div style='display:flex; justify-content:space-between; align-items:flex-start;'><p class='hero-city'>{pred['name']}</p><p class='hero-feels'>🌡️ {feels}°C Feels</p></div><div class='hero-center'><p class='hero-cond'>{weather_label}</p><p class='hero-range'>{t_min} ~ {t_max}°C &nbsp; Feels like {feels}°C</p><p class='hero-temp'>{c['temperature_2m']}<span>°C</span></p></div><div class='hero-bottom'><p>💧 {humidity}% &nbsp;&nbsp; 💨 {wind_speed} km/h</p><p>Rain {rain_chance}%</p></div></div></div>", unsafe_allow_html=True)
        st.write("")

        a1, a2 = st.columns(2)
        with a1:
            st.markdown(f"<div class='alert-card'><h4>{alert_title}</h4><p>{alert_msg2}</p><p class='small'>Rain {rain_chance}% • Max Wind {max_wind} km/h • Next 6 Hours</p></div>", unsafe_allow_html=True)
        with a2:
            st.markdown(f"<div class='alert-card'><h4>{adv_title}</h4><p>{adv_msg}</p><p class='small'>{adv_small}</p></div>", unsafe_allow_html=True)

        st.markdown("<p class='sec-title'>Today's Factors</p>", unsafe_allow_html=True)

        def gauge(pct, val, icon):
            deg = int(pct*3.6)
            return f"<div class='factor-gauge' style='background: conic-gradient(#38BDF8 0deg, #0284C7 {deg}deg, #E0F2FE {deg}deg, #E0F2FE 360deg);'><div class='factor-inner'><div class='factor-icon'>{icon}</div><div class='factor-val'>{val}</div></div></div>"

        hum_pct = humidity
        wind_pct = min(int(wind_speed/50*100),100)
        pres_pct = min(int((pressure-950)/100*100),100)
        uv_pct = min(int(uv_val/11*100),100)
        vis_pct = min(int(vis_km/10*100),100)
        feels_pct = min(max((feels-5)/35*100,5),95)

        f1, f2 = st.columns(2)
        with f1:
            st.markdown(f"<div class='factor-card'>{gauge(hum_pct, f'{humidity}%', '💧')}<p class='factor-name'>Humidity</p><p class='factor-sub'>{humidity}% • {'Damp' if humidity>65 else 'Comfortable' if humidity>40 else 'Dry'}</p></div>", unsafe_allow_html=True)
        with f2:
            st.markdown(f"<div class='factor-card'>{gauge(wind_pct, f'{wind_pct}%', '💨')}<p class='factor-name'>Wind • {dir_name}</p><p class='factor-sub'>{wind_speed} km/h • Gusts {c['wind_gusts_10m']} km/h</p></div>", unsafe_allow_html=True)
        st.write("")
        f3, f4 = st.columns(2)
        with f3:
            st.markdown(f"<div class='factor-card'>{gauge(pres_pct, f'{pres_pct}%', '🧭')}<p class='factor-name'>Pressure</p><p class='factor-sub'>{pressure} hPa • Stable</p></div>", unsafe_allow_html=True)
        with f4:
            st.markdown(f"<div class='factor-card'>{gauge(uv_pct, f'{int(uv_val)}', '☀️')}<p class='factor-name'>UV Index</p><p class='factor-sub'>{int(uv_val)} • {'Weakest' if uv_val<3 else 'Moderate' if uv_val<6 else 'Strong'}</p></div>", unsafe_allow_html=True)
        st.write("")
        f5, f6 = st.columns(2)
        with f5:
            st.markdown(f"<div class='factor-card'>{gauge(feels_pct, f'{feels}°', '🌡️')}<p class='factor-name'>Feels Like</p><p class='factor-sub'>{feels}°C • {'Cool' if feels<20 else 'Comfortable' if feels<=26 else 'Hot'}</p></div>", unsafe_allow_html=True)
        with f6:
            st.markdown(f"<div class='factor-card'>{gauge(vis_pct, f'{vis_pct}%', '👁️')}<p class='factor-name'>Visibility</p><p class='factor-sub'>{vis_km} km • {'Normal' if vis_km>5 else 'Low'}</p></div>", unsafe_allow_html=True)

        st.markdown("<p class='sec-title'>7-Day Forecast</p>", unsafe_allow_html=True)
        days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        raw_mins = d.get("temperature_2m_min", [t_min])
        raw_maxs = d.get("temperature_2m_max", [t_max])
        if not raw_mins: raw_mins = [t_min]
        if not raw_maxs: raw_maxs = [t_max]
        mins = (list(raw_mins) + [raw_mins[-1]]*7)[:7]
        maxs = (list(raw_maxs) + [raw_maxs[-1]]*7)[:7]
        if "time" in d and len(d["time"]) >= 7:
            try:
                import datetime as _dt
                days = [_dt.datetime.fromisoformat(str(x)[:10]).strftime("%a") for x in d["time"][:7]]
            except:
                pass
        prob_list = h.get("precipitation_probability", [rain_chance])
        if not prob_list: prob_list = [rain_chance]
        dcols = st.columns(7)
        for i in range(7):
            with dcols[i]:
                avg = int((mins[i] + maxs[i]) / 2)
                idx = min(i*2, len(prob_list)-1)
                _v = prob_list[idx]
                rain7 = int(_v) if _v is not None else rain_chance
                st.markdown(f"<div class='fore-card'><p class='fore-day'>{days[i]}</p><p class='fore-temp'>{avg}°</p><p class='fore-rain'>🌧️ {rain7}%</p></div>", unsafe_allow_html=True)

        st.markdown("<p class='sec-title'>Temperature Trend</p>", unsafe_allow_html=True)
        df = pd.DataFrame({"Time": [t[11:16] for t in h["time"][:12]], "Temperature": h["temperature_2m"][:12], "Rain %": h["precipitation_probability"][:12]})
        fig, ax = plt.subplots(figsize=(10, 3.2))
        fig.patch.set_facecolor('white'); ax.set_facecolor('white')
        ax.plot(df["Time"], df["Temperature"], color='#0284C7', linewidth=2.8, marker='o', markersize=5, markerfacecolor='#0284C7', markeredgecolor='white', markeredgewidth=1.5, label='Temperature')
        ax.plot(df["Time"], df["Rain %"], color='#38BDF8', linewidth=2.8, marker='o', markersize=5, markerfacecolor='#38BDF8', markeredgecolor='white', markeredgewidth=1.5, label='Rain %')
        ax.fill_between(df["Time"], df["Temperature"], alpha=0.10, color='#0284C7')
        ax.set_ylabel('Value', color='#64748B', fontsize=10); ax.set_xlabel('Time', color='#64748B', fontsize=10); ax.tick_params(colors='#64748B', labelsize=9)
        plt.xticks(rotation=45, ha='right'); ax.grid(True, color='#E2E8F0', linewidth=0.6)
        ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['left'].set_color('#E2E8F0'); ax.spines['bottom'].set_color('#E2E8F0')
        leg = ax.legend(frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2)
        for t in leg.get_texts(): t.set_color('#64748B')
        plt.tight_layout(); st.pyplot(fig)
        st.write("---")
        live_text = f"Temp {c['temperature_2m']}C, Feels {c['apparent_temperature']}C, Humidity {c['relative_humidity_2m']}%, Wind {c['wind_speed_10m']} km/h, Pressure {c['pressure_msl']} hPa, UV {uv_val}, Visibility {vis_km} km"
        pred_text = f"{level} - {msg} Max Wind {pred['max_wind']} km/h, Rain Chance {pred['max_rain_chance']}%"
        if st.button("↓ Get Weather Report"):
            filename = create_pdf(city, live_text, pred_text)
            with open(filename, "rb") as f:
                st.download_button("↓ Download PDF", f, file_name=filename, mime="application/pdf")
            st.success("PDF generated successfully!")