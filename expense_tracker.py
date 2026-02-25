import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state for expenses
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []

st.title("💰 Smart Expense Tracker & Dashboard")

# --- Add Expense Form ---
with st.form("add_expense"):
    title = st.text_input("Expense Title")
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Other"])
    date = st.date_input("Date")
    submitted = st.form_submit_button("Add Expense")

    if submitted and title and amount > 0:
        st.session_state["expenses"].append({
            "title": title,
            "amount": amount,
            "category": category,
            "date": str(date)
        })
        st.success("Expense added!")

# Convert to DataFrame
df = pd.DataFrame(st.session_state["expenses"])

# --- Display Expenses ---
st.subheader("📋 Expense List")
if not df.empty:
    st.dataframe(df)

    # Delete functionality
    delete_index = st.number_input("Enter row index to delete", min_value=0, max_value=len(df)-1, step=1)
    if st.button("Delete Expense"):
        st.session_state["expenses"].pop(delete_index)
        st.experimental_rerun()

    # --- Total Spending ---
    st.subheader("💵 Total Spending")
    st.write(f"Total: ${df['amount'].sum():.2f}")

    # --- Category Breakdown ---
    st.subheader("📊 Category Breakdown")
    category_totals = df.groupby("category")["amount"].sum()

    fig, ax = plt.subplots()
    category_totals.plot(kind="bar", ax=ax)
    st.pyplot(fig)

    # --- Filtering ---
    st.subheader("🔍 Filter Expenses")
    filter_category = st.selectbox("Filter by Category", ["All"] + df["category"].unique().tolist())
    filter_date = st.date_input("Filter by Date")

    filtered_df = df.copy()
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df["category"] == filter_category]
    if filter_date:
        filtered_df = filtered_df[filtered_df["date"] == str(filter_date)]

    st.dataframe(filtered_df)

else:
    st.info("No expenses yet. Add some above!")
