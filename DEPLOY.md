# FS Request Tracker — Deploy & Scripts

Guia rapida para actualizar y desplegar el tracker desde cualquier compu.
Este archivo NO contiene tokens ni credenciales (esos viven en el repo dev privado).

## Repos (NO confundir)
- **TRACKER** (este repo, PUBLICO): `jairgarciaintel/ifs-request-tracker`
  - Es lo que sirve la pagina: https://jairgarciaintel.github.io/ifs-request-tracker/
  - Aqui va: index.html, data/, guide/, Logo.png, watcher.py
- **DEV** (privado): `hackerjj/dashboards-strategy-2026`
  - Aqui van: notas, contexto, credenciales (l4ve). NO la pagina.

## Deploy / actualizar la pagina (repo TRACKER)
```
git config --global core.hooksPath /dev/null
git pull origin main
git add .
git commit -m "mensaje"
git push origin main
```
GitHub Pages redepliega solo en 1-2 min despues del push.

Si el push falla con "Authentication failed", el remote se desconfiguro.
El comando para arreglarlo (con el token) esta en el l4ve del repo dev privado.
Formato del remote correcto (sin el token):
  https://jairgarciaintel:<PAT>@github.com/jairgarciaintel/ifs-request-tracker.git

## Setup en PC de trabajo (watcher)
1. pip install watchdog openpyxl
2. cd a la carpeta del repo tracker
3. git pull
4. python watcher.py   (dejarlo corriendo)

## Actualizar datos
- SharePoint > Export CSV > guardar como data/requests.csv
- (o) Export a Excel > guardar como data/requests.xlsx
- El watcher detecta el cambio y pushea solo.

## PDF -> Word
Script incluido: pdf_to_word.py  (usa: python3 pdf_to_word.py)

## Correo automatico "Acknowledged"
- El HTML del correo lo genera el tracker (funcion buildAckEmailHtml en index.html).
- Se manda via flow de Power Automate (campo bodyHtml).
- Para cambiar el diseno: editar buildAckEmailHtml + push. No se toca Power Automate.
- Configuracion del flow: ver l4ve (repo dev privado).
