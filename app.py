import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

# Startwerte – neutral (alle auf 0.0)
default_values = {
    "leer_volvo_antrieb": 0.0,
    "leer_real_antrieb": 0.0,
    "mittel_volvo_antrieb": 0.0,
    "mittel_real_antrieb": 0.0,
    "voll_volvo_antrieb": 0.0,
    "voll_real_antrieb": 0.0,
    "leer_volvo_auflieger": 0.0,
    "leer_real_auflieger": 0.0,
    "mittel_volvo_auflieger": 0.0,
    "mittel_real_auflieger": 0.0,
    "voll_volvo_auflieger": 0.0,
    "voll_real_auflieger": 0.0
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f)

def berechne_kalibrierung(punkte):
    gefiltert = [(v, r) for v, r in punkte if v > 0 and r > 0]
    if len(gefiltert) < 2:
        return 1.0, 0.0
    x = [v for v, _ in gefiltert]
    y = [r for _, r in gefiltert]
    a = (y[-1] - y[0]) / (x[-1] - x[0]) if x[-1] != x[0] else 1.0
    b = y[0] - a * x[0]
    return a, b

kennzeichen = st.text_input("Kennzeichen eingeben:", value="")

alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

st.header("🔧 Kalibrierung – Leer, Mittel, Voll")

with st.expander("Zugmaschine (Antriebsachse)"):
    leer_volvo_antrieb = st.number_input("Volvo Anzeige leer", value=daten["leer_volvo_antrieb"])
    leer_real_antrieb = st.number_input("Waage leer", value=daten["leer_real_antrieb"])
    mittel_volvo_antrieb = st.number_input("Volvo Anzeige teilbeladen (optional)", value=daten["mittel_volvo_antrieb"])
    mittel_real_antrieb = st.number_input("Waage teilbeladen (optional)", value=daten["mittel_real_antrieb"])
    voll_volvo_antrieb = st.number_input("Volvo Anzeige voll", value=daten["voll_volvo_antrieb"])
    voll_real_antrieb = st.number_input("Waage voll", value=daten["voll_real_antrieb"])

with st.expander("Auflieger"):
    leer_volvo_auflieger = st.number_input("Volvo Anzeige leer (Auflieger)", value=daten["leer_volvo_auflieger"])
    leer_real_auflieger = st.number_input("Waage leer (Auflieger)", value=daten["leer_real_auflieger"])
    mittel_volvo_auflieger = st.number_input("Volvo Anzeige teilbeladen (optional)", value=daten["mittel_volvo_auflieger"])
    mittel_real_auflieger = st.number_input("Waage teilbeladen (optional)", value=daten["mittel_real_auflieger"])
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

st.header("📥 Aktuelle Volvo-Werte eingeben")

volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Antriebsachse", value=voll_volvo_antrieb)
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=voll_volvo_auflieger)

# Kalibrierung berechnen
punkte_antrieb = [(leer_volvo_antrieb, leer_real_antrieb),
                  (mittel_volvo_antrieb, mittel_real_antrieb),
                  (voll_volvo_antrieb, voll_real_antrieb)]
punkte_auflieger = [(leer_volvo_auflieger, leer_real_auflieger),
                    (mittel_volvo_auflieger, mittel_real_auflieger),
                    (voll_volvo_auflieger, voll_real_auflieger)]

a1, b1 = berechne_kalibrierung(punkte_antrieb)
a2, b2 = berechne_kalibrierung(punkte_auflieger)

real_antrieb = volvo_now_antrieb * a1 + b1
real_auflieger = volvo_now_auflieger * a2 + b2
real_gesamt = real_antrieb + real_auflieger

st.header("📊 Ergebnis")

st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

if real_antrieb > 11.5:
    st.error("⚠️ Achtung: Antriebsachse überladen (> 11.5 t)")

if real_gesamt > 40:
    st.warning("⚠️ Gesamtgewicht möglicherweise überladen (> 40 t)")
