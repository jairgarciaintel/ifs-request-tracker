# Chatbot con IA real (Gemini) - SETUP PASO A PASO

Objetivo: que el chatbot use IA de verdad (Gemini) para responder cualquier
pregunta, SIN exponer la API key en la pagina publica.

Arquitectura segura:
  Pagina (chatbot)  ->  Flow Power Automate (esconde la key)  ->  Gemini  ->  respuesta

La key NUNCA va en index.html (es publico en GitHub). Va escondida en el flow.

============================================================
## PARTE 1 - Crear proyecto y API key en Google Cloud Console
============================================================
(Como NO tienes acceso a AI Studio, se crea la key desde Cloud Console.)

### Paso 1.1 - Crear un proyecto
1. Entra a  https://console.cloud.google.com/
2. Arriba, junto al logo "Google Cloud", clic en el selector de proyecto.
3. Clic en "New Project" (Nuevo proyecto).
4. Nombre: por ejemplo  fs-tracker-ai   -> Create.
5. Espera ~10 seg y selecciona ese proyecto (que quede activo arriba).

### Paso 1.2 - Habilitar la API de Gemini
1. Menu (izquierda) -> "APIs & Services" -> "Library".
2. En el buscador escribe:  Generative Language API
3. Entra al resultado "Generative Language API" -> boton "ENABLE" (Habilitar).
   (Si te pide habilitar billing/facturacion, ver NOTA abajo.)

### Paso 1.3 - Crear la API key
1. Menu -> "APIs & Services" -> "Credentials".
2. Arriba: "+ CREATE CREDENTIALS" -> "API key".
3. Copia la key que aparece (empieza con  AIza... ). Guardala en un lugar seguro.
4. (Recomendado) Clic en "Edit API key" -> en "API restrictions" elige
   "Restrict key" -> marca solo "Generative Language API" -> Save.
   Asi esa key solo sirve para Gemini.

### NOTA sobre billing
- La Generative Language API tiene un tier GRATIS, pero Google a veces pide una
  tarjeta para "habilitar billing" aunque no cobre dentro del tier gratis.
- Si Intel no te deja poner tarjeta o billing, avisame: cambiamos de modelo
  (ej. Groq, que no pide tarjeta) o dejamos el FAQ.

### Si Cloud Console NO te deja (Intel lo bloquea)
- Puede que el tenant de Intel bloquee crear proyectos o habilitar APIs externas.
- Si te topas con "permission denied" o similar, dimelo y vamos a plan B.

### ERROR "you must select a parent organization folder / no organization"
Esto pasa porque estas usando tu CUENTA DE INTEL: Intel tiene una organizacion
que te obliga a crear el proyecto dentro de ella (y no te da permiso).

SOLUCION 1 (recomendada): usar una cuenta PERSONAL de Gmail (no la de Intel).
1. En Cloud Console, cierra sesion de la cuenta Intel.
2. Entra con una cuenta @gmail.com personal (o crea una gratis solo para esto).
3. Al crear el proyecto, en "Organization/Location" te saldra "No organization"
   -> esa ES la opcion correcta (no es error), y AHI SI te deja crear el proyecto.
4. Sigue igual: Enable "Generative Language API" -> crear API key.
Es valido: la key solo sirve para que el chatbot responda dudas; no toca datos
de Intel ni SharePoint.

SOLUCION 2 (si no quieres usar Gmail personal): usar GROQ en vez de Gemini.
Groq da API key gratis SIN proyecto, SIN organizacion y SIN tarjeta. Ver la
seccion "PLAN B - GROQ" al final de este archivo.

============================================================
## PARTE 2 - Probar que Gemini responde (rapido, sin Power Automate)
============================================================
Antes de montar el flow, confirma que la key sirve. En una terminal (o en el
navegador con un cliente REST), prueba:

curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=TU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Say hello in one short sentence."}]}]}'

- Si responde un JSON con texto -> la key sirve. Sigue a la Parte 3.
- Si da error 403 / API not enabled -> falta habilitar la API (Paso 1.2).
- Si da error de billing -> ver NOTA de billing arriba.

(No corras esto en la PC de Intel si te preocupa la red corporativa; puedes
probarlo desde tu telefono/casa. Es solo para validar la key.)

============================================================
## PARTE 3 - Flow de prueba en Power Automate (esconde la key)
============================================================
IMPORTANTE: antes vimos que el conector HTTP de Office 365 en tu tenant dio
error 411 al llamar APIs externas (Firebase). Este flow usa la accion "HTTP"
(premium) para llamar a Gemini. Hay que probar si tu tenant lo permite.

### Paso 3.1 - Crear el flow
1. Power Automate -> Create -> "Instant cloud flow".
2. Nombre:  FS Tracker AI Chat
3. Trigger: "When an HTTP request is received" (manual / HTTP).
4. En el trigger, "Request Body JSON Schema", pega:
   {
     "type": "object",
     "properties": {
       "question": { "type": "string" }
     }
   }

