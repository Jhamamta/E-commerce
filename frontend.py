import streamlit as st
import pandas as pd
from backend import compare_prices  # your backend function

st.title("📊 Automatic Price Comparison Tool")
st.write("Search and compare product prices across Jumia and Slot.")

# Search input
query = st.text_input("Enter product name:", "")

if st.button("Search"):
    if query.strip():
        results = compare_prices(query)

        if results:
            df = pd.DataFrame(results)

            # Display full results
            st.subheader("All Results")
            st.dataframe(df)

            # Top 5 cheapest
            top5 = df.nsmallest(5, "Price")

            st.subheader("Top 5 Cheapest Products")
            st.dataframe(top5)

            # ✅ Streamlit native visualization
            st.bar_chart(top5.set_index("Product Name")["Price"])

            # Download CSV button
            csv = top5.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Top 5 Cheapest (CSV)",
                data=csv,
                file_name="top5_cheapest.csv",
                mime="text/csv",
            )

        else:
            st.warning("No products found for your search.")
    else:
        st.error("Please enter a product name to search.")

