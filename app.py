import streamlit as st

st.title("🚛 LKW Gewichtsanalyse")

st.header("🛠️ Kalibrierung")

kennzeichen = st.text_input("Kennzeichen (optional)", placeholder="z. B. W123XYZ")

# Eingaben für Leergewicht
st.subheader("🔹 Leerfahrt")
leer_volvo_tractor = st.number_input("Volvo-Anzeige Zugmaschine (leer)", value=4.7)
leer_volvo_trailer = st.number_input("Volvo-Anzeige Auflieger (leer)", value=6.6)
leer_waage_tractor = st.number_input("Tatsächliches Gewicht Zugmaschine (leer)", value=5.1)
leer_waage_trailer = st.number_input("Tatsächliches Gewicht Auflieger (leer)", value=7.1)

# Eingaben für Volllast
st.subheader("🔸 Volllast")
voll_volvo_tractor = st.number_input("Volvo-Anzeige Zugmaschine (voll)", value=12.1)
voll_volvo_trailer = st.number_input("Volvo-Anzeige Auflieger (voll)", value=19.7)
voll_waage_tractor = st.number_input("Tatsächliches Gewicht Zugmaschine (voll)", value=12.9)
voll_waage_trailer = st.number_input("Tatsächliches Gewicht Auflieger (voll)", value=20.6)

# Berechnung Korrekturfaktor
try:
    faktor_tractor = (voll_waage_tractor - leer_waage_tractor) / (voll_volvo_tractor - leer_volvo_tractor)
    faktor_trailer = (voll_waage_trailer - leer_waage_trailer) / (voll_volvo_trailer - leer_volvo_trailer)
except ZeroDivisionError:
    faktor_tractor = 1.0
    faktor_trailer = 1.0

st.write(f"🔧 Korrekturfaktor Zugmaschine: `{faktor_tractor:.3f}`")
st.write(f"🔧 Korrekturfaktor Auflieger: `{faktor_trailer:.3f}`")

st.header("📊 Unterwegs-Kontrolle")

aktuell_volvo_tractor = st.number_input("Aktuelle Volvo-Anzeige Zugmaschine", value=10.0)
aktuell_volvo_trailer = st.number_input("Aktuelle Volvo-Anzeige Auflieger", value=18.0)

# Berechnung aktuelles Gewicht
gewicht_tractor = (aktuell_volvo_tractor - leer_volvo_tractor) * faktor_tractor + leer_waage_tractor
gewicht_trailer = (aktuell_volvo_trailer - leer_volvo_trailer) * faktor_trailer + leer_waage_trailer
gesamtgewicht = gewicht_tractor + gewicht_trailer

st.success(f"✅ Geschätztes Gewicht Zugmaschine: **{gewicht_tractor:.2f} t**")
st.success(f"✅ Geschätztes Gewicht Auflieger: **{gewicht_trailer:.2f} t**")
st.markdown(f"### 🔽 **Gesamtgewicht:** `{gesamtgewicht:.2f} t`")

if kennzeichen:
    st.markdown(f"🚚 Fahrzeug: **{kennzeichen}**")
