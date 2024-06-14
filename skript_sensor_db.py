import sqlite3
import os
from datetime import datetime, timedelta
from check_tower import check_or_select_tower_number


TOWERS = [1,2,3]
class SensorDB:
    def __init__(self, db_path) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):# Vytvoření tabulky
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sensors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                label TEXT NOT NULL UNIQUE,
                calibration_date DATE NOT NULL DEFAULT (date('now')),
                crash INTEGER NOT NULL CHECK (crash IN (0, 1)) DEFAULT 0,
                info_1_tower INTEGER NOT NULL CHECK (info_1_tower IN (0, 1)) DEFAULT 0,
                info_2_tower INTEGER NOT NULL CHECK (info_2_tower IN (0, 1)) DEFAULT 0,
                info_3_tower INTEGER NOT NULL CHECK (info_3_tower IN (0, 1)) DEFAULT 0
            )
        ''')
        
        
        for i in TOWERS:
            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS tower{i} (
                id INTEGER NOT NULL UNIQUE REFERENCES sensors (id),
                label TEXT NOT NULL UNIQUE REFERENCES sensors (label),
                sensor_check INTEGER NOT NULL CHECK (sensor_check IN (0, 1)) DEFAULT 0,
                connector TEXT,
                NIcard TEXT
            )
        ''')
        
            self.cursor.execute(f'''
                CREATE TRIGGER IF NOT EXISTS insert_tower{i}
                AFTER INSERT ON sensors
                WHEN NEW.info_{i}_tower = 1
                BEGIN
                    INSERT OR IGNORE INTO tower{i} (id, label, sensor_check, connector, NIcard)
                    VALUES (NEW.id, NEW.label, 0, '', '');
                END;
            ''')

            # Vytvoření triggeru pro automatické vložení do tower1 po aktualizaci v sensors          
            self.cursor.execute(f'''
                CREATE TRIGGER IF NOT EXISTS update_tower{i}
                AFTER UPDATE OF info_{i}_tower ON sensors
                BEGIN
                    -- Když se info_{i}_tower změní na 1, vloží nový záznam do tower{i}
                    INSERT OR IGNORE INTO tower{i} (id, label, sensor_check, connector, NIcard)
                    SELECT NEW.id, NEW.label, 0, '', ''
                    WHERE NEW.info_{i}_tower = 1;

                    -- Když se info_{i}_tower změní na 0, smaže odpovídající záznam z tower{i}
                    DELETE FROM tower{i}
                    WHERE OLD.info_{i}_tower = 1 AND NEW.info_{i}_tower = 0 AND id = NEW.id;
                END;
            ''')
        
        self.conn.commit()

    def insert_sensor(self, name, sensor_type, label, crash=0, info_1_tower=0, info_2_tower=0, info_3_tower=0):
        self.cursor.execute('''
            INSERT INTO sensors (name, type, label, crash, info_1_tower, info_2_tower, info_3_tower)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, sensor_type, label, crash, info_1_tower, info_2_tower, info_3_tower))
        self.conn.commit()

    def insert_tower_info(self):
        pass
    
    def get_sensor_info_by_label(self, label, tower):
        query = f'''
        SELECT sensors.*, tower{tower}.sensor_check, tower{tower}.connector, tower{tower}.NIcard
        FROM sensors
        JOIN tower{tower} ON sensors.label = tower{tower}.label
        WHERE tower{tower}.label = ?
        '''
        self.cursor.execute(query, (label,))
        return self.cursor.fetchone()
    
    def get_sensor_info_by_id(self, id):
        query = f'''
        SELECT sensors.*
        FROM sensors
        WHERE sensors.id = ?
        '''
        self.cursor.execute(query, (id,))
        return self.cursor.fetchone()
    
    def get_sensor_info_by_id_and_tower(self, id, tower):
        query = f'''
        SELECT *
        FROM sensors
        WHERE sensors.id = ? AND sensors.info_{tower}_tower = ?
        '''
        self.cursor.execute(query, (id, 1))
        return self.cursor.fetchone()

    
    def get_combobox_sensor_name(self):
        self.cursor.execute("SELECT name FROM sensors")
        rows = self.cursor.fetchall()
        result = [row[0] for row in rows]
        return result
    
    def get_combobox_tower_sensor(self, tower):
        result = []
        vyber_vez = tower
        self.cursor.execute(f"SELECT sensors.name FROM sensors JOIN tower{tower} ON sensors.label = tower{tower}.label")
        rows = self.cursor.fetchall()
        result.extend([row[0] for row in rows])
        return result
    
    def get_list_tower_sensor_id(self, tower):
        result = []
        # vyber_vez = tower
        self.cursor.execute(f"SELECT sensors.id FROM sensors JOIN tower{tower} ON sensors.label = tower{tower}.label")
        rows = self.cursor.fetchall()
        result.extend([row[0] for row in rows])
        return result
    
    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    this_folder = os.path.dirname(os.path.abspath(__file__)) # získání cesty k tomuto souboru
    db_path = 'sensors.db'
    sensor_db = SensorDB(db_path)

    file_path = 'tower_number.txt'
    tower_number = check_or_select_tower_number(file_path)
    
    sensor_db.close_connection()
    
    # # Vložit několik senzorů
    # sensor_db.insert_sensor("SensorA", "TypeA", "S-101", 0, 1, 0, 1)
    # sensor_db.insert_sensor("SensorB", "TypeB", "S-102", 1, 0, 1, 0)
    # sensor_db.insert_sensor("SensorC", "TypeC", "S-103", 0, 1, 1, 0)

    # # Získat informace o senzoru podle ID
    # print(sensor_db.get_sensor_info_by_id(1))
    # print(sensor_db.get_sensor_info_by_id(2))
    # print(sensor_db.get_sensor_info_by_id(3))

    # # Získat seznam ID senzorů podle věže
    # seznam_senzoru_veze = sensor_db.get_list_tower_sensor_id(tower_number)
    # print(seznam_senzoru_veze)
    
    # # Získat informace o senzoru podle ID a TOWER
    # for x in seznam_senzoru_veze:
    #     print(sensor_db.get_sensor_info_by_id_and_tower(x, tower_number))

    # # Získat seznam jmen senzorů
    # print(sensor_db.get_combobox_sensor_name())
    
    # # Získat seznam jmen senzorů z tabulek věží
    # print(sensor_db.get_combobox_tower_sensor(tower_number))

    # sensor_db.close_connection()