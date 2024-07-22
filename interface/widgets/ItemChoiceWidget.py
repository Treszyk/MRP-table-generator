import tkinter as tk
from tkinter import StringVar, messagebox
import pandas as pd
import os

class ImpossibleProduction(Exception):
    pass
class NoDemand(Exception):
    pass

class ItemChoiceWidget:
    def __init__(self, parent) -> None:
        self.product_buttons = []
        self.parent = parent
        self.button_pressed = StringVar()
        
    def on_item_click(self, item, bom, interface, callback):
        try:
            writer = pd.ExcelWriter(f'MRP_{item}.xlsx', engine='xlsxwriter')
            self.parent.choose_item(item)
            self.destroy_choice_widget()
            callback(bom, writer, interface)
        except PermissionError as e:
            # Obsługa błędu, gdy plik Excela jest już otwarty przez inną aplikację
            self.parent.custom_message(f'Zamknij obecnie otwarty plik Excela MRP_{item}.xlsx i naciśnij [OK]')
        except ImpossibleProduction:
            writer.close()
            os.remove(f'./MRP_{item}.xlsx')
            self.parent.custom_message('Produkcja niemozliwa kliknij [OK] aby rozpocząć ponownie', lambda: self.parent.restart(bom, callback))
        except NoDemand:
            self.parent.custom_message('Nie ustawiłeś żadnego zapotrzebowania kliknij [OK] aby zakończyć', self.parent.close_main_window)
        except Exception as e:
            #print(f'Unknown Error: [{e}]')
            writer.close()
            os.remove(f'./MRP_{item}.xlsx')
            pass


    def create_choice_widget(self, products, start_mrp):
        #print(self.parent.inventory.get_item_stock('test'), 'start')
        self.parent.master.title('Wybór Produktu')
        row_num = 1
        column_num = 0
        button_width = 20
        button_height = 3
        button_padding_x = 10
        button_padding_y = 10

        header_text = "Wybierz przedmiot:"
        header_label = tk.Label(self.parent.master, text=header_text, font=('Arial', 14, 'bold'))
        header_label.grid(row=0, column=0, columnspan=3, pady=10)  # Place label at row 0, spanning across 3 columns

        self.product_buttons.append(header_label)
        for item in products.keys():
            button = tk.Button(self.parent.master, text=item, width=button_width, height=button_height,font=("Arial", 14),
                               command=lambda item=item: self.on_item_click(item, products, self.parent,start_mrp))
            button.grid(row=row_num, column=column_num, padx=button_padding_x, pady=button_padding_y)
            self.product_buttons.append(button)
            
            column_num += 1
            
            # Start new row after every 3 buttons
            if column_num == 2:
                column_num = 0
                row_num += 1
    
    def destroy_choice_widget(self):
        for button in self.product_buttons:
            button.destroy()