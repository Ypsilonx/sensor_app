import os
import json

def check_or_select_tower_number(file_path):
    # Zkontrolujte, zda soubor existuje
    if os.path.exists(file_path):
        # Načtení čísla věže ze souboru
        with open(file_path, 'r') as file:
            if file_path.endswith('.json'):
                data = json.load(file)
                tower_number = data.get('tower_number')
            else:
                tower_number = file.read().strip()
        print(f"Číslo věže nalezeno v souboru: {tower_number}")
    else:
        # Pokud soubor neexistuje, požádejte uživatele o zadání čísla věže
        tower_number = input("Soubor s číslem věže nebyl nalezen. Zadejte číslo věže: ")
        # Uložte číslo věže do souboru
        if file_path.endswith('.json'):
            with open(file_path, 'w') as file:
                json.dump({'tower_number': tower_number}, file)
        else:
            with open(file_path, 'w') as file:
                file.write(tower_number)
        print(f"Číslo věže bylo uloženo: {tower_number}")
    return tower_number