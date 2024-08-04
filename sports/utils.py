import pandas as pd
from tkinter import Text, Listbox

def update_website_info(selected_website, description_text: Text, items_listbox: Listbox, websites: dict):
    website_info = websites.get(selected_website, {})
    description_text.config(state="normal")
    description_text.delete(1.0, "end")
    description_text.insert("end", website_info.get("description", ""))
    description_text.config(state="disabled")

    items_listbox.delete(0, "end")
    for item_name in website_info.get("data_items", {}).keys():
        items_listbox.insert("end", item_name)

def save_data_to_excel(data, filename, library):
    with pd.ExcelWriter(f"{filename}_{library}.xlsx") as writer:
        for sheet_name, sheet_data in data.items():
            if len(sheet_data) > 1 and any(row for row in sheet_data[1:] if any(row)):
                df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])
                df.to_excel(writer, sheet_name=sheet_name, index=False)
            else:
                print(f"Skipping sheet {sheet_name} due to lack of meaningful data.")
