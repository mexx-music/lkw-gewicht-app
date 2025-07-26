import streamlit as st

st.title("🚛 LKW Gewichtsanalyse")

st.header("🔧 Kalibrierung (echte Waage & Volvo-Anzeige)")
kennzeichen = st.text_input("Kennzeichen (optional)", "")

leer_volvo = st.number_input("Volvo-Anzeige Zugmaschine (leer)", value=12.0)
leer_waage_zug = st.number_input("Tatsächliches Gewicht Zugmaschine (leer)", value=13.2)
leer_waage_sattel = st.number_input("Tatsächliches Gewicht Auflieger (leer)", value=6.6)

voll_volvo = st.number_input("Volvo-Anzeige Zugmaschine (beladen)", value=40.0)
voll_waage_zug = st.number_input("Tatsächliches Gewicht Zugmaschine (beladen)", value=17.5)
voll_waage_sattel = st.number_input("Tatsächliches Gewicht Auflieger (beladen)", value=24.0)

if voll_volvo != leer_volvo:
    faktor = (voll_waage_zug + voll_waage_sattel - leer_waage_zug - leer_waage_sattel) / (voll_volvo - leer_volvo)
else:
    faktor = 1.0

st.write(f"⚙️ Automatisch berechneter Korrekturfaktor: `{faktor:.3f}`")

st.header("📊 Unterwegs-Kontrolle")

volvo_antriebsachse = st.number_input("Volvo-Anzeige: Antriebsachse (Zug)", value=10.8)
volvo_trailerachsen = st.number_input("Volvo-Anzeige: Aufliegerachsen gesamt", value=21.0)

volvo_summe = volvo_antriebsachse + volvo_trailerachsen
gewicht_gesamt = (volvo_summe - leer_volvo) * faktor + leer_waage_zug + leer_waage_sattel
gewicht_gesamt = round(gewicht_gesamt, 2)

st.success(f"✅ Geschätztes Gesamtgewicht: **{gewicht_gesamt:.2f} t**")

# Antriebsachse prüfen
if volvo_antriebsachse > 11.5:
    st.error("❗ Antriebsachslast überschritten (max. 11.5 t)")
else:
    st.info("✅ Antriebsachse im grünen Bereich (max. 11.5 t)")

st.caption("ℹ️ Die Lenkachse wird im Volvo-Display **nicht** mit Zahlen angezeigt – nur optischer Balken.")
