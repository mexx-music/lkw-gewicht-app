import streamlit as st

# 🧠 Session-Setup für Kalibrierdaten
if "kalibrierung" not in st.session_state:
    st.session_state["kalibrierung"] = {}

# 🚚 Eingabe: Kennzeichen
kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")

# 🔁 Reset-Button
if st.button("🔁 Kalibrierung für dieses Fahrzeug zurücksetzen"):
    st.session_state["kalibrierung"][kennzeichen] = {}

# 📦 Daten abrufen oder leeres Dict anlegen
truck_data = st.session_state["kalibrierung"].get(kennzeichen, {})

# 🧰 Auswahl: Zugmaschine oder Auflieger
st.markdown("### 🛠️ Kalibrierung – Leer und Voll")
typ = st.selectbox("Typ auswählen", ["Zugmaschine (Antriebsachse)", "Auflieger"])

# 🏷️ Schlüssel für die Speicherung je nach Typ
if typ == "Zugmaschine (Antriebsachse)":
    leer_key = "leer_real_antrieb"
    voll_key = "voll_real_antrieb"
else:
    leer_key = "leer_real_auflieger"
    voll_key = "voll_real_auflieger"

# 📝 Eingabefelder (sicher mit .get())
leer_wert = st.number_input(
    f"Waage leer ({typ}) in kg",
    value=truck_data.get(leer_key, 0)
)

voll_wert = st.number_input(
    f"Waage voll ({typ}) in kg",
    value=truck_data.get(voll_key, 0)
)

# 💾 Speicherung der eingegebenen Werte
truck_data[leer_key] = leer_wert
truck_data[voll_key] = voll_wert
st.session_state["kalibrierung"][kennzeichen] = truck_data

# 📋 Anzeige der aktuellen Kalibrierung (nur wenn Daten vorhanden)
if truck_data:
    st.success(f"Aktuelle Kalibrierung für {kennzeichen}:")
    st.json(truck_data)
else:
    st.info("ℹ️ Noch keine Kalibrierung vorhanden. Bitte Werte eingeben.")
