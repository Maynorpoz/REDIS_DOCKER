# Product Backlog: Reservar Cancha

Tablero Trello: https://trello.com/b/VoGJSjOv/reservar-cancha

---

## Lista de Historias (Prioridad MoSCoW)

| # | Historia | Prioridad | Sprint |
|---|---|---|---|
| 1 | Búsqueda de Canchas | **Must** | 1 |
| 2 | Creación de Reserva | **Must** | 1 |
| 3 | Cancelación de Reserva | **Must** | 1 |
| 4 | Panel del Administrador | **Must** | 1 |
| 5 | Alertas de Email por Reserva | Should | 2 |
| 6 | Actualización de Estados por el Administrador | Should | 2 |
| 7 | Reseñas del Jugador | Could | 3 |
| 8 | Pago Adelantado (Anticipo) | Won't | - |
| 9 | Cache de consultas frecuentes con Redis | **Must** | 2 |
| 10 | Containerización con Docker Compose | **Must** | 2 |

---

## Must Have (Debe tener — MVP)

### 1. Búsqueda de Canchas
**Prioridad:** Must (Debe tener)
**Historia:** Como jugador, quiero buscar una cancha de fútbol por su nombre para encontrarla rápidamente y ver su disponibilidad.

**Criterios de Aceptación:**
- El sistema debe permitir búsqueda por nombre de cancha (coincidencia parcial o total).
- Los resultados deben mostrarse con la información principal de cada cancha (nombre, ubicación, precio, tipo de superficie).
- Si no hay coincidencias, el sistema debe retornar una lista vacía.

**Endpoint:** `GET /canchas?nombre={texto}`

---

### 2. Creación de Reserva
**Prioridad:** Must (Debe tener)
**Historia:** Como jugador, quiero reservar una cancha en una fecha y hora específica para asegurar el turno para mi equipo.

**Criterios de Aceptación (Gherkin):**

- **Criterio 1 (Reserva exitosa):**
  - **Given** que el usuario ha seleccionado una cancha y existe disponibilidad para el horario seleccionado.
  - **When** el usuario hace clic en "Confirmar reserva".
  - **Then** el sistema registra la reserva con estado "CONFIRMADA", genera un código único y retorna `201 Created`.

- **Criterio 2 (Falta de disponibilidad):**
  - **Given** que el usuario intenta reservar un horario que acaba de ser ocupado.
  - **When** el usuario hace clic en "Confirmar reserva".
  - **Then** el sistema retorna `409 Conflict` con el mensaje "El horario ya no está disponible, elija otro".

**Endpoint:** `POST /reservas`

---

### 3. Cancelación de Reserva
**Prioridad:** Must (Debe tener)
**Historia:** Como jugador, quiero cancelar mi reserva a través del sistema si no podré asistir, para así liberar el turno de la cancha.

**Criterios de Aceptación (Gherkin):**

- **Criterio 1 (Cancelación antes del horario):**
  - **Given** que el jugador tiene una reserva "CONFIRMADA" que es para dentro de más de 2 horas.
  - **When** hace clic en el botón "Cancelar Reserva" y la confirma.
  - **Then** el sistema actualiza el estado a "CANCELADA" y el turno vuelve a estar disponible.

- **Criterio 2 (Límite de cancelación):**
  - **Given** que la reserva está programada para empezar en menos de 2 horas.
  - **When** el jugador intenta cancelar.
  - **Then** el sistema bloquea la acción y sugiere contactar por teléfono al administrador de la cancha.

**Endpoint:** `DELETE /reservas/{id}`

---

### 4. Visualización del Panel del Administrador de Cancha
**Prioridad:** Must (Debe tener)
**Historia:** Como administrador de la cancha, quiero ver la lista cronológica de las reservas del día para organizar y gestionar los turnos adecuadamente.

**Criterios de Aceptación:**
- El panel debe retornar las reservas filtradas por cancha y fecha.
- Cada reserva debe mostrar: Nombre del equipo/jugador, Teléfono, Hora inicio-fin, Duración y Estado.
- Las reservas se ordenan cronológicamente por hora de inicio.

**Endpoint:** `GET /reservas?cancha_id={id}&fecha={fecha}`

---

## Should Have (Debería tener)

### 5. Alertas de Email por Reserva
**Prioridad:** Should (Debería tener)
**Historia:** Como jugador, quiero recibir un correo de confirmación con los detalles al finalizar la reserva para tener un comprobante a la mano.

**Criterios de Aceptación:**
- El sistema debe enviar un mail a la dirección registrada del usuario.
- El mail debe contener el nombre de la cancha, fecha, hora, duración del turno y código de reserva.

> **Estado:** Pospuesta para Sprint 2. Requiere integración con servicio de email (SendGrid / SMTP).

---

### 6. Actualización de Estados por el Administrador
**Prioridad:** Should (Debería tener)
**Historia:** Como administrador de la cancha, quiero poder cambiar el estado de una reserva a "Finalizada" o "No Show" para llevar control de la asistencia de los equipos.

**Criterios de Aceptación:**
- Cada reserva debe poder actualizarse a los estados: FINALIZADA o NO_SHOW.
- No se puede modificar una reserva que ya fue CANCELADA.

**Endpoint:** `PATCH /reservas/{id}/estado`

---

## Could Have (Podría tener)

### 7. Reseñas del Jugador
**Prioridad:** Could (Podría tener)
**Historia:** Como jugador, quiero dejar una calificación de 1 a 5 estrellas a la cancha después de mi visita para compartir mi experiencia con otros usuarios.

**Criterios de Aceptación:**
- El botón de "Calificar" sólo debe mostrarse si la reserva tiene estado "FINALIZADA".
- El usuario solo debe poder ingresar valores enteros del 1 al 5 y opcionalmente un texto breve.

---

## Won't Have (No se hará ahora)

### 8. Pago Adelantado (Anticipo)
**Prioridad:** Won't (No se hará por ahora)
**Historia:** Como administrador de la cancha, quiero cobrar un anticipo a través de la aplicación para reducir los "No Shows".

> Historia pospuesta para iteraciones futuras, fuera del alcance del MVP. No se implementará lógica de pagos.

---

## MVP Rationale

El MVP incluye las historias marcadas como **Must** porque permiten cumplir el objetivo principal del sistema: permitir a los jugadores reservar canchas y a los administradores gestionar los turnos.

- Sin la búsqueda de canchas ni la creación de reservas, el sistema no tendría valor funcional.
- La cancelación de reservas es necesaria para liberar horarios y evitar conflictos.
- El panel del administrador es indispensable para organizar los turnos diarios.
- El cache con Redis (HU-09) mejora el rendimiento en endpoints de alta frecuencia.
- La containerización con Docker (HU-10) garantiza reproducibilidad del entorno de ejecución.
- Las historias **Should** y **Could** se consideran mejoras para versiones futuras del sistema.
- La historia **Won't** queda fuera del alcance inicial del proyecto.
