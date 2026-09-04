# Lab — Engineering Delivery Risk Heatmap

## 🎯 Objetivo

Construir un pequeño **Engineering Delivery Risk Engine** que transforme señales de ingeniería en un mapa de riesgo de entrega por equipo y servicio.

La pregunta central es:

> **¿Dónde se está concentrando el riesgo de entrega de software y por qué?**

La idea central es:

```text
Engineering Signals → Delivery Risk Score → Threshold → Heatmap → Drill-down → Action
```

El laboratorio usa datos sintéticos para representar una organización que no necesariamente tiene repositorios reales separados por dominio.

---

## 1. Contexto

Imagina que eres responsable de Engineering Management y tienes tres equipos:

- Digital
- Financial
- Platform

Cada equipo tiene servicios asociados.

El objetivo **no es medir si un equipo trabaja bien o mal**. El objetivo es detectar señales que indiquen que la entrega de software puede estar perdiendo estabilidad, velocidad o previsibilidad.

---

## 2. ¿Riesgo de qué?

Este laboratorio mide **Software Delivery Risk**: el riesgo de que un equipo o servicio tenga dificultades para entregar cambios de software de forma **predecible, estable y sostenible**.

No es directamente un score de riesgo financiero ni un score de ciberseguridad.

Las señales utilizadas representan distintos tipos de riesgo de delivery:

| Señal | Qué riesgo representa |
|---|---|
| `failed_workflows` | Riesgo de **inestabilidad del CI/CD** |
| `large_prs` | Riesgo de **cambios difíciles de revisar** |
| `rework_rate` | Riesgo de **calidad y retrabajo** |
| `average_review_hours` | Riesgo de **cuello de botella en reviews** |
| `component_risk` | Riesgo de **alto impacto por criticidad del componente** |

`pull_requests` se utiliza principalmente para ponderar los resultados por volumen de cambios.

Estas señales son **datos de laboratorio**. En una implementación real podrían alimentarse desde las APIs de GitHub.

---

## 3. Modelo de riesgo

Cada señal se normaliza a una escala de 0–100 y se combina mediante pesos.

```text
Delivery Risk Score =
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

La interpretación es:

```text
LOW     → señales de delivery bajo control
MEDIUM  → señales que requieren atención
HIGH    → concentración significativa de riesgo de delivery
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
4. Calcula el riesgo de entrega por servicio.
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
CI instability       +23
PR size              +20
Rework               +18
Component risk       +18
Review friction      +14
                     ───
                      92
```

La conversación de management debería pasar de:

> "Payments tiene muchos PRs"

a:

> **"Payments tiene un Delivery Risk alto. ¿Qué señales lo están provocando y qué acción podemos tomar para reducirlo?"**

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

Vuelve a ejecutar el workflow y observa cómo cambia el **Delivery Risk Score**.

### Preguntas para discusión

1. ¿Qué equipo presenta mayor Delivery Risk?
2. ¿Qué servicio explica la mayor concentración de riesgo?
3. ¿Cuál es el principal driver del riesgo?
4. ¿Qué pasaría si reducimos los fallos de CI?
5. ¿Un Delivery Risk alto significa necesariamente que el equipo trabaja mal?
6. ¿Qué señales adicionales incorporarías en una organización real?
7. ¿Qué acción de Engineering Management tendría mayor impacto sobre el score?

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
   Delivery Risk Engine
          │
          ▼
 Software Delivery Risk
          │
          ▼
      Heatmap
```

El objetivo de esta primera versión es enseñar el **modelo y el flujo de decisión** sin depender de una organización real con múltiples repositorios.

---

## 💡 Idea clave

El valor no está en crear otro dashboard.

El valor está en conectar:

**Engineering Signals → Delivery Risk → Prioritization → Management Action**
