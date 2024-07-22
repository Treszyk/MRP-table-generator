class Inventory:
    def __init__(self):
        self.inventory = {}
    def set_item_stock(self, item, amount):
        self.inventory.setdefault(item, 0)
        self.inventory[item] = amount
    def get_item_stock(self, item):
        return self.inventory.get(item, 0)
