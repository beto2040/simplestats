// functions/api/gemini.js
export async function onRequest(context) {
  // Sacamos la clave de las variables de entorno de Cloudflare
  const API_KEY = context.env.GEMINI_API_KEY;
  
  if (!API_KEY) {
    return new Response(JSON.stringify({ error: "Configuración incompleta en el servidor." }), { status: 500 });
  }

  try {
    const body = await context.request.json();
    
    // CAMBIO IMPORTANTE: Usamos 'gemini-1.5-flash-latest' para evitar el error 404
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${API_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    const data = await response.json();
    
    // Pasamos el status real de Google para que tu catch en el frontend funcione mejor
    return new Response(JSON.stringify(data), {
      status: response.status, 
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: "Fallo en la comunicación segura." }), { status: 500 });
  }
}