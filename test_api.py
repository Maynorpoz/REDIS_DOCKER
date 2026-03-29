"""
Test de la API — Reservar Cancha
=================================
Prueba todos los endpoints del flujo principal.

Requisitos:
    pip install -r requirements.txt

Cómo ejecutar (con el servidor corriendo en otra terminal):
    python test_api.py
"""

import requests

BASE = "http://127.0.0.1:8000"
LINEA = "─" * 55

def titulo(texto):
    print(f"\n{LINEA}")
    print(f"  {texto}")
    print(LINEA)

def mostrar(respuesta):
    color_ok  = "\033[92m"  # verde
    color_err = "\033[91m"  # rojo
    reset     = "\033[0m"

    ok = respuesta.status_code < 400
    color = color_ok if ok else color_err
    print(f"  Estado : {color}{respuesta.status_code}{reset}")
    try:
        print(f"  Cuerpo : {respuesta.json()}\n")
    except Exception:
        print(f"  Cuerpo : (sin contenido)\n")


# ==============================================================
# PRUEBA 1 — Listar todas las canchas
# ==============================================================
titulo("1. GET /canchas — listar todas")
r = requests.get(f"{BASE}/canchas")
mostrar(r)

# ==============================================================
# PRUEBA 2 — Buscar cancha por nombre (parcial)
# ==============================================================
titulo("2. GET /canchas?nombre=pinos — búsqueda")
r = requests.get(f"{BASE}/canchas", params={"nombre": "pinos"})
mostrar(r)

# ==============================================================
# PRUEBA 3 — Búsqueda sin coincidencias
# ==============================================================
titulo("3. GET /canchas?nombre=xyz — sin resultados")
r = requests.get(f"{BASE}/canchas", params={"nombre": "xyz"})
mostrar(r)

# ==============================================================
# PRUEBA 4 — Obtener cancha por ID
# ==============================================================
titulo("4. GET /canchas/c1 — detalle de cancha")
r = requests.get(f"{BASE}/canchas/c1")
mostrar(r)

# ==============================================================
# PRUEBA 5 — Cancha inexistente (404)
# ==============================================================
titulo("5. GET /canchas/c99 — cancha no encontrada (404)")
r = requests.get(f"{BASE}/canchas/c99")
mostrar(r)

# ==============================================================
# PRUEBA 6 — Verificar disponibilidad (libre)
# ==============================================================
titulo("6. GET /canchas/c1/disponibilidad — horario disponible")
r = requests.get(f"{BASE}/canchas/c1/disponibilidad", params={
    "fecha":          "2025-12-20",
    "hora_inicio":    "10:00",
    "duracion_horas": 2
})
mostrar(r)

# ==============================================================
# PRUEBA 7 — Crear reserva exitosa
# ==============================================================
titulo("7. POST /reservas — crear reserva")
r = requests.post(f"{BASE}/reservas", json={
    "cancha_id":         "c1",
    "nombre_equipo":     "Los Cracks FC",
    "telefono_contacto": "987654321",
    "fecha":             "2025-12-20",
    "hora_inicio":       "10:00",
    "duracion_horas":    2
})
mostrar(r)

# Guardamos el ID y código para pruebas siguientes
reserva_id     = None
codigo_reserva = None
if r.status_code == 201:
    datos          = r.json()
    reserva_id     = datos["id"]
    codigo_reserva = datos["codigo_reserva"]
    print(f"  >> ID guardado    : {reserva_id}")
    print(f"  >> Código guardado: {codigo_reserva}\n")

# ==============================================================
# PRUEBA 8 — Conflicto de horario (409)
# ==============================================================
titulo("8. POST /reservas — mismo horario (409 Conflict)")
r = requests.post(f"{BASE}/reservas", json={
    "cancha_id":         "c1",
    "nombre_equipo":     "Equipo Rival",
    "telefono_contacto": "111222333",
    "fecha":             "2025-12-20",
    "hora_inicio":       "10:00",
    "duracion_horas":    1
})
mostrar(r)

# ==============================================================
# PRUEBA 9 — Validación de entrada (422)
# ==============================================================
titulo("9. POST /reservas — datos inválidos (422)")
r = requests.post(f"{BASE}/reservas", json={
    "cancha_id":         "c1",
    "nombre_equipo":     "X",       # muy corto (min 2)
    "telefono_contacto": "123",     # muy corto (min 7)
    "fecha":             "2025-12-20",
    "hora_inicio":       "99:99",   # formato inválido
    "duracion_horas":    10          # fuera de rango (max 4)
})
mostrar(r)

# ==============================================================
# PRUEBA 10 — Obtener reserva por ID
# ==============================================================
titulo("10. GET /reservas/{id} — buscar por ID")
if reserva_id:
    r = requests.get(f"{BASE}/reservas/{reserva_id}")
    mostrar(r)
else:
    print("  (omitida: no se creó reserva en prueba 7)\n")

# ==============================================================
# PRUEBA 11 — Obtener reserva por código
# ==============================================================
titulo("11. GET /reservas/codigo/{codigo} — buscar por código")
if codigo_reserva:
    r = requests.get(f"{BASE}/reservas/codigo/{codigo_reserva}")
    mostrar(r)
else:
    print("  (omitida: no se creó reserva en prueba 7)\n")

# ==============================================================
# PRUEBA 12 — Panel admin: reservas del día
# ==============================================================
titulo("12. GET /reservas?cancha_id=c1&fecha=... — panel admin")
r = requests.get(f"{BASE}/reservas", params={
    "cancha_id": "c1",
    "fecha":     "2025-12-20"
})
mostrar(r)

# ==============================================================
# PRUEBA 13 — Actualizar estado (Admin → FINALIZADA)
# ==============================================================
titulo("13. PATCH /reservas/{id}/estado — marcar FINALIZADA")
if reserva_id:
    r = requests.patch(f"{BASE}/reservas/{reserva_id}/estado",
                       json={"estado": "FINALIZADA"})
    mostrar(r)
else:
    print("  (omitida)\n")

# ==============================================================
# PRUEBA 14 — Intentar modificar reserva FINALIZADA a CANCELADA
# ==============================================================
titulo("14. DELETE /reservas/{id} — cancelar reserva FINALIZADA (400)")
if reserva_id:
    r = requests.delete(f"{BASE}/reservas/{reserva_id}")
    mostrar(r)
else:
    print("  (omitida)\n")

# ==============================================================
# PRUEBA 15 — Crear y cancelar reserva (flujo completo)
# ==============================================================
titulo("15. POST + DELETE — crear y cancelar (flujo completo)")
r = requests.post(f"{BASE}/reservas", json={
    "cancha_id":         "c2",
    "nombre_equipo":     "Equipo Test",
    "telefono_contacto": "555000111",
    "fecha":             "2025-12-25",
    "hora_inicio":       "08:00",
    "duracion_horas":    1
})
mostrar(r)

if r.status_code == 201:
    rid = r.json()["id"]
    r2  = requests.delete(f"{BASE}/reservas/{rid}")
    print("  Cancelación:")
    mostrar(r2)

# ==============================================================
print(f"\n{LINEA}")
print("  Pruebas completadas.")
print(f"{LINEA}\n")
