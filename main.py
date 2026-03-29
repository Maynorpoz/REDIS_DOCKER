"""
Reservar Cancha - API MVP de Reservas de Canchas de Fútbol
==========================================================
Tarea 2 - Análisis de Sistemas

Cómo ejecutar:
    pip install -r requirements.txt
    uvicorn main:app --reload

Documentación interactiva:
    http://localhost:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum
import uuid


# ==============================================================
# 1. Configuración de la Aplicación
# ==============================================================

app = FastAPI(
    title="Reservar Cancha API",
    description=(
        "API REST para la gestión de reservas de canchas de fútbol. "
        "Permite a jugadores buscar canchas, verificar disponibilidad y crear reservas. "
        "Los administradores pueden gestionar el estado de los turnos del día."
    ),
    version="1.0.0",
    contact={
        "name": "Administrador del Sistema",
        "email": "admin@reservarcancha.com",
    },
    docs_url=None,
    redoc_url=None,
)


@app.get("/docs", include_in_schema=False)
async def documentacion_personalizada():
    html = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Reservar Cancha — API Docs</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css"/>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      background: #0d1117;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    /* ── BARRA SUPERIOR ── */
    .swagger-ui .topbar {
      background: linear-gradient(90deg, #0d2a1a 0%, #0d1117 60%, #0a1929 100%);
      border-bottom: 2px solid #22c55e;
      padding: 14px 0;
    }
    .swagger-ui .topbar .download-url-wrapper { display: none; }
    .swagger-ui .topbar-wrapper img { display: none; }
    .swagger-ui .topbar-wrapper::before {
      content: "⚽  Reservar Cancha API";
      color: #22c55e;
      font-size: 1.4rem;
      font-weight: 700;
      letter-spacing: 1px;
      padding-left: 24px;
      text-shadow: 0 0 16px rgba(34,197,94,0.4);
    }

    /* ── FONDO GENERAL ── */
    .swagger-ui { background: #0d1117; color: #e6edf3; }
    .swagger-ui .wrapper { background: #0d1117; }

    /* ── SECCIÓN INFO ── */
    .swagger-ui .information-container {
      background: linear-gradient(135deg, #0d2a1a 0%, #0d1f3a 100%);
      border-radius: 12px;
      border: 1px solid #22c55e33;
      box-shadow: 0 4px 24px rgba(34,197,94,0.08);
      margin: 20px 0;
      padding: 28px 32px;
    }
    .swagger-ui .info .title {
      color: #22c55e !important;
      font-size: 2.2rem;
      font-weight: 800;
      text-shadow: 0 0 20px rgba(34,197,94,0.35);
    }
    .swagger-ui .info .title small { color: #4ade8099; font-size: 1rem; }
    .swagger-ui .info p, .swagger-ui .info li { color: #8b949e; }
    .swagger-ui .info a { color: #4ade80; }

    /* ── SERVIDOR ── */
    .swagger-ui .scheme-container {
      background: #161b22;
      border: 1px solid #30363d;
      border-radius: 8px;
      box-shadow: none;
      padding: 16px 24px;
    }
    .swagger-ui .scheme-container label { color: #8b949e; }
    .swagger-ui .servers > label select {
      background: #0d1117;
      border: 1px solid #30363d;
      color: #e6edf3;
      border-radius: 6px;
      padding: 6px 10px;
    }

    /* ── ETIQUETAS DE GRUPO ── */
    .swagger-ui .opblock-tag {
      color: #4ade80 !important;
      border-bottom: 1px solid #21262d !important;
      font-size: 1.15rem;
      font-weight: 700;
      padding: 14px 4px;
    }
    .swagger-ui .opblock-tag:hover { background: #161b2280 !important; border-radius: 6px; }
    .swagger-ui .opblock-tag-section h4 { color: #8b949e; font-size: 0.9rem; }

    /* ── BLOQUES DE OPERACIÓN (base) ── */
    .swagger-ui .opblock {
      border-radius: 10px;
      margin: 8px 0;
      border: 1px solid #30363d;
      background: #161b22;
      transition: box-shadow 0.2s ease;
    }
    .swagger-ui .opblock:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.4); }

    /* GET */
    .swagger-ui .opblock.opblock-get { border-color: #1d4ed840; background: #0c1929; }
    .swagger-ui .opblock.opblock-get .opblock-summary { background: #0c192980; border-bottom: 1px solid #1d4ed840; }
    .swagger-ui .opblock.opblock-get .opblock-summary-method { background: #1d4ed8; border-radius: 6px; }

    /* POST */
    .swagger-ui .opblock.opblock-post { border-color: #15803d40; background: #0a1f0a; }
    .swagger-ui .opblock.opblock-post .opblock-summary { background: #0a1f0a80; border-bottom: 1px solid #15803d40; }
    .swagger-ui .opblock.opblock-post .opblock-summary-method { background: #15803d; border-radius: 6px; }

    /* PATCH */
    .swagger-ui .opblock.opblock-patch { border-color: #d9770640; background: #1a1200; }
    .swagger-ui .opblock.opblock-patch .opblock-summary { background: #1a120080; border-bottom: 1px solid #d9770640; }
    .swagger-ui .opblock.opblock-patch .opblock-summary-method { background: #d97706; border-radius: 6px; }

    /* DELETE */
    .swagger-ui .opblock.opblock-delete { border-color: #dc262640; background: #1a0a0a; }
    .swagger-ui .opblock.opblock-delete .opblock-summary { background: #1a0a0a80; border-bottom: 1px solid #dc262640; }
    .swagger-ui .opblock.opblock-delete .opblock-summary-method { background: #dc2626; border-radius: 6px; }

    /* Badges de método */
    .swagger-ui .opblock-summary-method {
      font-weight: 700; letter-spacing: 1px;
      min-width: 75px; text-align: center;
      padding: 5px 10px; font-size: 0.8rem;
    }

    /* Ruta y descripción */
    .swagger-ui .opblock-summary-path { color: #e6edf3 !important; font-weight: 500; }
    .swagger-ui .opblock-summary-description { color: #8b949e !important; font-style: italic; }

    /* ── CUERPO EXPANDIDO ── */
    .swagger-ui .opblock-body { background: #0d1117; border-radius: 0 0 10px 10px; }
    .swagger-ui .opblock-description-wrapper p { color: #8b949e; padding: 12px 0; }

    /* ── PARÁMETROS ── */
    .swagger-ui .parameters-container { background: #161b22; border-radius: 6px; padding: 8px 12px; }
    .swagger-ui table.parameters { background: transparent; }
    .swagger-ui table thead tr th { color: #22c55e; border-bottom: 1px solid #30363d; background: transparent; font-size: 0.85rem; }
    .swagger-ui table tbody tr td { color: #e6edf3; border-bottom: 1px solid #21262d; background: transparent; }
    .swagger-ui .parameter__name { color: #79c0ff; font-weight: 600; }
    .swagger-ui .parameter__type { color: #a5f3a5; font-size: 0.82rem; }
    .swagger-ui .parameter__in { color: #f59e0b99; font-size: 0.78rem; font-style: italic; }
    .swagger-ui .parameter__deprecated { color: #dc2626; }

    /* ── BOTONES ── */
    .swagger-ui .btn { border-radius: 6px; font-weight: 600; transition: all 0.18s ease; cursor: pointer; }
    .swagger-ui .btn.try-out__btn { background: #1a3a2a; border: 1px solid #22c55e; color: #22c55e; }
    .swagger-ui .btn.try-out__btn:hover { background: #22c55e; color: #0d1117; }
    .swagger-ui .btn.execute { background: #22c55e; border-color: #22c55e; color: #0d1117; font-weight: 700; padding: 8px 24px; }
    .swagger-ui .btn.execute:hover { background: #16a34a; }
    .swagger-ui .btn.btn-clear { background: transparent; border: 1px solid #6e7681; color: #8b949e; }
    .swagger-ui .btn.btn-clear:hover { border-color: #dc2626; color: #dc2626; }
    .swagger-ui .btn.authorize { background: #1a3a2a; border: 1px solid #22c55e; color: #22c55e; }
    .swagger-ui .btn.authorize:hover { background: #22c55e; color: #0d1117; }
    .swagger-ui .btn.modal-btn-action.authorize { background: #22c55e; color: #0d1117; }
    .swagger-ui .btn svg { fill: currentColor; }

    /* ── INPUTS ── */
    .swagger-ui input[type=text], .swagger-ui input[type=password],
    .swagger-ui input[type=search], .swagger-ui input[type=email],
    .swagger-ui textarea, .swagger-ui select {
      background: #0d1117;
      border: 1px solid #30363d;
      color: #e6edf3;
      border-radius: 6px;
      padding: 8px 12px;
    }
    .swagger-ui input:focus, .swagger-ui textarea:focus {
      border-color: #22c55e !important;
      outline: none;
      box-shadow: 0 0 0 3px rgba(34,197,94,0.15);
    }
    .swagger-ui .body-param__text { background: #0d1117; color: #e6edf3; }

    /* ── RESPUESTAS ── */
    .swagger-ui .responses-inner { background: #0d1117; border-radius: 0 0 8px 8px; padding: 12px; }
    .swagger-ui .responses-table .response { border-bottom: 1px solid #21262d; }
    .swagger-ui .response-col_status { color: #e6edf3; font-weight: 700; }
    .swagger-ui .response-col_description { color: #8b949e; }
    .swagger-ui .opblock-section-header { background: #161b22; border-top: 1px solid #21262d; }
    .swagger-ui .opblock-section-header h4 { color: #4ade80; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; }

    /* Código de estado */
    .swagger-ui table.responses-table td.response-col_status { font-size: 1.1rem; }

    /* ── CURL / CÓDIGO ── */
    .swagger-ui .curl-command { background: #161b22; border: 1px solid #30363d; border-radius: 8px; }
    .swagger-ui .curl { color: #79c0ff; font-family: 'Courier New', monospace; font-size: 0.85rem; white-space: pre-wrap; }
    .swagger-ui .microlight { background: #161b22 !important; color: #e6edf3; border-radius: 6px; padding: 14px; font-family: monospace; }
    .swagger-ui .highlight-code pre { background: #161b22 !important; border-radius: 6px; }

    /* ── MODELOS / SCHEMAS ── */
    .swagger-ui section.models { background: #161b22; border: 1px solid #30363d; border-radius: 10px; margin-top: 20px; }
    .swagger-ui section.models h4 { color: #22c55e; font-size: 1.05rem; }
    .swagger-ui section.models .model-container { background: #0d1117; border-radius: 6px; margin: 8px 0; }
    .swagger-ui .model-title { color: #79c0ff; font-weight: 600; }
    .swagger-ui .model-box { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 12px; }
    .swagger-ui .prop-name { color: #79c0ff; }
    .swagger-ui .prop-type { color: #4ade80; }
    .swagger-ui .prop-format { color: #f59e0b; font-size: 0.8rem; }
    .swagger-ui table.model tr.property-row td { color: #e6edf3; border-bottom: 1px solid #21262d; }

    /* ── MODAL (Autorización) ── */
    .swagger-ui .dialog-ux .backdrop-ux { background: rgba(0,0,0,0.75); }
    .swagger-ui .dialog-ux .modal-ux {
      background: #161b22;
      border: 1px solid #22c55e44;
      border-radius: 12px;
      box-shadow: 0 8px 40px rgba(34,197,94,0.15);
      color: #e6edf3;
    }
    .swagger-ui .dialog-ux .modal-ux-header { border-bottom: 1px solid #30363d; }
    .swagger-ui .dialog-ux .modal-ux-header h3 { color: #22c55e; }
    .swagger-ui .dialog-ux .modal-ux-content { background: #161b22; }

    /* ── TABS (Example Value / Schema) ── */
    .swagger-ui .tab li { color: #8b949e; border-bottom: 2px solid transparent; }
    .swagger-ui .tab li.active { color: #22c55e; border-bottom: 2px solid #22c55e; }
    .swagger-ui .tab li button { color: inherit; background: transparent; }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 7px; height: 7px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #22c55e; }

    /* ── LINKS ── */
    .swagger-ui a { color: #22c55e; }
    .swagger-ui a:hover { color: #4ade80; }

    /* ── ÍCONOS / SVG ── */
    .swagger-ui svg.arrow { fill: #22c55e; }
    .swagger-ui .expand-methods svg, .swagger-ui .expand-operation svg { fill: #22c55e; }
    .swagger-ui .close-tag svg { fill: #8b949e; }

    /* ── REQUIRED BADGE ── */
    .swagger-ui .parameter__name.required::after { color: #f87171; }
    .swagger-ui label.required::after { color: #f87171; }

    /* ── DEPRECATED ── */
    .swagger-ui .opblock.opblock-deprecated { opacity: 0.5; filter: grayscale(60%); }

    /* ── LOADING ── */
    .swagger-ui .loading-container { background: #0d1117; }
    .swagger-ui .loading-container .loading::after { border-color: #22c55e transparent transparent; }
  </style>
</head>
<body>
  <div id="swagger-ui"></div>

  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>
    // ── Inicializar Swagger UI ──────────────────────────────────
    const ui = SwaggerUIBundle({
      url: "/openapi.json",
      dom_id: "#swagger-ui",
      deepLinking: true,
      presets: [SwaggerUIBundle.presets.apis, SwaggerUIBundle.SwaggerUIStandalonePreset],
      layout: "BaseLayout",
      tryItOutEnabled: true,
      filter: true,
    });
    window.ui = ui;

    // ── Traducciones al español ─────────────────────────────────
    const t = {
      "Authorize":                  "Autorizar",
      "Try it out":                 "Probar",
      "Execute":                    "Ejecutar",
      "Cancel":                     "Cancelar",
      "Clear":                      "Limpiar",
      "Reset":                      "Restablecer",
      "Close":                      "Cerrar",
      "Parameters":                 "Parámetros",
      "Parameter":                  "Parámetro",
      "Name":                       "Nombre",
      "Description":                "Descripción",
      "Request body":               "Cuerpo de la solicitud",
      "Responses":                  "Respuestas",
      "Response body":              "Cuerpo de respuesta",
      "Response headers":           "Cabeceras de respuesta",
      "No parameters":              "Sin parámetros",
      "No response body":           "Sin cuerpo de respuesta",
      "Example Value":              "Valor de ejemplo",
      "Loading...":                 "Cargando...",
      "Server response":            "Respuesta del servidor",
      "Code":                       "Código",
      "Details":                    "Detalles",
      "Hide":                       "Ocultar",
      "Models":                     "Modelos",
      "Collapse all":               "Contraer todo",
      "Expand all":                 "Expandir todo",
      "Available authorizations":   "Autorizaciones disponibles",
      "Value":                      "Valor",
      "Send empty value":           "Enviar valor vacío",
      "Filter by tag":              "Filtrar por etiqueta",
      "media type":                 "tipo de contenido",
      "required":                   "requerido",
      "deprecated":                 "obsoleto",
      "Curl":                       "Curl",
    };

    function traducirNodo(nodo) {
      if (nodo.nodeType === Node.TEXT_NODE) {
        const original = nodo.nodeValue.trim();
        if (t[original] !== undefined) {
          nodo.nodeValue = nodo.nodeValue.replace(original, t[original]);
        }
      } else if (nodo.nodeType === Node.ELEMENT_NODE) {
        for (const hijo of nodo.childNodes) traducirNodo(hijo);
      }
    }

    const observer = new MutationObserver(mutaciones => {
      for (const m of mutaciones) {
        for (const nodo of m.addedNodes) traducirNodo(nodo);
      }
    });

    observer.observe(document.getElementById("swagger-ui"), {
      subtree: true,
      childList: true,
    });
  </script>
</body>
</html>
"""
    return HTMLResponse(html)


