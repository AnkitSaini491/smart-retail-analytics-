

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Smart Retail Analytics",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ Smart Retail Analytics Dashboard")
st.write("Customer Footfall and Sales Analysis using Python")

# Load dataset
uploaded_file = st.sidebar.file_uploader(
    "Upload Sales CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
elif Path("sales.csv").exists():
    df = pd.read_csv("sales.csv")
else:
    # Sample data for demonstration
    df = pd.DataFrame({
        "Product": [
            "Laptop", "Mobile", "Headphones",
            "Laptop", "Mobile", "Keyboard",
            "Headphones", "Mobile"
        ],
        "Category": [
            "Electronics", "Electronics", "Accessories",
            "Electronics", "Electronics", "Accessories",
            "Accessories", "Electronics"
        ],
        "Sales": [45000, 20000, 2500, 50000, 18000, 1500, 3000, 22000],
        "Customers": [12, 20, 15, 14, 25, 10, 18, 22],
        "Hour": ["10 AM", "11 AM", "12 PM", "1 PM",
                 "2 PM", "3 PM", "4 PM", "5 PM"]
    })

# Validate required columns
required_columns = ["Product", "Category", "Sales", "Customers"]

if not all(col in df.columns for col in required_columns):
    st.error(
        "CSV must contain: Product, Category, Sales, Customers"
    )
    st.stop()

# Clean numeric columns
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Customers"] = pd.to_numeric(df["Customers"], errors="coerce")
df = df.dropna(subset=["Sales", "Customers"])

if df.empty:
    st.warning("No valid sales data found.")
    st.stop()

# Sidebar filters
st.sidebar.header("Filters")

categories = sorted(df["Category"].dropna().unique().tolist())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories
)

filtered_df = df[df["Category"].isin(selected_categories)]

if filtered_df.empty:
    st.info("Select at least one category to view analytics.")
    st.stop()

# Key performance indicators
total_sales = filtered_df["Sales"].sum()
total_customers = filtered_df["Customers"].sum()
total_products = filtered_df["Product"].nunique()
average_sales = filtered_df["Sales"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("👥 Customer Visits", f"{total_customers:,.0f}")
col3.metric("📦 Products", total_products)
col4.metric("📊 Avg. Sale", f"₹{average_sales:,.0f}")

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("Sales by Product")
    product_sales = (
        filtered_df.groupby("Product", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        color="Sales",
        title="Product-wise Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Sales by Category")
    category_sales = (
        filtered_df.groupby("Category", as_index=False)["Sales"]
        .sum()
    )

    fig = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.4,
        title="Category-wise Sales"
    )
    st.plotly_chart(fig, use_container_width=True)

# Customer analysis
st.subheader("Customer Footfall by Product")

customer_data = (
    filtered_df.groupby("Product", as_index=False)["Customers"]
    .sum()
    .sort_values("Customers", ascending=False)
)

fig = px.bar(
    customer_data,
    x="Product",
    y="Customers",
    title="Customer Visits by Product",
    color="Customers"
)
st.plotly_chart(fig, use_container_width=True)

# Dataset
st.subheader("📋 Sales Data")
st.dataframe(filtered_df, use_container_width=True)

# Download filtered data
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Analytics Data",
    data=csv_data,
    file_name="retail_analytics.csv",
    mime="text/csv"
)

st.caption(
    "Smart Retail Analytics | Built with Python, Pandas, "
    "Plotly and Streamlit"
)
