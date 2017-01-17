# Alamierung für Defibrillator Einsatz

## Einführung
In der Firma Lippuner EMT sind im Werk 1-3 insgesamt 8 Notfallbuttons für die Alamierung eingerichtet. Die Buttons sind jeweils über eine Zweidraht-Leitung (Telefoninstallation) an eine Alamierungszentrale (Raspberry Pi) angeschlossen.

Dieses Repository enthält alle Scripts die für den Betrieb der Alamierungszentrale:
- defiscript.py: Das eigentliche Script welches den zustand der Buttons überwacht
- callerscripts/script0x.py : ein script pro button welches den Anruf tätigt und die Alarmmeldung abspielt.
- misc/defi_start : init script um defiscript beim system start auszuführen.
- misc/check_plivo_accout_credit : Bash Script um coinpolice.py als cronjob zu starten.
- misc/coinpolice.py : Script um das Guthaben vom plivo Account abzufragen und bei Unterschreitung eines Mindestwertes ein Warnhinweis per Mail zu versenden

### Weitere Dokumentation
Dokumentation: https://intranet.lemt.local/teams/it/System/Dokumentation/Defi-Alamirung.aspx 

Plivo Webseite: https://www.plivo.com/ 

## Installation

1. Repository von GitHub clonen (z.b. ins Home Verzeichnis):
   ```
   git clone https://github.com/LippDevTeam/pi-caller.git
   ```

2. Alles (ausser .git files) nach /opt/lemt kopieren
   ```
   sudo mkdir /opt/lemt
   sudo cp -r pi-caller/ /opt/lemt/
   ```

3. Ins Verzeichnis wechseln
   ```
   cd /opt/lemt/pi-caller/
   ```
   
4. Scripts ausführbar machen
   ```
   sudo chmod +x defiscript.py
   ```
   
5. Init Script ausführbar machen und ins init.d verschieben
   ```
   sudo chmod +x misc/defi_start
   sudo chown root:root misc/defi_start
   sudo mv misc/defi_start /etc/init.d/
   ```

6. Cronjob einrichten
   ```
   sudo chmod +x misc/check_plivo_accout_credit
   sudo chown root:root misc/check_plivo_accout_credit
   sudo mv misc/check_plivo_accout_credit /etc/cron.daily
   ```

