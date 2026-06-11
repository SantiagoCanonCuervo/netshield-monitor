🛡️ NETSHIELD-MONITOR

Sistema de monitoreo de red en Python con alertas en tiempo real por WhatsApp (Twilio)

------------------------------------------------------------

🚀 ¿QUÉ HACE ESTE PROYECTO?

NETSHIELD-MONITOR es una herramienta que:

- 📡 Hace ping automático a IPs y dominios
- 🌐 Detecta fallos de DNS con nslookup
- 📊 Muestra un dashboard en consola en tiempo real
- ⏱ Calcula latencia (ms)
- 📈 Calcula uptime por host
- 🚨 Envía alertas por WhatsApp si hay fallos
- 🧾 Guarda logs automáticos

------------------------------------------------------------

⚙️ INSTALACIÓN

1. Clona el repositorio:

git clone https://github.com/SantiagoCanonCuervo/netshield-monitor.git
cd netshield-monitor

2. Instala dependencias:

pip install -r requirements.txt

------------------------------------------------------------

🔐 CONFIGURACIÓN

1. Copia el archivo de ejemplo:

copy config.example.py config.py

2. Abre config.py y coloca tus credenciales:

TWILIO_SID = "ACxxxxxxxxxxxxxxxx"
TWILIO_AUTH = "xxxxxxxxxxxxxxxx"

TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
TWILIO_WHATSAPP_TO = "whatsapp:+57XXXXXXXXXX"

------------------------------------------------------------

▶️ EJECUCIÓN

python NETSHIELD-MONITOR.py

------------------------------------------------------------

🧠 CÓMO FUNCIONA

El sistema trabaja en ciclos:

1. Hace ping a cada host
2. Si responde → registra OK
3. Si falla → ejecuta nslookup
4. Clasifica el error:
   - DNS
   - servidor caído
   - problema de red
5. Si es crítico → envía alerta por WhatsApp

------------------------------------------------------------

📊 DASHBOARD

Muestra en consola:

- Estado del host 🟢🟡🔴
- Uptime %
- Latencia promedio

------------------------------------------------------------

🧾 LOGS

Se guardan en:

monitor_logs.txt (misma carpeta de ejecución)

------------------------------------------------------------

📦 REQUISITOS

- Python 3.8+
- Twilio API

Instalar dependencias:

pip install twilio

------------------------------------------------------------

🧑‍💻 AUTOR

SANTIAGO CAÑON CUERVO

Proyecto creado para monitoreo de redes tipo NOC con NETSHIELD-MONITOR