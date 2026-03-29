# Product Backlog: Reservar Cancha

link del tablero de trello: https://trello.com/invite/b/69a391a0ee00db77afb1a978/ATTI94a7cd52d7811265a4cf35622d296ed5435DD393/reservar-cancha
 

Lista de historias (prioridad)

Búsqueda de Canchas – Must

Creación de Reserva – Must

Cancelación de Reserva – Must

Panel del Administrador – Must

Alertas de Email por Reserva – Should

Actualización de Estados por el Administrador – Should

Reseñas del Jugador – Could

Pago Adelantado (Anticipo) – Won’t

---

### 1. Búsqueda de Canchas
**Prioridad:** Must (Debe tener)
**Historia:** Como jugador, quiero buscar una cancha de fútbol por su nombre para encontrarla rápidamente y ver su disponibilidad.
**Criterios de Aceptación:**
- El sistema debe tener una barra de búsqueda visible en la página principal.
- Los resultados deben actualizarse mostrando canchas que coincidan parcial o totalmente con el texto ingresado.
- Si no hay coincidencias, el sistema debe mostrar el mensaje "No se encontraron canchas".

### 2. Creación de Reserva (Con formato Given/When/Then)
**Prioridad:** Must (Debe tener)
**Historia:** Como jugador, quiero reservar una cancha en una fecha y hora específica para asegurar el turno para mi equipo.
**Criterios de Aceptación (Gherkin):**
- **Criterio 1 (Reserva exitosa):**
  - **Given** que el usuario ha seleccionado una cancha y existe disponibilidad para el horario seleccionado.
  - **When** el usuario hace clic en "Confirmar reserva".
  - **Then** el sistema registra la reserva en la base de datos con estado "Confirmada" y muestra un mensaje de éxito.
- **Criterio 2 (Falta de disponibilidad):**
  - **Given** que el usuario intenta reservar un horario que acaba de ser ocupado.
  - **When** el usuario hace clic en "Confirmar reserva".
  - **Then** el sistema muestra un error indicando "El horario ya no está disponible, elija otro".

### 3. Cancelación de Reserva (Con formato Given/When/Then)
**Prioridad:** Must (Debe tener)
**Historia:** Como jugador, quiero cancelar mi reserva a través del sistema si no podré asistir, para así liberar el turno de la cancha.
**Criterios de Aceptación (Gherkin):**
- **Criterio 1 (Cancelación antes del horario):**
  - **Given** que el jugador tiene una reserva "Confirmada" que es para dentro de más de 2 horas.
  - **When** hace clic en el botón "Cancelar Reserva" y la confirma.
  - **Then** el sistema actualiza el estado a "Cancelada" y el turno vuelve a estar disponible.
- **Criterio 2 (Límite de cancelación):**
  - **Given** que la reserva está programada para empezar en menos de 2 horas.
  - **When** el jugador intenta cancelar.
  - **Then** el sistema bloquea la acción y sugiere contactar por teléfono al administrador de la cancha.

### 4. Visualización del Panel del Administrador de Cancha
**Prioridad:** Must (Debe tener)
**Historia:** Como administrador de la cancha, quiero ver la lista cronológica de las reservas del día para organizar y gestionar los turnos adecuadamente.
**Criterios de Aceptación:**
- El dashboard debe mostrar por defecto la fecha actual.
- Cada fila de reserva debe mostrar: Nombre del equipo/jugador, Hora, Duración del turno y Estado.
- Debe existir un filtro de fecha para ver días anteriores o futuros.

### 5. Alertas de Email por Reserva
**Prioridad:** Should (Debería tener)
**Historia:** Como jugador, quiero recibir un correo de confirmación con los detalles al finalizar la reserva para tener un comprobante a la mano.
**Criterios de Aceptación:**
- El sistema debe enviar un mail a la dirección registrada del usuario.
- El mail debe contener el nombre de la cancha, fecha, hora, duración del turno y código de reserva.

### 6. Actualización de Estados por el Administrador
**Prioridad:** Should (Debería tener)
**Historia:** Como administrador de la cancha, quiero poder cambiar el estado de una reserva a "Finalizada" o "No Show" para llevar control de la asistencia de los equipos.
**Criterios de Aceptación:**
- Cada reserva en el dashboard debe tener un menú desplegable de "Cambiar Estado".
- Al seleccionar "Finalizada", la reserva desaparece de las reservas "Pendientes" y pasa al historial.

### 7. Reseñas del Jugador
**Prioridad:** Could (Podría tener)
**Historia:** Como jugador, quiero dejar una calificación de 1 a 5 estrellas a la cancha después de mi visita para compartir mi experiencia con otros usuarios.
**Criterios de Aceptación:**
- El botón de "Calificar" sólo debe mostrarse si la reserva tiene estado "Finalizada".
- El usuario solo debe poder ingresar valores enteros del 1 al 5 y opcionalmente un texto breve.

### 8. Pago Adelantado (Anticipo)
**Prioridad:** Won't (No se hará por ahora)
**Historia:** Como administrador de la cancha, quiero cobrar un anticipo a través de la aplicación para reducir los "No Shows" de equipos que reservan y no se presentan.
**Criterios de Aceptación:**
- (Historia pospuesta para iteraciones futuras, fuera del alcance del MVP). No se implementará lógica de pagos.


MVP rationale

El MVP incluye las historias marcadas como Must porque permiten cumplir el objetivo principal del sistema, que es permitir a los jugadores reservar canchas y a los administradores gestionar los turnos.
Sin la búsqueda de canchas ni la creación de reservas, el sistema no tendría valor funcional.
La cancelación de reservas es necesaria para liberar horarios y evitar conflictos.
El panel del administrador es indispensable para organizar los turnos diarios.
Las historias Should y Could se consideran mejoras para versiones futuras del sistema.
La historia Won’t queda fuera del alcance inicial del proyecto