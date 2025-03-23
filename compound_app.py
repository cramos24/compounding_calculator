import streamlit as st

# Set the title
st.title("COMPOUND INTEREST CALCULATOR")

# Input fields
initial = st.number_input("Initial investment amount ($)", min_value=0.0, value=0.0, step=100.0)
monthly = st.number_input("Monthly contribution ($)", min_value=0.0, value=0.0, step=10.0)
years = st.number_input("Number of years", min_value=1, value=1, step=1)
interest = st.number_input("Expected annual interest rate (%)", min_value=0.0, value=0.0, step=0.1)
range_offset = st.number_input("Interest range (+/- %, e.g. 2)", min_value=0.0, value=0.0, step=0.1)

# Button to calculate
if st.button("Calculate"):
    st.subheader("📊 Projected Growth")

    n = 12  # compounding monthly

    for rate in [interest - range_offset, interest, interest + range_offset]:
        r = rate / 100
        t = years

        future_value = initial * (1 + r/n)**(n*t)
        future_value += monthly * (((1 + r/n)**(n*t) - 1) / (r/n))

        total_contributions = initial + (monthly * 12 * years)
        interest_earned = future_value - total_contributions

        st.markdown(f"### At {rate:.1f}% annual return")
        st.write(f"💰 Final Value: **${future_value:,.2f}**")
        st.write(f"📥 Contributions: ${total_contributions:,.2f}")
        st.write(f"📈 Interest Earned: ${interest_earned:,.2f}")
        st.markdown("---")
