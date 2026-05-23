# 🚀 HOW TO RUN DataForge Analytics Dashboard

## Quick Start (3 Steps)

### Step 1: Open Command Prompt / PowerShell
```
Windows Key + R
Type: powershell
Press: Enter
```

### Step 2: Navigate to Project
```powershell
cd C:\Users\lokes\Downloads\DBT_Project
```

### Step 3: Start Dashboard
```powershell
python -m streamlit run dashboard/app.py
```

**That's it!** Dashboard opens automatically at: **http://localhost:8501**

---

## ✅ Detailed Steps with Screenshots

### **STEP 1: Open Windows Terminal/PowerShell**

**Option A: Using Windows Search**
1. Press `Windows Key`
2. Type `PowerShell`
3. Click `Windows PowerShell`

**Option B: Using Run Dialog**
1. Press `Windows Key + R`
2. Type `powershell`
3. Press `Enter`

**Option C: From File Explorer**
1. Open File Explorer
2. Navigate to: `C:\Users\lokes\Downloads\DBT_Project`
3. Right-click empty space
4. Select: `Open in Terminal` or `Open PowerShell window here`

---

### **STEP 2: Navigate to Project Folder**

Copy and paste this command:

```powershell
cd C:\Users\lokes\Downloads\DBT_Project
```

Press `Enter`

**Expected output:**
```
PS C:\Users\lokes\Downloads\DBT_Project>
```

---

### **STEP 3: Run Dashboard**

Copy and paste this command:

```powershell
python -m streamlit run dashboard/app.py
```

Press `Enter`

**Expected output:**
```
  Welcome to Streamlit!

      If you'd like to receive helpful onboarding emails...
      Email: [just press Enter to skip]

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

---

### **STEP 4: Open in Browser**

**Option A: Automatic (Recommended)**
- Browser may open automatically
- If not, manually go to: **http://localhost:8501**

**Option B: Manual**
1. Open any web browser (Chrome, Firefox, Edge, etc.)
2. Paste in address bar: `http://localhost:8501`
3. Press `Enter`

---

## 🎯 Expected Dashboard

Once open, you should see:

```
📊 DataForge Analytics Platform
├── 💰 Revenue Overview
├── 👥 Customer 360
├── 📈 RFM Segments
├── 🔗 Funnel Analytics
└── 📅 Cohort Retention
```

Click the **sidebar** on the left to switch between pages.

---

## 🎮 Interact with Dashboard

### **Navigation**
- Click page names in sidebar to switch
- Scroll down to see all charts

### **Explore Charts**
- **Hover** over charts to see values
- **Zoom** using chart toolbar
- **Download** using camera icon

---

## 🛑 Stop Dashboard (When Done)

In PowerShell window:
```
Press: Ctrl+C
```

Or just close the PowerShell window.

---

## ⚠️ Troubleshooting

### **Problem: "python: command not found"**
**Solution:** 
1. Close PowerShell
2. Open it again in the project folder
3. Try: `python --version`
4. If still fails, Python may not be in PATH
5. Use full path: `C:\Users\lokes\AppData\Local\Microsoft\WindowsApps\python.exe -m streamlit run dashboard/app.py`

### **Problem: "streamlit: command not found"**
**Solution:** 
- Use: `python -m streamlit run dashboard/app.py` (already included above)

### **Problem: "Port 8501 already in use"**
**Solution:**
- Use different port:
```powershell
python -m streamlit run dashboard/app.py --server.port 8502
```
- Then open: `http://localhost:8502`

### **Problem: Browser won't connect**
**Solution:**
1. Check PowerShell shows: `Local URL: http://localhost:8501`
2. Wait 10-15 seconds for startup
3. Try refreshing browser (F5)
4. Check if firewall is blocking (Windows Defender)

### **Problem: Charts show "No data"**
**Solution:**
1. Check if DuckDB file exists:
   ```powershell
   Test-Path "dataforge/dataforge.duckdb"
   ```
2. If missing, regenerate:
   ```powershell
   python init_database.py
   ```

---

## 📋 Common Commands

### **Run Dashboard (Normal)**
```powershell
python -m streamlit run dashboard/app.py
```

