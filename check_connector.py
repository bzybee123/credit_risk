import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt

# ---------- Load Data from MySQL ----------
@st.cache_data
def get_data():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='Shivani@123',
        database='my_database'
    )
    query = "SELECT * FROM credit_risk_data;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# ---------- Streamlit Layout ----------
st.set_page_config(page_title="Credit Risk Dashboard", layout="wide")
st.title("💳 Credit Risk Analysis Dashboard")

data = get_data()

# ---------- Top-Level Metrics ----------
st.markdown("### 📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Records", len(data))
with col2:
    st.metric("Loan Types", data['loan_intent'].nunique())
with col3:
    st.metric("Loan Grades", data['loan_grade'].nunique())
with col4:
    default_rate = data['cb_person_default_on_file'].value_counts(normalize=True).get('Y', 0) * 100
    st.metric("Default Rate", f"{default_rate:.2f}%")

st.markdown("---")

# ---------- Data Preview ----------
with st.expander("🔍 Preview Dataset"):
    st.dataframe(data.head(10), use_container_width=True)

# ---------- Visualizations ----------
st.markdown("## 📈 Visual Insights")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Loan Status")
    st.bar_chart(data['loan_status'].value_counts())

    st.subheader("Loan Grade")
    fig1, ax1 = plt.subplots(figsize=(4, 3))
    data['loan_grade'].value_counts().plot(kind='bar', ax=ax1, color='teal')
    ax1.set_ylabel("Count")
    st.pyplot(fig1)

with col2:
    st.subheader("Loan Intent (Pie)")
    fig2, ax2 = plt.subplots(figsize=(4, 3))
    data['loan_intent'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

    st.subheader("Default History (Pie)")
    fig3, ax3 = plt.subplots(figsize=(4, 3))
    data['cb_person_default_on_file'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['#ff6666','#66b3ff'], ax=ax3)
    ax3.set_ylabel("")
    st.pyplot(fig3)

# ---------- Interest Rate Histogram ----------
st.markdown("### 💡 Interest Rate Distribution")
fig4, ax4 = plt.subplots(figsize=(6, 3))
ax4.hist(data['loan_int_rate'], bins=20, color='skyblue', edgecolor='black')
ax4.set_xlabel("Interest Rate (%)")
ax4.set_ylabel("Frequency")
st.pyplot(fig4)

# ---------- Average Interest Rate by Loan Grade ----------
st.markdown("### 📉 Avg Interest Rate by Grade")
avg_rates = data.groupby("loan_grade")["loan_int_rate"].mean().sort_index()
fig5, ax5 = plt.subplots(figsize=(6, 3))
avg_rates.plot(kind='bar', ax=ax5, color='orange')
ax5.set_ylabel("Avg Interest Rate (%)")
st.pyplot(fig5)

# ---------- SQL-Based Query Results ----------
st.markdown("---")
st.subheader("🧠 Query-Based Insights")

# 1. How many people took Personal Loan with income>= 100000 and took loan amount>=10000?
st.markdown("**1. How many people took Personal Loan with income>= 100000 and took loan amount>=10000?**")
high_income_personal = data[
    (data['person_income'] >= 100000) &
    (data['loan_intent'].str.lower() == "personal") &
    (data['loan_amnt'] >= 10000)
]
st.dataframe(high_income_personal[['person_income', 'loan_intent', 'loan_amnt']])

# 2. To find count of defaulted loan with credit history=3.
st.markdown("**2. To find count of defaulted loan with credit history=3")
default_hist3 = data[
    (data['cb_person_default_on_file'] == "Y") &
    (data['cb_person_cred_hist_length'] == 3)
]
st.write(f"Total: {len(default_hist3)}")
st.dataframe(default_hist3)

# 3. How many people with own house took loan for Home Improvement ?
st.markdown("**3. How many people with own house took loan for Home Improvement ?**")
home_own_improve = data[
    (data['person_home_ownership'] == "OWN") &
    (data['loan_intent'].str.upper() == "HOMEIMPROVEMENT")
]
st.write(f"Total: {len(home_own_improve)}")
st.dataframe(home_own_improve)

# 4. To check defualted loan with loan to income>=0.4.
st.markdown("**4. To check defualted loan with loan to income>=0.4.**")
high_lti_defaults = data[
    (data['loan_percent_income'] >= 0.4) &
    (data['cb_person_default_on_file'] == "Y")
]
st.dataframe(high_lti_defaults[['person_income', 'loan_percent_income', 'cb_person_default_on_file']])

# 5. Line Chart: Find the average loan interest rate (loan_int_rate) for each loan grade, grouped by whether the person has previously defaulted,
#  but only for people earning more than 50,000 and with credit history length ≥ 5 years
st.markdown("**5.  Find the average loan interest rate (loan_int_rate) for each loan grade, grouped by whether the person has previously defaulted, \
but only for people earning more than 50,000 and with credit history length ≥ 5 years)**")
filtered = data[
    (data['person_income'] > 50000) &
    (data['cb_person_cred_hist_length'] >= 5)
]
grouped = filtered.groupby(['loan_grade', 'cb_person_default_on_file'])['loan_int_rate'].mean().reset_index()
grouped.columns = ['Loan Grade', 'Defaulted Before', 'Avg Interest Rate']
grouped = grouped.sort_values(['Loan Grade', 'Defaulted Before'])

# Pivot for line chart
pivot_line = grouped.pivot(index='Loan Grade', columns='Defaulted Before', values='Avg Interest Rate')

st.dataframe(grouped)

st.markdown("#### 📈 Line Chart: Avg Interest Rate by Grade & Default")
fig6, ax6 = plt.subplots(figsize=(6, 3))
pivot_line.plot(marker='o', ax=ax6)
ax6.set_ylabel("Avg Interest Rate (%)")
ax6.set_xlabel("Loan Grade")
ax6.set_title("Avg Interest Rate by Grade & Default")
st.pyplot(fig6)

# ---------- Footer ----------
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | SQL + Python | Author: Shivani")
