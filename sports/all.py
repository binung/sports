import tkinter as tk
from tkinter import ttk, messagebox
import mechanicalsoup
import pandas as pd

# Sample data
websites = {
    "FBREF": {
        "url": "https://fbref.com/en/comps/9/Premier-League-Stats",
        "description": "This is a site that shows the results of the European Football League.",
        "data_items": {
            "Premier League": "results2024-202591_overall",
            "League Notes": "note_result",
        }
    },
    "WhoScored": {
        "url": "https://www.whoscored.com/Statistics",
        "description": "This website provides detailed statistics on football matches and players.",
        "data_items": {
            "Team Stats": "top-team-stats-summary-content",
            "Player Stats": "top-player-stats-summary-content",
        }
    }
}

# Initialize Tkinter
root = tk.Tk()
root.title("Web Scraping Library Comparison")
root.geometry("600x450")
root.configure(bg="#2c3e50")

# Function to update the description and data items based on the selected website
def update_website_info(*args):
    selected_website = selected_website_var.get()
    website_info = websites.get(selected_website, {})
    description_text.config(state=tk.NORMAL)
    description_text.delete(1.0, tk.END)
    description_text.insert(tk.END, website_info.get("description", ""))
    description_text.config(state=tk.DISABLED)

    items_listbox.delete(0, tk.END)
    for item_name, _ in website_info.get("data_items", {}).items():
        items_listbox.insert(tk.END, item_name)

# Function to scrape data using MechanicalSoup
def scrape_mechanicalsoup():
    selected_website = selected_website_var.get()
    website_info = websites.get(selected_website, {})
    url = website_info.get("url")
    
    # Start scraping
    browser = mechanicalsoup.StatefulBrowser()
    try:
        browser.open(url)
        page = browser.get_current_page()
        data = extract_data_mechanicalsoup(page, website_info.get("data_items", {}))
        save_data_to_excel(data, selected_website)
        messagebox.showinfo("Success", "Data scraped and saved successfully using MechanicalSoup.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to scrape data: {e}")

# Function to extract data using MechanicalSoup
def extract_data_mechanicalsoup(page, data_items):
    data = {}
    for item_name, item_id in data_items.items():
        table = page.find('table', {'id': item_id})
        rows = []
        if table:
            tbody = table.find('tbody')
            if tbody:
                for tr in tbody.find_all('tr'):
                    row = [td.text.strip() for td in tr.find_all('td')]
                    if row:
                        rows.append(row)
        data[item_name] = rows
    return data

# Function to save data to Excel
def save_data_to_excel(data, filename):
    with pd.ExcelWriter(f"{filename}.xlsx") as writer:
        for sheet_name, sheet_data in data.items():
            df = pd.DataFrame(sheet_data)
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# Tkinter Variables
selected_library_var = tk.StringVar(value="MechanicalSoup")
selected_website_var = tk.StringVar(value=list(websites.keys())[0])  # Set the first item as selected

# Layout Configuration
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

# Labels and dropdowns
library_label = tk.Label(root, text="Select Library:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
library_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
libraries = ["MechanicalSoup", "Scrapy"]
library_dropdown = ttk.Combobox(root, textvariable=selected_library_var, values=libraries, state="readonly", font=("Arial", 12))
library_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

website_label = tk.Label(root, text="Select Website:", font=("Arial", 12), bg="#2c3e50", fg="#ecf0f1")
website_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
website_dropdown = ttk.Combobox(root, textvariable=selected_website_var, values=list(websites.keys()), state="readonly", font=("Arial", 12))
website_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

description_label = tk.Label(root, text="Description:", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#ecf0f1")
description_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
description_text = tk.Text(root, height=4, wrap="word", font=("Arial", 11), bg="#34495e", fg="#ecf0f1", bd=0, padx=10, pady=10)
description_text.grid(row=3, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
description_text.config(state=tk.DISABLED)

items_label = tk.Label(root, text="Data Items:", font=("Arial", 12, "bold"), bg="#2c3e50", fg="#ecf0f1")
items_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
items_listbox = tk.Listbox(root, height=6, font=("Arial", 11), bg="#34495e", fg="#ecf0f1", selectbackground="#2980b9")
items_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

# Scrape button
scrape_button = tk.Button(root, text="Scrape Data", command=scrape_mechanicalsoup, font=("Arial", 12), bg="#2980b9", fg="#ecf0f1", bd=0, relief="flat")
scrape_button.grid(row=6, column=0, columnspan=2, pady=15, sticky="ew", padx=20)

# Update the description and items when the first item is automatically selected
update_website_info()

# Bind event to update description and items when a website is selected
selected_website_var.trace_add("write", update_website_info)

# Start the Tkinter main loop
root.mainloop()
