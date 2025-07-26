import streamlit as st

st.set_page_config(page_title="LKW-Gewichtsanalyse", page_icon="🚛")
st.title("🚛 LKW-Gewichtsanalyse – Kalibriert & Echtzeit")

st.header("🧪 Kalibrierung mit Herstellerschätzung")

# Herstellerschätzwerte als Default
leer_antrieb_volvo = st.number_input("Volvo-Anzeige Antriebsachse (leer)", value=4.7)
leer_auflieger_volvo = st.number_input("Volvo-Anzeige Auflieger (leer)", value=6.6)
leer_waage_zug = st.number_input("Zugmaschine: echte Waage (leer)", value=7.8)
leer_waage_auflieger = st.number_input("Auflieger: echte Waage (leer)", value=6.8)

voll_antrieb_volvo = st.number_input("Volvo-Anzeige Antriebsachse (voll)", value=9.5)
voll_auflieger_volvo = st.number_input("Volvo-Anzeige Auflieger (voll)", value=27.0)
voll_waage_zug = st.number_input("Zugmaschine: echte Waage (voll)", value=9.9)
voll_waage_auflieger = st.number_input("Auflieger: echte Waage (voll)", value=30.3)

# Korrekturfaktoren berechnen
delta_antrieb_volvo = voll_antrieb_volvo - leer_antrieb_volvo
delta_antrieb_waage = voll_waage_zug - leer_waage_zug
faktor_antrieb = delta_antrieb_waage / delta_antrieb_volvo if delta_antrieb_volvo else 1.0

delta_auflieger_volvo = voll_auflieger_volvo - leer_auflieger_volvo
delta_auflieger_waage = voll_waage_auflieger - leer_waage_auflieger
faktor_auflieger = delta_auflieger_waage / delta_auflieger_volvo if delta_auflieger_volvo else 1.0

st.success(f"📐 Faktor Antriebsachse: **{faktor_antrieb:.3f}**")
st.success(f"📐 Faktor Auflieger: **{faktor_auflieger:.3f}**")

# Eingabe unterwegs
st.header("🚚 Unterwegs-Wiegung")

aktuell_antrieb_volvo = st.number_input("Aktuelle Antriebsachse (Volvo)", value=7.5)
aktuell_auflieger_volvo = st.number_input("Aktuelle Auflieger (Volvo)", value=20.0)

real_zuggewicht = leer_waage_zug + faktor_antrieb * (aktuell_antrieb_volvo - leer_antrieb_volvo)
real_aufliegergewicht = leer_waage_auflieger + faktor_auflieger * (aktuell_auflieger_volvo - leer_auflieger_volvo)
real_gesamt = real_zuggewicht + real_aufliegergewicht

st.info(f"📊 Zugmaschine real: **{real_zuggewicht:.2f} t**")
st.info(f"📊 Auflieger real: **{real_aufliegergewicht:.2f} t**")
st.success(f"📦 Gesamtgewicht real: **{real_gesamt:.2f} t**")

# Warnung bei Antriebsachse > 11.5 t
if real_zuggewicht > 11.5:
    st.error(f"⚠️ ANTRIEBSACHSE ÜBERLADEN! ({real_zuggewicht:.2f} t)")

# Kennzeichen (optional)
kennzeichen = st.text_input("Kennzeichen (optional)")
if kennzeichen:
    st.write(f"📌 Fahrzeug: **{kennzeichen}**")