# ==============================================================
# 2. Enumeraciones
# ==============================================================

class EstadoReserva(str, Enum):
    CONFIRMADA = "CONFIRMADA"
    CANCELADA  = "CANCELADA"
    FINALIZADA = "FINALIZADA"
    NO_SHOW    = "NO_SHOW"


class TipoSuperficie(str, Enum):
    CESPED_NATURAL   = "CESPED_NATURAL"
    CESPED_SINTETICO = "CESPED_SINTETICO"
    CEMENTO          = "CEMENTO"


# ==============================================================
# 3. Modelos Pydantic (Contrato de la API)
# ==============================================================

class Cancha(BaseModel):
    id: str
    nombre: str
    ubicacion: str
    tipo_superficie: TipoSuperficie
    precio_por_hora: float = Field(gt=0, description="Precio en moneda local por hora")
    capacidad_jugadores: int = Field(gt=0, description="Número máximo de jugadores")
    descripcion: Optional[str] = None
    activa: bool = True


class ReservaCreate(BaseModel):
    cancha_id: str = Field(..., description="ID de la cancha a reservar")
    nombre_equipo: str = Field(..., min_length=2, description="Nombre del equipo o jugador")
    telefono_contacto: str = Field(..., min_length=7, description="Teléfono de contacto")
    fecha: date = Field(..., description="Fecha del turno (YYYY-MM-DD)")
    hora_inicio: str = Field(..., pattern=r"^\d{2}:\d{2}$", description="Hora de inicio (HH:MM)")
    duracion_horas: int = Field(..., ge=1, le=4, description="Duración en horas (1 a 4)")


