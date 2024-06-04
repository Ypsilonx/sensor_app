import sqlite3
import os
from datetime import datetime, timedelta

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
        
        towers = [1,2,3]
        
        for i in towers:
            self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS tower{i} (
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
                    INSERT OR IGNORE INTO tower{i} (label, sensor_check, connector, NIcard)
                    VALUES (NEW.label, 0, '', '');
                END;
            ''')

            # Vytvoření triggeru pro automatické vložení do tower1 po aktualizaci v sensors
            self.cursor.execute(f'''
                CREATE TRIGGER IF NOT EXISTS update_tower{i}
                AFTER UPDATE OF tower, label ON sensors
                WHEN NEW.info_{i}_tower = {i}
                BEGIN
                    INSERT OR IGNORE INTO tower{i} (label, sensor_check, connector, NIcard)
                    VALUES (NEW.label, 0, '', '');
                END;
            ''')
        
        self.conn.commit()

    def insert_sensor(self):
        pass
    
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
    
    def close_connection(self):
        self.conn.close()


if __name__ == "__main__":
    this_folder = os.path.dirname(os.path.abspath(__file__)) # získání cesty k tomuto souboru
    db_path = 'sensors.db'
    sensor_app = SensorDB(db_path)
    
    info = sensor_app.get_sensor_info_by_label('S-123-2', 1)
    print(info)
    
    sensor_app.close_connection()