#!/usr/bin/env python3
import streamlit as st
import duckdb
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os

# Professional config
st.set_page_config(
    page_title="DataForge Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1f3a93 0%, #2d5a9e 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stMetric {
        background: linear-gradient(135deg, #0f1419 0%, #1a202c 100%);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00d9ff;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"
if "refresh_count" not in st.session_state:
    st.session_state.refresh_count = 0

# Check for refresh
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

current_time = datetime.now()
if (current_time - st.session_state.last_refresh).total_seconds() > 30:
    st.session_state.refresh_count += 1
    st.session_state.last_refresh = current_time
    st.rerun()

# Cache with 29 second TTL
@st.cache_data(ttl=29, max_entries=200)
def query(sql):
    db_path = os.path.join(os.path.dirname(__file__), '..', 'dataforge', 'dataforge.duckdb')
    conn = duckdb.connect(db_path, read_only=True)
    result = pd.read_sql(sql, conn)
    conn.close()
    return result

# Sidebar navigation
with st.sidebar:
    st.title("📊 DataForge")
    st.markdown("---")

    pages = {
        "Dashboard": "📈 Overview",
        "Customer 360": "👥 Customers",
        "Analytics": "📉 Metrics",
        "Funnel": "🔗 Conversion",
        "Retention": "📅 Cohorts"
    }

    for page_key, page_label in pages.items():
        if st.button(page_label, use_container_width=True, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key

    st.markdown("---")
    st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')}")
    st.caption(f"Refresh: #{st.session_state.refresh_count}")

# PAGE 1: DASHBOARD (Overview)
if st.session_state.current_page == "Dashboard":
    st.markdown("# 📊 Real-Time Analytics Dashboard")
    st.markdown("**Live data streaming • Updated every 30 seconds**")

    # Top metrics
    col1, col2, col3, col4, col5 = st.columns(5)

    orders_30 = query("SELECT COUNT(*) as c FROM raw.orders WHERE order_date > now() - INTERVAL 30 MINUTE")
    events_30 = query("SELECT COUNT(*) as c FROM raw.web_events WHERE event_date > now() - INTERVAL 30 MINUTE")
    revenue = query("SELECT SUM(total_amount) as r FROM raw.orders WHERE status = 'Completed'")
    customers = query("SELECT COUNT(DISTINCT customer_id) as c FROM raw.orders")
    total_orders = query("SELECT COUNT(*) as c FROM raw.orders WHERE status = 'Completed'")

    col1.metric("Orders (30m)", f"{int(orders_30['c'].values[0]):,}" if not orders_30.empty else "0", "+30m")
    col2.metric("Events (30m)", f"{int(events_30['c'].values[0]):,}" if not events_30.empty else "0", "+30m")
    col3.metric("Revenue", f"${revenue['r'].values[0]:,.0f}" if not revenue.empty else "$0", "Total")
    col4.metric("Customers", f"{int(customers['c'].values[0]):,}" if not customers.empty else "0", "Active")
    col5.metric("Total Orders", f"{int(total_orders['c'].values[0]):,}" if not total_orders.empty else "0", "Completed")

    st.markdown("---")

    # Charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Trend (30 Days)")
        daily_rev = query("""
            SELECT DATE(order_date) as d, SUM(total_amount) as r
            FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY DATE(order_date)
            ORDER BY d DESC LIMIT 30
        """)
        if not daily_rev.empty:
            daily_rev = daily_rev.sort_values('d')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=daily_rev['d'], y=daily_rev['r'], fill='tozeroy', name='Revenue', line=dict(color='#00d9ff')))
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0), hovermode='x unified')
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Order Distribution")
        orders_by_status = query("""
            SELECT status, COUNT(*) as c
            FROM raw.orders
            GROUP BY status
        """)
        if not orders_by_status.empty:
            fig = px.pie(orders_by_status, values='c', names='status', color_discrete_sequence=['#00d9ff', '#ff6b6b', '#ffd93d'])
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