class ReservaEstadoUpdate(BaseModel):
    estado: EstadoReserva = Field(..., description="Nuevo estado de la reserva")


class Reserva(BaseModel):
    id: str
    cancha_id: str
    nombre_equipo: str
    telefono_contacto: str
    fecha: date
    hora_inicio: str
    hora_fin: str
    duracion_horas: int
    estado: EstadoReserva
    total: float
    codigo_reserva: str
    created_at: datetime


# ==============================================================
# 4. Base de Datos en Memoria (MVP)
# ==============================================================

db_canchas: dict[str, Cancha] = {
    "c1": Cancha(
        id="c1",
        nombre="Cancha Los Pinos",
        ubicacion="Av. Principal 123, Zona Norte",
        tipo_superficie=TipoSuperficie.CESPED_SINTETICO,
        precio_por_hora=80.0,
        capacidad_jugadores=10,
        descripcion="Cancha de fútbol 5 con césped sintético de última generación. "
                    "Iluminación nocturna y vestuarios disponibles.",
    ),
    "c2": Cancha(
        id="c2",
        nombre="Cancha El Estadio",
        ubicacion="Calle Deportiva 456, Centro",
        tipo_superficie=TipoSuperficie.CESPED_NATURAL,
        precio_por_hora=120.0,
        capacidad_jugadores=22,
        descripcion="Cancha oficial tamaño reglamentario con césped natural. "
                    "Ideal para partidos de fútbol 11.",
    ),
    "c3": Cancha(
        id="c3",
        nombre="Mini Cancha Rápida",
        ubicacion="Jr. Los Deportes 789, Sector Sur",
        tipo_superficie=TipoSuperficie.CEMENTO,
        precio_por_hora=50.0,
        capacidad_jugadores=6,
        descripcion="Cancha de cemento cubierta, ideal para grupos pequeños y partidos express.",
    ),
}

