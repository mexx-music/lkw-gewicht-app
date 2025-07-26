import streamlit as st

# 🧠 Setup: Session State
if "kalibrierung" not in st.session_state:
    st.session_state["kalibrierung"] = {}

# 🚚 Kennzeichen-Eingabe
kennzeichen = st.text_input("Kennzeichen eingeben", value="WL782GW")

# 📦 Neue Fahrzeuge mit Schätzwerten initialisieren
if kennzeichen not in st.session_state["kalibrierung"]:
    st.session_state["kalibrierung"][kennzeichen] = {
        "leer_real_antrieb": 4200,
        "voll_real_antrieb": 7100,
        "leer_real_auflieger": 6800,
        "voll_real_auflieger": 11500
    }

truck_data = st.session_state["kalibrierung"][kennzeichen]

# 🔁 Reset-Funktion
if st.button("🔁 Kalibrierung zurücksetzen"):
    truck_data["leer_real_antrieb"] = 4200
    truck_data["voll_real_antrieb"] = 7100
    truck_data["leer_real_auflieger"] = 6800
    truck_data["voll_real_auflieger"] = 11500
    st.success("Schätzwerte wurden zurückgesetzt.")

# 🧰 Auswahl: Zugmaschine oder Auflieger
st.markdown("### 🛠️ Kalibrierung – Leer und Voll")
typ = st.selectbox("Typ auswählen", ["Zugmaschine (Antriebsachse)", "Auflieger"])

# 🔑 Feldauswahl je nach Typ
if typ == "Zugmaschine (Antriebsachse)":
    leer_key = "leer_real_antrieb"
    voll_key = "voll_real_antrieb"
else:
    leer_key = "leer_real_auflieger"
    voll_key = "voll_real_auflieger"

# 📝 Eingabe der Werte mit bereits geladenem Standard
leer_wert = st.number_input(f"Waage leer ({typ}) in kg", value=truck_data.get(leer_key, 0), step=50)
voll_wert = st.number_input(f"Waage voll ({typ}) in kg", value=truck_data.get(voll_key, 0), step=50)

# 💾 Speichern
truck_data[leer_key] = leer_wert
truck_data[voll_key] = voll_wert

# 📋 Anzeige
st.markdown("### 📋 Aktuelle Kalibrierung")
st.json(truck_data)
