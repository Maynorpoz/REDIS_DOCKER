# Cache con Redis: Reservar Cancha API

## 1. Endpoints con cache

| Endpoint | Clave Redis | TTL | Motivo |
|---|---|---|---|
| `GET /canchas/{id}` | `cancha:{id}` | 300 s | Los datos de una cancha rara vez cambian |
| `GET /reservas/{id}` | `reserva:{id}` | 120 s | Consultada frecuentemente por el jugador tras crear la reserva |

---

## 2. Estrategia: Cache-Aside

La API gestiona el cache manualmente siguiendo el patrón **cache-aside**:

```
Cliente → API → ¿Está en Redis?
                   ├── SÍ  (cache hit)  → responder desde Redis
                   └── NO  (cache miss) → buscar en memoria
                                          → guardar en Redis con TTL
                                          → responder al cliente
```

---

## 3. Flujo detallado

### Cache hit — `GET /canchas/c1` (segunda vez)
```
GET /canchas/c1
  → cache.get("cancha:c1")  →  dato encontrado en Redis
  ← respuesta inmediata desde cache (sin tocar la memoria principal)
```

### Cache miss — `GET /canchas/c1` (primera vez)
```
GET /canchas/c1
  → cache.get("cancha:c1")  →  None (no existe)
  → buscar en db_canchas["c1"]
  → cache.setex("cancha:c1", 300, datos_json)
  ← respuesta con dato fresco
```

### Invalidación — `PATCH /reservas/1/estado` o `DELETE /reservas/1`
```
PATCH /reservas/1/estado
  → actualizar estado en db_reservas
  → cache.delete("reserva:1")   ← se elimina el dato viejo
  ← respuesta con reserva actualizada
```

---

## 4. TTL definidos

| Recurso | TTL | Justificación |
|---|---|---|
| Cancha | **300 segundos** | Los datos de cancha (nombre, precio, superficie) son estables. 5 minutos es seguro sin riesgo de datos obsoletos. |
| Reserva | **120 segundos** | El estado puede cambiar (admin marca NO_SHOW, jugador cancela). 2 minutos reduce riesgo de mostrar estado incorrecto. |

---

## 5. Claves Redis generadas

```
cancha:c1
cancha:c2
cancha:c3
reserva:1
reserva:2
reserva:42
```

Formato: `{recurso}:{id}` — simple, predecible, fácil de invalidar.

---

## 6. Riesgos y limitaciones

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Redis no disponible | La API sigue funcionando sin cache | El código tiene fallback: si Redis falla, responde desde memoria |
| Dato obsoleto en cache | El jugador ve un estado viejo por máx. 120 s | TTL corto + invalidación explícita al modificar |
| Pérdida de datos al reiniciar Redis | Cache vacío — no hay pérdida de datos reales | El cache es temporal por diseño; los datos reales están en memoria |
| Storage in-memory de la API | Al reiniciar la API se pierden reservas | Limitación del MVP — se resuelve en v2 con PostgreSQL |
