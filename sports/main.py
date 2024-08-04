import tkinter as tk
from tkinter import ttk, messagebox
from scrape_mechanicalsoup import scrape_mechanicalsoup
from scrape_requests_html import scrape_requests_html
from utils import update_website_info
from websites_data import websites
from library import libraries

# Configuration Variables
BACKGROUND_COLOR = "#2c3e50"
LABEL_COLOR = "#000"
TEXT_BACKGROUND_COLOR = "#c7c7c4"
BUTTON_COLOR = "#2980b9"
CLOSE_BUTTON_COLOR = "#e74c3c"
SELECT_BACKGROUND_COLOR = "#2980b9"
FONT_LARGE = ("Arial", 12)
FONT_MEDIUM = ("Arial", 11)
FONT_BOLD = ("Arial", 12, "bold")

# Initialize Tkinter
root = tk.Tk()
root.title("Web Scraping Library Comparison")

# Set window to fullscreen mode
root.attributes('-fullscreen', True)

# Close the application when the escape key is pressed
def quit_fullscreen(event=None):
    root.attributes('-fullscreen', False)
    root.quit()

root.bind('<Escape>', quit_fullscreen)

# Tkinter Variables
selected_library_var = tk.StringVar(value="MechanicalSoup")
selected_website_var = tk.StringVar(value=list(websites.keys())[0])

# Layout Configuration
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)
root.rowconfigure(5, weight=2)      # Make the Data Items section larger
root.rowconfigure(6, weight=1)      # Make the button row flexible
root.columnconfigure(1, weight=1)   # Ensure column 1 expands to use available space

# Labels and dropdowns
library_label = tk.Label(root, text="Select Library:", font=FONT_LARGE, fg=LABEL_COLOR)
library_label.grid(row=0, column=0, padx=20, pady=(80, 10), sticky="w")
library_dropdown = ttk.Combobox(root, textvariable=selected_library_var, values=libraries, state="readonly", font=FONT_LARGE)
library_dropdown.grid(row=0, column=1, padx=20, pady=(80, 10), sticky="ew")

website_label = tk.Label(root, text="Select Website:", font=FONT_LARGE, fg=LABEL_COLOR)
website_label.grid(row=1, column=0, padx=20, pady=10, sticky="w") 
website_dropdown = ttk.Combobox(root, textvariable=selected_website_var, values=list(websites.keys()), state="readonly", font=FONT_LARGE)
website_dropdown.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

description_label = tk.Label(root, text="Description:", font=FONT_BOLD, fg=LABEL_COLOR)
description_label.grid(row=2, column=0, padx=20, pady=5, sticky="w")
description_text = tk.Text(root, height=3, wrap="word", font=FONT_MEDIUM, bg=TEXT_BACKGROUND_COLOR, fg=LABEL_COLOR, bd=0, padx=10, pady=10)
description_text.grid(row=3, column=0, columnspan=2, padx=20, pady=5, sticky="nsew")
description_text.config(state=tk.DISABLED)

items_label = tk.Label(root, text="Data Items:", font=FONT_BOLD, fg=LABEL_COLOR)
items_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")
items_listbox = tk.Listbox(root, height=10, font=FONT_MEDIUM, bg=TEXT_BACKGROUND_COLOR, fg=LABEL_COLOR, selectbackground=SELECT_BACKGROUND_COLOR)
items_listbox.grid(row=5, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")

# Button Configuration
button_width = 20
button_height = 2

# Create a frame for buttons to align them to the right
button_frame = tk.Frame(root)
button_frame.grid(row=6, column=1, pady=20, padx=20, sticky="e")

# Scrape button
scrape_button = tk.Button(button_frame, text="Start", command=lambda: scrape_data(selected_library_var.get()), font=FONT_LARGE, bg=BUTTON_COLOR, fg=LABEL_COLOR, bd=0, relief="flat", width=button_width, height=button_height)
scrape_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# Close button
close_button = tk.Button(button_frame, text="Close", command=quit_fullscreen, font=FONT_LARGE, bg=CLOSE_BUTTON_COLOR, fg=LABEL_COLOR, bd=0, relief="flat", width=button_width, height=button_height)
close_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

def scrape_data(library):
    response = False
    if library == "MechanicalSoup":
        response = scrape_mechanicalsoup(selected_website_var.get())
    # elif library == "Scrapy":

    elif library == "Manual":
        response = scrape_requests_html(selected_website_var.get())


    if response:
        messagebox.showinfo("Success", "Data scraped successfully!")
    else:
        messagebox.showerror("Error", "An error occurred during scraping.")
        
# Update the description and items when the first item is automatically selected
update_website_info(selected_website_var.get(), description_text, items_listbox, websites)

# Bind event to update description and items when a website is selected
selected_website_var.trace_add("write", lambda *args: update_website_info(selected_website_var.get(), description_text, items_listbox, websites))

# Start the Tkinter main loop
root.mainloop()
