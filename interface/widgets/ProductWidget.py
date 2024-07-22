import tkinter as tk
from tkinter import StringVar
class ProductWidget:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.current_product_index = 0
        self.button_pressed = StringVar()
        self.set_already = False
        self.need_visible = False

    def create_product_widgets(self):
        if self.set_already:
            return
        self.parent.master.title('Produkt Info')

        self.product_name_label = tk.Label(self.parent.master, text='Nazwa produktu:', font=('Arial', 14, 'bold'))
        self.product_name_label.pack(pady=0)

        self.product_production_label = tk.Label(self.parent.master, text="Czas produkcji:")
        self.product_production_label.pack(pady=10)
        self.product_production_entry = tk.Entry(self.parent.master)
        self.product_production_entry.pack(pady=5)
        self.product_production_entry.focus_set()

        self.product_stock_label = tk.Label(self.parent.master, text="Ilość w magazynie:")
        self.product_stock_label.pack(pady=10)
        self.product_stock_label_entry = tk.Entry(self.parent.master)
        self.product_stock_label_entry.pack(pady=5)

        self.product_needed_label = tk.Label(self.parent.master, text="Ile sztuk potrzebne do produkcji:")
        self.product_needed_label.pack(pady=10)
        self.product_needed_label_entry = tk.Entry(self.parent.master)
        self.product_needed_label_entry.pack(pady=5)

        # Frame to contain the buttons
        self.button_frame = tk.Frame(self.parent.master)
        self.button_frame.pack(pady=20)

        self.submit_button = tk.Button(self.button_frame, text="Zapisz", command=self.submit_product,font=("Arial", 14))
        self.submit_button.pack(side=tk.LEFT, padx=10)

        self.fill_button = tk.Button(self.button_frame, text="AutoFill", command=self.open_fill_window,font=("Arial", 14))
        self.fill_button.pack(side=tk.LEFT, padx=10)

        self.set_already = True
    def delete_widget(self):
        # Destroy or remove all widgets created by ProductWidget
        self.product_name_label.destroy()
        self.product_production_label.destroy()
        self.product_production_entry.destroy()
        self.product_stock_label.destroy()
        self.product_stock_label_entry.destroy()
        self.product_needed_label.destroy()
        self.product_needed_label_entry.destroy()
        self.submit_button.destroy()
        self.fill_button.destroy()

        # Reset set_already flag for re-creation if needed
        self.set_already = False

        # Optionally perform additional cleanup or actions here
    def update_widget(self, product):
        self.product_name_label.config(text=f"Nazwa produktu: {product.name}")
        self.product_production_label.config(text="Czas produkcji:")
        self.product_production_entry.focus()
        self.product_stock_label.config(text="Ilość w magazynie:")
        if product.parent is not None:
            self.product_needed_label.pack(pady=10)
            self.product_needed_label_entry.pack(pady=5)
            self.product_stock_label_entry.insert(0, f'{self.parent.inventory.get_item_stock(product.name)}')
            self.product_needed_label.config(text=f"Ile sztuk potrzebne do produkcji {product.parent.name}:")
            self.button_frame.forget()
            self.button_frame.pack(pady=20)
            self.need_visible = True
        else:
            self.product_needed_label.forget()
            self.product_needed_label_entry.forget()
            self.need_visible = False


    def submit_product(self):
        product_production = self.product_production_entry.get()
        product_stock = self.product_stock_label_entry.get()
        product_need = self.product_needed_label_entry.get()

        if not product_production or not product_stock or (not product_need and self.need_visible):
            self.parent.custom_message('Żadne pole nie może być puste')
            return

        if not product_production.isnumeric() or not product_stock.isnumeric() or (not product_need.isnumeric() and len(product_need) > 0):
            self.parent.custom_message('W polach mogą znajdować się tylko liczby')
            return

        self.parent.product_data.append({
            "name": self.product_name_label.cget("text"),
            "production_time": int(product_production),
            "stock": int(product_stock),
            "need": 1 if product_need == '' else int(product_need)
        })

        self.product_production_entry.delete(0, tk.END)
        self.product_stock_label_entry.delete(0, tk.END)
        self.product_needed_label_entry.delete(0, tk.END)

        self.button_pressed.set("button pressed")
        
    def open_fill_window(self):
        fill_window = tk.Toplevel(self.parent.master)
        fill_window.title("AutoFill")

        header_text = "Wpisz wartości którymi chcesz uzupełnic reszte przedmiotów:"
        tk.Label(fill_window, text=header_text, font=('Arial', 14, 'bold')).pack(pady=10)

        # Labels and Entry fields for value inputs
        tk.Label(fill_window, font=("Arial", 14),text="Czas produkcji:").pack()
        self.production_time = tk.Entry(fill_window)
        self.production_time.insert(0, f'1')
        self.production_time.pack()

        tk.Label(fill_window, font=("Arial", 14), text="Ilość w magazynie:").pack()
        self.stock_fill = tk.Entry(fill_window)
        self.stock_fill.insert(0, f'0')
        self.stock_fill.pack()

        tk.Label(fill_window, font=("Arial", 14), text="Ilość potrzebne do produkcji nadrzędnego produktu:").pack()
        self.amount_needed = tk.Entry(fill_window)
        self.amount_needed.insert(0, f'1')
        self.amount_needed.pack()

        submit_button = tk.Button(fill_window, text="Uzupełnij", font=("Arial", 14), command=lambda: self.submit_fill(fill_window))
        submit_button.pack(pady=10)


    def submit_fill(self, fill_window):
        production_time = self.production_time.get()
        stock_fill = self.stock_fill.get()
        amount_needed = self.amount_needed.get()

        if not production_time or not stock_fill or not amount_needed:
            self.parent.custom_message("Żadne pole nie może być puste")
            return

        self.parent.product_data.append({
            "name": self.product_name_label.cget("text"),
            "production_time": int(production_time),
            "stock": int(stock_fill),
            "need": 1 if amount_needed == '' else int(amount_needed)
        })
        self.parent.fill = {'production_time': int(production_time), 'stock': int(stock_fill), 'need': int(amount_needed)}

        # Close the fill window
        fill_window.destroy()
        self.parent.master.focus_set()  # Return focus to main window
        self.button_pressed.set('button pressed')