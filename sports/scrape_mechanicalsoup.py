import mechanicalsoup

def extract_data_mechanicalsoup(page, data_items):
    data = {}
    for item_name, item_id in data_items.items():

        table = page.find('table', {'id': item_id})
        rows = []
        
        thead = table.find('thead')
        if thead:
            headers = [th.text.strip() for th in thead.find_all(['td', 'th'])]
            if headers: rows.append(headers)

        if table:
            tbody = table.find('tbody')
            if tbody:
                for tr in tbody.find_all('tr'):
                    row = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                    if row:
                        rows.append(row)
        data[item_name] = rows
    return data

def scrape_mechanicalsoup(website_key):
    from utils import save_data_to_excel
    from websites_data import websites

    website_info = websites.get(website_key, {})
    url = website_info.get("url")

    # Start scraping
    browser = mechanicalsoup.StatefulBrowser()
    try:
        browser.open(url)
        page = browser.get_current_page()
        data = extract_data_mechanicalsoup(page, website_info.get("data_items", {}))
        save_data_to_excel(data, website_key, 'mechanicalsoup')
        return True
    except Exception as e:
        return False

