#!/usr/bin/env python3
import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

st.set_page_config(page_title="DataForge", layout="wide")

@st.cache_data(ttl=29)
def query(sql):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'dataforge', 'dataforge.duckdb')
    conn = duckdb.connect(db_path, read_only=True)
    result = pd.read_sql(sql, conn)
    conn.close()
    return result

# Title
st.title("DataForge Real-Time Analytics")
st.subheader("Live Dashboard | Data Updates Every 30 Seconds")

# Sidebar - Page Selection
page = st.sidebar.radio("SELECT PAGE",
    ["Dashboard", "Customer 360", "Analytics", "Funnel", "Retention"],
    label_visibility="visible")

st.sidebar.divider()
st.sidebar.write(f"Updated: {datetime.now().strftime('%H:%M:%S')}")

# ============ DASHBOARD PAGE ============
if page == "Dashboard":
    st.header("Overview")

    col1, col2, col3, col4, col5 = st.columns(5)

    orders = query("SELECT COUNT(*) as c FROM raw.orders WHERE status='Completed'")
    events = query("SELECT COUNT(*) as c FROM raw.web_events")
    rev = query("SELECT SUM(total_amount) as r FROM raw.orders WHERE status='Completed'")
    cust = query("SELECT COUNT(DISTINCT customer_id) as c FROM raw.orders")
    avg_order = query("SELECT AVG(total_amount) as a FROM raw.orders")

    col1.metric("Orders", f"{int(orders['c'].values[0]):,}")
    col2.metric("Events", f"{int(events['c'].values[0]):,}")
    col3.metric("Revenue", f"${rev['r'].values[0]:,.0f}")
    col4.metric("Customers", f"{int(cust['c'].values[0]):,}")
    col5.metric("Avg Order", f"${avg_order['a'].values[0]:.2f}")

    st.divider()

    # Revenue chart
    daily = query("SELECT DATE(order_date) as d, SUM(total_amount) as r FROM raw.orders WHERE status='Completed' GROUP BY DATE(order_date) ORDER BY d DESC LIMIT 30")
    if not daily.empty:
        daily = daily.sort_values('d')
        fig = px.line(daily, x='d', y='r', title='Revenue Trend', markers=True)
        st.plotly_chart(fig, use_container_width=True)

# ============ CUSTOMER 360 PAGE ============
elif page == "Customer 360":
    st.header("Customer Analytics")

    # Get data
    total_cust = query("SELECT COUNT(DISTINCT customer_id) as c FROM raw.orders WHERE status='Completed'")
    avg_spend = query("SELECT AVG(total_amount) as a FROM raw.orders WHERE status='Completed'")
    total_rev = query("SELECT SUM(total_amount) as r FROM raw.orders WHERE status='Completed'")
    repeat = query("SELECT COUNT(*) as c FROM (SELECT customer_id FROM raw.orders WHERE status='Completed' GROUP BY customer_id HAVING COUNT(*) > 1)")

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{int(total_cust['c'].values[0]):,}")
    col2.metric("Avg Spend", f"${avg_spend['a'].values[0]:,.2f}")
    col3.metric("Total Revenue", f"${total_rev['r'].values[0]:,.0f}")
    col4.metric("Repeat Customers", f"{int(repeat['c'].values[0]):,}")

    st.divider()
    st.subheader("Top Customers by Revenue")

    # Top customers chart
    top_cust = query("""
        SELECT customer_id, SUM(total_amount) as total, COUNT(*) as orders
        FROM raw.orders WHERE status='Completed'
        GROUP BY customer_id ORDER BY total DESC LIMIT 15
    """)

    if not top_cust.empty:
        fig = px.bar(top_cust, x='customer_id', y='total', title='Top 15 Customers by Spend')
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Top Customers Table")
        st.dataframe(top_cust, use_container_width=True)

    st.divider()
    st.subheader("Customer Segmentation")

    # Customer segments
    segments = query("""
        SELECT segment, COUNT(*) as customers
        FROM (
            SELECT
                CASE
                    WHEN SUM(total_amount) > 10000 THEN 'VIP (>$10k)'
                    WHEN SUM(total_amount) > 5000 THEN 'Gold ($5k-10k)'
                    WHEN SUM(total_amount) > 1000 THEN 'Silver ($1k-5k)'
                    ELSE 'Standard (<$1k)'
                END as segment
            FROM raw.orders WHERE status='Completed'
            GROUP BY customer_id
        ) subquery
        GROUP BY segment
    """)

    if not segments.empty:
        fig = px.pie(segments, values='customers', names='segment', title='Customer Segments')
        st.plotly_chart(fig, use_container_width=True)

# ============ ANALYTICS PAGE ============
elif page == "Analytics":
    st.header("RFM Analysis")

    rfm = query("""
        SELECT COUNT(DISTINCT customer_id) as customers, AVG(total_amount) as avg_val
        FROM raw.orders WHERE status='Completed'
    """)

    col1, col2 = st.columns(2)
    col1.metric("Customers", f"{int(rfm['customers'].values[0]):,}")
    col2.metric("Avg Order Value", f"${rfm['avg_val'].values[0]:,.2f}")

    st.divider()

    # AOV trend
    aov = query("""
        SELECT DATE(order_date) as d, AVG(total_amount) as avg_val
        FROM raw.orders WHERE status='Completed'
        GROUP BY DATE(order_date) ORDER BY d DESC LIMIT 30
    """)

    if not aov.empty:
        aov = aov.sort_values('d')
        fig = px.line(aov, x='d', y='avg_val', title='Average Order Value Trend', markers=True)
        st.plotly_chart(fig, use_container_width=True)

# ============ FUNNEL PAGE ============
elif page == "Funnel":
    st.header("Conversion Funnel")

    funnel = query("""
        SELECT event_type, COUNT(DISTINCT customer_id) as customers
        FROM raw.web_events GROUP BY event_type ORDER BY customers DESC
    """)

    if not funnel.empty:
        fig = go.Figure(data=[go.Funnel(y=funnel['event_type'], x=funnel['customers'])])
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Event Summary")
        st.dataframe(funnel, use_container_width=True)

# ============ RETENTION PAGE ============
elif page == "Retention":
    st.header("Cohort Analysis")

    cohort = query("""
        SELECT DATE_TRUNC('month', order_date) as month, COUNT(DISTINCT customer_id) as customers, COUNT(*) as orders, SUM(total_amount) as revenue
        FROM raw.orders WHERE status='Completed'
        GROUP BY DATE_TRUNC('month', order_date) ORDER BY month DESC LIMIT 12
    """)

    if not cohort.empty:
        col1, col2 = st.columns(2)
        col1.metric("Total Cohorts", len(cohort))
        col2.metric("Avg Customers/Month", f"{int(cohort['customers'].mean()):,}")

        st.divider()

        # Cohort chart
        fig = px.bar(cohort, x='month', y='customers', title='Customers by Cohort')
        st.plotly_chart(fig, use_container_width=True)

        # Cohort table
        st.subheader("Cohort Details")
        st.dataframe(cohort, use_container_width=True)
