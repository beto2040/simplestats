// functions/api/gemini.js
export async function onRequest(context) {
  const API_KEY = context.env.GEMINI_API_KEY;
  
  if (!API_KEY) {
    return new Response(JSON.stringify({ 
      error: "Error: No se encontró la API_KEY en Cloudflare." 
    }), { status: 500 });
  }

  try {
    const body = await context.request.json();
    
    // URL DEFINITIVA: v1beta y gemini-1.5-flash (sin el -latest)
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    return new Response(JSON.stringify(data), {
      status: response.status, 
      headers: { 
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*' 
      }
    });

  } catch (error) {
    return new Response(JSON.stringify({ 
      error: "Error de servidor", 
      details: error.message 
    }), { status: 500 });
  }
}