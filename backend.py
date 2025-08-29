import re
import requests
from bs4 import BeautifulSoup

# =================================================================
#                       Price Comparison Backend
# =================================================================

# Global header to make the scraper look like a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36'
}

# =================================================================
#                         Jumia Scraper
# =================================================================

def scrape_jumia(product_name):
    """
    Scrapes Jumia for the given product name and returns a list of dictionaries.
    """
    search_query = product_name.replace(" ", "%20")
    jumia_url = f"https://www.jumia.com.ng/catalog/?q={search_query}"

    products = []
    try:
        response = requests.get(jumia_url, headers=headers, verify=False)
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

                # Clean price
                cleaned_price = re.sub(r'[₦,]', '', price_text)
                numbers = re.findall(r'\d+', cleaned_price)
                if numbers:
                    price_numeric = float(numbers[0])

                    products.append({
                        'Product Name': name,
                        'Price': price_numeric,
                        'Store': 'Jumia',
                        'URL': url
                    })

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while scraping Jumia: {e}")

    return products

# =================================================================
#                         Slot Scraper
# =================================================================

def scrape_slot(product_name):
    """
    Scrapes Slot.ng for the given product name and returns a list of dictionaries.
    """
    search_query = product_name.replace(" ", "+")
    slot_url = f"https://www.slot.ng/catalogsearch/result/?q={search_query}"

    products = []
    try:
        response = requests.get(slot_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        containers = soup.select('li.product-item')

        for container in containers:
            url_tag = container.select_one('a.product-item-link')
            name_tag = container.select_one('a.product-item-link')
            price_tag = container.select_one('span.price')

            if name_tag and price_tag and url_tag:
                name = name_tag.get_text(strip=True)
                price_text = price_tag.get_text(strip=True)
                url = url_tag['href']

                # Clean price
                price_numeric = float(re.sub(r'[₦,]', '', price_text))

                products.append({
                    'Product Name': name,
                    'Price': price_numeric,
                    'Store': 'Slot',
                    'URL': url
                })

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while scraping Slot: {e}")

    return products

# =================================================================
#                       Main Function
# =================================================================

def compare_prices(product_name):
    """
    Compares prices for a given product on multiple e-commerce sites.
    """
    jumia_results = scrape_jumia(product_name)
    slot_results = scrape_slot(product_name)

    all_products = jumia_results + slot_results

    if not all_products:
        print("No products found.")
        return None

    # Sort the products by price
    sorted_products = sorted(all_products, key=lambda x: x['Price'])
    return sorted_products


if __name__ == '__main__':
    test_product = "Samsung Galaxy S24"
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
        print("Failed to find any products. Check your network or CSS selectors.")