db_reservas: dict[str, Reserva] = {}


# ==============================================================
# 5. Funciones Auxiliares (Lógica de Negocio)
# ==============================================================

def _calcular_hora_fin(hora_inicio: str, duracion_horas: int) -> str:
    """Suma la duración en horas a la hora de inicio."""
    h, m = map(int, hora_inicio.split(":"))
    h_fin = h + duracion_horas
    if h_fin > 23:
        raise HTTPException(
            status_code=400,
            detail="El turno excede el horario de cierre (00:00). Reduzca la duración."
        )
    return f"{h_fin:02d}:{m:02d}"


def _hay_conflicto(
    cancha_id: str,
    fecha: date,
    hora_inicio: str,
    duracion_horas: int,
    excluir_id: Optional[str] = None,
) -> bool:
    """
    Retorna True si existe una reserva activa que se superponga
    con el horario solicitado.
    """
    hora_fin = _calcular_hora_fin(hora_inicio, duracion_horas)
    inicio_nuevo = int(hora_inicio.replace(":", ""))
    fin_nuevo    = int(hora_fin.replace(":", ""))

    for rid, reserva in db_reservas.items():
        if rid == excluir_id:
            continue
        if reserva.cancha_id != cancha_id:
            continue
        if reserva.fecha != fecha:
            continue
        if reserva.estado == EstadoReserva.CANCELADA:
            continue

        inicio_existente = int(reserva.hora_inicio.replace(":", ""))
        fin_existente    = int(reserva.hora_fin.replace(":", ""))

        # Hay conflicto si los intervalos se superponen
        if not (fin_nuevo <= inicio_existente or inicio_nuevo >= fin_existente):
            return True

    return False


