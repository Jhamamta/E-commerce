import re
import requests
from bs4 import BeautifulSoup
import csv

# =================================================================
#                       Price Comparison Backend
# =================================================================

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36'
}

# =================================================================
#                         Jumia Scraper
# =================================================================

def scrape_jumia(product_name):
    search_query = product_name.replace(" ", "%20")
    jumia_url = f"https://www.jumia.com.ng/catalog/?q={search_query}"

    products = []
    try:
        response = requests.get(jumia_url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        containers = soup.select('a.core')

        for container in containers:
            url = "https://www.jumia.com.ng" + container['href']
            name_tag = container.select_one('h3.name')
            price_tag = container.select_one('div.prc')

            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price_text = price_tag.get_text(strip=True)

                cleaned_price = re.sub(r'[₦,]', '', price_text)
                numbers = re.findall(r'\d+', cleaned_price)
                if not numbers:
                    continue
                price_numeric = float(numbers[0])

                products.append({
                    'Product Name': name,
                    'Price': price_numeric,
                    'Store': 'Jumia',
                    'URL': url
                })

    except Exception as e:
        print(f"⚠️ Jumia error: {e}")

    return products

# =================================================================
#                         Slot Scraper
# =================================================================

def scrape_slot(product_name):
    search_query = product_name.replace(" ", "+")
    slot_url = f"https://slot.ng/index.php/catalogsearch/result/?q={search_query}"

    products = []
    try:
        response = requests.get(slot_url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        containers = soup.select("li.item.product.product-item")

        for container in containers:
            name_tag = container.select_one("a.product-item-link")
            price_tag = container.select_one("span.price")

            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                url = name_tag["href"]
                price_text = price_tag.get_text(strip=True)

                cleaned_price = re.sub(r'[₦,NGN\s]', '', price_text)
                numbers = re.findall(r'\d+', cleaned_price)
                if not numbers:
                    continue
                price_numeric = float(numbers[0])

                products.append({
                    'Product Name': name,
                    'Price': price_numeric,
                    'Store': 'Slot',
                    'URL': url
                })

    except Exception as e:
        print(f"⚠️ Slot error: {e}")

    return products

# =================================================================
#                         Filtering
# =================================================================

# =================================================================
#                   Filtering Function (Hybrid)
# =================================================================

def filter_results(products, query):
    """
    Filters products with a hybrid approach:
    1. Prefer exact phrase matches of the query.
    2. If no exact phrase matches exist, fall back to word-based filtering.
    """
    query = query.lower().strip()
    query_words = query.split()

    exact_matches = []
    word_matches = []

    for p in products:
        title = p["Product Name"].lower()

        # Check for exact phrase
        if query in title:
            exact_matches.append(p)
        # Otherwise check for all words present
        elif all(word in title for word in query_words):
            word_matches.append(p)

    # Prefer exact matches; if none, return word matches
    if exact_matches:
        return exact_matches
    else:
        return word_matches


# =================================================================
#                         Main Function
# =================================================================

def compare_prices(product_name):
    jumia_results = scrape_jumia(product_name)
    slot_results = scrape_slot(product_name)

    all_products = jumia_results + slot_results

    all_products = filter_results(all_products, product_name)

    if not all_products:
        print("No products found.")
        return None

    sorted_products = sorted(all_products, key=lambda x: x['Price'])

    # Save to CSV (overwrite each time)
    with open("price_comparison.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Product Name", "Price", "Store", "URL"])
        writer.writeheader()
        writer.writerows(sorted_products)

    return sorted_products

# =================================================================
#                         Test Runner
# =================================================================

if __name__ == '__main__':
    test_product = "Redmi Note 14"
    print(f"Searching for '{test_product}' on Jumia and Slot...")
    final_data = compare_prices(test_product)

    if final_data:
        print("\n--- Price Comparison Results ---")
        for product in final_data:
            print(f"Product: {product['Product Name']}")
            print(f"Price: ₦{product['Price']:,}")
            print(f"Store: {product['Store']}")
            print(f"URL: {product['URL']}\n")
    else:
        print("Failed to find any products.")
