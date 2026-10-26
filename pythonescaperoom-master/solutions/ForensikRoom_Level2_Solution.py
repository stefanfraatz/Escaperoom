# Musterlösung Level 2: CSV-Analyse & Log-Auswertung
# Autor: Stefan
#
# Das Framework ruft run(data) auf. data ist der Dateiname aus Level 1,
# also "log_journal.csv".
# Rückgabe: die Transaktions-ID der Zeile mit der höchsten Temperatur.

import csv    # Standardmodul zum Lesen von CSV-Dateien (Studienbrief 4.5.2)


def run(data):
    log_file_path = data

    # Hier merken wir uns den bisher "schlimmsten" Fund.
    # None heißt: noch nichts gefunden.
    max_temperature = None
    suspicious_transaction_id = None

    # --- Schritt 1: Datei öffnen ----------------------------------------
    # "with" schließt die Datei am Ende automatisch (Studienbrief 4.4.2).
    with open(log_file_path, "r", encoding="utf-8") as file:

        # DictReader macht aus jeder Zeile ein Dictionary. Die Schlüssel
        # kommen aus der Kopfzeile, z.B. row["Temperatur"] -> "71.3"
        reader = csv.DictReader(file)

        # --- Schritt 2: Alle Zeilen nacheinander prüfen -----------------
        for row in reader:

            # CSV liefert immer Text. Zum Vergleichen brauchen wir eine Zahl.
            # Zerstörte Werte wie "ERR" lassen sich nicht umwandeln und
            # lösen einen ValueError aus -> diese Zeile überspringen.
            try:
                temperature = float(row["Temperatur"])
            except ValueError:
                continue

            # --- Schritt 3: Ist das die bisher höchste Temperatur? ------
            if max_temperature is None or temperature > max_temperature:
                max_temperature = temperature
                suspicious_transaction_id = row["Transaktions_ID"]

    # --- Schritt 4: Ergebnis zurückgeben --------------------------------
    return suspicious_transaction_id
