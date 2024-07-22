from product import Product
import os

#'nazwa_przedmiotu': [poziom, bom dla 1 sztuki przedmiotu]
BOM = {
    #Poziomy 2
    'Stół': [2, {
        'Nogi': {'Gwoździe': {}, 'Podkładki': {}},
        'Blat': {'Gwoździe': {}, 'Deski': {}, 'Listwy': {}}
    }],
    'Biurko': [2, {
        'Nogi': {'Gwoździe': {}, 'Podkładki': {}},
        'Blat': {'Deski': {}, 'Listwy': {}},
        'Szafki': {'Deski': {}, 'Prowadnice': {}}
    }],
    'Krzesło': [2, {
        'Nogi': {'Śruby': {}, 'Podkładki': {}},
        'Siedzisko': {'Deski': {}, 'Tapicerka': {}}
    }],
    'Szafa': [2, {
        'Boki': {'Deski': {}, 'Listwy': {}},
        'Drzwi': {'Deski': {}, 'Klamki': {}},
        'Półki': {'Deski': {}, 'Wsporniki': {}}
    }],
    'Łóżko': [2, {
        'Nogi': {'Wkręty': {}, 'Podkładki': {}},
        'Rama': {'Deski': {}, 'Listwy': {}},
        'Stelaż': {'Deski': {}, 'Śruby': {}}
    }],
    #Poziomy 3
    'Samochód': [3, {
        'Silnik': {
            'Tłoki': {'Pierścienie tłokowe': {}, 'Walec': {}},
            'Chłodzenie': {'Chłodnica': {}, 'Pompa': {}}
        },
        'Podwozie': {
            'Rama': {'Belki': {}, 'Zawieszenie': {}},
            'Koła': {'Opony': {}, 'Felgi': {}}
        },
        'Karoseria': {
            'Drzwi': {'Blacha': {}, 'Szyby': {}},
            'Maska': {'Blacha': {}, 'Zawiasy': {}},
            'Lampy': {'Żarówki': {}, 'Obudowy': {}}
        }
    }],
    'Komputer': [3, {
        'Procesor': {
            'Rdzenie': {'Jądra': {}, 'Cache': {}},
            'Chłodzenie': {'Wentylator': {}, 'Chłodnica': {}}
        },
        'Pamięć': {
            'RAM': {'Kostki pamięci': {}, 'Złącza': {}},
            'Dysk SSD': {'Kontroler': {}, 'Pamięć flash': {}}
        },
        'Obudowa': {
            'Płyta główna': {'Złącza': {}, 'Chipset': {}},
            'Zasilacz': {'Kondensatory': {}, 'Przewody': {}}
        }
    }],
    'Statek': [3, {
        'Kadłub': {
            'Burty': {'Blachy stalowe': {}, 'Deski': {}},
            'Dno': {'Płaty balastowe': {}, 'Izolacja': {}}
        },
        'Napęd': {
            'Napęd': {'Łopatki śrub': {}, 'Silniki': {}},
            'Ster': {'Koło sterowe': {}, 'Układ sterowania': {}}
        },
        'Wyposażenie': {
            'Winda': {'Silnik': {}, 'Liny': {}},
            'Pokład': {'Barierki': {}}
        }
    }],
}


def create_tables(bom, parent, writer, max_week, interface):
    """
    Tworzenie rekurencyjnie tabel MRP dla podkomponentów w strukturze BOM.
    Args:
        bom (dict): Struktura BOM dla aktualnie analizowanego komponentu.
        parent (Product): Obiekt rodzica w strukturze BOM.
        writer: Obiekt do zapisu do arkusza Excela.
        max_week (int): Maksymalny tydzień analizy zapotrzebowania.
    """
    for component in bom:
        sub_bom = bom[component]  # BOM dla komponentu

        # Tworzenie obiektu Product dla aktualnego komponentu
        comp_object = Product(component, interface, parent=parent)
        
        # Tworzenie tabeli MRP dla komponentu i zapis do arkusza Excela
        comp_object.create_mrp_table(writer, max_week)
        # tutaj wait na submit buttonie???????????
        # Rekurencyjne wywołanie create_tables dla podkomponentu
        create_tables(sub_bom, comp_object, writer, max_week, interface)
    return True
def start_mrp(bom: dict, writer, interface) -> str:
    """
    Funkcja umożliwiająca użytkownikowi wybór przedmiotu z listy dostępnych przedmiotów.
    Args:
        bom (dict): Słownik zawierający listę dostępnych przedmiotów i ich strukturę BOM.
    Returns:
        str: Nazwa wybranego przedmiotu.
    """

    #print(f'chosen item = {interface.chosen_item}')
    chosen_item = interface.chosen_item

    lvl0_item = Product(chosen_item, interface, BOM[chosen_item][1])
    
    # Określenie maksymalnego tygodnia potrzebnego do analizy zapotrzebowania
    max_week = max(lvl0_item.demands.keys())
    
    # Tworzenie tabeli MRP dla przedmiotu głównego poziomu (lvl0) i zapis do arkusza Excela
    lvl0_item.create_mrp_table(writer, max_week)
    
    # Tworzenie tabel MRP dla podkomponentów wybranego przedmiotu i zapis do arkusza Excela
    result = create_tables(BOM[lvl0_item.name][1], lvl0_item, writer, max_week, interface)
    if result:
        writer.close()
        os.startfile(f'.\\MRP_{chosen_item}.xlsx')    
        interface.custom_message(f'Udało się wygenerować plik: MRP_{chosen_item}.xlsx. Kliknij [OK] aby kontynuować', lambda: interface.restart(BOM, start_mrp))

    return interface.chosen_item

