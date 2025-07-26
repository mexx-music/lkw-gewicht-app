import streamlit as st

# 🧠 Session-Setup
if "kalibrierung" not in st.session_state:
    st.session_state["kalibrierung"] = {}

# 🚚 Kennzeichen-Eingabe
kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")

# 📦 Fahrzeug-Daten initialisieren
if kennzeichen not in st.session_state["kalibrierung"]:
    st.session_state["kalibrierung"][kennzeichen] = {}

truck_data = st.session_state["kalibrierung"][kennzeichen]

# 🔁 Reset-Button
if st.button("🔁 Kalibrierung zurücksetzen"):
    truck_data.clear()

# 🧰 Auswahl: Zugmaschine oder Auflieger
st.markdown("### 🛠️ Kalibrierung – Leer und Voll")
typ = st.selectbox("Typ auswählen", ["Zugmaschine (Antriebsachse)", "Auflieger"])

# 🔑 Schlüssel bestimmen
if typ == "Zugmaschine (Antriebsachse)":
    leer_key = "leer_real_antrieb"
    voll_key = "voll_real_antrieb"
else:
    leer_key = "leer_real_auflieger"
    voll_key = "voll_real_auflieger"

# 📝 Eingaben holen (aktuelle Werte oder 0)
leer_wert = truck_data.get(leer_key, 0)
voll_wert = truck_data.get(voll_key, 0)

# 📥 Eingabefelder anzeigen
leer_wert = st.number_input(f"Waage leer ({typ}) in kg", value=leer_wert, step=10)
voll_wert = st.number_input(f"Waage voll ({typ}) in kg", value=voll_wert, step=10)

# 💾 Eingaben speichern
truck_data[leer_key] = leer_wert
truck_data[voll_key] = voll_wert
st.session_state["kalibrierung"][kennzeichen] = truck_data

# 📋 Anzeige
st.markdown("### 📋 Aktuelle Kalibrierung")
st.json(truck_data)
