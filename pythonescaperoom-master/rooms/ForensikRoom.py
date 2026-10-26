import csv
import random
from EscapeRoom import EscapeRoom


class ForensikRoom(EscapeRoom):
    """
    Escape Room "Incident Response im IT-Forensik-Labor".

    Das Servernetzwerk des Forensik-Labors wurde angegriffen. Der Spieler
    folgt Schritt für Schritt den Spuren des Angreifers. Die Lösung eines
    Levels ist jeweils der Input (data) für das nächste Level.

    Level 1 + 2: Stefan
    Level 3 + 4: Nina    (werden später hier ergänzt)
    Level 5 + 6: Jannik  (werden später hier ergänzt)
    """

    # Buchstaben, mit denen bei der Verschlüsselung gerechnet wird
    ALPHABET = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self):
        super().__init__()
        self.set_metadata("Stefan, Nina, Jannik", __name__)

        # WICHTIG: Levels OHNE Klammern übergeben (create_level1 statt
        # create_level1()). Dann wird ein Level erst gebaut, wenn der Spieler
        # dort ankommt - nur so ist die Lösung des vorherigen Levels
        # über get_last_solution() schon bekannt.
        self.add_level(self.create_level1)
        self.add_level(self.create_level2)
        # self.add_level(self.create_level3)   # Nina
        # self.add_level(self.create_level4)   # Nina
        # self.add_level(self.create_level5)   # Jannik
        # self.add_level(self.create_level6)   # Jannik

    # ==================================================================
    # LEVEL 1 (Stefan, mittelschwer): Vigenère-Entschlüsselung & Slicing
    # Lernziel: Strings, Schleifen, Indizes, Modulo, Slicing [::-1]
    # ==================================================================

    def create_level1(self):
        # Der Schlüssel wird bei jedem Spiel zufällig gewählt, damit sich der
        # Geheimtext ändert und man die Lösung nicht einfach abschreiben kann.
        shift_key = random.choice(["SPUR", "HACKER", "FORENSIK", "ANGRIFF"])

        # Der Angreifer hat den Dateipfad erst umgedreht und dann verschlüsselt.
        log_file_path = "log_journal.csv"
        reversed_path = log_file_path[::-1]                 # "vsc.lanruoj_gol"
        encrypted_log = self.vigenere(reversed_path, shift_key, 1)

        secret = {"encrypted_log": encrypted_log, "shift_key": shift_key}

        task_messages = [
            "Montagmorgen, 06:12 Uhr. Im IT-Forensik-Labor blinken alle Monitore rot: "
            "Das Servernetzwerk wurde angegriffen!",
            "Im System-Log findest du einen einzigen Eintrag, den der Angreifer "
            "vergessen hat zu löschen:",
            "<b>" + encrypted_log + "</b>",
            "Auf einem Post-it am Monitor des Angreifers steht das Wort <b>" + shift_key + "</b>.",
            "Der Eintrag ist mit der <b>Vigenère-Chiffre</b> verschlüsselt. Finde heraus, "
            "auf welche Datei der Angreifer zugegriffen hat.",
            "Schreibe eine Methode <code>run(data)</code>. <code>data</code> ist ein Dictionary "
            "mit den Schlüsseln <code>'encrypted_log'</code> und <code>'shift_key'</code>. "
            "Gib den Dateinamen als String zurück."
        ]
        hints = [
            "Vigenère ist ein Caesar mit wechselnder Verschiebung: Jeder Buchstabe des "
            "Schlüssels gibt eine eigene Verschiebung an (A=0, B=1, C=2, ...). "
            "Der Schlüssel wird so oft wie nötig wiederholt.",
            "Zeichen wie '_' und '.' sind nicht verschlüsselt und verbrauchen auch "
            "keinen Schlüsselbuchstaben.",
            "Zum Entschlüsseln wird zurück (also nach links) verschoben. "
            "Der Modulo-Operator % hilft, wenn man vor dem 'a' landet.",
            "Der entschlüsselte Text sieht noch komisch aus? Lies ihn mal rückwärts ... (Slicing!)"
        ]
        return {"task_messages": task_messages, "hints": hints,
                "solution_function": self.solve_level1, "data": secret}

    # ==================================================================
    # LEVEL 2 (Stefan, komplex): CSV-Datei auswerten
    # Lernziel: Dateihandling, csv.DictReader, Typkonvertierung,
    #           Exception Handling, Maximum per Schleife bestimmen
    # ==================================================================

    def create_level2(self):
        # Lösung aus Level 1 = Dateiname. Falls Level 2 einzeln getestet
        # wird (keine Vorlösung vorhanden), nehmen wir den bekannten Namen.
        log_file_path = self.get_last_solution() or "log_journal.csv"

        # Die CSV-Datei wird erst jetzt erzeugt (mit Zufallswerten).
        self.write_log_file(log_file_path)

        task_messages = [
            "Volltreffer! Der Angreifer hat die Datei <b>" + log_file_path + "</b> manipuliert.",
            "Sie liegt im Hauptordner des Escape Rooms. Sie enthält die Messwerte "
            "aller Server während des Angriffs: Zeitstempel, Server, Transaktions-ID und Temperatur.",
            "Der Angriff hat eine Transaktion ausgelöst, die einen Server extrem "
            "überhitzt hat. Finde die <b>Transaktions-ID der Zeile mit der höchsten Temperatur</b>.",
            "Vorsicht: Der Angreifer hat einige Messwerte zerstört - dort steht "
            "statt einer Zahl nur Datenmüll.",
            "Schreibe eine Methode <code>run(data)</code>. <code>data</code> enthält den "
            "Dateinamen. Gib die verdächtige Transaktions-ID als String zurück."
        ]
        hints = [
            "Öffne die Datei mit dem with-Statement und lies sie mit csv.DictReader. "
            "Jede Zeile wird dann zu einem Dictionary.",
            "Alles, was aus einer CSV-Datei kommt, ist ein String. Für einen Zahlenvergleich "
            "musst du die Temperatur mit float() umwandeln.",
            "float('ERR') erzeugt einen ValueError. Fange ihn mit try/except ab und "
            "überspringe die Zeile mit continue.",
            "Merke dir in einer Schleife die bisher höchste Temperatur und die dazugehörige ID."
        ]
        return {"task_messages": task_messages, "hints": hints,
                "solution_function": self.solve_level2, "data": log_file_path}

    # ==================================================================
    # HILFSFUNKTIONEN (nur für den Bau der Levels)
    # ==================================================================

    def vigenere(self, text, shift_key, direction):
        """
        Ver- oder entschlüsselt einen Text mit der Vigenère-Chiffre.
        direction = +1 -> verschlüsseln (nach rechts schieben)
        direction = -1 -> entschlüsseln (nach links schieben)
        """
        result = ""
        key_position = 0                       # welcher Schlüsselbuchstabe ist dran?
        for char in text:
            if char in self.ALPHABET:
                key_char = shift_key[key_position % len(shift_key)].lower()
                shift = self.ALPHABET.index(key_char)
                new_index = (self.ALPHABET.index(char) + direction * shift) % 26
                result = result + self.ALPHABET[new_index]
                key_position = key_position + 1
            else:
                result = result + char         # '_' und '.' bleiben, wie sie sind
        return result

    def write_log_file(self, file_name):
        """Erzeugt die CSV-Datei mit Server-Messwerten."""
        servers = ["srv-web-01", "srv-db-02", "srv-mail-03", "srv-backup-04"]
        rows = []

        # 15 normale Zeilen mit unauffälligen Temperaturen (40 - 75 °C)
        for i in range(15):
            rows.append([
                "2026-10-19 03:" + str(10 + i * 2) + ":00",
                random.choice(servers),
                "TX_" + str(random.randint(1000, 9899)) + "_STD",
                str(round(random.uniform(40.0, 75.0), 1))
            ])

        # 3 zerstörte Messwerte (Stolperfalle für den Spieler)
        for i in range(3):
            rows.insert(random.randint(0, len(rows)), [
                "2026-10-19 03:5" + str(i) + ":00",
                random.choice(servers),
                "TX_" + str(random.randint(1000, 9899)) + "_ERR",
                random.choice(["ERR", "n/a", "#####"])
            ])

        # Die verdächtige Zeile wird an einer zufälligen Stelle versteckt.
        # Die ID ist fest, weil Level 3 (Nina) genau mit ihr weiterarbeitet.
        rows.insert(random.randint(0, len(rows)),
                    ["2026-10-19 03:33:07", "srv-db-02", "TX_9942_SEC", "88.5"])

        with open(file_name, "w", encoding="utf-8") as file:
            file.write("Zeitstempel,Server,Transaktions_ID,Temperatur\n")
            for row in rows:
                file.write(",".join(row) + "\n")

    # ==================================================================
    # MUSTERLÖSUNGEN (damit prüft das Framework die Lösung des Spielers)
    # ==================================================================

    def solve_level1(self, data):
        decrypted_log = self.vigenere(data["encrypted_log"], data["shift_key"], -1)
        log_file_path = decrypted_log[::-1]
        return log_file_path

    def solve_level2(self, log_file_path):
        max_temperature = None
        suspicious_transaction_id = None
        with open(log_file_path, "r", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                try:
                    temperature = float(row["Temperatur"])
                except ValueError:
                    continue
                if max_temperature is None or temperature > max_temperature:
                    max_temperature = temperature
                    suspicious_transaction_id = row["Transaktions_ID"]
        return suspicious_transaction_id
