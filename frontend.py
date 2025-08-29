import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import compare_prices  # import backend function

# ==============================
#   Streamlit Frontend
# ==============================
st.set_page_config(page_title="Price Comparison", layout="wide")

st.title("🛒 E-commerce Price Comparison Tool")

# Search input
product_name = st.text_input("Enter the product you want to search:")

if st.button("Search"):
    if not product_name.strip():
        st.warning("Please enter a product name.")
    else:
        with st.spinner("Searching across Jumia & Slot..."):
            results = compare_prices(product_name)

        if results:
            # Convert results to DataFrame
            df = pd.DataFrame(results)

            st.subheader("📋 All Results")
            st.dataframe(df, use_container_width=True)

            # Show top 5 cheapest
            top5 = df.nsmallest(5, "Price")

            st.subheader("💰 Top 5 Cheapest Options")
            st.dataframe(top5, use_container_width=True)

            # Visualization
            st.subheader("📊 Price Comparison (Top 5)")
            fig, ax = plt.subplots()
            ax.barh(top5["Product Name"], top5["Price"], color="skyblue")
            ax.set_xlabel("Price (₦)")
            ax.set_ylabel("Product")
            ax.set_title("Top 5 Cheapest Prices")
            st.pyplot(fig)

            # Download button
            csv = top5.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Top 5 as CSV",
                data=csv,
                file_name="top5_cheapest.csv",
                mime="text/csv"
            )

        else:
            st.error("No products found for your search. Try another keyword.")
