import tkinter as tk
from tkinter import messagebox
from interface.widgets.ItemChoiceWidget import ItemChoiceWidget
from interface.widgets.DemandWidget import DemandWidget
from interface.widgets.ProductWidget import ProductWidget
class Interface:
    def __init__(self, inventory):
        self.master = tk.Tk()
        self.master.resizable(False, False)
        self.master.title("Product Input")
        self.chosen_item = None
        self.demands = {}
        self.product_data = []
        self.inventory = inventory
        self.master.protocol("WM_DELETE_WINDOW", lambda: on_window_close(self))
        self.choice_widget = ItemChoiceWidget(self)
        self.demand_widget = DemandWidget(self)
        self.product_widget = ProductWidget(self)
        self.fill = {}

    def close_main_window(self):
        #self.parent.inventory.set_item_stock('test', 420)
        #print('close')
        self.master.destroy()

    def custom_message(self, text, callback_func=None):
        top = tk.Toplevel(self.master)
        top.title("Informacja")
        # Display the message in a label
        label = tk.Label(top, text=text, padx=20, pady=10)
        label.pack()
        def on_ok_click():
            if callback_func:
                callback_func()
            else:
                top.destroy()

        ok_button = tk.Button(top, text="OK", command=on_ok_click)
        
        ok_button.pack(pady=10)
    def choose_item(self, item):
        self.chosen_item = item
        #print(f"Selected Item: {item}")

    def set_demand(self, demands):
        self.demands = demands
    
    def restart(self, BOM, start_mrp):
        self.master.destroy()
        self.fill = {}
        self.master = tk.Tk()
        self.master.resizable(False, False)
        self.choice_widget = ItemChoiceWidget(self)
        self.demand_widget = DemandWidget(self)
        self.product_widget = ProductWidget(self)
        self.choice_widget.create_choice_widget(BOM, start_mrp)
        self.master.mainloop()

def on_window_close(interface):
    interface.demand_widget.button_pressed.set('pressed')
    interface.product_widget.button_pressed.set('pressed')
    interface.master.destroy()

