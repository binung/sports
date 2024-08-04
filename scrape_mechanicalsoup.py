import mechanicalsoup
import pandas as pd

# Create a browser object
browser = mechanicalsoup.StatefulBrowser()
browser.session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
})

url = "https://fbref.com/en/comps/9/Premier-League-Stats"

# Open the main page
try:
    browser.open(url)
    print("Successfully opened the page")
except Exception as e:
    print(f"Error opening the page: {e}")

# Parse the main page content
page = browser.get_current_page()

# Debugging: Print the page content to find the correct table ID and structure
# print(page.prettify())

# Example: Extract Stats Summary
def extract_live_scores(soup):
    rows = []
    # Locate the stats table or relevant elements
    table = soup.find('table', {'id': 'results2024-202591_overall'})  # Update this ID based on actual page
    if table:
        print('Table found')
        # Extract rows
        thead = table.find('thead')
        if thead:
            headers = [th.text.strip() for th in thead.find_all(['td', 'th'])]
            if headers: rows.append(headers)

        tbody = table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                row = [td.text.strip() for td in tr.find_all(['td', 'th'])]
                if row:
                    rows.append(row)
    else:
        print('Table not found')
    return rows

# Extract data
data = extract_live_scores(page)

# Print the first few rows of data to inspect
print("Extracted data:")
for row in data[:5]:  # Print the first 5 rows
    print(row)

# Create DataFrame
df = pd.DataFrame(data[1:], columns=data[0])

# Save data to an Excel file
df.to_excel("fbref.com.xlsx", sheet_name="Premier League", index=False)

print("Data saved to 'whoscored_data.xlsx'")
