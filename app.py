import streamlit as st
import json
import os

# 🔁 Lade bestehende Kalibrierdaten aus Datei (falls vorhanden)
KALIBRIERDATEI = "kalibrierung.json"
if os.path.exists(KALIBRIERDATEI):
    with open(KALIBRIERDATEI, "r") as f:
        kalibrierdaten = json.load(f)
else:
    kalibrierdaten = {}

# 🪪 Kennzeichen eingeben
kennzeichen = st.text_input("Kennzeichen eingeben", value="WL782GW")

# 🧠 Datenstruktur vorbereiten
if kennzeichen not in kalibrierdaten:
    kalibrierdaten[kennzeichen] = {
        "leer_antrieb": 0.0,
        "leer_auflieger": 0.0,
        "voll_antrieb": 0.0,
        "voll_auflieger": 0.0,
        "teil_antrieb": 0.0,
        "teil_auflieger": 0.0
    }

fahrzeug = kalibrierdaten[kennzeichen]

# 🧾 Eingabe der Kalibrierwerte – mit Fallback auf vorhandene oder 0.0
fahrzeug["leer_antrieb"] = st.number_input(
    "Volvo Anzeige leer (Zugmaschine)",
    value=fahrzeug.get("leer_antrieb", 0.0),
    help="Luftwert bei leerer Zugmaschine"
)

fahrzeug["leer_auflieger"] = st.number_input(
    "Volvo Anzeige leer (Auflieger)",
    value=fahrzeug.get("leer_auflieger", 0.0),
    help="Luftwert bei leerem Auflieger"
)

fahrzeug["voll_antrieb"] = st.number_input(
    "Volvo Anzeige voll beladen (Zugmaschine)",
    value=fahrzeug.get("voll_antrieb", 0.0),
    help="Luftwert bei maximaler Beladung – Zugmaschine"
)

fahrzeug["voll_auflieger"] = st.number_input(
    "Volvo Anzeige voll beladen (Auflieger)",
    value=fahrzeug.get("voll_auflieger", 0.0),
    help="Luftwert bei maximaler Beladung – Auflieger"
)

fahrzeug["teil_antrieb"] = st.number_input(
    "Volvo Anzeige teilbeladen (Zugmaschine)",
    value=fahrzeug.get("teil_antrieb", 0.0),
    help="Optional – bei Teilbeladung"
)

fahrzeug["teil_auflieger"] = st.number_input(
    "Volvo Anzeige teilbeladen (Auflieger)",
    value=fahrzeug.get("teil_auflieger", 0.0),
    help="Optional – bei Teilbeladung"
)

# 💾 Speichern-Button
if st.button("Kalibrierung speichern"):
    with open(KALIBRIERDATEI, "w") as f:
        json.dump(kalibrierdaten, f, indent=2)
    st.success(f"Kalibrierdaten für {kennzeichen} gespeichert.")
