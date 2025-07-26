import streamlit as st

st.set_page_config(page_title="Volvo Gewicht mit Kalibrierung", layout="centered")

st.title("🚛 Volvo Gewicht – mit Kalibrierung & Verbundwaage")

with st.expander("ℹ️ Info zur Kalibrierung"):
    st.markdown("""
    **So funktioniert’s:**

    1. Fahren Sie **leer** auf eine Verbundwaage:
       - Zugmaschine separat wiegen
       - Auflieger separat wiegen
    2. Notieren Sie gleichzeitig die **Volvo-Anzeige** (Zug & Auflieger)
    3. Tragen Sie die Werte unten ein – die App berechnet automatisch Korrekturfaktoren.
    4. Unterwegs reicht dann die Volvo-Anzeige allein, um das reale Gewicht zuverlässig zu bestimmen.

    

st.markdown("### Schritt 1: Kalibrierung (einmalig eingeben)")
col1, col2 = st.columns(2)
with col1:
    volvo_zug_leer = st.number_input("Volvo-Anzeige Zugmaschine leer (t)", 0.0, 40.0, 11.3, 0.1)
    real_zug_leer = st.number_input("Reale Waage Zugmaschine leer (t)", 0.0, 40.0, 14.5, 0.1)
with col2:
    volvo_auflieger_leer = st.number_input("Volvo-Anzeige Auflieger leer (t)", 0.0, 40.0, 7.9, 0.1)
    real_auflieger_leer = st.number_input("Reale Waage Auflieger leer (t)", 0.0, 40.0, 8.4, 0.1)

st.markdown("### Schritt 2: Volvo-Anzeige unterwegs")
kennzeichen = st.text_input("Kennzeichen (optional)", "")
volvo_zug_aktuell = st.number_input("Aktuelle Volvo-Zugmaschine (t)", 0.0, 40.0, 12.0, 0.1)
volvo_auflieger_aktuell = st.number_input("Aktueller Volvo-Auflieger (t)", 0.0, 40.0, 24.0, 0.1)

# Korrekturfaktoren berechnen
faktor_zug = real_zug_leer / volvo_zug_leer if volvo_zug_leer > 0 else 1.0
faktor_auflieger = real_auflieger_leer / volvo_auflieger_leer if volvo_auflieger_leer > 0 else 1.0

# Korrigierte Werte
real_zug = volvo_zug_aktuell * faktor_zug
real_auflieger = volvo_auflieger_aktuell * faktor_auflieger
gesamtgewicht = real_zug + real_auflieger

st.subheader("📊 Ergebnis")
st.markdown(f"**Korrigiertes Gewicht (geschätzt):** `{gesamtgewicht:.2f} t`")

if kennzeichen:
    st.caption(f"Fahrzeug: **{kennzeichen.upper()}**")

with st.expander("Details"):
    st.write(f"Zugmaschine (korrigiert): {real_zug:.2f} t")
    st.write(f"Auflieger (korrigiert): {real_auflieger:.2f} t")
    st.write(f"Faktor Zugmaschine: {faktor_zug:.3f}")
    st.write(f"Faktor Auflieger: {faktor_auflieger:.3f}")
