# Musterlösung Level 1: Vigenère-Entschlüsselung & Slicing
# Autor: Stefan
#
# Das Framework ruft run(data) auf. data ist ein Dictionary, z.B.:
#   {"encrypted_log": "zuw.pdrfdd_yhs", "shift_key": "HACKER"}
# Rückgabe: der Dateiname, auf den der Angreifer zugegriffen hat.


def run(data):
    # --- Schritt 1: Eingabedaten aus dem Dictionary holen ---------------
    encrypted_log = data["encrypted_log"]
    shift_key = data["shift_key"].lower()     # "HACKER" -> "hacker"

    # Das Alphabet als String. Die Position eines Buchstabens darin
    # ist gleichzeitig seine "Verschiebung": a=0, b=1, c=2, ...
    alphabet = "abcdefghijklmnopqrstuvwxyz"

    # --- Schritt 2: Text Zeichen für Zeichen entschlüsseln --------------
    decrypted_log = ""
    key_position = 0                          # welcher Schlüsselbuchstabe ist dran?

    for char in encrypted_log:
        if char in alphabet:
            # Schlüsselbuchstaben bestimmen. Das % sorgt dafür, dass der
            # Schlüssel von vorne beginnt, wenn er aufgebraucht ist.
            key_char = shift_key[key_position % len(shift_key)]
            shift = alphabet.index(key_char)

            # Nach LINKS verschieben (= entschlüsseln). Das % 26 sorgt dafür,
            # dass man nach "a" wieder bei "z" landet (Kreis statt Linie).
            new_index = (alphabet.index(char) - shift) % 26
            decrypted_log = decrypted_log + alphabet[new_index]

            key_position = key_position + 1   # nächster Schlüsselbuchstabe
        else:
            # Sonderzeichen ('_' und '.') wurden nicht verschlüsselt
            decrypted_log = decrypted_log + char

    # --- Schritt 3: Der Text steht rückwärts -> per Slicing umdrehen ----
    log_file_path = decrypted_log[::-1]       # Schrittweite -1 = rückwärts lesen

    return log_file_path
