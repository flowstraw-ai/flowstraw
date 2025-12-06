# FlowStraw

**FlowStraw** is an AI-powered, lightweight, on-prem data ingestion engine.  
It reads CSVs and other flat files, transforms them into curated tables and star schemas, and exposes analytics via a small web UI.

This repo contains the **FlowStraw PoC** that demonstrates:

- CSV → SQLite staging tables (`stg_*`)
- SQLite → Star schema (`dim_*`, `fact_sales`)
- Interactive analytics dashboard on top of the star schema
- Optional AI-assisted insights (LLM-driven)

---

## Architecture (PoC)

```text
[ CSV Files ]
  customers.csv
  products.csv
  sales.csv / sales_big.csv

      │
      ▼
[ FlowStraw ETL - Python ]
  - load staging tables:
      stg_customers
      stg_products
      stg_sales
  - build star schema:
      dim_customer
      dim_product
      dim_date
      fact_sales

      │
      ▼
[ SQLite DB ]
  flowstraw.db

      │
      ▼
[ Analytics UI (Streamlit) ]
  - Overview KPIs
  - Revenue by month / region
  - Customer & product explorers
  - Custom SQL workbench
  - (Optional) AI insight panel
