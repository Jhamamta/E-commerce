# frontend.py
import pandas as pd
import matplotlib.pyplot as plt
from backend import compare_prices  # make sure your backend.py is in the same folder

def main():
    product_name = input("Enter the product to search: ")

    # Get all results from backend
    results = compare_prices(product_name)

    if not results:
        print("No products found.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(results)

    # Get top 5 cheapest
    top5 = df.nsmallest(5, 'Price')

    # Display table
    print("\n--- Top 5 Cheapest Products ---")
    print(top5[['Product Name', 'Price', 'Store', 'URL']].to_string(index=False))

    # Visualization
    plt.figure(figsize=(10,6))
    plt.barh(top5['Product Name'], top5['Price'], color='skyblue')
    plt.xlabel('Price (₦)')
    plt.title(f'Top 5 Cheapest "{product_name}" Products')
    plt.gca().invert_yaxis()  # cheapest on top
    plt.tight_layout()
    plt.show()

    # Save top 5 to CSV
    csv_filename = "top5_products.csv"
    top5.to_csv(csv_filename, index=False)
    print(f"\nTop 5 products saved to {csv_filename}")

if __name__ == "__main__":
    main()