# PAGE 2: CUSTOMER 360
elif st.session_state.current_page == "Customer 360":
    st.markdown("# 👥 Customer 360 Profile")
    st.markdown("**Complete customer analytics and segmentation**")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    total_cust = query("SELECT COUNT(DISTINCT customer_id) as c FROM raw.orders WHERE status = 'Completed'")
    avg_spend = query("SELECT AVG(total_amount) as a FROM raw.orders WHERE status = 'Completed'")
    total_revenue = query("SELECT SUM(total_amount) as r FROM raw.orders WHERE status = 'Completed'")
    repeat_customers = query("""
        SELECT COUNT(*) as c FROM (
            SELECT customer_id FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY customer_id
            HAVING COUNT(*) > 1
        )
    """)

    col1.metric("Total Customers", f"{int(total_cust['c'].values[0]):,}" if not total_cust.empty else "0", "Active")
    col2.metric("Avg Spend", f"${avg_spend['a'].values[0]:,.2f}" if not avg_spend.empty else "$0", "Per Order")
    col3.metric("Total Revenue", f"${total_revenue['r'].values[0]:,.0f}" if not total_revenue.empty else "$0", "Completed")
    col4.metric("Repeat Rate", f"{int(repeat_customers['c'].values[0]):,}" if not repeat_customers.empty else "0", "Customers")

    st.markdown("---")

    # Customer visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top Customers by Revenue")
        top_cust = query("""
            SELECT customer_id, SUM(total_amount) as total, COUNT(*) as orders
            FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY customer_id
            ORDER BY total DESC LIMIT 15
        """)
        if not top_cust.empty:
            fig = px.bar(top_cust, x='customer_id', y='total', title='Top 15 Customers',
                        color='total', color_continuous_scale='Blues')
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=30,b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Customer Value Distribution")
        cust_spend = query("""
            WITH customer_totals AS (
                SELECT customer_id, SUM(total_amount) as total_spent
                FROM raw.orders
                WHERE status = 'Completed'
                GROUP BY customer_id
            )
            SELECT
                CASE
                    WHEN total_spent > 10000 THEN 'VIP (>$10k)'
                    WHEN total_spent > 5000 THEN 'Gold ($5k-10k)'
                    WHEN total_spent > 1000 THEN 'Silver ($1k-5k)'
                    ELSE 'Standard (<$1k)'
                END as segment,
                COUNT(*) as count
            FROM customer_totals
            GROUP BY segment
        """)
        if not cust_spend.empty:
            fig = px.bar(cust_spend, x='segment', y='count', color='segment',
                        color_discrete_map={'VIP (>$10k)': '#FFD700', 'Gold ($5k-10k)': '#C0C0C0',
                                           'Silver ($1k-5k)': '#CD7F32', 'Standard (<$1k)': '#808080'})
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=30,b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Customer order frequency
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Orders per Customer")
        order_freq = query("""
            SELECT COUNT(*) as orders, COUNT(DISTINCT customer_id) as customers
            FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY customer_id
            ORDER BY orders DESC LIMIT 30
        """)
        if not order_freq.empty:
            fig = px.histogram(order_freq, x='orders', nbins=20, title='Order Frequency Distribution')
            fig.update_layout(height=350, margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Customer Lifetime Value")
        ltv = query("""
            SELECT
                customer_id,
                COUNT(*) as order_count,
                SUM(total_amount) as ltv,
                AVG(total_amount) as avg_order_value
            FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY customer_id
            ORDER BY ltv DESC LIMIT 100
        """)
        if not ltv.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ltv['order_count'], y=ltv['ltv'], mode='markers',
                                     marker=dict(size=8, color=ltv['ltv'], colorscale='Viridis', showscale=True),
                                     name='LTV'))
            fig.update_layout(title='LTV vs Order Count', xaxis_title='Order Count', yaxis_title='LTV ($)',
                             height=350, margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig, use_container_width=True)

