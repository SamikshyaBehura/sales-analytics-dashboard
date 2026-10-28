from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "sample_sales.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["profit"] = df["revenue"] * df["profit_margin"]
    return df

df = load_data()

st.title("📊 Sales Analytics Dashboard")
st.caption("An interactive portfolio project built with Python, Pandas, Plotly, and Streamlit.")
with st.sidebar:
    st.header("Filters")
    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["region"].unique()), default=sorted(df["region"].unique()))
    categories = st.multiselect("Category", sorted(df["category"].unique()), default=sorted(df["category"].unique()))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = df[
    df["order_date"].dt.date.between(start_date, end_date)
    & df["region"].isin(regions)
    & df["category"].isin(categories)
]

if filtered.empty:
    st.warning("No sales match these filters. Select a wider date range or more categories/regions.")
    st.stop()

revenue = filtered["revenue"].sum()
profit = filtered["profit"].sum()
orders = filtered["order_id"].nunique()
avg_order = revenue / orders if orders else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total revenue", f"${revenue:,.0f}")
c2.metric("Total profit", f"${profit:,.0f}")
c3.metric("Orders", f"{orders:,}")
c4.metric("Average order value", f"${avg_order:,.2f}")

st.divider()
left, right = st.columns(2)
with left:
    st.subheader("Revenue over time")
    daily = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["revenue"].sum()
    fig = px.line(daily, x="month", y="revenue", markers=True, title="Monthly revenue")
    fig.update_layout(xaxis_title="", yaxis_title="Revenue ($)")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Revenue by category")
    by_cat = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    fig = px.bar(by_cat, x="category", y="revenue", color="category", title="Category performance")
    fig.update_layout(showlegend=False, xaxis_title="", yaxis_title="Revenue ($)")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Regional performance")
    by_region = filtered.groupby("region", as_index=False).agg(revenue=("revenue", "sum"), profit=("profit", "sum"))
    fig = px.bar(by_region, x="region", y=["revenue", "profit"], barmode="group", title="Revenue and profit by region")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Top products")
    products = filtered.groupby("product", as_index=False).agg(
        revenue=("revenue", "sum"), units_sold=("quantity", "sum"), profit=("profit", "sum")
    ).sort_values("revenue", ascending=False).head(10)
    st.dataframe(products.style.format({"revenue": "${:,.2f}", "profit": "${:,.2f}"}), use_container_width=True, hide_index=True)

st.subheader("Business insights")
best_category = by_cat.sort_values("revenue", ascending=False).iloc[0]
best_region = by_region.sort_values("revenue", ascending=False).iloc[0]
margin = (profit / revenue * 100) if revenue else 0
i1, i2, i3 = st.columns(3)
i1.info(f"**Top category:** {best_category['category']} generated ${best_category['revenue']:,.0f} in revenue.")
i2.info(f"**Top region:** {best_region['region']} generated ${best_region['revenue']:,.0f} in revenue.")
i3.info(f"**Profit margin:** {margin:.1f}% across the selected data.")

st.subheader("Filtered sales data")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
csv_data = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered data as CSV", data=csv_data, file_name="filtered_sales.csv", mime="text/csv")

st.caption("Dataset is synthetic and intended for demonstration. Replace it with properly licensed data for real analysis.")
