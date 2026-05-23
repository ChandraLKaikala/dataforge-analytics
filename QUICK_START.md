# DataForge Real-Time Analytics - Quick Start Guide

## 🚀 Three Command Setup

### Current Status
✅ Data generation IN PROGRESS:
- customers.csv: 500,000 rows (100%)
- products.csv: 50,000 rows (100%)
- campaigns.csv: 10,000 rows (100%)
- orders.csv: 4.4M rows (88% complete, target 5M)
- order_items.csv: 250K rows (1.7%, target 15M - still generating)
- web_events.csv: 100K rows (0.2%, target 100M max)

**Est. time to completion: 5-10 minutes**

---

## ⏱️ While Data Generates

You can prepare the environment while data generates:

```powershell
# Install/verify dependencies
pip install -q duckdb streamlit plotly faker numpy pandas
```

---

## 🎯 Once Data Generation Completes

### Step 1: Load Data into DuckDB
```powershell
cd C:\Users\lokes\Downloads\DBT_Project
python init_database.py
```

**What this does**:
- Creates `raw` schema in DuckDB
- Loads all CSV files (currently: 5.3M+ records)
- Optimizes database settings
- Creates cache views

**Time**: ~30 seconds for current data

---

### Step 2: Build Analytical Marts
```powershell
python build_marts.py
```

**What this does**:
- Creates 7 analytical tables:
  - `mart_revenue_analytics` - daily revenue trends
  - `mart_customer_360` - customer profiles
  - `mart_product_analytics` - product performance
  - `mart_rfm_segmentation` - customer segments
  - `mart_funnel_analytics` - conversion funnel
  - `mart_attribution` - campaign attribution
  - `mart_cohort_analysis` - retention analysis

**Time**: ~1-2 minutes

---

### Step 3: Launch Dashboard
```powershell
python -m streamlit run dashboard/app.py
```

**Opens**: http://localhost:8501

Dashboard auto-refreshes every 30 seconds with:
- 📊 Revenue Overview
- 👥 Customer 360
- 📈 RFM Segments
- 🔗 Funnel Analytics
- 📅 Cohort Retention

---

## 📊 What You'll See

### Metrics with 5M+ Orders:
- Total Revenue: Multi-millions
- Customers: 500K unique
- Product Categories: 8 categories
- Daily orders: Thousands per day
- Customer segments: 5 RFM groups
- Funnel stages: 7 event types

### Charts Auto-Update:
- Every 30 seconds (configurable)
- Real-time refresh indicator
- Live status badge

---

## 🛑 Stop Dashboard

```powershell
Ctrl+C  # in PowerShell window
```

---

## 🆘 If Data Generation Stalls

Data generation creates large files and takes time. If it seems stuck:

1. Check progress:
   ```powershell
   python monitor_data_generation.py
   ```

2. If still generating, wait 2-3 more minutes

3. If genuinely stuck, stop it (Ctrl+C) and start with smaller data:
   ```powershell
   # Use existing data (250K records)
   python init_database.py
   python build_marts.py
   python -m streamlit run dashboard/app.py
   ```

---

## 📁 Files You Need

✅ Pre-generated:
- `generate_large_data.py` - (currently running)
- `init_database.py` - (ready to use)
- `build_marts.py` - (ready to use)
- `dashboard/app.py` - (enhanced with real-time refresh)
- `dataforge/dataforge.duckdb` - (will be created)

---

## 🎯 Success Indicators

After step 3 (Dashboard Launch), you should see:

✅ Dashboard loads at http://localhost:8501  
✅ "Last Refresh" shows current time  
✅ "Status" shows 🟢 Live  
✅ Charts display data (not empty)  
✅ All 5 sidebar pages available  

---

## 📚 Full Documentation

For detailed info on architecture, optimization, troubleshooting:
- See: `REALTIME_ANALYTICS_SETUP.md`

---

## ⏱️ Time Estimates

| Step | Time | Notes |
|------|------|-------|
| Data Generation | 5-10 min | In progress |
| Load to DuckDB | 30 sec | After gen complete |
| Build Marts | 1-2 min | SQL aggregations |
| Dashboard Load | 5 sec | First load |
| Dashboard Refresh | 30 sec | Then auto-refresh |
| **TOTAL** | **~7-14 min** | One-time setup |

---

## 🎉 You're Ready!

Once dashboard opens, you have a **production-grade real-time analytics platform** running on your local machine with:
- 5M+ synthetic orders
- 500K customers
- Zero cloud infrastructure
- Zero recurring cost
- 30-second auto-refresh
- Full data lineage

Enjoy your real-time analytics! 🚀
