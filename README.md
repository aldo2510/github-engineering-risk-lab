# GitHub Engineering Delivery Risk Lab

Laboratorio práctico para convertir señales de ingeniería en un **Software Delivery Risk Heatmap** usando GitHub Actions.

> El laboratorio simula una organización con varios equipos y servicios dentro de un único repositorio. No requiere repositorios reales de Payments, Loans, Mobile, etc.

## ¿Riesgo de qué?

El laboratorio mide **Software Delivery Risk**: el riesgo de que un equipo o servicio tenga dificultades para entregar cambios de software de forma **predecible, estable y sostenible**.

No es directamente un score de riesgo financiero ni un score de ciberseguridad.

## Objetivo

Pasar de:

**Engineering Signals → Delivery Risk Score → Heatmap → Drivers → Action**

El ejercicio está pensado para demostrar cómo GitHub Actions puede apoyar una conversación de Engineering Management, además de automatización técnica.

## Estructura

- `lab.md`: guía paso a paso del laboratorio.
- `risk/teams.yml`: equipos y servicios simulados.
- `risk/risk-rules.yml`: pesos y umbrales del modelo.
- `risk/sample-data.yml`: señales sintéticas de ingeniería.
- `risk/calculate-risk.py`: motor de cálculo y generación del reporte.
- `.github/workflows/engineering-risk.yml`: automatización del análisis.
