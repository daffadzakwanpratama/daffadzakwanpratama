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
    current_time = datetime.now(timezone.utc).astimezone(wib_tz)
    last_update = current_time.strftime("%d %b %Y, %H:%M WIB")
    
    # Determine Day/Night
    current_hour = current_time.hour
    is_day = 6 <= current_hour < 18

    # Determine theme
    # Theme categories: 2 = Rainy/Stormy, 1 = Cloudy, 0 = Clear
    if weather_code in [51, 53, 55, 61, 63, 65, 80, 81, 82, 95, 96, 99]:
        theme = 2 # Rainy
    elif weather_code in [1, 2, 3, 45, 48]:
        theme = 1 # Cloudy
    else:
        theme = 0 # Clear

    # Build the weather animation window based on the theme
    animation_defs = ""
    animation_content = ""

    # Shared Building silhouettes (Pixel Art Style)
    buildings = """
      <!-- Buildings Silhouettes -->
      <rect x="25" y="65" width="20" height="65" fill="#1e293b" />
      <rect x="48" y="45" width="28" height="85" fill="#0f172a" />
      <rect x="78" y="60" width="18" height="70" fill="#1e293b" />
      <rect x="98" y="75" width="28" height="55" fill="#334155" />
      
      <!-- Lit Pixel Windows -->
      <rect x="54" y="55" width="3" height="3" fill="#fef08a" />
      <rect x="68" y="55" width="3" height="3" fill="#fde047" />
      <rect x="54" y="70" width="3" height="3" fill="#fef08a" opacity="0.8" />
      <rect x="68" y="70" width="3" height="3" fill="#fef08a" />
      <rect x="54" y="85" width="3" height="3" fill="#fde047" />
      <rect x="68" y="85" width="3" height="3" fill="#fef08a" opacity="0.5" />
      <rect x="54" y="100" width="3" height="3" fill="#fef08a" />
      <rect x="68" y="100" width="3" height="3" fill="#fef08a" />
      
      <rect x="85" y="70" width="3" height="3" fill="#fde047" />
      <rect x="85" y="85" width="3" height="3" fill="#fde047" opacity="0.7" />
      <rect x="85" y="100" width="3" height="3" fill="#fef08a" />
      
      <rect x="104" y="85" width="3" height="3" fill="#fde047" />
      <rect x="114" y="85" width="3" height="3" fill="#fde047" />
    """

    if theme == 2:  # Rainy Theme
        animation_defs = """
    <!-- Rainy Sky Gradient -->
    <linearGradient id="win-sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#0b0f19" />
      <stop offset="100%" style="stop-color:#1e293b" />
    </linearGradient>
    <style>
      @keyframes fall {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-12px, 120px); }
      }
      @keyframes lightning {
        0%, 95%, 98%, 100% { opacity: 0; }
        96%, 97% { opacity: 0.15; }
      }
      .rain-drop {
        stroke: #60a5fa;
        stroke-width: 1.5;
        stroke-linecap: round;
        opacity: 0.6;
        animation: fall 0.8s linear infinite;
      }
      .lightning-flash {
        fill: #ffffff;
        opacity: 0;
        animation: lightning 6s infinite;
      }
    </style>
        """
        animation_content = f"""
      <!-- Sky Background -->
      <rect x="20" y="20" width="110" height="110" fill="url(#win-sky)" />
      
      <!-- Lightning Effect -->
      <rect class="lightning-flash" x="20" y="20" width="110" height="110" />
      
      {buildings}
      
      <!-- Rain Drops -->
      <line class="rain-drop" x1="30" y1="-20" x2="25" y2="-10" style="animation-delay: 0.0s; animation-duration: 0.7s;" />
      <line class="rain-drop" x1="50" y1="-20" x2="45" y2="-10" style="animation-delay: 0.2s; animation-duration: 0.9s;" />
      <line class="rain-drop" x1="70" y1="-20" x2="65" y2="-10" style="animation-delay: 0.4s; animation-duration: 0.8s;" />
      <line class="rain-drop" x1="90" y1="-20" x2="85" y2="-10" style="animation-delay: 0.1s; animation-duration: 1.0s;" />
      <line class="rain-drop" x1="110" y1="-20" x2="105" y2="-10" style="animation-delay: 0.3s; animation-duration: 0.75s;" />
      <line class="rain-drop" x1="40" y1="-20" x2="35" y2="-10" style="animation-delay: 0.5s; animation-duration: 0.85s;" />
      <line class="rain-drop" x1="60" y1="-20" x2="55" y2="-10" style="animation-delay: 0.15s; animation-duration: 0.95s;" />
      <line class="rain-drop" x1="80" y1="-20" x2="75" y2="-10" style="animation-delay: 0.45s; animation-duration: 0.72s;" />
      <line class="rain-drop" x1="100" y1="-20" x2="95" y2="-10" style="animation-delay: 0.6s; animation-duration: 0.8s;" />
      <line class="rain-drop" x1="120" y1="-20" x2="115" y2="-10" style="animation-delay: 0.25s; animation-duration: 0.88s;" />
        """
    elif theme == 1:  # Cloudy Theme
        animation_defs = """
    <!-- Cloudy Sky Gradient -->
    <linearGradient id="win-sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#334155" />
      <stop offset="100%" style="stop-color:#64748b" />
    </linearGradient>
    <style>
      @keyframes float {
        0% { transform: translateX(130px); }
        100% { transform: translateX(-80px); }
      }
      .cloud {
        fill: #cbd5e1;
        opacity: 0.7;
        animation: float 25s linear infinite;
      }
      .cloud-slow {
        fill: #94a3b8;
        opacity: 0.5;
        animation: float 40s linear infinite;
      }
    </style>
        """
        animation_content = f"""
      <!-- Sky Background -->
      <rect x="20" y="20" width="110" height="110" fill="url(#win-sky)" />
      
      <!-- Floating Clouds in Background -->
      <g class="cloud-slow" style="animation-delay: -15s; transform: translateY(40px);">
        <rect x="0" y="4" width="30" height="6" rx="3" />
        <rect x="8" y="0" width="16" height="6" rx="3" />
      </g>
      
      {buildings}
      
      <!-- Floating Clouds in Foreground -->
      <g class="cloud" style="animation-delay: -5s; transform: translateY(30px);">
        <rect x="0" y="5" width="24" height="8" rx="4" />
        <rect x="6" y="0" width="14" height="8" rx="4" />
      </g>
      <g class="cloud" style="animation-delay: -18s; transform: translateY(55px);">
        <rect x="0" y="4" width="20" height="6" rx="3" />
        <rect x="5" y="0" width="10" height="6" rx="3" />
      </g>
        """
    else:  # Clear Theme
        if is_day:
            animation_defs = """
    <!-- Clear Day Sky (Sunset/Twilight vibe) -->
    <linearGradient id="win-sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#fdba74" />
      <stop offset="100%" style="stop-color:#f43f5e" />
    </linearGradient>
    <style>
      @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.1); opacity: 1; }
      }
      .sun {
        fill: #fef08a;
        transform-origin: 75px 45px;
        animation: pulse 4s ease-in-out infinite;
      }
      .sun-glow {
        fill: #fde047;
        opacity: 0.25;
        transform-origin: 75px 45px;
        animation: pulse 4s ease-in-out infinite;
        animation-delay: 0.5s;
      }
    </style>
            """
            animation_content = f"""
      <!-- Sky Background -->
      <rect x="20" y="20" width="110" height="110" fill="url(#win-sky)" />
      
      <!-- Pulsating Sun -->
      <circle class="sun-glow" cx="75" cy="45" r="18" />
      <circle class="sun" cx="75" cy="45" r="10" />
      
      {buildings}
            """
        else:
            animation_defs = """
    <!-- Clear Night Sky -->
    <linearGradient id="win-sky" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#020617" />
      <stop offset="100%" style="stop-color:#1e1b4b" />
    </linearGradient>
    <style>
      @keyframes twinkle {
        0%, 100% { opacity: 0.3; }
        50% { opacity: 1; }
      }
      .star {
        fill: #ffffff;
        animation: twinkle 2s infinite ease-in-out;
      }
    </style>
            """
            animation_content = f"""
      <!-- Sky Background -->
      <rect x="20" y="20" width="110" height="110" fill="url(#win-sky)" />
      
      <!-- Twinkling Stars -->
      <rect class="star" x="35" y="35" width="2" height="2" style="animation-delay: 0.0s;" />
      <rect class="star" x="55" y="25" width="1.5" height="1.5" style="animation-delay: 0.5s;" />
      <rect class="star" x="45" y="50" width="2" height="2" style="animation-delay: 1.0s;" />
      <rect class="star" x="105" y="28" width="1.5" height="1.5" style="animation-delay: 1.5s;" />
      <rect class="star" x="115" y="48" width="2" height="2" style="animation-delay: 0.2s;" />
      
      <!-- Moon -->
      <path fill="#fde047" d="M80,30 A12,12 0 1,0 92,42 A9,9 0 1,1 80,30" />
      
      {buildings}
            """

    # Generate complete SVG content
    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="450" height="150" viewBox="0 0 450 150">
  <defs>
    <!-- Background Gradient for Card -->
    <linearGradient id="bg-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a;stop-opacity:0.95" />
      <stop offset="100%" style="stop-color:#1e1b4b;stop-opacity:0.95" />
    </linearGradient>
    <!-- Border Gradient for Card -->
    <linearGradient id="border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#818cf8;stop-opacity:0.8" />
      <stop offset="50%" style="stop-color:#c084fc;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#6366f1;stop-opacity:0.8" />
    </linearGradient>
    
    {animation_defs}
    
    <style>
      .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 700; font-size: 16px; fill: #f8fafc; }}
      .temp {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 800; font-size: 34px; fill: #f8fafc; }}
      .condition {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 500; font-size: 14px; fill: #38bdf8; }}
      .detail-label {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 9px; fill: #64748b; font-weight: bold; letter-spacing: 0.5px; }}
      .detail-val {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-weight: 600; font-size: 12px; fill: #cbd5e1; }}
      .update-time {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; font-size: 9px; fill: #475569; }}
    </style>
    
    <!-- Clip Path for Weather Window -->
    <clipPath id="window-clip">
      <rect x="20" y="20" width="110" height="110" rx="12" />
    </clipPath>
  </defs>
  
  <!-- Card Border and Background -->
  <rect x="2" y="2" width="446" height="146" rx="16" fill="url(#bg-grad)" stroke="url(#border-grad)" stroke-width="2" />
  
  <!-- Weather Window containing Pixel Art Scene -->
  <g>
    <!-- Background Frame -->
    <rect x="20" y="20" width="110" height="110" rx="12" fill="#111827" />
    
    <!-- Clipped Animated Scene -->
    <g clip-path="url(#window-clip)">
      {animation_content}
    </g>
    
    <!-- Foreground Border Frame -->
    <rect x="20" y="20" width="110" height="110" rx="12" fill="none" stroke="#334155" stroke-width="1.5" />
  </g>
  
  <!-- Temperature & Condition Info -->
  <text x="145" y="65" class="temp">{temp}°C</text>
  <text x="145" y="88" class="condition">{emoji} {condition}</text>
  
  <!-- Location Information -->
  <text x="145" y="35" class="title">Bogor, Indonesia</text>
  
  <!-- Vertical Divider -->
  <line x1="300" y1="20" x2="300" y2="130" stroke="#334155" stroke-width="1" stroke-dasharray="3 3" />
  
  <!-- Details Section -->
  <!-- Humidity -->
  <text x="320" y="38" class="detail-label">KELEMBABAN</text>
  <text x="320" y="55" class="detail-val">{humidity}%</text>
  
  <!-- Feels Like -->
  <text x="320" y="80" class="detail-label">TERASA SEPERTI</text>
  <text x="320" y="97" class="detail-val">{feels_like}°C</text>
  
  <!-- Wind Speed -->
  <text x="320" y="122" class="detail-val">{wind_speed} km/h</text>
  <text x="320" y="110" class="detail-label">ANGIN</text>
  
  <!-- Last Update -->
  <text x="145" y="130" class="update-time">Diperbarui: {last_update}</text>
</svg>
"""
    
    # Save the weather.svg file
    output_path = os.path.join(os.path.dirname(__file__), "weather.svg")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(svg_content)
        print(f"Weather SVG successfully updated at {output_path} with Theme ID: {theme}")
    except Exception as e:
        print(f"Error writing SVG file: {e}")

if __name__ == "__main__":
    main()
