import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# Page configuration
st.set_page_config(page_title="Compound Interest Calculator", layout="centered")

# Apply custom font and styling - red, white, and blue theme
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: Helvetica, Arial, sans-serif;
            background-color: white;
            color: black;
        }
        .st-bb, .st-c8, .st-cn {
            background-color: white !important;
            color: #002e5d !important;
        }
        .stButton>button {
            background-color: #002e5d;
            color: white;
        }
        .stSelectbox>div>div {
            background-color: #ffffff;
            color: #002e5d;
        }
    </style>
""", unsafe_allow_html=True)

# Title and intro
st.title("Compound Interest Calculator")
st.write("Learn to build wealth with the power of compounding.")

st.info("Over the past 30 years, the average annual return of the S&P 500 has been approximately 10%. You can use this as a historical benchmark when estimating your interest rate.")

# --- Initial Investment ---
st.markdown("#### Initial Investment")
st.caption("This is the first step to building long-term wealth.")
initial = st.number_input("Initial Investment *", min_value=0.0, value=0.0, step=100.0, format="%.2f", help="Amount of money that you have available to invest initially.")

# --- Monthly Contribution ---
st.markdown("#### Monthly Contribution")
st.caption("Consistent contributions accelerate your path to financial freedom.")
monthly = st.number_input("Monthly Contribution", value=0.0, step=10.0, format="%.2f", help="Amount that you plan to add to the principal every month, or a negative number for withdrawals.")

# --- Time Horizon ---
st.markdown("#### Investment Duration")
st.caption("Time in the market beats timing the market. The longer you invest, the more you benefit from compounding.")
years = st.number_input("Length of Time in Years *", min_value=1, value=1, step=1, help="Length of time, in years, that you plan to save.")

# --- Interest Rate ---
st.markdown("#### Expected Annual Return")
st.caption("Estimate your average return based on historical performance or market assumptions.")
interest = st.number_input("Estimated Interest Rate *", min_value=0.0, value=0.0, step=0.1, format="%.2f", help="Your estimated annual interest rate.")

st.markdown("#### Interest Rate Variance")
st.caption("Explore how different return rates can impact your investment outcomes.")
range_offset = st.number_input("Interest Rate Variance Range", min_value=0.0, value=0.0, step=0.1, format="%.2f", help="Range of interest rates (above and below the estimated rate) to view results for.")

# --- Compound Frequency ---
st.markdown("#### Compound Frequency")
st.caption("More frequent compounding can enhance your long-term gains.")
frequency_option = st.selectbox("Compound Frequency", ["Annually", "Quarterly", "Monthly", "Daily"], help="Times per year that interest will be compounded.")

frequency_map = {
    "Annually": 1,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365
}

# --- Calculation ---
if st.button("Calculate"):
    st.markdown("---")
    st.subheader("The Results Are In")

    compound_per_year = frequency_map[frequency_option]
    year_range = range(0, years + 1)
    df = pd.DataFrame()

    if range_offset == 0:
        rates = [interest]
        labels = [f"Future Value ({interest:.2f}%)"]
        colors = ["#002e5d"]
    else:
        rates = [interest - range_offset, interest, interest + range_offset]
        labels = [f"Variance Below ({rates[0]:.2f}%)", f"Future Value ({rates[1]:.2f}%)", f"Variance Above ({rates[2]:.2f}%)"]
        colors = ["#ff0000", "#002e5d", "#0000ff"]  # red, blue, and deeper blue

    for i, rate in enumerate(rates):
        r = rate / 100
        values = []
        contributions = []
        for t in year_range:
            future_val = initial * (1 + r / compound_per_year) ** (compound_per_year * t)
            contribution_val = monthly * (((1 + r / compound_per_year) ** (compound_per_year * t) - 1) / (r / compound_per_year))
            total = future_val + contribution_val
            values.append(total)
            contributions.append(initial + monthly * t * compound_per_year)
        df[labels[i]] = values
        df[f"Contributions ({rate:.2f}%)"] = contributions

    df.insert(0, "Year", year_range)
    df["Total Contributions"] = [initial + monthly * t * compound_per_year for t in year_range]

    # Final value display
    final_value = df[labels[len(labels)//2]].iloc[-1]
    st.markdown(f"In **{years} years**, you could have **${final_value:,.2f}** based on your inputs.")

    # Chart
    fig = go.Figure()
    for i, label in enumerate(labels):
        fig.add_trace(go.Scatter(x=df["Year"], y=df[label], mode='lines+markers', name=label, line=dict(color=colors[i])))

    fig.add_trace(go.Scatter(x=df["Year"], y=df["Total Contributions"], mode='lines+markers', name="Total Contributions", line=dict(color="green", dash='dot')))

    fig.update_layout(
        title="Total Savings Over Time",
        xaxis_title="Year",
        yaxis_title="US Dollars",
        legend_title="Scenario",
        plot_bgcolor="white",
        font=dict(family="Helvetica, Arial, sans-serif", size=18),
        height=700
    )

    # Format y-axis to show dollar amounts with commas and no decimals
    fig.update_yaxes(tickprefix="$", tickformat=",.0f")

    st.plotly_chart(fig, use_container_width=True)
