# Sonidos: nuevo ticket (tracker) y correo del tracker (Outlook)

## SONIDO 1 - Nuevo ticket (YA HECHO en el tracker, v1.8.43)
- La pagina suena una campanita cuando aparece un request nuevo al refrescar
  (compara IDs; si llega un ID que no estaba, suena).
- Boton "Sound / Muted" (icono de campana) en la barra de herramientas para
  prender/apagar. Se recuerda.
- El sonido se genera en el navegador (Web Audio API), NO usa archivo mp3/wav.
  Por eso siempre funciona y no hay que hostear nada.
- NOTA del navegador: por seguridad, el audio se "desbloquea" con el primer clic
  en la pagina. Con darle una vez al boton de sonido (o cualquier clic) queda listo.
- La pagina debe estar ABIERTA para que suene (es un sonido de la web, no del SO).

## SONIDO 2 - Cuando llega un correo del tracker (en Outlook)
Outlook NO puede sonar "cuando un correo se mueve a un folder". Pero SI puede sonar
cuando llega un correo que cumple una regla. Usamos la MISMA regla que mueve las
notificaciones al folder y le agregamos "reproducir un sonido".

### Importante sobre wav/mp3/mp4
- Outlook de escritorio (Windows) permite ELEGIR UN ARCHIVO .WAV para el sonido de
  la regla. Solo acepta .WAV (no mp3 ni mp4). Si tienes un mp3, hay que convertirlo
  a wav (se puede con cualquier convertidor online o con: ffmpeg -i sonido.mp3 sonido.wav).
- Outlook WEB (navegador) NO deja poner sonido personalizado por regla; solo la
  notificacion estandar. Para sonido personalizado usa Outlook de ESCRITORIO (Windows).

### Pasos (Outlook de escritorio - Windows)
1. File -> Manage Rules & Alerts -> New Rule.
2. "Apply rule on messages I receive" -> Next.
3. Condiciones (para que sea SOLO notificaciones del tracker, no respuestas de cliente):
   - "with specific words in the subject" -> escribe:  REQ.
   - "from people or public group" -> la cuenta que manda el flow
     (tu cuenta jair.garcia@intel.com, o fs.da.ops@intel.com si el flow usa esa).
   (Las respuestas del cliente vienen de SU correo y con "RE:", no cumplen el "from").
4. Next -> Acciones:
   - "move it to the specified folder" -> elige tu carpeta (ej. FS Tracker).
   - "play a sound" -> elige tu archivo .WAV.
5. Next -> (sin excepciones) -> Finish. Activa la regla.

### Resultado
- Notificacion del tracker (from = tu/flow, subject con REQ.) -> va a la carpeta
  Y suena tu .wav.
- Cliente RESPONDE (from = cliente, subject RE: REQ.) -> NO cumple el "from",
  se queda en el INBOX y no suena.

### Si quieres un wav
- Puedes usar uno de los sonidos de Windows (C:\Windows\Media\*.wav), o
- convertir un mp3/mp4 tuyo a wav (ffmpeg -i entrada.mp3 salida.wav) y elegir ese.
- Guarda el .wav en una ruta fija (ej. Documentos) para que Outlook siempre lo halle.

## Resumen
- Sonido cuando entra ticket nuevo -> en la PAGINA del tracker (ya hecho).
- Sonido cuando llega correo del tracker -> en la REGLA de Outlook escritorio, con
  "play a sound" (.wav) en la misma regla que lo mueve al folder.
