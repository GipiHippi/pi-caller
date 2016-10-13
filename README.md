# RPI

Damit alles funktioniert muss noch eine config-datei sowie ein plivo account erstellt werden 

Plivo Webseite: https://www.plivo.com/

Beispiel für eine config-datei:
Dateiname number.conf

[settings]  
auth_id = plivo id  
auth_token = plivo token  
from_number = absender nummer  
log_dir = /home/pi/RPI/pi/log  
url = webseite  

[numbers]  
Name = Nummer