def _generar_codigo() -> str:
    """Genera un código de reserva único con prefijo RC-."""
    return "RC-" + str(uuid.uuid4())[:8].upper()


# ==============================================================
# 6. Endpoints — Canchas
# ==============================================================

@app.get(
    "/canchas",
    response_model=List[Cancha],
    tags=["Canchas"],
    summary="Buscar y listar canchas",
    description=(
        "Retorna las canchas activas. Si se envía el parámetro `nombre`, "
        "filtra por coincidencia parcial (sin distinguir mayúsculas/minúsculas). "
        "Si no hay coincidencias devuelve una lista vacía."
    ),
)
def listar_canchas(
    nombre: Optional[str] = Query(None, description="Texto para buscar canchas por nombre"),
):
    canchas = [c for c in db_canchas.values() if c.activa]

    if nombre:
        canchas = [c for c in canchas if nombre.lower() in c.nombre.lower()]

    return canchas


@app.get(
    "/canchas/{cancha_id}",
    response_model=Cancha,
    tags=["Canchas"],
    summary="Obtener cancha por ID",
    description="Retorna los datos detallados de una cancha específica.",
)
def obtener_cancha(cancha_id: str):
    if cancha_id not in db_canchas:
        raise HTTPException(status_code=404, detail=f"Cancha '{cancha_id}' no encontrada.")
    return db_canchas[cancha_id]


