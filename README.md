# Assignment #4 - Prometheus Monitoring System

## Project Structure


## Services
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Node Exporter**: http://localhost:9100/metrics
- **Postgres Exporter**: http://localhost:9187/metrics
- **Custom Exporter**: http://localhost:8000/metrics

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <my git>
   cd assignment4

   docker-compose up -d

   pip install -r requirements.txt
python custom_exporter.py

Access services

Grafana: http://localhost:3000

Prometheus: http://localhost:9090

Dashboards
Node Dashboard
System metrics: CPU, Memory, Disk, Network

10+ PromQL queries with functions

Custom Dashboard
Weather data, exchange rates, cryptocurrency prices

10+ custom metrics from external APIs

Database Dashboard
PostgreSQL performance metrics

Connection stats, cache efficiency, query performance
