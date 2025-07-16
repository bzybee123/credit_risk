# 💳 Credit Risk Analysis Dashboard

A visual, data-driven dashboard to analyze credit risk patterns using SQL, Python, and Streamlit. This project connects to a MySQL database and provides insights into loan types, default behavior, interest rates, and more.

---

## 🚀 Project Overview

This dashboard helps stakeholders explore key credit-related patterns such as:
- Loan intent and default correlations
- Interest rate trends by loan grade
- High-risk borrower profiles
- Default likelihood based on income and credit history

All data is pulled directly from a **MySQL database**, processed using **pandas**, and visualized using **Streamlit** and **Matplotlib**.

---

## 🛠️ Technologies Used

| Tech         | Description                         |
|--------------|-------------------------------------|
| **Python**   | Data processing and backend logic   |
| **Streamlit**| Web app and dashboard UI            |
| **MySQL**    | Backend relational database         |
| **Pandas**   | Data transformation                 |
| **Matplotlib** | Custom visualizations             |

---

## 📊 Features & Visuals

- ✅ Summary KPIs (records, loan types, grades, default rate)
- ✅ Data preview with expandable panel
- ✅ Mixed visualizations:
  - Bar, Pie, Line charts, and Histograms
- ✅ Five SQL-based insights displayed dynamically

---

## 🔍 SQL-Based Insights Shown

1. **High Income + Personal Loan ≥ ₹10K**  
2. **Defaults with Credit History = 3**
3. **OWN Home + Loan for Home Improvement**
4. **Loan-to-Income ≥ 0.4 + Defaulted**
5. **Average Interest by Grade & Default Status** *(Line Chart)*

---

## 📷 Dashboard Preview

![credit-risk-dashboard](preview.png) <!-- Add a screenshot named preview.png -->

---

## 🧑‍💻 How to Run

### 🔧 1. Clone this Repo

```bash
git clone https://github.com/your-username/credit-risk-dashboard.git
cd credit-risk-dashboard
