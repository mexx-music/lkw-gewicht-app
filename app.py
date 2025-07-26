import streamlit as st

# 🧠 Initialisierung des Kalibrier-Datenbereichs im Session State
if "kalibrierung" not in st.session_state:
    st.session_state["kalibrierung"] = {}

# 🚚 Eingabefeld für Kennzeichen
kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")

# 🧼 Fahrzeug-Daten sicherstellen
if kennzeichen not in st.session_state["kalibrierung"]:
    st.session_state["kalibrierung"][kennzeichen] = {}

truck_data = st.session_state["kalibrierung"][kennzeichen]

# 🔁 Reset-Funktion für Kalibrierung
if st.button("🔁 Kalibrierung zurücksetzen"):
    truck_data.clear()

# 🧰 Auswahl: Zugmaschine oder Auflieger
st.markdown("### 🛠️ Kalibrierung – Leer und Voll")
typ = st.selectbox("Typ auswählen", ["Zugmaschine (Antriebsachse)", "Auflieger"])

# 🔑 Schlüssel je nach Typ bestimmen
if typ == "Zugmaschine (Antriebsachse)":
    leer_key = "leer_real_antrieb"
    voll_key = "voll_real_antrieb"
else:
    leer_key = "leer_real_auflieger"
    voll_key = "voll_real_auflieger"

# 🧾 Eingabefelder mit Fallback (0 = Standard)
leer_wert = st.number_input(
    f"Waage leer ({typ}) in kg",
    value=truck_data.get(leer_key, 0)
)

voll_wert = st.number_input(
    f"Waage voll ({typ}) in kg",
    value=truck_data.get(voll_key, 0)
)

# 💾 Speichern der Eingaben im Session State
truck_data[leer_key] = leer_wert
truck_data[voll_key] = voll_wert

# 📊 Ausgabe: aktuelle Kalibrierwerte (immer sichtbar)
st.markdown("### 📋 Aktuelle Kalibrierung")
if truck_data:
    st.json(truck_data)
else:
    st.info("Noch keine Kalibrierung eingegeben.")
