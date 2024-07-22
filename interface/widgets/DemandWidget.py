import tkinter as tk
from tkinter import StringVar, messagebox

class DemandWidget:
    def __init__(self, parent) -> None:
        self.parent = parent
        self.week_demand_pairs = []
        self.button_pressed = StringVar()
    
    def create_demand_widget(self):
        self.parent.master.title('Zapotrzebowanie')
        # Frame to hold existing pairs and add new pair
        self.pairs_frame = tk.Frame(self.parent.master)
        self.pairs_frame.pack(pady=20)

        # Button to add new pair
        self.add_button = tk.Button(self.pairs_frame, text="Dodaj nowy", command=self.add_new_pair, font=("Arial", 14))
        self.add_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Button to delete last pair
        self.delete_button = tk.Button(self.pairs_frame, text="Usuń ostatni", command=self.delete_last_pair, font=("Arial", 14))
        self.delete_button.pack(side=tk.LEFT, padx=10, pady=5)

        # Frame to hold input pairs
        self.pairs_frame = tk.Frame(self.parent.master)
        self.pairs_frame.pack(pady=20)

        # Button to submit
        self.submit_button = tk.Button(self.parent.master, text="Zapisz", command=self.submit_data, font=("Arial", 14))
        self.submit_button.pack(pady=10)

        self.add_new_pair()

    def add_new_pair(self):
        # Create a new pair of labeled inputs
        new_pair_frame = tk.Frame(self.pairs_frame)
        new_pair_frame.pack(pady=5)

        # Week label and entry
        week_label = tk.Label(new_pair_frame, text="Tydzień:")
        week_label.pack(side=tk.LEFT, padx=5)
        week_entry = tk.Entry(new_pair_frame, width=10)
        week_entry.pack(side=tk.LEFT, padx=5)
        week_entry.focus_set()

        # Demand label and entry
        demand_label = tk.Label(new_pair_frame, text="Zapotrzebowanie:")
        demand_label.pack(side=tk.LEFT, padx=5)
        demand_entry = tk.Entry(new_pair_frame, width=10)
        demand_entry.pack(side=tk.LEFT, padx=5)

        # Append the new pair to the list
        self.week_demand_pairs.append((new_pair_frame, [week_entry, demand_entry]))

    def delete_last_pair(self):
        # Check if there are pairs to delete
        if self.week_demand_pairs:
            # Get the last pair from the list
            last_pair, values = self.week_demand_pairs[-1]

            # Destroy all widgets associated with the last pair
            last_pair.destroy()
            
            # Remove the last pair from the list
            self.week_demand_pairs.pop()
    
    def destroy_week_widget(self):
        # Destroy all widgets in pairs_frame
        for pair, values in self.week_demand_pairs:
            pair.destroy()

        # Destroy buttons_frame widgets
        self.add_button.destroy()
        self.delete_button.destroy()
        self.submit_button.destroy()

        # Destroy pairs_frame and buttons_frame
        self.pairs_frame.destroy()

    def submit_data(self):
        demands = {}
        for frame, values in self.week_demand_pairs:
            week = values[0]
            demand = values[1]
            #print(demand.get().isnumeric(), week.get().isnumeric())

            if week.get() == '' or demand.get() == '':
                self.parent.custom_message('Żadne pole nie może być puste')
                return
            if not demand.get().isnumeric() or not week.get().isnumeric():
                self.parent.custom_message('W polach mogą znajdować się tylko liczby')
                return 
            demands.setdefault(int(week.get()), 0)
            demands[int(week.get())] = int(demand.get())
        
        if len(self.week_demand_pairs) == 0:
            self.parent.custom_message('Musisz ustawic jakies zapotrzebowanie')
        else:
            self.parent.set_demand(demands)
            self.button_pressed.set("button pressed")
            self.destroy_week_widget()
