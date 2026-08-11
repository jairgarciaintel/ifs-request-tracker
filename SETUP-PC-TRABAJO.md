# Setup — PC de Trabajo (Windows)

## Una sola vez (instalación):

```powershell
# 1. Clona el repo (si no lo tienes)
git clone https://github.com/jairgarciaintel/ifs-request-tracker.git
cd ifs-request-tracker

# 2. Instala dependencias de Python
pip install watchdog openpyxl

# 3. Configura el remote con tu token (copia de .kiro/hooks/l4ve)
git remote set-url origin "https://jairgarciaintel:TU_TOKEN_AQUI@github.com/jairgarciaintel/ifs-request-tracker.git"
```

## Cada día (uso normal):

```powershell
# 1. Abre PowerShell en la carpeta del proyecto
cd C:\MEGA\Intel\2026\FS-Tracker\ifs-request-tracker

# 2. Arranca el watcher (déjalo corriendo en background)
python watcher.py
```

## Para actualizar datos de SharePoint:

1. Abre `https://intel.sharepoint.com/sites/ifs-igo-requests/Lists/New%20DA%20Request/Customer%20View.aspx`
2. Click **Export** (descarga un `.iqy`)
3. Abre el `.iqy` en Excel
4. **File → Save As** → guárdalo como `data/requests.xlsx` (en la carpeta del repo)
5. El watcher detecta el archivo nuevo → convierte → pushea automático
6. La página se actualiza en ~1 minuto

## Si el watcher no está corriendo:

```powershell
python convert_excel.py
```

Eso convierte y pushea manualmente.

## URLs importantes:

- **Página**: https://jairgarciaintel.github.io/ifs-request-tracker/
- **Repo**: https://github.com/jairgarciaintel/ifs-request-tracker
- **Firebase**: https://fs-request-tracker-default-rtdb.firebaseio.com/
- **SharePoint**: https://intel.sharepoint.com/sites/ifs-igo-requests

## Notas:

- El token de GitHub está en `.kiro/hooks/l4ve` del repo de hackerjj
- El watcher solo detecta archivos `.xlsx` en la carpeta `data/`
- Los sub-steps que tú y Jenn editan se guardan en Firebase (no se pierden al actualizar el Excel)
