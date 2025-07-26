import streamlit as st

# --- Session Setup ---
if "kalibrierung" not in st.session_state:
    st.session_state["kalibrierung"] = {}

# --- Kennzeichen-Eingabe ---
kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")

# --- Reset-Button ---
if st.button("🔁 Kalibrierung für dieses Fahrzeug zurücksetzen"):
    st.session_state["kalibrierung"][kennzeichen] = {}

# --- Datensatz für dieses Fahrzeug abrufen (oder neu anlegen) ---
truck_data = st.session_state["kalibrierung"].get(kennzeichen, {})

# --- Typ-Auswahl (Zugmaschine oder Auflieger) ---
st.markdown("### 🛠️ Kalibrierung – Leer und Voll")
typ = st.selectbox("Typ auswählen", ["Zugmaschine (Antriebsachse)", "Auflieger"])

# --- Variablennamen je nach Auswahl setzen ---
if typ == "Zugmaschine (Antriebsachse)":
    leer_key = "leer_real_antrieb"
    voll_key = "voll_real_antrieb"
else:
    leer_key = "leer_real_auflieger"
    voll_key = "voll_real_auflieger"

# --- Eingabefelder mit Fallback-Werten ---
leer_wert = st.number_input(
    f"Waage leer ({typ}) in kg",
    value=truck_data.get(leer_key, 0)
)

voll_wert = st.number_input(
    f"Waage voll ({typ}) in kg",
    value=truck_data.get(voll_key, 0)
)

# --- Daten speichern ---
truck_data[leer_key] = leer_wert
truck_data[voll_key] = voll_wert
st.session_state["kalibrierung"][kennzeichen] = truck_data

# --- Anzeige zur Kontrolle ---
st.success(f"Aktuelle Kalibrierung für {kennzeichen}:")
st.json(truck_data)
