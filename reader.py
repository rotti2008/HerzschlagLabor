import time
from datetime import datetime
from ky039 import KY039
import mysql.connector

# Datenbankverbindung
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="johannes",
        password="",
        database="HomeAutomationDB"
    )

# Daten in DB schreiben
def insert_herzfrequenz(cursor, bpm, avg):
    sql = "INSERT INTO herzfrequenz (timestamp, bpm, avg_value) VALUES (%s, %s, %s)"
    cursor.execute(sql, (datetime.now(), bpm, avg))

def main():
    # Sensor initialisieren
    try:
        sensor = KY039(channel=0)
    except Exception as e:
        print(f"Fehler beim Initialisieren des Sensors: {e}")
        return

    # DB verbinden
    try:
        db = connect_db()
        cursor = db.cursor()
        print("Datenbankverbindung erfolgreich!")
    except Exception as e:
        print(f"Fehler bei Datenbankverbindung: {e}")
        return

    last_save = time.time()

    try:
        while True:
            # Sensor schnell samplen
            sensor.read_bpm()

            now = time.time()
            if now - last_save >= 1.0:
                try:
                    bpm, avg = sensor.read_bpm()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] Avg: {avg:>6} | BPM: {bpm:>3}")

                    # In DB schreiben
                    insert_herzfrequenz(cursor, bpm, avg)
                    db.commit()

                    last_save = now

                except mysql.connector.Error as e:
                    print(f"Datenbankfehler: {e}")
                    db.rollback()

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\nProgramm beendet.")

    finally:
        cursor.close()
        db.close()
        print("Datenbankverbindung geschlossen.")

if __name__ == "__main__":
    main()
