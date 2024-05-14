import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import json

def load_config(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def load_currency_codes(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_config(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def plot_forex_pair(pair, start_date, end_date):
    try:
        data = yf.download(pair, start=start_date, end=end_date)['Close']
        if data.empty:
            messagebox.showinfo("Error", "No data available for the selected period.")
        else:
            plt.figure(figsize=(8, 4))
            data.plot()
            plt.title(pair + " Daily Close Price")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(True)

            
            save_button.grid(row=6, column=0, columnspan=2, pady=(10, 0))
            global plt_data
            plt_data = data
            global plt_pair
            plt_pair = pair
            global plt_start_date
            plt_start_date = start_date
            global plt_end_date
            plt_end_date = end_date

            plt.show()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def save_chart():
    global plt_data
    global plt_pair
    global plt_start_date
    global plt_end_date
    file_path = filedialog.asksaveasfilename(defaultextension=".png")
    if file_path:
        try:
            plt.figure(figsize=(8, 4))
            plt_data.plot()
            plt.title(plt_pair + " Daily Close Price")
            plt.xlabel("Date")
            plt.ylabel("Price")
            plt.grid(True)
            plt.savefig(file_path)
            messagebox.showinfo("Success", "Chart saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def show_chart():
    numerator = combo_numerator.get()
    denominator = combo_denominator.get()
    start_year = entry_start_year.get()
    start_month = entry_start_month.get()
    start_day = entry_start_day.get()
    end_year = entry_end_year.get()
    end_month = entry_end_month.get()
    end_day = entry_end_day.get()

    if not start_year or not start_month or not start_day or not end_year or not end_month or not end_day:
        messagebox.showerror("Error", "Please enter start and end dates.")
    else:
        start_date = f"{start_year}-{start_month.zfill(2)}-{start_day.zfill(2)}"
        end_date = f"{end_year}-{end_month.zfill(2)}-{end_day.zfill(2)}"
        pair = currency_codes[numerator] + currency_codes[denominator] + "=X"
        plot_forex_pair(pair, start_date, end_date)

config = load_config("config.json")

currency_codes = load_currency_codes("currency_codes.json")

#画面
root = tk.Tk()
root.title(config["window_title"])
root.geometry(config["window_size"])

#TKフレーム
frame = ttk.Frame(root)
frame.grid(column=0, row=0, padx=config["frame_padding_x"], pady=config["frame_padding_y"])

label_numerator = ttk.Label(frame, text=config["numerator_label_text"])
label_numerator.grid(column=config["numerator_label_column"], row=config["numerator_label_row"])

combo_numerator = ttk.Combobox(frame, values=list(currency_codes.keys()))
combo_numerator.grid(column=config["numerator_combo_column"], row=config["numerator_combo_row"])
combo_numerator.current(0)

label_denominator = ttk.Label(frame, text=config["denominator_label_text"])
label_denominator.grid(column=config["denominator_label_column"], row=config["denominator_label_row"])

combo_denominator = ttk.Combobox(frame, values=list(currency_codes.keys()))
combo_denominator.grid(column=config["denominator_combo_column"], row=config["denominator_combo_row"])
combo_denominator.current(1)

start_frame = ttk.Frame(frame)
start_frame.grid(column=config["start_frame_column"], row=config["start_frame_row"], columnspan=config["start_frame_columnspan"], pady=config["start_frame_padding_y"], sticky="ew")

#start year
label_start_year = ttk.Label(start_frame, text=config["start_year_label_text"])
label_start_year.grid(column=config["start_year_label_column"], row=config["start_year_label_row"], padx=config["start_year_label_padding_x"])

entry_start_year = ttk.Entry(start_frame, width=config["start_year_entry_width"])
entry_start_year.grid(column=config["start_year_entry_column"], row=config["start_year_entry_row"])


#start mouth
label_start_month = ttk.Label(start_frame, text=config["start_month_label_text"])
label_start_month.grid(column=config["start_month_label_column"], row=config["start_month_label_row"], padx=config["start_month_label_padding_x"])

entry_start_month = ttk.Entry(start_frame, width=config["start_month_entry_width"])
entry_start_month.grid(column=config["start_month_entry_column"], row=config["start_month_entry_row"])


#start day
label_start_day = ttk.Label(start_frame, text=config["start_day_label_text"])
label_start_day.grid(column=config["start_day_label_column"], row=config["start_day_label_row"], padx=config["start_day_label_padding_x"])

entry_start_day = ttk.Entry(start_frame, width=config["start_day_entry_width"])
entry_start_day.grid(column=config["start_day_entry_column"], row=config["start_day_entry_row"])


end_frame = ttk.Frame(frame)
end_frame.grid(column=config["end_frame_column"], row=config["end_frame_row"], columnspan=config["end_frame_columnspan"], pady=config["end_frame_padding_y"], sticky="ew")

#end year
label_end_year = ttk.Label(end_frame, text=config["end_year_label_text"])
label_end_year.grid(column=config["end_year_label_column"], row=config["end_year_label_row"], padx=config["end_year_label_padding_x"])

entry_end_year = ttk.Entry(end_frame, width=config["end_year_entry_width"])
entry_end_year.grid(column=config["end_year_entry_column"], row=config["end_year_entry_row"])

#end mouth
label_end_month = ttk.Label(end_frame, text=config["end_month_label_text"])
label_end_month.grid(column=config["end_month_label_column"], row=config["end_month_label_row"], padx=config["end_month_label_padding_x"])

entry_end_month = ttk.Entry(end_frame, width=config["end_month_entry_width"])
entry_end_month.grid(column=config["end_month_entry_column"], row=config["end_month_entry_row"])

#end day
label_end_day = ttk.Label(end_frame, text=config["end_day_label_text"])
label_end_day.grid(column=config["end_day_label_column"], row=config["end_day_label_row"], padx=config["end_day_label_padding_x"])

entry_end_day = ttk.Entry(end_frame, width=config["end_day_entry_width"])
entry_end_day.grid(column=config["end_day_entry_column"], row=config["end_day_entry_row"])


button = ttk.Button(frame, text=config["button_text"], command=show_chart)
button.grid(column=config["button_column"], row=config["button_row"], columnspan=config["button_columnspan"], pady=config["button_padding_y"])

save_button = ttk.Button(frame, text="Save Chart", command=save_chart)
save_button.grid_forget()


root.mainloop()
