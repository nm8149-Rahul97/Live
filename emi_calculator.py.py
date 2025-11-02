import streamlit as st
import math
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# ----------------------------
# 🎯 Title and Description
# ----------------------------
st.set_page_config(page_title="EMI Calculator", page_icon="💰", layout="centered")
st.title("🏦 EMI Calculator App")
st.write("Calculate your monthly EMI, total interest, and total payment easily!")

# ----------------------------
# 🧮 Input Section
# ----------------------------
loan_amount = st.number_input("Enter Loan Amount (₹)", min_value=1000.0, value=500000.0, step=1000.0)
interest_rate = st.number_input("Annual Interest Rate (%)", min_value=0.1, value=8.5, step=0.1)
loan_tenure = st.number_input("Loan Tenure (Years)", min_value=0.5, value=5.0, step=0.5)

# ----------------------------
# 📊 EMI Calculation Logic
# ----------------------------
n = loan_tenure * 12              # total months
r = interest_rate / 12 / 100      # monthly interest rate

if r > 0:
    emi = loan_amount * r * (1 + r)**n / ((1 + r)**n - 1)
else:
    emi = loan_amount / n  # zero-interest case

total_payment = emi * n
total_interest = total_payment - loan_amount

# ----------------------------
# 🧾 Results Display
# ----------------------------
st.subheader("📈 Results")
st.write(f"**Monthly EMI:** ₹{emi:,.2f}")
st.write(f"**Total Interest Payable:** ₹{total_interest:,.2f}")
st.write(f"**Total Payment (Principal + Interest):** ₹{total_payment:,.2f}")

# ----------------------------
# 📉 Visualization (Pie Chart)
# ----------------------------
st.subheader("💰 Payment Breakdown")
data = {
    'Principal': loan_amount,
    'Total Interest': total_interest
}
fig, ax = plt.subplots()
ax.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=90)
ax.axis('equal')
st.pyplot(fig)

# ----------------------------
# 📊 Amortization Table + Download Options
# ----------------------------
if st.checkbox("Show Amortization Schedule"):
    balance = loan_amount
    schedule = []
    for i in range(1, int(n)+1):
        interest_payment = balance * r
        principal_payment = emi - interest_payment
        balance -= principal_payment
        schedule.append([
            i,
            round(emi, 2),
            round(principal_payment, 2),
            round(interest_payment, 2),
            round(max(balance, 0), 2)
        ])

    df = pd.DataFrame(schedule, columns=["Month", "EMI", "Principal", "Interest", "Balance"])
    st.dataframe(df, use_container_width=True)

    # ----------------------------
    # 📥 Download as Excel
    # ----------------------------
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Amortization Schedule")
    excel_data = output.getvalue()

    st.download_button(
        label="📘 Download Schedule as Excel",
        data=excel_data,
        file_name="emi_amortization_schedule.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # ----------------------------
    # 📥 Download as CSV
    # ----------------------------
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📄 Download Schedule as CSV",
        data=csv_data,
        file_name="emi_amortization_schedule.csv",
        mime="text/csv"
    )
