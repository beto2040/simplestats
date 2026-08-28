🎯 Plan Maestro Definitivo: E-commerce de Bases de Datos (Data Brokerage)
Objetivo Principal: Validar y construir un sistema automatizado de extracción de prospectos (leads) B2B usando la cuota gratuita de Google Places API, enriquecido con web scraping cuidadoso, y vendido como archivos CSV pasivos.

Pilar de Seguridad Absoluta:

Límite de API: El código incluirá un "botón de apagado" automático a las 4,800 peticiones para jamás superar las 5,000 del mes calendario (reinicio el día 1 a las 00:00 UTC).

Anti-Bloqueo: El scraper secundario de correos usará tiempos de espera aleatorios (3 a 7 segundos) y rotación de User-Agents para proteger la IP del servidor.

🧪 Fase 0: El Mini-MVP (Prueba de Concepto Inmediata)
Extracción Mínima: Ejecutar el script solo para extraer 50 negocios.

Enriquecimiento: Extraer correos de solo 10 de esos negocios para probar la lógica.

Enmascaramiento: Aplicar la lógica de Pandas para ocultar teléfonos y correos.

Validación de Mercado: Publicar el CSV de muestra en grupos de emprendedores (ej. Facebook) para medir la demanda real antes de construir el resto de la infraestructura.

🛠️ Fase 1: Extracción Segura (El Motor en Python)
Búsqueda Primaria: Usar Text Search (Google Places API) para obtener la lista inicial y filtrar exclusivamente los negocios que tengan sitio web.

Búsqueda Detallada: Usar Place Details solo en los filtrados para extraer: Nombre, Teléfono, Sitio Web y Calificación.

Scraper Secundario (Correos): Con BeautifulSoup, visitar las webs resultantes respetando siempre el archivo robots.txt de cada página para extraer el email de contacto.

🗄️ Fase 2: Limpieza y Formato (PostgreSQL / Pandas)
Transformación: Usar pandas para estructurar datos, eliminar duplicados y usar librerías como phonenumbers para validar el formato nacional.

CSV Premium: Base de datos completa, limpia y lista para la venta.

CSV Freemium: Base de datos con los datos de contacto ofuscados mediante funciones lambda en Pandas (ej. los teléfonos conservan 2 dígitos y se rellenan con 'X', los correos muestran solo un fragmento).

💳 Fase 3: Pasarela de Pago y Escaparate
Infraestructura Base: Landing Page en GitHub Pages.

Plataforma Inicial: Usar Gumroad para la venta del CSV completo. Es ideal para empezar de inmediato con depósitos a cuentas CLABE sin los requisitos de registro empresarial temprano. (Migración futura a Stripe al superar los $500 USD/mes).

Flujo: El usuario descarga la muestra Freemium en la Landing Page -> Clic en comprar -> Gumroad procesa tarjeta y entrega el CSV Premium automáticamente.

🚀 Fase 4: Tráfico (Corto y Largo Plazo)
Manual (Primeras ventas): Foros, LinkedIn y Reddit.

Automático (SEO Programático): Generar plantillas HTML por nicho y ciudad para posicionamiento orgánico en Google (estrategia a 3-6 meses).