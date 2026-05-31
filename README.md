# 🚀 fastapi-otel-jaeger

A robust FastAPI backend designed to demonstrate **clean layered architecture** and deep **distributed tracing (Observability)** using **OpenTelemetry** and **Jaeger**.

This project showcases the clear separation of concerns across different software layers (API, Service, and Repository) and visualizes the exact lifecycle and duration of incoming requests.

---

## 🏗️ Architectural Overview

The application is structured into three distinct layers to ensure maintainability, scalability, and loose coupling:

1. **API Layer (`api.py`)**: Handles incoming HTTP requests, enforces strict data validation using Pydantic Schemas, and routes traffic.
2. **Service Layer (`service.py`)**: Encapsulates the core business logic and orchestrates validation checks.
3. **Repository Layer (`repository.py`)**: Manages direct database interactions and operations with PostgreSQL.

---

## 🔬 Observability & Instrumentation Pattern

To eliminate system blindness under production loads, this project implements a hybrid observability pattern:

* **Automatic Instrumentation**: Seamlessly monitors the entire FastAPI web ecosystem, capturing metadata, HTTP statuses, and overall routing latencies without modifying core logic.
* **Manual Instrumentation**: Leverages custom context managers (`with tracer.start_as_current_span`) injected inside the Service and Repository layers to slice, dice, and isolate bottleneck locations.

---

## 🛠️ Tech Stack & Ecosystem

* **Framework**: FastAPI
* **Data Validation**: Pydantic v2
* **Environment & Dependency Management**: `uv`
* **Database**: PostgreSQL / Psycopg2
* **Telemetry Standard**: OpenTelemetry (OTel API & SDK)
* **Tracing Backend**: Jaeger (Deployed via Docker)

---

## ⚡ Quick Start & Setup Guide

### 1. Environment Initialization
```powershell
uv init --bare
uv add opentelemetry-api opentelemetry-sdk opentelemetry-instrumentation-fastapi opentelemetry-exporter-otlp-proto-http
---

## 📊 Visualizing Traces

1. Open interactive API docs: `http://localhost:8000/docs`.
2. Fire a few successful test requests through the `/register` endpoint.
3. Access the **Jaeger UI** dashboard at `http://localhost:16686`.
4. Select `MONITORING` from the **Service** dropdown and click **Find Traces** to explore the beautiful cascading waterfall charts representing your system's layered operation!
