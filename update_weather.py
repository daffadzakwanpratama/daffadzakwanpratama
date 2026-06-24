import urllib.request
import json
import os
from datetime import datetime, timedelta, timezone

def main():
    # Coordinates for Bogor, Indonesia
    lat = "-6.59"
    lon = "106.79"
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m&timezone=Asia/Jakarta"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        current = data.get("current", {})
        temp = current.get("temperature_2m")
        humidity = current.get("relative_humidity_2m")
        feels_like = current.get("apparent_temperature")
        wind_speed = current.get("wind_speed_10m")
        weather_code = current.get("weather_code")
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return

    # Weather code translation and emoji mapping
    weather_map = {
        0: ("Cerah", "☀️"),
        1: ("Cerah Berawan", "🌤️"),
        2: ("Berawan", "⛅"),
        3: ("Mendung", "☁️"),
        45: ("Berkabut", "🌫️"),
        48: ("Kabut Rime", "🌫️"),
        51: ("Gerimis Ringan", "🌧️"),
        53: ("Gerimis Sedang", "🌧️"),
        55: ("Gerimis Lebat", "🌧️"),
        61: ("Hujan Ringan", "🌧️"),
        63: ("Hujan Sedang", "🌧️"),
        65: ("Hujan Lebat", "🌧️"),
        71: ("Salju Ringan", "❄️"),
        73: ("Salju Sedang", "❄️"),
        75: ("Salju Lebat", "❄️"),
        80: ("Hujan Rintik", "🌦️"),
        81: ("Hujan Sedang", "🌦️"),
        82: ("Hujan Lebat", "🌦️"),
        95: ("Badai Petir", "⛈️"),
        96: ("Badai dengan Hujan Es", "⛈️"),
        99: ("Badai Es Lebat", "⛈️"),
    }
    
    condition, emoji = weather_map.get(weather_code, ("Cuaca Tidak Diketahui", "🌡️"))
    
    # Calculate WIB timestamp (UTC+7)
    wib_tz = timezone(timedelta(hours=7))
    last_update = datetime.now(timezone.utc).astimezone(wib_tz).strftime("%d %b %Y, %H:%M WIB")
    
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="450" height="150" viewBox="0 0 450 150">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a;stop-opacity:0.95" />
      <stop offset="100%" style="stop-color:#1e1b4b;stop-opacity:0.95" />
    </linearGradient>
    <!-- Border Gradient -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#818cf8;stop-opacity:0.8" />
      <stop offset="50%" style="stop-color:#c084fc;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#6366f1;stop-opacity:0.8" />
    </linearGradient>
    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 700; font-size: 16px; fill: #f8fafc; }}
      .subtitle {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 12px; fill: #94a3b8; }}
      .temp {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 800; font-size: 36px; fill: #f8fafc; }}
      .condition {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 500; font-size: 14px; fill: #38bdf8; }}
      .detail-label {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 10px; fill: #64748b; font-weight: bold; letter-spacing: 0.5px; }}
      .detail-val {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 600; font-size: 13px; fill: #cbd5e1; }}
      .update-time {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 9px; fill: #475569; }}
      .emoji {{ font-size: 55px; }}
    </style>
  </defs>
  
  <!-- Card Border and Background -->
  <rect x="2" y="2" width="446" height="146" rx="16" fill="url(#bg-grad)" stroke="url(#border-grad)" stroke-width="2" />
  
  <!-- Weather Icon/Emoji -->
  <text x="30" y="95" class="emoji">{emoji}</text>
  
  <!-- Temperature & Condition -->
  <text x="110" y="65" class="temp">{temp}°C</text>
  <text x="110" y="88" class="condition">{condition}</text>
  
  <!-- Location Information -->
  <text x="110" y="32" class="title">Bogor, Indonesia</text>
  
  <!-- Divider -->
  <line x1="285" y1="20" x2="285" y2="130" stroke="#334155" stroke-width="1" stroke-dasharray="3 3" />
  
  <!-- Details Section -->
  <!-- Humidity -->
  <text x="305" y="38" class="detail-label">KELEMBABAN</text>
  <text x="305" y="55" class="detail-val">{humidity}%</text>
  
  <!-- Feels Like -->
  <text x="305" y="80" class="detail-label">TERASA SEPERTI</text>
  <text x="305" y="97" class="detail-val">{feels_like}°C</text>
  
  <!-- Wind Speed -->
  <text x="305" y="122" class="detail-val">{wind_speed} km/h</text>
  <text x="305" y="110" class="detail-label">ANGIN</text>
  
  <!-- Last Update -->
  <text x="110" y="130" class="update-time">Diperbarui: {last_update}</text>
</svg>
"""
    
    # Save the weather.svg file
    output_path = os.path.join(os.path.dirname(__file__), "weather.svg")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Weather SVG successfully updated at {output_path}")
    except Exception as e:
        print(f"Error writing SVG file: {e}")

if __name__ == "__main__":
    main()
