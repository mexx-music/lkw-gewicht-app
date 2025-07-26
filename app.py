import streamlit as st

st.title("🚛 LKW-Gewichtsanalyse (Kalibrierung + Schätzung)")

st.header("🔧 Kalibrierung mit realen Werten")

# Eingaben leerer Zustand (Volvo Anzeige + echte Waage)
leer_antriebsachse = st.number_input("Volvo-Anzeige (Antriebsachse, leer)", value=4.7)
leer_auflieger = st.number_input("Volvo-Anzeige (Auflieger gesamt, leer)", value=6.6)
leer_gesamt_real = st.number_input("Gesamtgewicht laut echter Waage (leer)", value=14.6)

# Automatisch berechnete Lenkachse (geschätzt)
leer_lenkachse = leer_gesamt_real - (leer_antriebsachse + leer_auflieger)
st.write(f"🔍 Geschätztes Gewicht Lenkachse: **{leer_lenkachse:.2f} t**")

# Eingaben voller Zustand (Volvo Anzeige + echte Waage)
st.header("🔧 Kalibrierung voll beladen")
voll_antriebsachse = st.number_input("Volvo-Anzeige (Antriebsachse, voll)", value=9.5)
voll_auflieger = st.number_input("Volvo-Anzeige (Auflieger gesamt, voll)", value=27.0)
voll_gesamt_real = st.number_input("Gesamtgewicht laut echter Waage (voll)", value=40.2)

# Kalibrierfaktor berechnen
anzeige_leer = leer_antriebsachse + leer_auflieger
anzeige_voll = voll_antriebsachse + voll_auflieger

if anzeige_voll != anzeige_leer:
    faktor = (voll_gesamt_real - leer_gesamt_real) / (anzeige_voll - anzeige_leer)
else:
    faktor = 1.0

st.success(f"📐 Automatisch berechneter Kalibrierfaktor: **{faktor:.3f}**")

# Aktuelle Messung unterwegs
st.header("🚚 Unterwegs-Gewicht berechnen")
aktuell_antriebsachse = st.number_input("Aktuelle Volvo-Anzeige Antriebsachse", value=7.5)
aktuell_auflieger = st.number_input("Aktuelle Volvo-Anzeige Auflieger gesamt", value=20.0)

aktuell_gesamt = leer_gesamt_real + faktor * ((aktuell_antriebsachse + aktuell_auflieger) - anzeige_leer)

st.info(f"📊 Geschätztes aktuelles Gesamtgewicht: **{aktuell_gesamt:.2f} t**")

# Warnung bei Antriebsachse über 11.5 t (je nach Land)
grenze = 11.5
if aktuell_antriebsachse * faktor > grenze:
    st.error(f"⚠️ ACHTUNG: Antriebsachse über {grenze} t! ({aktuell_antriebsachse * faktor:.2f} t)")

# Optional: Kennzeichen eingeben
kennzeichen = st.text_input("Kennzeichen (optional)")
if kennzeichen:
    st.write(f"📌 Fahrzeugkennung: **{kennzeichen}**")
