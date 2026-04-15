# Reservar Cancha — API de Reservas de Canchas de Fútbol

Plataforma diseñada para conectar a jugadores y equipos con canchas de fútbol disponibles, facilitando el proceso de reserva de turnos de forma digital y en tiempo real. Los administradores de canchas cuentan con un panel centralizado para gestionar los turnos y optimizar la ocupación de sus instalaciones.

---

## Tabla de Contenidos

1. [Descripción del Sistema](#descripción-del-sistema)
2. [Instalación y Ejecución](#instalación-y-ejecución)
3. [Cache con Redis](#cache-con-redis)
4. [Endpoints de la API](#endpoints-de-la-api)
5. [Flujo Principal de Negocio](#flujo-principal-de-negocio)
6. [Reglas de Negocio](#reglas-de-negocio)
7. [Estructura del Proyecto](#estructura-del-proyecto)

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

### Opción A — Docker Compose (recomendado)

**Requisitos:** Docker Desktop instalado y corriendo.

```bash
# Levantar API + Redis con un solo comando
docker compose up --build
```

La API queda disponible en: **http://localhost:8000**

### Opción B — Ejecución local sin Docker

**Requisitos:** Python 3.10 o superior.

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la API
uvicorn main:app --reload
```

> Sin Redis corriendo localmente, la API funciona igual pero sin cache.

### Documentación interactiva (Swagger UI)
Abrir en el navegador: **http://localhost:8000/docs**

---

## Cache con Redis

La API implementa cache **cache-aside** con Redis en dos endpoints de alta frecuencia:

| Endpoint | Clave Redis | TTL |
|---|---|---|
| `GET /canchas/{id}` | `cancha:{id}` | 300 s |
| `GET /reservas/{id}` | `reserva:{id}` | 120 s |

**Flujo:**
- **Cache hit:** el dato existe en Redis → se responde directamente sin tocar la memoria principal.
- **Cache miss:** se busca en memoria → se guarda en Redis con TTL → se responde.
- Al modificar o cancelar una reserva, su clave se elimina de Redis automáticamente.

Ver documentación completa en [docs/cache.md](docs/cache.md).

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
tarea3/
├── main.py                  # API ejecutable (FastAPI) con cache Redis
├── requirements.txt         # Dependencias Python
├── Dockerfile               # Imagen Docker de la API
├── docker-compose.yml       # Orquestación API + Redis
├── API_CONTRACT.md          # Contrato de la API con request/response y ejemplos curl
├── SYSTEM_BRIEF.md          # Arquitectura, diagramas de casos de uso y modelo de datos
├── BACKLOG.md               # Product Backlog con 10 historias de usuario (MoSCoW)
├── REQUERIMENTS.md          # Requerimientos originales del sistema
├── docs/
│   ├── architecture.md      # Diagrama de arquitectura con Redis (Mermaid)
│   ├── cache.md             # Documentación del cache: TTL, claves, flujo, riesgos
│   ├── requirements.md      # Requerimientos funcionales y no funcionales
│   └── system-brief.md      # Resumen ejecutivo del sistema
└── README.md                # Este archivo
```
