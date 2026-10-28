# Sales Analytics Dashboard

An interactive sales analytics dashboard built with **Python**, **Pandas**, **Plotly**, and **Streamlit**. It uses a clearly labeled synthetic dataset so the project can run locally without API keys or database credentials.

## Features
- KPI cards for revenue, profit, order count, and average order value
- Filters for date range, region, and product category
- Monthly revenue trend
- Revenue by category and region
- Top-product table and simple business insights
- Download filtered results as CSV

## Screenshots
Run the app locally and add screenshots here, for example `![Dashboard](screenshots/dashboard.png)`.

## Requirements
- Python 3.10 or newer
- Internet access for installing dependencies the first time

## Run on Windows

Open PowerShell in this project folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, you can skip activation and run:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Project structure

```text
sales-analytics-dashboard/
├── app.py
├── data/
│   └── sample_sales.csv
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## How to customize it
1. Replace `data/sample_sales.csv` with a dataset you are permitted to use. Keep columns `order_id`, `order_date`, `region`, `category`, `product`, `quantity`, `unit_price`, and `profit_margin`.
2. Update the dashboard title, currency format, or categories to fit your chosen domain.
3. Add a new analysis, such as monthly growth, repeat customers, or a forecast. Explain your methodology in the README.
4. Capture screenshots of the running dashboard and add them to a `screenshots/` folder.
5. Add tests and document any limitations.

## Data note
The included records are synthetic demonstration data, not real company sales. Do not present the generated results as real business findings.

## License
This project is released under the MIT License. See `LICENSE`. The license applies to this project's original code; verify the licenses of any third-party assets or data you add.
