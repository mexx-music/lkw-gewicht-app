
import streamlit as st

st.set_page_config(page_title="Volvo Gewichtsschätzung", layout="centered")

st.title("🚛 Volvo Gewichtsschätzung – Kalibrierte Version")
st.markdown("Gib die **Volvo-Anzeige**, **Tankfüllung** und optional die **Auflieger-Korrektur** ein.")

# Eingaben
volvo_zug = st.number_input("Volvo-Anzeige Zugmaschine (t)", min_value=0.0, max_value=40.0, value=11.3, step=0.1)
volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (t)", min_value=0.0, max_value=40.0, value=7.9, step=0.1)
tank_zug = st.slider("Tankfüllung Zugmaschine (%)", 0, 100, 60)
tank_kuehler = st.slider("Tankfüllung Kühlaggregat (%)", 0, 100, 80)
auflieger_korrektur = st.slider("Aufliegergewichtskorrektur (optional, kg)", -1000, 1000, 0, step=100)

# Kalibrierte Referenzwerte
volvo_zug_ref = 11.3
real_zug_ref = 14.5
volvo_auflieger_ref = 7.9
real_auflieger_ref = 8.4

# Tankdaten
tankvolumen_zug = 800  # Liter
tankvolumen_kuehler = 240  # Liter
diesel_dichte = 0.84  # kg/l

# Korrekturfaktoren
faktor_zug = real_zug_ref / volvo_zug_ref
faktor_auflieger = real_auflieger_ref / volvo_auflieger_ref

# Tankgewicht
tankgewicht_zug = (tank_zug / 100) * tankvolumen_zug * diesel_dichte / 1000
tankgewicht_kuehler = (tank_kuehler / 100) * tankvolumen_kuehler * diesel_dichte / 1000
tankgewicht_gesamt = tankgewicht_zug + tankgewicht_kuehler

# Berechnung
real_zug = volvo_zug * faktor_zug
real_auflieger = volvo_auflieger * faktor_auflieger + auflieger_korrektur / 1000
gesamtgewicht = real_zug + real_auflieger

# Tankkorrektur
ref_tankgewicht = (0.6 * tankvolumen_zug + 0.8 * tankvolumen_kuehler) * diesel_dichte / 1000
tankdifferenz = tankgewicht_gesamt - ref_tankgewicht
gesamtgewicht_korrigiert = gesamtgewicht + tankdifferenz

# Anzeige
st.subheader("📊 Ergebnis")
st.markdown(f"**Korrigiertes realistisches Gewicht:** `{gesamtgewicht_korrigiert:.2f} t`")
st.caption(f"(Enthält Tankkorrektur von {tankdifferenz:+.2f} t und Aufliegerkorrektur von {auflieger_korrektur:+} kg)")

with st.expander("Details"):
    st.write(f"Zugmaschine (korrigiert): {real_zug:.2f} t")
    st.write(f"Auflieger (korrigiert inkl. Offset): {real_auflieger:.2f} t")
    st.write(f"Tankgewicht gesamt: {tankgewicht_gesamt:.2f} t")
