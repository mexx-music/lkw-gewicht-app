import streamlit as st

st.set_page_config(page_title="LKW Achslast-Rechner", layout="centered")

st.title("🚛 LKW Achslast-Rechner")

st.markdown("## 🧮 Kalibrierung")

st.info("Bitte die Volvo-Anzeigen und echten Waagenwerte bei Leer- und Volllast eingeben – getrennt nach Zugmaschine und Auflieger.")

# Kalibrierung: Zugmaschine
st.subheader("Zugmaschine")

zug_leer_volvo = st.number_input("Volvo-Anzeige leer (Zugmaschine)", value=6.0)
zug_leer_waage = st.number_input("Echte Waage leer (Zugmaschine)", value=7.0)
zug_voll_volvo = st.number_input("Volvo-Anzeige voll (Zugmaschine)", value=10.0)
zug_voll_waage = st.number_input("Echte Waage voll (Zugmaschine)", value=12.0)

zug_faktor = (zug_voll_waage - zug_leer_waage) / (zug_voll_volvo - zug_leer_volvo) if zug_voll_volvo != zug_leer_volvo else 1.0

# Kalibrierung: Auflieger
st.subheader("Auflieger")

aufl_leer_volvo = st.number_input("Volvo-Anzeige leer (Auflieger)", value=6.0)
aufl_leer_waage = st.number_input("Echte Waage leer (Auflieger)", value=6.5)
aufl_voll_volvo = st.number_input("Volvo-Anzeige voll (Auflieger)", value=28.0)
aufl_voll_waage = st.number_input("Echte Waage voll (Auflieger)", value=29.5)

aufl_faktor = (aufl_voll_waage - aufl_leer_waage) / (aufl_voll_volvo - aufl_leer_volvo) if aufl_voll_volvo != aufl_leer_volvo else 1.0

st.markdown("---")
st.markdown("## 🚚 Gewicht unterwegs ermitteln")

aktuell_zug_volvo = st.number_input("Aktuelle Volvo-Anzeige (Zugmaschine)", value=9.0)
aktuell_aufl_volvo = st.number_input("Aktuelle Volvo-Anzeige (Auflieger)", value=27.0)

gewicht_zug = zug_leer_waage + (aktuell_zug_volvo - zug_leer_volvo) * zug_faktor
gewicht_aufl = aufl_leer_waage + (aktuell_aufl_volvo - aufl_leer_volvo) * aufl_faktor
gesamtgewicht = gewicht_zug + gewicht_aufl

st.success(f"**Zugmaschine:** {gewicht_zug:.2f} t")
st.success(f"**Auflieger:** {gewicht_aufl:.2f} t")
st.success(f"**Gesamtgewicht:** {gesamtgewicht:.2f} t")
