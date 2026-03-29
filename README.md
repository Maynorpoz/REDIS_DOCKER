# Reservar Cancha — API de Reservas de Canchas de Fútbol

Plataforma diseñada para conectar a jugadores y equipos con canchas de fútbol disponibles, facilitando el proceso de reserva de turnos de forma digital y en tiempo real. Los administradores de canchas cuentan con un panel centralizado para gestionar los turnos y optimizar la ocupación de sus instalaciones.

---

## Tabla de Contenidos

1. [Descripción del Sistema](#descripción-del-sistema)
2. [Instalación y Ejecución](#instalación-y-ejecución)
3. [Endpoints de la API](#endpoints-de-la-api)
4. [Flujo Principal de Negocio](#flujo-principal-de-negocio)
5. [Reglas de Negocio](#reglas-de-negocio)
6. [Estructura del Proyecto](#estructura-del-proyecto)

---

## Descripción del Sistema

**Problema:** Los jugadores deben llamar por teléfono para reservar canchas sin garantía de disponibilidad. Los administradores gestionan reservas en cuadernos o WhatsApp, generando errores de doble reserva y pérdida de clientes.

**Solución (MVP):** API REST que implementa el flujo principal de reservas:

| Actor | Acciones disponibles |
|---|---|
| **Jugador / Equipo** | Buscar canchas, verificar disponibilidad, crear y cancelar reservas |
| **Administrador** | Ver panel del día, actualizar estados (FINALIZADA, NO_SHOW) |

---

## Instalación y Ejecución

### Requisitos
- Python 3.10 o superior

### Pasos

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la API
uvicorn main:app --reload
```

La API queda disponible en: **http://localhost:8000**

### Documentación interactiva (Swagger UI)
Abrir en el navegador: **http://localhost:8000/docs**

Desde ahí se pueden probar todos los endpoints directamente sin herramientas externas.

---

## Endpoints de la API

### Canchas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/canchas` | Listar/buscar canchas (`?nombre=texto`) |
| `GET` | `/canchas/{id}` | Obtener detalle de una cancha |
| `GET` | `/canchas/{id}/disponibilidad` | Verificar disponibilidad en un horario |

### Reservas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/reservas` | Crear nueva reserva |
| `GET` | `/reservas` | Panel admin (`?cancha_id=&fecha=&estado=`) |
| `GET` | `/reservas/{id}` | Obtener reserva por ID |
| `GET` | `/reservas/codigo/{codigo}` | Buscar reserva por código (RC-XXXXXXXX) |
| `PATCH` | `/reservas/{id}/estado` | Actualizar estado (Admin) |
| `DELETE` | `/reservas/{id}` | Cancelar reserva |

Ver especificación completa con ejemplos en [API_CONTRACT.md](API_CONTRACT.md).

---

## Flujo Principal de Negocio

```
Jugador:
  1. GET /canchas?nombre=pinos       → buscar cancha
  2. GET /canchas/c1/disponibilidad  → confirmar que el horario está libre
  3. POST /reservas                  → crear reserva → recibe código RC-XXXXXXXX
  4. GET /reservas/codigo/RC-...     → consultar comprobante en cualquier momento
  5. DELETE /reservas/{id}           → cancelar (solo si faltan >= 2 horas)

Administrador:
  6. GET /reservas?cancha_id=c1&fecha=2025-06-15  → ver panel del día
  7. PATCH /reservas/{id}/estado                  → marcar FINALIZADA o NO_SHOW
```

---

## Reglas de Negocio

- No se permiten dos reservas que se superpongan en el mismo horario y cancha (`409 Conflict`).
- El jugador solo puede cancelar si faltan **al menos 2 horas** para el turno (`400` si no).
- El precio se calcula automáticamente: `precio_por_hora × duracion_horas`.
- No se puede modificar una reserva con estado `CANCELADA`.
- Estados válidos: `CONFIRMADA → FINALIZADA / NO_SHOW / CANCELADA`.

---

## Estructura del Proyecto

```
tarea2/
├── main.py              # API ejecutable (FastAPI) — punto de entrada
├── requirements.txt     # Dependencias Python
├── API_CONTRACT.md      # Contrato de la API con request/response y ejemplos curl
├── SYSTEM_BRIEF.md      # Arquitectura, diagramas de casos de uso y modelo de datos
├── BACKLOG.md           # Product Backlog con 8 historias de usuario (MoSCoW)
├── REQUERIMENTS.md      # Requerimientos originales del sistema (Tarea 1)
└── README.md            # Este archivo
```