### Paso 3.2 - Accion HTTP a Gemini
1. + New step -> busca "HTTP" -> accion "HTTP".
2. Method:  POST
3. URI:
   https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=TU_API_KEY
   (pega TU_API_KEY aqui; queda escondida en el flow, no en la pagina)
4. Headers:
   Content-Type : application/json
5. Body:
   {
     "contents": [
       { "parts": [ { "text": "@{triggerBody()?['question']}" } ] }
     ]
   }

### Paso 3.3 - Responder al chatbot
1. + New step -> busca "Response" (accion "Response", del conector Request).
2. Status Code: 200
3. Headers:  Content-Type : application/json
4. Body: pon esta expresion para regresar solo el texto de Gemini:
   {
     "answer": "@{body('HTTP')?['candidates']?[0]?['content']?['parts']?[0]?['text']}"
   }
   (si el nombre de la accion HTTP no es 'HTTP', ajusta body('HTTP') al nombre real)
5. Guarda el flow.

### Paso 3.4 - Copiar la URL del trigger
1. Abre el trigger "When an HTTP request is received".
2. Copia el campo "HTTP POST URL" (una URL larga con sig=...).
3. Pegala abajo en este archivo, en AI_CHAT_URL.

### Paso 3.5 - Probar el flow solo
Usa la prueba manual del flow o un curl:
curl "PEGAR_AI_CHAT_URL" -H "Content-Type: application/json" \
  -d '{"question":"What is the FS Request Tracker?"}'

- Si regresa {"answer":"..."} -> FUNCIONA. Avisame y conecto el chatbot.
- Si da 411 / bloqueado -> el tenant no deja salir; vamos a plan B.

============================================================
## AI_CHAT_URL (pegar aqui cuando tengas el flow)
============================================================
AI_CHAT_URL: (pegar aqui la HTTP POST URL del trigger)

============================================================
## PARTE 4 - Que hare yo cuando la prueba funcione
============================================================
- Conectar el chatbot (tracker + guia) a AI_CHAT_URL.
- Mantener el FAQ como respaldo: primero intenta responder local (instantaneo);
  si no encuentra, le pregunta a Gemini (IA real).
- Darle a Gemini un "system prompt" con el contexto del tracker para que responda
  bien sobre nuestra herramienta.
- El boton "Report it" (bugs/features por correo) se queda igual.

============================================================
## PLAN B (si Power Automate no puede llamar a Gemini - error 411)
============================================================
Opciones si el tenant bloquea la llamada:
1. Groq en vez de Gemini (mismo esquema de flow) - por si el bloqueo es solo a Google.
2. Una funcion serverless gratis (Cloudflare Workers / Vercel) como intermediario
   en vez de Power Automate. Esconde la key igual y casi no tiene limites de red.
3. Quedarnos con el FAQ ampliado (lo actual) - cero costo, cero riesgo.

Dime como sale la Parte 2 y 3 y seguimos.

============================================================
## PLAN B - GROQ (API key gratis, SIN proyecto ni organizacion ni tarjeta)
============================================================
Groq corre modelos Llama (rapidos) y da API gratis con solo registrarte. Ideal
si Cloud Console te bloquea por la organizacion de Intel.

### B.1 - Obtener la key de Groq
1. Entra a  https://console.groq.com/
2. Registrate (puedes usar Google o correo). No pide tarjeta.
3. Menu "API Keys" -> "Create API Key" -> copia la key (empieza con  gsk_... ).

### B.2 - Probar la key (opcional, rapido)
curl "https://api.groq.com/openai/v1/chat/completions" \
  -H "Authorization: Bearer TU_GROQ_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"llama-3.3-70b-versatile","messages":[{"role":"user","content":"Say hi in one sentence."}]}'
- Si responde JSON con texto -> sirve.

### B.3 - Flow de Power Automate para Groq
Igual que la Parte 3, pero la accion HTTP cambia:
- Method: POST
- URI:  https://api.groq.com/openai/v1/chat/completions
- Headers:
    Authorization : Bearer TU_GROQ_KEY
    Content-Type  : application/json
- Body:
  {
    "model": "llama-3.3-70b-versatile",
    "messages": [
      { "role": "system", "content": "You are the FS Request Tracker help assistant. Answer briefly about how to use the tracker." },
      { "role": "user", "content": "@{triggerBody()?['question']}" }
    ]
  }
- Response Body:
  {
    "answer": "@{body('HTTP')?['choices']?[0]?['message']?['content']}"
  }

Pega la URL del trigger en AI_CHAT_URL (arriba) igual que con Gemini.

### Nota
Sea Gemini o Groq, el chatbot en la pagina se conecta IGUAL (manda {question},
recibe {answer}). Solo cambia el flow por dentro. Asi que puedes elegir el que
te deje tu red/permisos y yo conecto el chatbot al AI_CHAT_URL sin importar cual.
