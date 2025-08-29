import streamlit as st
import pandas as pd
from backend import compare_prices   # import your backend function

st.set_page_config(page_title="E-Commerce Price Comparison", layout="wide")

st.title("🛒 Automated Price Comparison Tool")

# --- User Input ---
product_name = st.text_input("Enter the product name to search:")

if st.button("Search"):
    if product_name.strip() == "":
        st.warning("⚠️ Please enter a product name")
    else:
        st.info(f"Searching for **{product_name}** across stores...")

        results = compare_prices(product_name)

        if results:
            # Convert to dataframe for display
            df = pd.DataFrame(results)

            # Normalize Naira price display
            df["Price"] = df["Price"].apply(lambda x: f"₦{x:,.0f}")

            # Show table
            st.subheader("📊 Price Comparison Results")
            st.dataframe(df, use_container_width=True)

            # CSV download
            csv = pd.DataFrame(results).to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download Results as CSV",
                data=csv,
                file_name="price_comparison.csv",
                mime="text/csv",
            )

            # Show cheapest 5 (optional)
            st.subheader("🏷️ Top 5 Cheapest Options")
            st.table(df.head(5))
        else:
            st.error("No results found. Please try another product.")

