import streamlit as st
import pandas as pd
from backend import compare_prices

st.title("🛒 Price Comparison Tool")

# Input field
product_name = st.text_input("Enter a product name (e.g. Samsung Galaxy S24):")

if st.button("Search"):
    if product_name.strip():
        results = compare_prices(product_name)

        if results:
            df = pd.DataFrame(results)

            # Show the full table
            st.subheader("Search Results")
            st.dataframe(df)

            # Download CSV
            st.download_button(
                label="📥 Download Results as CSV",
                data=df.to_csv(index=False),
                file_name="price_comparison.csv",
                mime="text/csv"
            )

            # Visualization: Top 5 cheapest products
            st.subheader("📊 Top 5 Cheapest Options")
            top5 = df.nsmallest(5, "Price")
            st.bar_chart(top5.set_index("Product Name")["Price"])

        else:
            st.warning("No products found. Try a different search.")
    else:
        st.error("Please enter a product name.")
