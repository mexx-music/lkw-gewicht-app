import streamlit as st

st.set_page_config(page_title="LKW-Gewichtsanalyse", page_icon="🚛")
st.title("🚛 LKW-Gewichtsanalyse – Kalibrierung & Live-Berechnung")

st.markdown("Diese App berechnet dein **Gesamtgewicht** unterwegs auf Basis der Volvo-Anzeige – nach einmaliger Kalibrierung mit realer Waage.")

# Abschnitt 1: Kalibrierung (einmalig)
st.header("1️⃣ Kalibrierung mit echter Waage")

st.subheader("📍 Leerfahrt")
leer_antrieb_volvo = st.number_input("Volvo-Anzeige Antriebsachse (leer)", value=4.7)
leer_auflieger_volvo = st.number_input("Volvo-Anzeige Auflieger (leer)", value=6.6)
leer_waage_zug = st.number_input("Reale Waage – Zugmaschine leer", value=7.8)
leer_waage_auflieger = st.number_input("Reale Waage – Auflieger leer", value=6.8)

st.subheader("📍 Vollladung")
voll_antrieb_volvo = st.number_input("Volvo-Anzeige Antriebsachse (voll)", value=9.5)
voll_auflieger_volvo = st.number_input("Volvo-Anzeige Auflieger (voll)", value=27.0)
voll_waage_zug = st.number_input("Reale Waage – Zugmaschine voll", value=9.9)
voll_waage_auflieger = st.number_input("Reale Waage – Auflieger voll", value=30.3)

# Korrekturfaktor berechnen
delta_antrieb_volvo = voll_antrieb_volvo - leer_antrieb_volvo
delta_antrieb_waage = voll_waage_zug - leer_waage_zug
faktor_antrieb = delta_antrieb_waage / delta_antrieb_volvo if delta_antrieb_volvo else 1.0

delta_auflieger_volvo = voll_auflieger_volvo - leer_auflieger_volvo
delta_auflieger_waage = voll_waage_auflieger - leer_waage_auflieger
faktor_auflieger = delta_auflieger_waage / delta_auflieger_volvo if delta_auflieger_volvo else 1.0

st.success(f"✅ Faktor Antriebsachse: {faktor_antrieb:.3f}")
st.success(f"✅ Faktor Auflieger: {faktor_auflieger:.3f}")

# Abschnitt 2: Unterwegs (Echtzeit-Berechnung nur mit Volvo-Werten)
st.header("2️⃣ Unterwegs – Volvo-Anzeige eingeben")

aktuell_antrieb_volvo = st.number_input("Volvo-Anzeige Antriebsachse (jetzt)", value=7.5)
aktuell_auflieger_volvo = st.number_input("Volvo-Anzeige Auflieger (jetzt)", value=20.0)

# Berechnung basierend auf Kalibrierung
real_zuggewicht = leer_waage_zug + faktor_antrieb * (aktuell_antrieb_volvo - leer_antrieb_volvo)
real_aufliegergewicht = leer_waage_auflieger + faktor_auflieger * (aktuell_auflieger_volvo - leer_auflieger_volvo)
real_gesamtgewicht = real_zuggewicht + real_aufliegerweight

# Ergebnisdarstellung
st.subheader("📊 Ergebnis")
st.info(f"Zugmaschine (berechnet): **{real_zuggewicht:.2f} t**")
st.info(f"Auflieger (berechnet): **{real_aufliegergewicht:.2f} t**")
st.success(f"Gesamtgewicht: **{real_gesamtgewicht:.2f} t**")

# Warnung bei Überladung Antriebsachse
if real_zuggewicht > 11.5:
    st.error(f"⚠️ ANTRIEBSACHSE ÜBERLADEN! ({real_zuggewicht:.2f} t)")

# Optional: Kennzeichen
kennzeichen = st.text_input("Kennzeichen (optional)")
if kennzeichen:
    st.caption(f"📌 Fahrzeug: **{kennzeichen}**")
