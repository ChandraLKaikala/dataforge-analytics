# DataForge Analytics Platform

A **production-grade, portfolio-quality** dbt project showcasing every advanced analytics engineering pattern. Built with dbt Core + DuckDB (free/local) and pre-wired for Snowflake and Databricks.

## 🎯 Project Highlights

### Architecture: 5-Layer Medallion
- **Bronze**: Raw data ingestion with source freshness checks
- **Silver** (Staging): Cleaned, typed, deduplicated data
- **Gold** (Intermediate): Business logic, window functions, attribution
- **Platinum** (Marts): 360° customer views, RFM segmentation, cohort analysis
- **Diamond** (Semantic): MetricFlow semantic layer for metrics

### Advanced dbt Features ✨

| Feature | Implementation |
|---|---|
| **Incremental Models** | Append, merge, delete+insert strategies |
| **Snapshots** | SCD Type 2 on customers & product pricing |
| **Custom Macros** | generate_surrogate_key, safe_divide, date_spine |
| **Model Contracts** | Enforced schema on all mart models |
| **Versioned Models** | Breaking schema change demo (orders_v1/v2) |
| **Tags & Meta** | Tiered ownership, SLA, PII classification |
| **Source Freshness** | Warn/error thresholds on all sources |
| **Generic Tests** | Custom test cases: accepted_range, referential_integrity |
| **Singular Tests** | Revenue reconciliation, orphan detection |
| **dbt Packages** | dbt_utils, dbt_expectations, elementary |
| **Exposures** | Streamlit dashboard, analytics apps |
| **MetricFlow Semantics** | Semantic models for metric queries |

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Git
- ~500MB disk space

### Installation (5 minutes)

```bash
# 1. Clone or enter the project
cd DBT_Project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Full setup: install, generate data, seed, run, test
make full-setup

# 4. View documentation
make docs

# 5. (Optional) Run Streamlit dashboard
make dashboard
```

## 📊 Project Structure

```
DBT_Project/
├── dataforge/                    # dbt project root
│   ├── dbt_project.yml          # project config
│   ├── profiles.yml             # dev (DuckDB), snowflake, databricks targets
│   ├── models/
│   │   ├── staging/             # 6 staging models (stg_*)
│   │   ├── intermediate/        # 4 intermediate models (int_*)
│   │   └── marts/
│   │       ├── core/            # customer_360, revenue, product analytics
│   │       ├── marketing/       # attribution, funnel analytics
│   │       └── finance/         # cohort analysis, RFM segmentation
│   ├── snapshots/               # customer & product pricing SCD Type 2
│   ├── macros/                  # custom SQL functions
│   ├── tests/                   # revenue reconciliation, orphan detection
│   ├── semantic_models/         # MetricFlow definitions
│   └── seeds/                   # reference data (country codes, currencies, channels)
├── scripts/
│   └── generate_data.py         # synthetic data generator (100K+ records)
├── dashboard/
│   └── app.py                   # Streamlit analytics dashboard
├── .github/workflows/
│   └── dbt_ci.yml              # GitHub Actions CI/CD pipeline
├── requirements.txt             # Python dependencies
├── Makefile                     # convenient commands
└── README.md
```

## 📈 Data Model Overview

### Staging Models (Views)
- `stg_customers` — deduplicated, PII hashed, explicit typing
- `stg_orders` — validated orders with status filtering
- `stg_order_items` — line items with discount logic
- `stg_products` — product master with active flag
- `stg_campaigns` — marketing campaigns
- `stg_web_events` — clickstream events with sessionization

### Intermediate Models (Tables)
- `int_customer_orders` — customer-order fact with running totals (order_count_to_date, cumulative_revenue)
- `int_product_performance` — product metrics (units_sold, revenue, gross_profit)
- `int_campaign_attribution` — first/last/linear touch attribution models
- `int_session_analytics` — web sessions from 30-min event gaps

### Mart Models (Tables with Contracts)
- `mart_customer_360` — full customer profile (LTV, AOV, churn_risk_score)
- `mart_revenue_analytics` — daily revenue, profit, AOV trends
- `mart_product_analytics` — product performance ranking
- `mart_attribution` — campaign touch attribution (3 models)
- `mart_funnel_analytics` — event-to-conversion funnels
- `mart_cohort_analysis` — cohort acquisition & retention
- `mart_rfm_segmentation` — RFM scoring with Champions/At-Risk/Lost segments

### Snapshots (SCD Type 2)
- `customer_snapshot` — tracks email, tier, address changes
- `product_pricing_snapshot` — tracks price & cost history

## 🛠 Key Commands

```bash
make install        # Install Python dependencies
make deps          # Install dbt packages
make seed          # Load reference data (seeds)
make run           # Run all dbt models
make test          # Run all dbt tests (~50 tests)
make docs          # Generate & serve dbt lineage graph
make dashboard     # Start Streamlit dashboard
make full-setup    # One-command: install → generate-data → seed → run → test
```

## 🔌 Connecting to Snowflake or Databricks

### Snowflake

