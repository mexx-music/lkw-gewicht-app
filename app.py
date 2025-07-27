import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

# Startwerte – geschätzt
default_values = {
    "leer_volvo_antrieb": 4.7,
    "leer_real_antrieb": 7.5,
    "mittel_volvo_antrieb": 6.5,
    "mittel_real_antrieb": 9.4,
    "voll_volvo_antrieb": 7.9,
    "voll_real_antrieb": 11.3,
    "leer_volvo_auflieger": 6.6,
    "leer_real_auflieger": 8.5,
    "mittel_volvo_auflieger": 12.0,
    "mittel_real_auflieger": 18.0,
    "voll_volvo_auflieger": 19.0,
    "voll_real_auflieger": 27.5
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f)

def lineare_interpolation(volvo_wert, kalibrierung):
    (v1, r1), (v2, r2), (v3, r3) = kalibrierung
    if volvo_wert <= v1:
        return r1
    elif volvo_wert <= v2:
        return r1 + (r2 - r1) * (volvo_wert - v1) / (v2 - v1)
    else:
        return r2 + (r3 - r2) * (volvo_wert - v2) / (v3 - v2)

kennzeichen = st.text_input("Kennzeichen eingeben:", value="W-12345")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

st.header("🔧 Kalibrierung – Leer / Mittel / Voll")

with st.expander("Zugmaschine (Antriebsachse)"):
    leer_volvo_antrieb = st.number_input("Volvo Anzeige leer", value=daten["leer_volvo_antrieb"])
    leer_real_antrieb = st.number_input("Waage leer", value=daten["leer_real_antrieb"])
    mittel_volvo_antrieb = st.number_input("Volvo Anzeige mittel", value=daten["mittel_volvo_antrieb"])
    mittel_real_antrieb = st.number_input("Waage mittel", value=daten["mittel_real_antrieb"])
    voll_volvo_antrieb = st.number_input("Volvo Anzeige voll", value=daten["voll_volvo_antrieb"])
    voll_real_antrieb = st.number_input("Waage voll", value=daten["voll_real_antrieb"])

with st.expander("Auflieger"):
    leer_volvo_auflieger = st.number_input("Volvo Anzeige leer (Auflieger)", value=daten["leer_volvo_auflieger"])
    leer_real_auflieger = st.number_input("Waage leer (Auflieger)", value=daten["leer_real_auflieger"])
    mittel_volvo_auflieger = st.number_input("Volvo Anzeige mittel (Auflieger)", value=daten["mittel_volvo_auflieger"])
    mittel_real_auflieger = st.number_input("Waage mittel (Auflieger)", value=daten["mittel_real_auflieger"])
    voll_volvo_auflieger = st.number_input("Volvo Anzeige voll (Auflieger)", value=daten["voll_volvo_auflieger"])
    voll_real_auflieger = st.number_input("Waage voll (Auflieger)", value=daten["voll_real_auflieger"])

if st.button("💾 Kalibrierung speichern"):
    alle_daten[kennzeichen] = {
        "leer_volvo_antrieb": leer_volvo_antrieb,
        "leer_real_antrieb": leer_real_antrieb,
        "mittel_volvo_antrieb": mittel_volvo_antrieb,
        "mittel_real_antrieb": mittel_real_antrieb,
        "voll_volvo_antrieb": voll_volvo_antrieb,
        "voll_real_antrieb": voll_real_antrieb,
        "leer_volvo_auflieger": leer_volvo_auflieger,
        "leer_real_auflieger": leer_real_auflieger,
        "mittel_volvo_auflieger": mittel_volvo_auflieger,
        "mittel_real_auflieger": mittel_real_auflieger,
        "voll_volvo_auflieger": voll_volvo_auflieger,
        "voll_real_auflieger": voll_real_auflieger
    }
    speichere_daten(alle_daten)
    st.success("✅ Kalibrierung gespeichert")

st.header("📥 Eingabe aktueller Volvo-Werte")

volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Antriebsachse", value=voll_volvo_antrieb)
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=voll_volvo_auflieger)

real_antrieb = lineare_interpolation(volvo_now_antrieb, [
    (leer_volvo_antrieb, leer_real_antrieb),
    (mittel_volvo_antrieb, mittel_real_antrieb),
    (voll_volvo_antrieb, voll_real_antrieb)
])
real_auflieger = lineare_interpolation(volvo_now_auflieger, [
    (leer_volvo_auflieger, leer_real_auflieger),
    (mittel_volvo_auflieger, mittel_real_auflieger),
    (voll_volvo_auflieger, voll_real_auflieger)
])

real_gesamt = real_antrieb + real_auflieger

st.header("📊 Ergebnis")

st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

if real_antrieb > 11.5:
    st.error("⚠️ Achtung: Antriebsachse überladen (> 11.5 t)")
