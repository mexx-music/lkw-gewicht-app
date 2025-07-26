import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Kalibrierung", page_icon="🚛")

st.title("🚛 LKW Gewichtsanalyse mit Kalibrierung")
DATEIPFAD = "kalibrierung.json"

def lade_kalibrierung():
    if os.path.exists(DATEIPFAD):
        with open(DATEIPFAD, "r") as f:
            return json.load(f)
    return {}

def speichere_kalibrierung(daten):
    with open(DATEIPFAD, "w") as f:
        json.dump(daten, f)

# Schritt 1: Kennzeichen eingeben
kennzeichen = st.text_input("Kennzeichen eingeben:", value="W-12345")

if not kennzeichen.strip():
    st.warning("Bitte ein gültiges Kennzeichen eingeben.")
    st.stop()

# Schritt 2: Daten laden (falls vorhanden)
kalibrierungen = lade_kalibrierung()
vorhanden = kalibrierungen.get(kennzeichen)

st.header("⚙️ Kalibrierung")

if vorhanden:
    st.success(f"Kalibrierung für {kennzeichen} gefunden.")
    leer_volvo_antrieb = st.number_input("Volvo-Anzeige Antriebsachse (leer)", value=vorhanden["leer_volvo_antrieb"])
    leer_volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (leer)", value=vorhanden["leer_volvo_auflieger"])
    leer_real_zug = st.number_input("Reales Gewicht Zugmaschine (leer)", value=vorhanden["leer_real_zug"])
    leer_real_auflieger = st.number_input("Reales Gewicht Auflieger (leer)", value=vorhanden["leer_real_auflieger"])
else:
    st.info("Noch keine Kalibrierung für dieses Fahrzeug gespeichert.")
    leer_volvo_antrieb = st.number_input("Volvo-Anzeige Antriebsachse (leer)", value=4.7)
    leer_volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (leer)", value=6.6)
    leer_real_zug = st.number_input("Reales Gewicht Zugmaschine (leer)", value=7.5)
    leer_real_auflieger = st.number_input("Reales Gewicht Auflieger (leer)", value=8.5)

    if st.button("✅ Kalibrierung speichern"):
        kalibrierungen[kennzeichen] = {
            "leer_volvo_antrieb": leer_volvo_antrieb,
            "leer_volvo_auflieger": leer_volvo_auflieger,
            "leer_real_zug": leer_real_zug,
            "leer_real_auflieger": leer_real_auflieger
        }
        speichere_kalibrierung(kalibrierungen)
        st.success("Kalibrierung gespeichert!")

# Berechne Korrekturfaktoren
faktor_antrieb = leer_real_zug / leer_volvo_antrieb if leer_volvo_antrieb else 1.0
faktor_auflieger = leer_real_auflieger / leer_volvo_auflieger if leer_volvo_auflieger else 1.0

st.header("📊 Aktuelle Volvo-Anzeige eingeben")
aktuell_volvo_antrieb = st.number_input("Volvo-Anzeige Antriebsachse (jetzt)", value=7.5)
aktuell_volvo_auflieger = st.number_input("Volvo-Anzeige Auflieger (jetzt)", value=20.0)

# Berechnung
real_zuggewicht = aktuell_volvo_antrieb * faktor_antrieb
real_aufliegergewicht = aktuell_volvo_auflieger * faktor_auflieger
real_gesamtgewicht = real_zuggewicht + real_aufliegergewicht

st.subheader("🧾 Ergebnis")
st.write(f"🚛 Zugmaschine (geschätzt): **{real_zuggewicht:.2f} t**")
st.write(f"🛻 Auflieger (geschätzt): **{real_aufliegergewicht:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamtgewicht:.2f} t**")

if real_zuggewicht > 11.5:
    st.error("⚠️ Antriebsachse überladen! (> 11.5 t)")

st.caption("Alle Werte sind Näherungen auf Basis deiner Kalibrierung.")
