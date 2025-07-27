import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

default_values = {
    "leer_volvo_antrieb": 4.7,
    "leer_real_antrieb": 7.5,
    "voll_volvo_antrieb": 7.9,
    "voll_real_antrieb": 11.3,
    "leer_volvo_auflieger": 6.6,
    "leer_real_auflieger": 8.5,
    "voll_volvo_auflieger": 19.0,
    "voll_real_auflieger": 27.5,
    "mid_volvo_antrieb": None,
    "mid_real_antrieb": None,
    "mid_volvo_auflieger": None,
    "mid_real_auflieger": None
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f)

def berechne_2pkt_kalibrierung(v1, r1, v2, r2):
    if v2 - v1 == 0:
        return 1.0, 0.0
    a = (r2 - r1) / (v2 - v1)
    b = r1 - a * v1
    return a, b

def berechne_3pkt_interpolation(volvo, p1, p2, p3):
    x_vals = [p[0] for p in [p1, p2, p3] if None not in p]
    y_vals = [p[1] for p in [p1, p2, p3] if None not in p]
    if len(x_vals) < 2:
        return None
    # Falls nur 2 Punkte → lineare Regression
    if len(x_vals) == 2:
        a, b = berechne_2pkt_kalibrierung(x_vals[0], y_vals[0], x_vals[1], y_vals[1])
        return a * volvo + b
    # 3-Punkt-Interpolation: quadratische Regression
    coeffs = list(reversed(list(polyfit(x_vals, y_vals, 2))))
    return coeffs[0]*volvo**2 + coeffs[1]*volvo + coeffs[2]

def polyfit(x, y, degree):
    import numpy as np
    return np.polyfit(x, y, degree)

kennzeichen = st.text_input("Kennzeichen eingeben:", value="W-12345")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

st.header("🔧 Kalibrierung – Leer / Teilbeladen / Voll")

with st.expander("Zugmaschine (Antriebsachse)"):
    leer_volvo_antrieb = st.number_input("Volvo Anzeige leer", value=daten["leer_volvo_antrieb"])
    leer_real_antrieb = st.number_input("Waage leer", value=daten["leer_real_antrieb"])
    mid_volvo_antrieb = st.number_input("Volvo Anzeige teilbeladen (optional)", value=daten.get("mid_volvo_antrieb") or 0.0)
    mid_real_antrieb = st.number_input("Waage teilbeladen (optional)", value=daten.get("mid_real_antrieb") or 0.0)
    voll_volvo_antrieb = st.number_input("Volvo Anzeige voll", value=daten["voll_volvo_antrieb"])
    voll_real_antrieb = st.number_input("Waage voll", value=daten["voll_real_antrieb"])

with st.expander("Auflieger"):
    leer_volvo_auflieger = st.number_input("Volvo Anzeige leer (Auflieger)", value=daten["leer_volvo_auflieger"])
    leer_real_auflieger = st.number_input("Waage leer (Auflieger)", value=daten["leer_real_auflieger"])
    mid_volvo_auflieger = st.number_input("Volvo Anzeige teilbeladen (optional)", value=daten.get("mid_volvo_auflieger") or 0.0)
    mid_real_auflieger = st.number_input("Waage teilbeladen (optional)", value=daten.get("mid_real_auflieger") or 0.0)
    voll_volvo_auflieger = st.number_input("Volvo Anzeige voll (Auflieger)", value=daten["voll_volvo_auflieger"])
    voll_real_auflieger = st.number_input("Waage voll (Auflieger)", value=daten["voll_real_auflieger"])

if st.button("💾 Kalibrierung speichern"):
    alle_daten[kennzeichen] = {
        "leer_volvo_antrieb": leer_volvo_antrieb,
        "leer_real_antrieb": leer_real_antrieb,
        "mid_volvo_antrieb": mid_volvo_antrieb,
        "mid_real_antrieb": mid_real_antrieb,
        "voll_volvo_antrieb": voll_volvo_antrieb,
        "voll_real_antrieb": voll_real_antrieb,
        "leer_volvo_auflieger": leer_volvo_auflieger,
        "leer_real_auflieger": leer_real_auflieger,
        "mid_volvo_auflieger": mid_volvo_auflieger,
        "mid_real_auflieger": mid_real_auflieger,
        "voll_volvo_auflieger": voll_volvo_auflieger,
        "voll_real_auflieger": voll_real_auflieger
    }
    speichere_daten(alle_daten)
    st.success("✅ Kalibrierung gespeichert")

st.header("📥 Eingabe aktueller Volvo-Werte")

volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Antriebsachse", value=voll_volvo_antrieb)
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=voll_volvo_auflieger)

# Berechnung – Interpolation oder lineare Kalibrierung
real_antrieb = berechne_3pkt_interpolation(
    volvo_now_antrieb,
    (leer_volvo_antrieb, leer_real_antrieb),
    (mid_volvo_antrieb if mid_volvo_antrieb > 0 else None,
     mid_real_antrieb if mid_real_antrieb > 0 else None),
    (voll_volvo_antrieb, voll_real_antrieb)
)

real_auflieger = berechne_3pkt_interpolation(
    volvo_now_auflieger,
    (leer_volvo_auflieger, leer_real_auflieger),
    (mid_volvo_auflieger if mid_volvo_auflieger > 0 else None,
     mid_real_auflieger if mid_real_auflieger > 0 else None),
    (voll_volvo_auflieger, voll_real_auflieger)
)

if real_antrieb and real_auflieger:
    real_gesamt = real_antrieb + real_auflieger

    st.header("📊 Ergebnis")
    st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
    st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
    st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

    if real_antrieb > 11.5:
        st.error("⚠️ Achtung: Antriebsachse überladen (> 11.5 t)")
else:
    st.warning("ℹ️ Bitte mindestens Leer- und Volldaten eingeben.")
