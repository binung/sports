from requests_html import HTMLSession

# Function to extract data using Requests-HTML
def extract_data_requests_html(html, data_items):
    data = {}
    for item_name, item_id in data_items.items():
        try:
            table = html.find(f'table#{item_id}', first=True)
            if not table:
                print(f"Table with ID '{item_id}' not found.")
                continue

            print(f"Processing table with ID: {item_id}")
            rows = []
            # Extract headers
            thead = table.find('thead', first=True)
            if thead:
                headers = [th.text.strip() for th in thead.find('th')]
                print(f"Headers found: {headers}")
                if headers:
                    rows.append(headers)
            else:
                print(f"No thead found in table with ID '{item_id}'.")

            # Extract rows
            tbody = table.find('tbody', first=True)
            if tbody:
                for tr in tbody.find('tr'):
                    row = [td.text.strip() for td in tr.find('td')]
                    print(f"Row found: {row}")
                    if row:
                        rows.append(row)
            else:
                print(f"No tbody found in table with ID '{item_id}'.")

            data[item_name] = rows
        except Exception as e:
            print(f"Error processing table with ID '{item_id}': {e}")
    return data

def scrape_requests_html(website_key):
    from utils import save_data_to_excel
    from websites_data import websites

    website_info = websites.get(website_key, {})
    url = website_info.get("url")
    
    # Start scraping
    session = HTMLSession()
    try:
        response = session.get(url)
        response.raise_for_status()  # Ensure we got a successful response
        print(f"Response status code: {response.status_code}")

        # Uncomment if JavaScript rendering is necessary
        # response.html.render()

        print("Raw HTML content:")
        print(response.html.html[:1000])  # Print the first 1000 characters of the HTML for inspection

        data = extract_data_requests_html(response.html, website_info.get("data_items", {}))
        save_data_to_excel(data, website_key, 'manual')
        return True
    except Exception as e:
        print(("Error", f"Failed to scrape data: {e}"))
        return False
