from mrp_helper import BOM, start_mrp
from interface.interface import Interface
from inventory import Inventory

inventory = Inventory()
try:
    interface = Interface(inventory)
    interface.choice_widget.create_choice_widget(BOM, start_mrp)
    interface.master.mainloop()
except Exception as e:
    print(f'Unknown Error: [{e}]')
