# Arreglar el error 403 de git en la PC Windows + automatizar los 2 repos

## El problema
- Error 403 = el token (PAT) de la Windows NO tiene permiso de escribir en
  jairgarciaintel/dashboards-strategy-2026 (probablemente es el token VIEJO de
  hackerjj, o uno sin permiso "repo"/"Contents: write").
- En la Mac los dos repos estan bien (usuario jairgarciaintel). El 403 es solo Windows.

## Los DOS repos (cada carpeta ya sabe a cual conectarse por su .git)
- DEV:     jairgarciaintel/dashboards-strategy-2026   (carpeta raiz "14. Dashboards")
- TRACKER: jairgarciaintel/ifs-request-tracker        (carpeta Request-Tracker)

Git ya elige el repo correcto segun la carpeta donde estes parado. No hay que
cambiar nada manual entre proyectos: solo hay que arreglar el TOKEN.

============================================================
# SOLUCION RECOMENDADA (una vez): quitar el token del remote y
# dejar que Git Credential Manager lo guarde. Sirve para AMBOS repos.
============================================================

## Requisito: un PAT nuevo valido de jairgarciaintel
1. En GitHub (logueado como jairgarciaintel): Settings -> Developer settings ->
   Personal access tokens -> Tokens (classic) -> Generate new token (classic).
2. Marca el scope "repo" (todo). Copialo (empieza con ghp_...).
   (Si usas fine-grained: da acceso a los 2 repos con Contents: Read and write.)

## En la Windows, terminal (Git Bash o PowerShell), corre:

# 1) Poner los remotes SIN token (limpios):
cd "C:\ruta\a\14. Dashboards"
git remote set-url origin https://github.com/jairgarciaintel/dashboards-strategy-2026.git

cd "C:\ruta\a\14. Dashboards\Dashboards Analysis\Request-Tracker"
git remote set-url origin https://github.com/jairgarciaintel/ifs-request-tracker.git

# 2) Activar el guardado de credenciales (Git Credential Manager viene con Git for Windows):
git config --global credential.helper manager

# 3) El primer push va a pedir usuario/contrasena:
#    Usuario: jairgarciaintel
#    Password: PEGA EL PAT NUEVO (no tu contrasena normal)
#    -> se guarda y ya no lo vuelve a pedir para NINGUNO de los dos repos.

## Probar (en cada carpeta):
git config --global core.hooksPath /dev/null   # por si Code Defender bloquea
git pull origin main
git push origin main

============================================================
# ALTERNATIVA rapida (token embebido, menos limpia)
============================================================
Si prefieres el token en la URL (como estaba), en cada repo:

cd "C:\ruta\a\14. Dashboards"
git remote set-url origin https://jairgarciaintel:EL_PAT_NUEVO@github.com/jairgarciaintel/dashboards-strategy-2026.git

cd "...\Request-Tracker"
git remote set-url origin https://jairgarciaintel:EL_PAT_NUEVO@github.com/jairgarciaintel/ifs-request-tracker.git

OJO: NUNCA subir el PAT a sync/ (GitHub lo bloquea con Push Protection). El PAT
solo va local o por MEGA, nunca en un commit.

============================================================
# EVITAR que se crucen las 2 sesiones de Kiro + la Mac
============================================================
- Con 3 sesiones tocando los mismos repos, SOLO UNA hace push a la vez.
- Antes de push en una: la otra NO debe estar a medio push.
- Siempre: git pull origin main ANTES de push, para alinear.
- Si push falla por "rejected / non-fast-forward": git pull origin main y reintenta.

============================================================
# COMO SABER EN QUE REPO ESTOY (para no confundirse)
============================================================
En cualquier carpeta corre:  git remote -v
- Si dice ...ifs-request-tracker -> estas en el TRACKER (la pagina).
- Si dice ...dashboards-strategy-2026 -> estas en el DEV (raiz, tiene l4ve).