```bash
export SNOWFLAKE_ACCOUNT=xy12345.us-east-1
export SNOWFLAKE_USER=analytics_user
export SNOWFLAKE_PASSWORD=your_password
export SNOWFLAKE_ROLE=ANALYST
export SNOWFLAKE_DATABASE=ANALYTICS
export SNOWFLAKE_WAREHOUSE=COMPUTE_WH

cd dataforge && dbt run --target snowflake
```

### Databricks

```bash
export DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
export DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
export DATABRICKS_TOKEN=your_pat_token
export DATABRICKS_CATALOG=main
export DATABRICKS_SCHEMA=dataforge

cd dataforge && dbt run --target databricks
```

## 🧪 Testing & Quality

The project includes:
- **Source freshness checks** — validates data recency
- **Generic tests** — not_null, unique, relationships, dbt_expectations
- **Singular tests** — revenue reconciliation, orphan detection
- **Model contracts** — enforced schemas on all mart models
- **dbt Elementary** — data quality monitoring package

Run tests:
```bash
dbt test
dbt test --select tag:daily      # Run daily-tagged tests only
dbt test --select stg_customers  # Test one model
dbt source freshness             # Check source data freshness
```

## 📊 Streamlit Dashboard Features

- **Revenue Overview** — daily trends, profit margins, AOV
- **Customer 360** — LTV distribution, churn risk, tier analysis
- **RFM Segments** — customer segmentation (Champions, Loyal, At-Risk, Lost)
- **Funnel Analytics** — event-to-conversion visualizations
- **Cohort Retention** — acquisition cohorts with rolling retention rates

Launch:
```bash
make dashboard
# Opens http://localhost:8501
```

## 🔄 Synthetic Data

The `scripts/generate_data.py` script creates:
- **50,000** customers (Bronze/Silver/Gold/Platinum tiers)
- **200,000** orders (various statuses, payment methods)
- **500,000** order items (with discounts, quantities)
- **1,000** products (6 categories)
- **100** campaigns (5 channels)
- **2M** web events (page_view, add_to_cart, purchase, wishlist)

Data includes intentional quality issues (nulls, duplicates, late-arriving records) to make tests meaningful.

## 🚀 CI/CD Pipeline

GitHub Actions workflow (`.github/workflows/dbt_ci.yml`):
1. Install dependencies
2. Generate synthetic data
3. `dbt seed` — load reference data
4. SQL linting with sqlfluff
5. `dbt run --select staging` — fast staging check
6. `dbt test --select staging` — validate staging layer
7. `dbt run` — full model run
8. `dbt test` — comprehensive test suite
9. `dbt docs generate` — build documentation
10. Comment PR with results

## 📚 dbt Documentation

View the lineage graph and column-level documentation:

```bash
make docs
```

This opens http://localhost:8000 with interactive DAG showing:
- Model lineage
- Column descriptions & types
- Test coverage
- Source freshness checks
- Exposures (dashboard, BI tools)

## 🎓 Learning Resources

Each model includes:
- Column-level descriptions
- Data type specifications
- Contract enforcement
- Test coverage
- Owner & steward metadata

Check out:
- `dataforge/models/sources.yml` — source definitions & freshness
- `dataforge/models/staging/_staging.yml` — schema contracts
- `dataforge/dbt_project.yml` — project-wide config
- `dataforge/macros/` — reusable SQL functions

## 🔐 Data Privacy & Governance

- **PII masking** — customer emails hashed in staging
- **PII tag** — marked on sensitive columns
- **Row-level tests** — orphan detection, revenue reconciliation
- **Source freshness** — warn after 12h, error after 24h
- **Model contracts** — enforced schemas prevent breaking changes

## 💡 Advanced Patterns Used

1. **Window Functions** — running totals, sessionization, ranking
2. **CTEs** — nested logic for attribution, cohort analysis
3. **Surrogate Keys** — MD5 hashing for customer/session IDs
4. **Slowly Changing Dimensions** — snapshots with dbt_valid_from/to
5. **Attribution Modeling** — first-touch, last-touch, linear
6. **Incremental Loads** — append/merge strategies (configured in profiles)
7. **Materialization Logic** — views for staging, tables for marts
8. **Safe Arithmetic** — divide-by-zero handling via macros

## 📞 Support & Troubleshooting

### Common Issues

**"dbt parse" fails**
```bash
dbt deps && dbt parse  # Reinstall packages and retry
```

**DuckDB file locked**
```bash
rm dataforge/dataforge.duckdb*  # Delete and re-run
dbt run
```

**Port 8000/8501 already in use**
```bash
make docs -- --port 8001      # Use different port
make dashboard -- --server.port 8502
```

## 📜 License & Portfolio Use

This project is designed for:
- ✅ Portfolio demonstration
- ✅ Interview preparation
- ✅ Learning dbt best practices
- ✅ Template for new analytics projects
- ✅ Open source contribution examples

## 🤝 Contributing

Fork, customize, and make it your own! Suggestions:
- Add real data connectors (APIs, databases)
- Extend semantic models with more metrics
- Deploy to Snowflake/Databricks
- Add ML features (propensity scoring, clustering)
- Implement row-level security (RLS)

---

**Built with ❤️ for analytics engineers**  
DataForge Analytics Platform v1.0  
Zero-cost, production-ready, portfolio-grade.