@app.get(
    "/canchas/{cancha_id}/disponibilidad",
    tags=["Canchas"],
    summary="Verificar disponibilidad",
    description=(
        "Consulta si una cancha está libre para un horario específico. "
        "Retorna también el precio estimado del turno."
    ),
)
def verificar_disponibilidad(
    cancha_id: str,
    fecha: date = Query(..., description="Fecha del turno (YYYY-MM-DD)"),
    hora_inicio: str = Query(..., description="Hora de inicio (HH:MM)", pattern=r"^\d{2}:\d{2}$"),
    duracion_horas: int = Query(1, ge=1, le=4, description="Duración en horas (1-4)"),
):
    if cancha_id not in db_canchas:
        raise HTTPException(status_code=404, detail=f"Cancha '{cancha_id}' no encontrada.")

    cancha = db_canchas[cancha_id]
    hora_fin = _calcular_hora_fin(hora_inicio, duracion_horas)
    conflicto = _hay_conflicto(cancha_id, fecha, hora_inicio, duracion_horas)

    return {
        "disponible":      not conflicto,
        "cancha_id":       cancha_id,
        "cancha_nombre":   cancha.nombre,
        "fecha":           fecha,
        "hora_inicio":     hora_inicio,
        "hora_fin":        hora_fin,
        "precio_estimado": cancha.precio_por_hora * duracion_horas,
    }


# ==============================================================
# 7. Endpoints — Reservas
# ==============================================================

@app.post(
    "/reservas",
    response_model=Reserva,
    status_code=201,
    tags=["Reservas"],
    summary="Crear reserva",
    description=(
        "Crea una nueva reserva para una cancha. "
        "Verifica disponibilidad en tiempo real antes de confirmar. "
        "Retorna un código único (RC-XXXXXXXX) para consultas futuras."
    ),
)
def crear_reserva(datos: ReservaCreate):
    if datos.cancha_id not in db_canchas:
        raise HTTPException(status_code=404, detail=f"Cancha '{datos.cancha_id}' no encontrada.")

    cancha = db_canchas[datos.cancha_id]

    if _hay_conflicto(datos.cancha_id, datos.fecha, datos.hora_inicio, datos.duracion_horas):
        raise HTTPException(
            status_code=409,
            detail="El horario ya no está disponible, elija otro.",
        )

    hora_fin = _calcular_hora_fin(datos.hora_inicio, datos.duracion_horas)
    reserva_id = str(uuid.uuid4())

    nueva_reserva = Reserva(
        id=reserva_id,
        cancha_id=datos.cancha_id,
        nombre_equipo=datos.nombre_equipo,
        telefono_contacto=datos.telefono_contacto,
        fecha=datos.fecha,
        hora_inicio=datos.hora_inicio,
        hora_fin=hora_fin,
        duracion_horas=datos.duracion_horas,
        estado=EstadoReserva.CONFIRMADA,
        total=cancha.precio_por_hora * datos.duracion_horas,
        codigo_reserva=_generar_codigo(),
        created_at=datetime.now(),
    )

    db_reservas[reserva_id] = nueva_reserva
    return nueva_reserva


