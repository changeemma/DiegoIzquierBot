# diego-izquierbot

## Requerimentos
- Instalar claves SSH con el servidor pfSense.
- Python 3.6 o mayor
- pip3
- Telegram API Token

## Instalación de librerías
```bash
pip3 install -r requirements.txt -e .
```
### Notas adicionales

Se deben generar los archivos `*_cfg.py` en base a los archivos `*_cfg.py.example`

## Scripts

### BOTON

Inicia una instancia de `IzquierBot`.

### DORIMON

Monitorea el estado y la configuración de la cámara Doris (`CamDoris`). En caso de que se desconfigure, el script se conecta por telnet para configurarlo.

### GATOMON-SCPCGW/WANGW

Monitorea los gateways (`Gatoway`) y envía alertas cuando alguno de ellos tiene mucha perdida de paquetes o el rtt es alto.