# PAGE 3: ANALYTICS
elif st.session_state.current_page == "Analytics":
    st.markdown("# 📉 RFM Analytics")
    st.markdown("**Recency • Frequency • Monetary Value**")

    col1, col2, col3 = st.columns(3)

    rfm = query("""
        SELECT
            COUNT(DISTINCT customer_id) as customers,
            AVG(total_amount) as avg_value,
            SUM(total_amount) as total_value
        FROM raw.orders
        WHERE status = 'Completed'
    """)

    if not rfm.empty:
        col1.metric("Total Customers", f"{int(rfm['customers'].values[0]):,}")
        col2.metric("Avg Order Value", f"${rfm['avg_value'].values[0]:,.2f}")
        col3.metric("Total Value", f"${rfm['total_value'].values[0]:,.0f}")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Average Order Value Trend")
        aov = query("""
            SELECT DATE(order_date) as d, AVG(total_amount) as avg_val
            FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY DATE(order_date)
            ORDER BY d DESC LIMIT 30
        """)
        if not aov.empty:
            aov = aov.sort_values('d')
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=aov['d'], y=aov['avg_val'], mode='lines+markers',
                                    name='AOV', line=dict(color='#00d9ff', width=3)))
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Order Value Distribution")
        val_dist = query("""
            SELECT
                CASE
                    WHEN total_amount < 100 THEN '<$100'
                    WHEN total_amount < 500 THEN '$100-500'
                    WHEN total_amount < 1000 THEN '$500-1k'
                    ELSE '>$1k'
                END as range,
                COUNT(*) as count
            FROM raw.orders
            WHERE status = 'Completed'
            GROUP BY range
        """)
        if not val_dist.empty:
            fig = px.bar(val_dist, x='range', y='count', color='count', color_continuous_scale='Blues')
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# PAGE 4: FUNNEL
elif st.session_state.current_page == "Funnel":
    st.markdown("# 🔗 Conversion Funnel")
    st.markdown("**Customer journey analysis**")

    funnel_data = query("""
        SELECT event_type, COUNT(DISTINCT customer_id) as customers
        FROM raw.web_events
        GROUP BY event_type
        ORDER BY customers DESC
    """)

    if not funnel_data.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            fig = go.Figure(data=[go.Funnel(
                y=funnel_data['event_type'],
                x=funnel_data['customers'],
                marker=dict(color=['#00d9ff', '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'])
            )])
            fig.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col1:
            st.subheader("Event Summary")
            for idx, row in funnel_data.iterrows():
                pct = (row['customers'] / funnel_data['customers'].max()) * 100
                st.write(f"**{row['event_type'].title()}**: {int(row['customers']):,} ({pct:.1f}%)")

# PAGE 5: RETENTION
elif st.session_state.current_page == "Retention":
    st.markdown("# 📅 Cohort Analysis")
    st.markdown("**Customer retention and cohort performance**")

    cohort_data = query("""
        SELECT
            DATE_TRUNC('month', order_date) as month,
            COUNT(DISTINCT customer_id) as customers,
            COUNT(*) as orders,
            SUM(total_amount) as revenue
        FROM raw.orders
        WHERE status = 'Completed'
        GROUP BY DATE_TRUNC('month', order_date)
        ORDER BY month DESC LIMIT 12
    """)

    if not cohort_data.empty:
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Cohorts", len(cohort_data))
        col2.metric("Avg Customers/Month", f"{int(cohort_data['customers'].mean()):,}")
        col3.metric("Avg Revenue/Month", f"${cohort_data['revenue'].mean():,.0f}")

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Cohort Size Trend")
            fig = px.bar(cohort_data, x='month', y='customers', title='Customers per Cohort')
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=30,b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Cohort Revenue Trend")
            fig = px.line(cohort_data, x='month', y='revenue', title='Revenue per Cohort', markers=True)
            fig.update_layout(height=400, margin=dict(l=0,r=0,t=30,b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption(f"🚀 DataForge Analytics | Last Updated: {datetime.now().strftime('%H:%M:%S')} | Refresh Count: #{st.session_state.refresh_count}")
