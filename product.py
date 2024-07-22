import pandas as pd
from interface.widgets.ItemChoiceWidget import ImpossibleProduction, NoDemand

class Product:
    def __init__(self, name: str, interface, amount=1, bom={}, parent=None) -> None:
        """
        Inicjalizacja klasy Product.
        Args:
            name (str): Nazwa produktu.
            interface (Interface): interfejs graficzny
            amount (int, optional): Ilość produktu. Domyślnie 1.
            bom (dict, optional): Struktura BOM (Bill of Materials) produktu. Domyślnie pusta.
            parent (Product, optional): Nadrzędny produkt w strukturze BOM. Domyślnie None.
        """
        fill = interface.fill
        self.interface = interface
        self.name = name
        self.bom = bom
        self.stock_changes = {}
        self.parent = parent
        self.inventory = self.interface.inventory
        self.lvl = self.set_lvl()
        self.amount = None
        self.production_time = None
        self.stock = None
        if self.lvl == 0:
            self.demands = self.set_demands()
            self.set_info()
        elif len(fill) != 0:
            #print(f'fill: {fill}')
            self.production_time = fill['production_time']
            self.inventory.set_item_stock(self.name, fill['stock'])
            self.stock = self.inventory.get_item_stock(self.name)
            self.amount = fill['need']
            self.demands = self.set_demands()  # Ustalenie zapotrzebowania na produkt
        else:
            self.set_info()
            self.demands = self.set_demands()  # Ustalenie zapotrzebowania na produkt

        #print('demands donendende')
        
        self.brutto = self.calc_brutto()  # Obliczenie brutto zapotrzebowania
        self.netto = self.calc_netto()  # Obliczenie netto zapotrzebowania
        self.production_start = self.calc_production_start()  # Obliczenie planowanego rozpoczęcia produkcji

    def set_info(self):
        self.interface.product_widget.create_product_widgets()
        self.interface.product_widget.update_widget(self)
        self.interface.master.wait_variable(self.interface.product_widget.button_pressed)
        info = self.interface.product_data[-1]
        self.production_time = info['production_time']
        self.inventory.set_item_stock(self.name, info['stock'])
        self.stock = self.inventory.get_item_stock(self.name)
        self.amount = info['need']
        #print(self.inventory.inventory)

    def set_quantity(self) -> int:
        """
        Ustalenie ilości potrzebnej na wyprodukowanie produktu nadrzędnego.
        Returns:
            int: ilość potrzebna na wyprodukowanie produktu nadrzędnego.
        """
        if self.lvl == 0:
            return 1
        while True:
            try:
                n = int(input(f'Ile trzeba [{self.name}] aby wyprodukowac jedna sztuke [{self.parent.name}]?: '))
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        return n
    
    def set_stock(self) -> int:
        """
        Ustalenie stanu magazynowego produktu.
        Returns:
            int: Stan magazynowy.
        """
        while True:
            try:
                n = int(input(f'Ile masz [{self.name}] w magazynie: '))
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        return n

    def set_demands(self) -> dict:
        """
        Ustalenie zapotrzebowania na produkt.
        Returns:
            dict: Słownik zawierający zapotrzebowanie na poszczególne tygodnie.
        """
        demands = {}
        if self.lvl == 0:
            self.interface.demand_widget.create_demand_widget()
            self.interface.master.wait_variable(self.interface.demand_widget.button_pressed)
            demands = self.interface.demands
            #print('demands done')
            return demands
        else:
            final_items = self.parent.stock * self.amount
            for week, quantity in self.parent.demands.items():
                demand = self.amount * quantity
                final_items, demand = self.subtract(final_items, demand)
                demands.setdefault(week - self.parent.production_time, 0)
                demands[week - self.parent.production_time] = demand
        if len(demands) == 0:
            raise NoDemand()
        return demands

    def set_production_time(self) -> int:
        """
        Ustalenie czasu produkcji produktu.
        Returns:
            int: Czas produkcji.
        """
        while True:
            try:
                n = int(input(f'Jak długo produkujesz [{self.name}]: '))
                break
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except:
                pass
        return n

    def set_lvl(self) -> int:
        """
        Ustalenie poziomu produktu w strukturze BOM.
        Returns:
            int: Poziom produktu.
        """
        if self.parent is not None:
            return self.parent.lvl + 1
        else:
            return 0

    def calc_brutto(self):
        """
        Obliczenie zapotrzebowania brutto.
        Returns:
            dict: Słownik zawierający brutto zapotrzebowanie na poszczególne tygodnie.
        """
        brutto = {}
        for week, quantity in self.demands.items():
            brutto.setdefault(week, 0)
            brutto[week] = quantity
        return brutto

    def calc_netto(self):
        """
        Obliczenie zapotrzebowania netto oraz zapisanie zmian stanu magazynu.
        Returns:
            dict: Słownik zawierający netto zapotrzebowanie na poszczególne tygodnie.
        """
        netto = {}
        inv = self.stock
        for week, quantity in self.demands.items():
            inv, quantity = self.subtract(inv, quantity)
            if inv != self.stock:
                self.stock_changes.setdefault(week, inv)
                self.inventory.set_item_stock(self.name, inv)
            netto.setdefault(week, 0)
            netto[week] = quantity
        return netto

    def calc_production_start(self):
        """
        Obliczenie planowanego rozpoczęcia produkcji.
        Returns:
            dict: Słownik zawierający planowane rozpoczęcie produkcji na poszczególne tygodnie.
        Raises:
            ImpossibleProduction: Wyjątek rzucany w przypadku niemożliwej produkcji.
        """
        production_start = {}
        for week, quantity in self.netto.items():
            production_start.setdefault(week - self.production_time, quantity)
        min_week = min(production_start)
        if min_week <= 0 and production_start[min_week] != 0:
            raise ImpossibleProduction('Produkcja niemożliwa')
        return production_start

    def create_mrp_table(self, writer, max_week):
        """
        Tworzenie tabeli MRP i zapis do arkusza Excela.
        Args:
            writer: Obiekt do zapisu do arkusza Excela.
            max_week (int): Maksymalny tydzień analizy zapotrzebowania.
        """
        prefix = (self.parent.name + '-') if self.parent is not None else ''
        df = pd.DataFrame({
            f'Poziom {self.lvl} {self.name}': ['Tydzień', 'Potrzeby brutto', 'Wstępny zapas', 'Potrzeby netto', 'Zamówienie', 'Zaplanowany odbiór']
        })
        shadow_stock = self.stock
        for i in range(1, max_week + 1):
            column = []
            column.append(i)
            column.append(self.format_for_excel(self.brutto.get(i, '')))
            column.append(self.format_for_excel(shadow_stock))
            if i in self.stock_changes.keys():
                shadow_stock = self.stock_changes[i]
            column.append(self.format_for_excel(self.netto.get(i, '')))
            column.append(self.format_for_excel(self.production_start.get(i, '')))
            column.append(self.format_for_excel(self.netto.get(i, '')))
            df.insert(len(df.columns), None, column, allow_duplicates=True)
        prefix = (self.parent.name + '-') if self.parent is not None else ''
        df.to_excel(writer, sheet_name=f'{prefix}LVL{self.lvl} {self.name}', index=False)
        writer.sheets[f'{prefix}LVL{self.lvl} {self.name}'].set_column(0, 0, 30)

    def format_for_excel(self, val):
        """
        Formatowanie wartości do zapisu w arkuszu Excela.
        Args:
            val: Wartość do sformatowania.
        Returns:
            str: Sformatowana wartość (pusty ciąg znaków dla wartości zero).
        """
        if val == 0:
            return ''
        return val

    def subtract(self, x, y):
        """
        Odejmowanie wartości wiekszej od mniejszej.
        Args:
            x: Wartość 1
            y: Wartość 2
        Returns:
            tuple: Krotka zawierająca (x, y).
        """
        if x > y:
            x -= y
            y = 0
        elif x < y:
            y -= x
            x = 0
        else:
            y = 0
            x = 0
        return (x, y)
