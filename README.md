# 📈 Financial Market ETL Warehouse

[![Streamlit App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?logo=streamlit&logoColor=white)](https://financial-market-etl-warehouse.streamlit.app/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://www.postgresql.org/)
[![Automation](https://img.shields.io/badge/Automation-GitHub%20Actions-green)](https://github.com/features/actions)

## 🌟 Overview
This project is a production-grade **Automated Data Warehouse** designed to ingest, process, and visualize financial market data. Moving beyond simple scripts, this system implements a full **ETL (Extract, Transform, Load)** pipeline that runs autonomously in the cloud.

The pipeline focuses on "Derived Insights"—calculating technical indicators like Moving Averages and Volatility within the processing layer before storing them in a persistent PostgreSQL instance for high-speed dashboarding.

---

## 🏗️ Architecture
The system is built using a decoupled architecture to ensure scalability and reliability:

1.  **Extraction:** Python-based ingestion from the `yfinance` API for ASX market data.
2.  **Transformation:** Data cleaning and feature engineering using **Pandas** (7-day Moving Averages, Normalization, Daily Returns).
3.  **Storage:** Persistent storage in a **PostgreSQL** database (hosted on Supabase) utilizing **SQLAlchemy** for ORM and schema management.
4.  **Orchestration:** Fully automated via **GitHub Actions** using CRON scheduling (Daily at 00:00 UTC).
5.  **Visualization:** A live **Streamlit** dashboard pulling directly from the SQL warehouse to provide real-time analytics.

---

## 🚀 Key Features
*   **Idempotent Upsert Logic:** Implemented `ON CONFLICT` SQL logic to prevent data duplication and ensure the pipeline is re-runnable without corrupting the history.
*   **Cloud-Native Design:** Developed locally using **Docker** and migrated to a cloud-based PostgreSQL instance (Supabase) for production.
*   **Security First:** Utilized **GitHub Secrets** and **Streamlit Secrets** management to handle sensitive database credentials, ensuring no hardcoded passwords in the version control.
*   **Optimized Performance:** Implemented SQL Indexing on `(date, ticker)` to ensure sub-second query times for the frontend dashboard.
*   **Automated Failure Handling:** Integrated logging and exit-code triggers within GitHub Actions to monitor pipeline health.

---

## 🛠️ Tech Stack
*   **Language:** Python 3.10+
*   **Data Analysis:** Pandas, NumPy
*   **Database:** PostgreSQL, SQLAlchemy
*   **DevOps:** Docker, GitHub Actions (CI/CD), YAML
*   **Visualization:** Streamlit, Plotly Express

---

## 📊 Live Dashboard
Access the live interactive analytics here: 
👉 **[Financial Market Warehouse App](https://financial-market-etl-warehouse.streamlit.app/)**

---

## 📂 Project Structure
```text
├── .github/workflows/
│   └── daily_etl.yml    # Automation & CRON logic
├── main.py              # ETL Script (Extract, Transform, Load)
├── app.py               # Streamlit Dashboard code
├── requirements.txt     # Dependency management
└── README.md            # Documentation
```

---

## ⚙️ Local Setup
1. **Clone the repo:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Financial-Market-ETL-Warehouse.git
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Environment Variables:**
   Set up a `secrets.toml` file with your `DATABASE_URL`.
4. **Run the Dashboard:**
   ```bash
   streamlit run app.py
   ```