@app.get(
    "/reservas",
    response_model=List[Reserva],
    tags=["Reservas"],
    summary="Listar reservas (Panel Admin)",
    description=(
        "Lista reservas con filtros opcionales por cancha, fecha y estado. "
        "Ordenadas cronológicamente. Ideal para el panel del administrador."
    ),
)
def listar_reservas(
    cancha_id: Optional[str]          = Query(None, description="Filtrar por ID de cancha"),
    fecha: Optional[date]             = Query(None, description="Filtrar por fecha (YYYY-MM-DD)"),
    estado: Optional[EstadoReserva]   = Query(None, description="Filtrar por estado"),
):
    resultado = list(db_reservas.values())

    if cancha_id:
        resultado = [r for r in resultado if r.cancha_id == cancha_id]
    if fecha:
        resultado = [r for r in resultado if r.fecha == fecha]
    if estado:
        resultado = [r for r in resultado if r.estado == estado]

    return sorted(resultado, key=lambda r: (r.fecha, r.hora_inicio))


@app.get(
    "/reservas/{reserva_id}",
    response_model=Reserva,
    tags=["Reservas"],
    summary="Obtener reserva por ID",
    description="Retorna los detalles completos de una reserva usando su ID interno.",
)
def obtener_reserva(reserva_id: str):
    if reserva_id not in db_reservas:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")
    return db_reservas[reserva_id]


@app.get(
    "/reservas/codigo/{codigo}",
    response_model=Reserva,
    tags=["Reservas"],
    summary="Buscar reserva por código",
    description=(
        "Permite al jugador consultar su reserva con el código recibido al confirmar "
        "(formato RC-XXXXXXXX). No distingue mayúsculas/minúsculas."
    ),
)
def obtener_reserva_por_codigo(codigo: str):
    codigo_upper = codigo.upper()
    for reserva in db_reservas.values():
        if reserva.codigo_reserva == codigo_upper:
            return reserva
    raise HTTPException(
        status_code=404,
        detail=f"No se encontró ninguna reserva con el código '{codigo_upper}'."
    )


@app.patch(
    "/reservas/{reserva_id}/estado",
    response_model=Reserva,
    tags=["Reservas"],
    summary="Actualizar estado de reserva (Admin)",
    description=(
        "Permite al administrador cambiar el estado de una reserva a "
        "FINALIZADA o NO_SHOW. No se puede modificar una reserva CANCELADA."
    ),
)
def actualizar_estado_reserva(reserva_id: str, datos: ReservaEstadoUpdate):
    if reserva_id not in db_reservas:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")

    reserva = db_reservas[reserva_id]

    if reserva.estado == EstadoReserva.CANCELADA:
        raise HTTPException(
            status_code=400,
            detail="No se puede modificar el estado de una reserva CANCELADA."
        )

    reserva.estado = datos.estado
    db_reservas[reserva_id] = reserva
    return reserva


@app.delete(
    "/reservas/{reserva_id}",
    status_code=204,
    tags=["Reservas"],
    summary="Cancelar reserva",
    description=(
        "Cancela una reserva. Solo se permite si faltan al menos 2 horas para el turno. "
        "Si el turno es inminente, se debe contactar al administrador de la cancha."
    ),
)
def cancelar_reserva(reserva_id: str):
    if reserva_id not in db_reservas:
        raise HTTPException(status_code=404, detail="Reserva no encontrada.")

    reserva = db_reservas[reserva_id]

    if reserva.estado == EstadoReserva.CANCELADA:
        raise HTTPException(status_code=400, detail="La reserva ya se encuentra cancelada.")

    if reserva.estado == EstadoReserva.FINALIZADA:
        raise HTTPException(
            status_code=400,
            detail="No se puede cancelar un turno que ya fue finalizado."
        )

    # Regla de negocio: mínimo 2 horas de anticipación para cancelar
    turno_dt = datetime.combine(
        reserva.fecha,
        datetime.strptime(reserva.hora_inicio, "%H:%M").time()
    )
    horas_restantes = (turno_dt - datetime.now()).total_seconds() / 3600

    if horas_restantes < 2:
        raise HTTPException(
            status_code=400,
            detail=(
                "No se puede cancelar con menos de 2 horas de anticipación. "
                "Por favor contacta directamente al administrador de la cancha."
            ),
        )

    reserva.estado = EstadoReserva.CANCELADA
    db_reservas[reserva_id] = reserva
    # 204 No Content — sin cuerpo en la respuesta
