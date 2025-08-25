# Multi-Store Profitability Analysis App (Dash + Mantine)

A Python-only web app for multi-store profitability analysis with better design than Streamlit.
Includes: data ingestion, dashboards, store P&L, overhead allocation, and scenario simulation.

## 1. Quick Start

```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

```bash
# macOS / Linux
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open the URL printed in the console (usually http://127.0.0.1:8050).

## 2. Project Structure

```
multistore_profit_app/
├─ app.py
├─ requirements.txt
├─ README.md
├─ .env.example
├─ assets/
│   └─ style.css
├─ lib/
│   ├─ data_loader.py
│   ├─ metrics.py
│   ├─ allocator.py
│   ├─ simulator.py
│   └─ utils.py
├─ pages/
│   ├─ 1_📥_データ取込.py
│   ├─ 2_📊_ダッシュボード.py
│   ├─ 3_🏬_店舗別PL.py
│   ├─ 4_🧮_間接費配賦.py
│   └─ 5_🧪_シミュレーション.py
└─ data/
    └─ sample/
        ├─ sales.csv
        ├─ expenses.csv
        ├─ overhead.csv
        └─ store_master.csv
```

## 3. Pages Overview

- **📥 データ取込**: Upload CSV/Excel, preview, basic validation, and save to `data/`.
- **📊 ダッシュボード**: KPIs (Revenue, Gross Profit, EBIT), charts by month/store/channel.
- **🏬 店舗別PL**: Monthly P&L by store. Drill-down by account/product category.
- **🧮 間接費配賦**: Allocate HQ overhead with selectable bases (sales, GP, headcount, area).
- **🧪 シミュレーション**: Price/volume/mix/cost sliders; BEP and profit sensitivity.

## 4. Environment

Copy `.env.example` to `.env` if you want to customize settings (like PORT or DATA_DIR).
