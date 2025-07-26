import streamlit as st

st.set_page_config(page_title="Volvo Gewicht (einfach)", layout="centered")

st.title("🚛 Volvo Gewichtsschätzung – Einfach & Kalibriert")

# Optionales Kennzeichen
kennzeichen = st.text_input("Kennzeichen (optional)", "")

# Eingabe Volvo-Werte
volvo_zug = st.number_input("Volvo-Anzeige Zugmaschine (t)", min_value=0.0, max_value=40.0, value=11.3, step=0.1)
volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (t)", min_value=0.0, max_value=40.0, value=7.9, step=0.1)

# Kalibrierung (fest gespeichert)
volvo_zug_ref = 11.3
real_zug_ref = 14.5
volvo_auflieger_ref = 7.9
real_auflieger_ref = 8.4

# Berechnung der Korrekturfaktoren
faktor_zug = real_zug_ref / volvo_zug_ref
faktor_auflieger = real_auflieger_ref / volvo_auflieger_ref

# Berechnung realer Gewichte
real_zug = volvo_zug * faktor_zug
real_auflieger = volvo_auflieger * faktor_auflieger
gesamtgewicht = real_zug + real_auflieger

# Ausgabe
st.subheader("📊 Ergebnis")
st.markdown(f"**Reales Gesamtgewicht (korrigiert):** `{gesamtgewicht:.2f} t`")

if kennzeichen:
    st.caption(f"Fahrzeug: **{kennzeichen.upper()}**")

with st.expander("Details"):
    st.write(f"Zugmaschine (korrigiert): {real_zug:.2f} t")
    st.write(f"Auflieger (korrigiert): {real_auflieger:.2f} t")
    st.write("Kalibrierung basiert auf Werksvergleich (echte Waage vs. Volvo-Anzeige).")
