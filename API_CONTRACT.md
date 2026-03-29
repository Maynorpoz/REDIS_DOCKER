# Contrato de API: Reservar Cancha

**Versión:** 1.0.0
**Base URL:** `http://localhost:8000`
**Formato:** JSON
**Documentación interactiva:** `http://localhost:8000/docs` (Swagger UI generado automáticamente)

---

## Resumen de Endpoints

| Método | Ruta | Historia | Descripción |
|--------|------|----------|-------------|
| `GET` | `/canchas` | HU-01 | Buscar/listar canchas por nombre |
| `GET` | `/canchas/{id}` | HU-01 | Obtener detalle de una cancha |
| `GET` | `/canchas/{id}/disponibilidad` | HU-02 | Verificar disponibilidad de horario |
| `POST` | `/reservas` | HU-02 | Crear nueva reserva |
| `GET` | `/reservas` | HU-04 | Panel admin: listar reservas con filtros |
| `GET` | `/reservas/{id}` | HU-02 | Obtener reserva por ID |
| `GET` | `/reservas/codigo/{codigo}` | HU-02 | Buscar reserva por código |
| `PATCH` | `/reservas/{id}/estado` | HU-06 | Actualizar estado (Admin) |
| `DELETE` | `/reservas/{id}` | HU-03 | Cancelar reserva |

> La autenticación (JWT) está fuera del alcance del MVP y se implementará en Sprint 2.

---

## Modelos de Datos

### `Cancha`
```json
{
  "id": "c1",
  "nombre": "Cancha Los Pinos",
  "ubicacion": "Av. Principal 123, Zona Norte",
  "tipo_superficie": "CESPED_SINTETICO",
  "precio_por_hora": 80.0,
  "capacidad_jugadores": 10,
  "descripcion": "Cancha con iluminación nocturna",
  "activa": true
}
```

**Valores válidos para `tipo_superficie`:**
- `CESPED_NATURAL`
- `CESPED_SINTETICO`
- `CEMENTO`

---

### `Reserva`
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "cancha_id": "c1",
  "nombre_equipo": "Los Cracks FC",
  "telefono_contacto": "987654321",
  "fecha": "2025-06-15",
  "hora_inicio": "18:00",
  "hora_fin": "20:00",
  "duracion_horas": 2,
  "estado": "CONFIRMADA",
  "total": 160.0,
  "codigo_reserva": "RC-A1B2C3D4",
  "created_at": "2025-06-10T14:30:00"
}
```

**Ciclo de vida del estado (`estado`):**
```
CONFIRMADA ──→ FINALIZADA   (admin marca turno completado)
           ──→ NO_SHOW      (admin marca inasistencia)
           ──→ CANCELADA    (jugador cancela con >= 2h de anticipación)
```

---

## Endpoints Detallados

---

### `GET /canchas`
**Historia:** HU-01 — Búsqueda de Canchas

Lista todas las canchas activas. Si se envía `nombre`, filtra por coincidencia parcial (sin distinguir mayúsculas/minúsculas).

**Query Parameters:**
| Param | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `nombre` | string | No | Texto para buscar por nombre de cancha |

**Ejemplos:**
```
GET /canchas              → todas las canchas
GET /canchas?nombre=pinos → canchas cuyo nombre contiene "pinos"
GET /canchas?nombre=xyz   → [] (lista vacía si no hay coincidencias)
```

**Response 200:**
```json
[
  {
    "id": "c1",
    "nombre": "Cancha Los Pinos",
    "ubicacion": "Av. Principal 123, Zona Norte",
    "tipo_superficie": "CESPED_SINTETICO",
    "precio_por_hora": 80.0,
    "capacidad_jugadores": 10,
    "descripcion": "Cancha con iluminación",
    "activa": true
  }
]
```

---

### `GET /canchas/{cancha_id}`
**Historia:** HU-01 — Búsqueda de Canchas

Obtiene los datos completos de una cancha por su ID.

**Response 200:** Objeto `Cancha`

**Response 404:**
```json
{ "detail": "Cancha 'c99' no encontrada." }
```

---

### `GET /canchas/{cancha_id}/disponibilidad`
**Historia:** HU-02 — Creación de Reserva (paso previo)

Verifica si una cancha está libre en el horario solicitado y devuelve el precio estimado.

**Query Parameters:**
| Param | Tipo | Requerido | Descripción |
|-------|------|-----------|-------------|
| `fecha` | date | Sí | Fecha del turno (YYYY-MM-DD) |
| `hora_inicio` | string | Sí | Hora de inicio (HH:MM) |
| `duracion_horas` | int | No (def: 1) | Duración 1-4 horas |

**Response 200 (disponible):**
```json
{
  "disponible": true,
  "cancha_id": "c1",
  "cancha_nombre": "Cancha Los Pinos",
  "fecha": "2025-06-15",
  "hora_inicio": "18:00",
  "hora_fin": "20:00",
  "precio_estimado": 160.0
}
```

**Response 200 (no disponible):**
```json
{
  "disponible": false,
  "cancha_id": "c1",
  "cancha_nombre": "Cancha Los Pinos",
  "fecha": "2025-06-15",
  "hora_inicio": "18:00",
  "hora_fin": "20:00",
  "precio_estimado": 160.0
}
```

---

### `POST /reservas`
**Historia:** HU-02 — Creación de Reserva

Crea una nueva reserva. Verifica disponibilidad en tiempo real antes de confirmar.

**Request Body:**
```json
{
  "cancha_id": "c1",
  "nombre_equipo": "Los Cracks FC",
  "telefono_contacto": "987654321",
  "fecha": "2025-06-15",
  "hora_inicio": "18:00",
  "duracion_horas": 2
}
```

**Validaciones:**
- `cancha_id` debe existir.
- `nombre_equipo` mínimo 2 caracteres.
- `telefono_contacto` mínimo 7 caracteres.
- `hora_inicio` formato `HH:MM`.
- `duracion_horas` entre 1 y 4.
- El turno no puede superar las 23:59.

**Response 201 Created:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "cancha_id": "c1",
  "nombre_equipo": "Los Cracks FC",
  "telefono_contacto": "987654321",
  "fecha": "2025-06-15",
  "hora_inicio": "18:00",
  "hora_fin": "20:00",
  "duracion_horas": 2,
  "estado": "CONFIRMADA",
  "total": 160.0,
  "codigo_reserva": "RC-A1B2C3D4",
  "created_at": "2025-06-10T14:30:00"
}
```

