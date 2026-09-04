# Lab — Engineering Risk Heatmap

## 🎯 Objetivo

Construir un pequeño **Engineering Risk Engine** que transforme señales de ingeniería en un mapa de riesgo por equipo y servicio.

La idea central es:

```text
Signals → Risk Score → Threshold → Heatmap → Drill-down → Action
```

El laboratorio usa datos sintéticos para representar una organización que no necesariamente tiene repositorios reales separados por dominio.

---

## 1. Contexto

Imagina que eres responsable de Engineering Management y tienes tres equipos:

- Digital
- Financial
- Platform

Cada equipo tiene servicios asociados.

La pregunta no es simplemente:

> ¿Cuántos PR tenemos?

La pregunta es:

> **¿Dónde se está concentrando el riesgo de ingeniería y por qué?**

---

## 2. Señales utilizadas

El laboratorio considera señales como:

| Señal | Qué representa |
|---|---|
| `pull_requests` | Volumen de cambios |
| `failed_workflows` | Inestabilidad del CI |
| `average_review_hours` | Fricción en reviews |
| `rework_rate` | Trabajo que vuelve a modificarse |
| `large_prs` | Cambios grandes y difíciles de revisar |
| `component_risk` | Criticidad del componente |

Estas señales son **datos de laboratorio**. En una implementación real podrían alimentarse desde las APIs de GitHub.

---

## 3. Modelo de riesgo

Cada señal se normaliza a una escala de 0–100 y se combina mediante pesos.

```text
Risk Score =
    CI Instability  × 25%
  + PR Size         × 20%
  + Rework          × 20%
  + Review Friction × 15%
  + Component Risk  × 20%
```

Umbrales:

```text
0–39   🟢 LOW
40–69  🟡 MEDIUM
70–100 🔴 HIGH
```

---

## 4. Ejecutar el laboratorio

El workflow se encuentra en:

```text
.github/workflows/engineering-risk.yml
```

Ejecuta el workflow manualmente desde **Actions → Engineering Risk Heatmap → Run workflow**.

El workflow:

1. Instala Python.
2. Lee los datos de `risk/sample-data.yml`.
3. Ejecuta `risk/calculate-risk.py`.
4. Calcula el riesgo por servicio.
5. Agrega el riesgo por equipo.
6. Genera un resumen en **GitHub Actions Job Summary**.
7. Publica un artefacto con el reporte Markdown.

---

## 5. Analizar el resultado

El reporte debe permitir responder:

### Nivel organización

```text
Digital       🟡 MEDIUM
Financial     🔴 HIGH
Platform      🟢 LOW
```

### Nivel equipo

```text
Financial — 🔴 HIGH

Payments     🔴 HIGH
Loans        🟡 MEDIUM
```

### Nivel servicio

Para el servicio de mayor riesgo se muestran sus principales drivers:

```text
CI instability       +25
PR size              +20
Rework               +18
Review friction      +13
Component risk        +8
                     ───
                      84
```

---

## 6. Ejercicio práctico

Modifica una señal en:

```text
risk/sample-data.yml
```

Por ejemplo, aumenta:

```yaml
failed_workflows: 5
```

a:

```yaml
failed_workflows: 12
```

Vuelve a ejecutar el workflow y observa cómo cambia el Risk Score.

### Preguntas para discusión

1. ¿Qué equipo presenta mayor riesgo?
2. ¿Qué servicio explica la mayor parte del riesgo?
3. ¿Cuál es el principal driver?
4. ¿Qué pasaría si reducimos los fallos de CI?
5. ¿Un Risk Score alto significa necesariamente que el equipo trabaja mal?
6. ¿Qué señales adicionales incorporarías en una organización real?

---

## 7. Evolución hacia datos reales

Una evolución natural del laboratorio sería sustituir los datos sintéticos por señales obtenidas mediante GitHub API:

```text
GitHub API
   │
   ├── Pull Requests
   ├── Reviews
   ├── Actions
   ├── Issues
   └── Commits
          │
          ▼
    Risk Engine
          │
          ▼
 Engineering Risk
          │
          ▼
      Heatmap
```

El objetivo de esta primera versión es enseñar el **modelo y el flujo de decisión** sin depender de una organización real con múltiples repositorios.

---

## 💡 Idea clave

El valor no está en crear otro dashboard.

El valor está en conectar:

**Engineering Signals → Risk → Prioritization → Management Action**
