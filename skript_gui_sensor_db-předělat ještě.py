import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from skript_sensor_db import SensorDB

class SensorApp:
    def __init__(self, root, db_path):
        self.root = root
        self.root.title("Sensor Database Application")

        self.set_style_app()
        self.db = SensorDB(db_path)

        self.set_fixed_size(800, 600)  # Nastavení pevné šířky a výšky okna

        self.create_menu()

    def set_fixed_size(self, width, height):
        # Nastavení pevné šířky a výšky okna
        self.root.geometry(f'{width}x{height}')
        self.root.resizable(False, False)

        # Výpočet středu obrazovky
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = int((screen_width / 2) - (width / 2))
        position_y = int((screen_height / 2) - (height / 2))

        # Nastavení okna na střed obrazovky
        self.root.geometry(f'+{position_x}+{position_y}')

    def set_style_app(self):
        style = ttk.Style()
        style.configure('TLabel', font=('Consolas', 12))
        style.configure('TButton', font=('Consolas', 12))
        style.configure('TEntry', font=('Consolas', 12), foreground='green', padding=5)
        style.map('TEntry', 
                  foreground=[('disabled', 'gray'), ('focus', 'blue'), ('hover', 'red')],
                  background=[('focus', 'lightyellow')])

    def create_menu(self):
        menubar = tk.Menu(self.root)

        menubar.add_cascade(label="Add Sensor", command=self.add_sensor_window)
        menubar.add_cascade(label="Update Sensor", command=self.update_sensor_window)
        menubar.add_cascade(label="Delete Sensor") # doplnit command='funkce'
        menubar.add_separator()
        menubar.add_cascade(label="Exit", command=self.root.quit)

        self.root.config(menu=menubar)

    def center_window(self, window, width, height):
        window.geometry(f'{width}x{height}')
        window.resizable(False, False)

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        position_x = int((screen_width / 2) - (width / 2))
        position_y = int((screen_height / 2) - (height / 2))

        window.geometry(f'+{position_x}+{position_y}')

    def add_sensor_window(self):
        window = tk.Toplevel(self.root)
        window.title("Add Sensor")
        self.center_window(window, 500, 500)

        label_name = ttk.Label(window, text="Name")
        label_name.grid(row=0, column=0, padx=5, pady=5)
        entry_name = ttk.Entry(window)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        label_type = ttk.Label(window, text="Type")
        label_type.grid(row=1, column=0, padx=5, pady=5)
        entry_type = ttk.Entry(window)
        entry_type.grid(row=1, column=1, padx=5, pady=5)

        label_label = ttk.Label(window, text="Label")
        label_label.grid(row=2, column=0, padx=5, pady=5)
        entry_label = ttk.Entry(window)
        entry_label.grid(row=2, column=1, padx=5, pady=5)

        # Additional fields for towers
        label_crash = ttk.Label(window, text="Crash (0 or 1)")
        label_crash.grid(row=3, column=0, padx=5, pady=5)
        entry_crash = ttk.Entry(window)
        entry_crash.grid(row=3, column=1, padx=5, pady=5)

        label_info1 = ttk.Label(window, text="Info 1 Tower (0 or 1)")
        label_info1.grid(row=4, column=0, padx=5, pady=5)
        entry_info1 = ttk.Entry(window)
        entry_info1.grid(row=4, column=1, padx=5, pady=5)

        label_info2 = ttk.Label(window, text="Info 2 Tower (0 or 1)")
        label_info2.grid(row=5, column=0, padx=5, pady=5)
        entry_info2 = ttk.Entry(window)
        entry_info2.grid(row=5, column=1, padx=5, pady=5)

        label_info3 = ttk.Label(window, text="Info 3 Tower (0 or 1)")
        label_info3.grid(row=6, column=0, padx=5, pady=5)
        entry_info3 = ttk.Entry(window)
        entry_info3.grid(row=6, column=1, padx=5, pady=5)

        button_add = ttk.Button(window, text="Add", command=lambda: self.add_sensor(
            entry_name.get(), entry_type.get(), entry_label.get(), entry_crash.get(), entry_info1.get(), entry_info2.get(), entry_info3.get()))
        button_add.grid(row=7, column=0, columnspan=2)

    def update_sensor_window(self):
        window = tk.Toplevel(self.root)
        window.title("Update Sensor")
        self.center_window(window, 500, 500)
        
        label_id = ttk.Label(window, text="Sensor ID")
        label_id.grid(row=0, column=0, padx=5, pady=5)
        entry_id = ttk.Entry(window)
        entry_id.grid(row=0, column=1, padx=5, pady=5)

        button_load = ttk.Button(window, text="Load", command=lambda: self.load_sensor_info(entry_id.get(), window))
        button_load.grid(row=1, column=0, columnspan=2)

    def add_sensor(self, name, sensor_type, label, crash, info_1, info_2, info_3):
        if name and sensor_type and label:
            try:
                self.db.insert_sensor(name, sensor_type, label, int(crash), int(info_1), int(info_2), int(info_3))
                messagebox.showinfo("Success", "Sensor added successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding sensor: {e}")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    def view_sensors_window(self):
        window = tk.Toplevel(self.root)
        window.title("View Sensors")

        sensors = self.db.get_combobox_sensor_name()
        for i, sensor in enumerate(sensors):
            ttk.Label(window, text=sensor).grid(row=i, column=0)

    def load_sensor_info(self, sensor_id, parent_window):
        sensor_info = self.db.get_sensor_info_by_id(sensor_id)
        if sensor_info:
            self.show_sensor_info(sensor_info, parent_window)
        else:
            messagebox.showerror("Error", "Sensor not found")

    def show_sensor_info(self, sensor_info, parent_window):
        # Display sensor info in entries for editing
        labels = ["Name", "Type", "Label", "Crash", "Info 1 Tower", "Info 2 Tower", "Info 3 Tower"]
        for i, (label, value) in enumerate(zip(labels, sensor_info[1:])):
            ttk.Label(parent_window, text=label).grid(row=i+2, column=0)
            entry = ttk.Entry(parent_window)
            entry.insert(0, value)
            entry.grid(row=i+2, column=1, padx=2, pady=2)

        button_update = tk.Button(parent_window, text="Update", command=lambda: self.update_sensor(sensor_info[0], parent_window))
        button_update.grid(row=len(labels)+2, column=0, columnspan=2)

    def update_sensor(self, sensor_id, parent_window):
        # Collect updated values from entries and update the database
        updated_values = [entry.get() for entry in parent_window.grid_slaves() if isinstance(entry, tk.Entry)]
        try:
            self.db.update_sensor(sensor_id, *updated_values)
            messagebox.showinfo("Success", "Sensor updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating sensor: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SensorApp(root, 'sensors.db')
    root.mainloop()
