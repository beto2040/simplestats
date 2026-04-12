// functions/api/gemini.js
export async function onRequest(context) {
  // Sacamos la clave de las variables de entorno de Cloudflare
  const API_KEY = context.env.GEMINI_API_KEY;
  
  if (!API_KEY) {
    return new Response(JSON.stringify({ 
      error: "Configuración incompleta: No se encontró la API_KEY en el servidor." 
    }), { 
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }

  try {
    const body = await context.request.json();
    
    // CAMBIO CLAVE: Usamos 'v1' y el nombre de modelo 'gemini-1.5-flash'
    const url = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

    const response = await fetch(url, {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    // Retornamos la respuesta de Google a nuestro frontend
    return new Response(JSON.stringify(data), {
      status: response.status, 
      headers: { 
        'Content-Type': 'application/json',
        // Habilitar CORS si es necesario (Cloudflare lo maneja, pero por seguridad)
        'Access-Control-Allow-Origin': '*' 
      }
    });

  } catch (error) {
    return new Response(JSON.stringify({ 
      error: "Error de conexión", 
      details: error.message 
    }), { 
      status: 500,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}