**Response 409 Conflict:**
```json
{ "detail": "El horario ya no está disponible, elija otro." }
```

---

### `GET /reservas`
**Historia:** HU-04 — Panel del Administrador

Lista reservas con filtros opcionales. Las reservas se ordenan por fecha y hora de inicio.

**Query Parameters (todos opcionales):**
| Param | Tipo | Descripción |
|-------|------|-------------|
| `cancha_id` | string | Filtrar por cancha |
| `fecha` | date | Filtrar por fecha (YYYY-MM-DD) |
| `estado` | string | Filtrar por estado |

**Ejemplo para el panel del día:**
```
GET /reservas?cancha_id=c1&fecha=2025-06-15
```

**Response 200:** Array de `Reserva` ordenado cronológicamente.

---

### `GET /reservas/{reserva_id}`
Obtiene una reserva por su ID interno (UUID).

**Response 200:** Objeto `Reserva`
**Response 404:** `{ "detail": "Reserva no encontrada." }`

---

### `GET /reservas/codigo/{codigo}`
**Historia:** HU-02 — Consulta del comprobante

El jugador puede buscar su reserva con el código recibido al confirmar. No distingue mayúsculas/minúsculas.

**Ejemplo:** `GET /reservas/codigo/rc-a1b2c3d4`

**Response 200:** Objeto `Reserva`

**Response 404:**
```json
{ "detail": "No se encontró ninguna reserva con el código 'RC-ZZZZZZZZ'." }
```

---

### `PATCH /reservas/{reserva_id}/estado`
**Historia:** HU-06 — Actualización de Estados por el Administrador

Actualiza el estado de una reserva. No se puede modificar una reserva CANCELADA.

**Request Body:**
```json
{ "estado": "FINALIZADA" }
```

**Valores válidos:** `CONFIRMADA`, `CANCELADA`, `FINALIZADA`, `NO_SHOW`

**Response 200:** Objeto `Reserva` actualizado.

**Response 400:**
```json
{ "detail": "No se puede modificar el estado de una reserva CANCELADA." }
```

---

### `DELETE /reservas/{reserva_id}`
**Historia:** HU-03 — Cancelación de Reserva

Cancela una reserva. Solo válido si faltan **al menos 2 horas** para el turno.

**Response 204 No Content:** Reserva cancelada (sin cuerpo en la respuesta).

**Response 400 (menos de 2 horas):**
```json
{
  "detail": "No se puede cancelar con menos de 2 horas de anticipación. Por favor contacta directamente al administrador de la cancha."
}
```

**Response 400 (ya cancelada):**
```json
{ "detail": "La reserva ya se encuentra cancelada." }
```

---

## Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| `200` | OK — Operación exitosa |
| `201` | Created — Reserva creada |
| `204` | No Content — Reserva cancelada |
| `400` | Bad Request — Error de validación o regla de negocio |
| `404` | Not Found — Recurso no existe |
| `409` | Conflict — Conflicto de horario (doble reserva) |
| `422` | Unprocessable Entity — Error de formato en el body |

---

## Flujo Completo (curl)

```bash
# 1. Buscar canchas
curl http://localhost:8000/canchas
curl "http://localhost:8000/canchas?nombre=pinos"

# 2. Verificar disponibilidad
curl "http://localhost:8000/canchas/c1/disponibilidad?fecha=2025-06-15&hora_inicio=18:00&duracion_horas=2"

# 3. Crear reserva
curl -X POST http://localhost:8000/reservas \
  -H "Content-Type: application/json" \
  -d '{
    "cancha_id": "c1",
    "nombre_equipo": "Los Cracks FC",
    "telefono_contacto": "987654321",
    "fecha": "2025-06-15",
    "hora_inicio": "18:00",
    "duracion_horas": 2
  }'

# 4. Consultar reserva por código
curl http://localhost:8000/reservas/codigo/RC-A1B2C3D4

# 5. Panel del admin — reservas del día
curl "http://localhost:8000/reservas?cancha_id=c1&fecha=2025-06-15"

# 6. Marcar como finalizada (admin)
curl -X PATCH http://localhost:8000/reservas/{id}/estado \
  -H "Content-Type: application/json" \
  -d '{"estado": "FINALIZADA"}'

# 7. Cancelar reserva
curl -X DELETE http://localhost:8000/reservas/{id}
```
