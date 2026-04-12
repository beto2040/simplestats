// functions/api/gemini.js
export async function onRequest(context) {
  // Sacamos la clave de las variables de entorno de Cloudflare
  const API_KEY = context.env.GEMINI_API_KEY;
  
  if (!API_KEY) {
    return new Response(JSON.stringify({ error: "Configuración incompleta en el servidor." }), { status: 500 });
  }

  try {
    const body = await context.request.json();
    
    // Hacemos la petición desde el servidor de Cloudflare a Google
    const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    const data = await response.json();
    
    return new Response(JSON.stringify(data), {
      headers: { 'Content-Type': 'application/json' }
    });

  } catch (error) {
    return new Response(JSON.stringify({ error: "Fallo en la comunicación segura." }), { status: 500 });
  }
}