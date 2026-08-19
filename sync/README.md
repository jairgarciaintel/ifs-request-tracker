# sync/ — Carpeta compartida entre compus

Pon aqui cualquier archivo que quieras compartir entre las dos compus
(notas, scripts de Power Automate, HTML de correos, instrucciones, etc.).

Este repo (ifs-request-tracker) sincroniza bien en ambas compus, asi que
lo que dejes aqui lo tienes en las dos y Kiro lo puede leer/escribir.

## Como usar
En cualquier compu:

    cd ".../Dashboards Analysis/Request-Tracker"
    git pull            # traer lo ultimo
    # (editas o agregas archivos en sync/)
    git add sync/
    git commit -m "update sync"
    git push origin main

## IMPORTANTE — este es un repo PUBLICO
NUNCA pongas aqui tokens, PATs, contrasenas ni credenciales.
Esos van en el l4ve del repo dev (privado), que el .gitignore bloquea aqui.
