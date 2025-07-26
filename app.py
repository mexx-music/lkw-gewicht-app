import streamlit as st

st.title("🚛 LKW Gewichtsanalyse")

# --- Eingabefeld für Kennzeichen ---
kennzeichen = st.text_input("Kennzeichen", value="W-12345")

st.header("⚙️ Kalibrierung")

# Hersteller-Schätzwerte (Leergewicht)
leer_volvo_antrieb = st.number_input("Volvo-Anzeige Antriebsachse (leer)", value=4.7)
leer_volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (leer)", value=6.6)

leer_real_zug = st.number_input("Reales Gewicht Zugmaschine (leer)", value=7.5)
leer_real_auflieger = st.number_input("Reales Gewicht Auflieger (leer)", value=8.5)

# Kalibrierung (Faktor)
faktor_antrieb = 1.0
faktor_auflieger = 1.0

if leer_volvo_antrieb > 0:
    faktor_antrieb = leer_real_zug / leer_volvo_antrieb

if leer_volvo_auflieger > 0:
    faktor_auflieger = leer_real_auflieger / leer_volvo_auflieger

st.write(f"🔧 Antriebsachsen-Faktor: {faktor_antrieb:.3f}")
st.write(f"🔧 Auflieger-Faktor: {faktor_auflieger:.3f}")

st.header("📊 Unterwegs-Daten")

# Aktuelle Volvo-Anzeige unterwegs
aktuell_volvo_antrieb = st.number_input("Volvo-Anzeige Antriebsachse (jetzt)", value=7.5)
aktuell_volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (jetzt)", value=20.0)

# Berechnung der realen Achsgewichte
real_zuggewicht = aktuell_volvo_antrieb * faktor_antrieb
real_aufliegergewicht = aktuell_volvo_auflieger * faktor_auflieger
real_gesamtgewicht = real_zuggewicht + real_aufliegergewicht

# Ausgabe
st.subheader("🧾 Ergebnis")
st.write(f"🚛 Realgewicht Zugmaschine (Antriebsachse): **{real_zuggewicht:.2f} t**")
st.write(f"🛻 Realgewicht Auflieger: **{real_aufliegergewicht:.2f} t**")
st.write(f"📦 Gesamtgewicht (geschätzt): **{real_gesamtgewicht:.2f} t**")

# Warnung bei Überladung
if real_zuggewicht > 11.5:
    st.error("⚠️ Achtung: Antriebsachse überladen! (> 11.5 t)")

# Kennzeichen-Info unten
if kennzeichen.strip():
    st.caption(f"Analyse für Fahrzeug: **{kennzeichen}**")
