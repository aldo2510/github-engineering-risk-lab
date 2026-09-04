# GitHub Engineering Risk Lab

Laboratorio práctico para convertir señales de ingeniería en un **Engineering Risk Heatmap** usando GitHub Actions.

> El laboratorio simula una organización con varios equipos y servicios dentro de un único repositorio. No requiere repositorios reales de Payments, Loans, Mobile, etc.

## Objetivo

Pasar de:

**Signals → Risk Score → Heatmap → Drivers → Action**

El ejercicio está pensado para demostrar cómo GitHub Actions puede apoyar una conversación de Engineering Management, además de automatización técnica.

## Estructura

- `lab.md`: guía paso a paso del laboratorio.
- `risk/teams.yml`: equipos y servicios simulados.
- `risk/risk-rules.yml`: pesos y umbrales del modelo.
- `risk/sample-data.yml`: señales sintéticas de ingeniería.
- `risk/calculate-risk.py`: motor de cálculo y generación del reporte.
- `.github/workflows/engineering-risk.yml`: automatización del análisis.