### **Run Dashboard (Debug Mode)**
```powershell
python -m streamlit run dashboard/app.py --logger.level=debug
```

### **Run Dashboard (Custom Port)**
```powershell
python -m streamlit run dashboard/app.py --server.port 8502
```

### **Run Dashboard (External Access)**
```powershell
python -m streamlit run dashboard/app.py --server.address 0.0.0.0
```
Then access from another computer: `http://<YOUR_PC_IP>:8501`

### **Check Configuration**
```powershell
python -m streamlit config show
```

### **Regenerate Synthetic Data**
```powershell
python scripts/generate_data.py
python init_database.py
```

---

## 🔄 Full Workflow

If you want to also run dbt models + dashboard:

### **Complete Setup**
```powershell
cd C:\Users\lokes\Downloads\DBT_Project

# 1. Regenerate synthetic data
python scripts/generate_data.py

# 2. Load data into DuckDB
python init_database.py

# 3. Install/update dbt packages
python run_dbt.py deps

# 4. Load seeds
python run_dbt.py seed

# 5. Run dbt models (builds views/tables)
python run_dbt.py run

# 6. Run tests (validates data)
python run_dbt.py test

# 7. Start dashboard
python -m streamlit run dashboard/app.py
```

---

## 📊 What Each Dashboard Page Shows

### **1. Revenue Overview**
- Total revenue, orders, AOV
- Daily revenue trend (30 days)
- Daily profit trend (30 days)

### **2. Customer 360**
- Total customers, avg LTV, max LTV
- Customers by tier
- Churn risk distribution

### **3. RFM Segments**
- Customers by RFM segment
- Average value per segment
- Segment performance

### **4. Funnel Analytics**
- Event-to-conversion funnel
- Drop-off at each stage
- Revenue per funnel step

### **5. Cohort Retention**
- Heatmap of retention by cohort
- Months since acquisition
- Retention trends

---

## 💡 Tips & Tricks

### **Keep Dashboard Running**
- Don't close the PowerShell window
- Dashboard continues running as long as window is open

### **Make Changes**
- Edit files in `dashboard/app.py`
- Dashboard auto-reloads (watch for "Rerun" button in browser)
- Or press `R` in browser to manually rerun

### **Clear Cache**
- Press `C` in browser or
- Delete: `.streamlit/` folder

### **Share URL**
- Local: `http://localhost:8501` (only works on your computer)
- Remote: Get your IP with `ipconfig` in PowerShell
- Share: `http://<YOUR_IP>:8501` (others on same network)

---

## 🎓 Learning Path

1. **Run Dashboard** (this guide)
2. **Explore Data** (click through 5 pages)
3. **Understand Models** (check `dataforge/models/marts/`)
4. **Customize** (edit `dashboard/app.py`)
5. **Add Metrics** (create new dbt model)
6. **Deploy** (host on Streamlit Cloud)

---

## 📞 Quick Reference

| Task | Command |
|------|---------|
| Start dashboard | `python -m streamlit run dashboard/app.py` |
| Stop dashboard | `Ctrl+C` |
| Regenerate data | `python scripts/generate_data.py` |
| Load data to DB | `python init_database.py` |
| Run dbt models | `python run_dbt.py run` |
| Run dbt tests | `python run_dbt.py test` |
| View dbt docs | `python run_dbt.py docs serve` |
| Debug dashboard | `python -m streamlit run dashboard/app.py --logger.level=debug` |

---

## ✅ Checklist: Before You Start

- [ ] PowerShell/Terminal open
- [ ] In folder: `C:\Users\lokes\Downloads\DBT_Project`
- [ ] `dataforge/dataforge.duckdb` exists
- [ ] `dashboard/app.py` exists
- [ ] Python installed (`python --version` works)
- [ ] Streamlit installed (`pip show streamlit`)

---

## 🎉 You're Ready!

```powershell
cd C:\Users\lokes\Downloads\DBT_Project
python -m streamlit run dashboard/app.py
```

**Then open:** http://localhost:8501

---

**Last Updated:** 2026-05-23  
**Status:** Ready to use ✅
