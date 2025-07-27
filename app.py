import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

# Standardwerte (geschätzt)
default_values = {
    "leer_volvo_antrieb": 4.7,
    "leer_real_antrieb": 7.5,
    "voll_volvo_antrieb": 7.9,
    "voll_real_antrieb": 11.3,
    "teilbel_volvo_antrieb": 6.5,
    "teilbel_real_antrieb": 9.5,
    "leer_volvo_auflieger": 6.6,
    "leer_real_auflieger": 8.5,
    "voll_volvo_auflieger": 19.0,
    "voll_real_auflieger": 27.5,
    "teilbel_volvo_auflieger": 13.5,
    "teilbel_real_auflieger": 18.0
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f)

def berechne_kalibrierung(volvo1, real1, volvo2, real2, teil_volvo=None, teil_real=None):
    if teil_volvo is not None and teil_real is not None and volvo2 - volvo1 != 0 and teil_volvo - volvo1 != 0:
        # Quadratische Kalibrierung mit 3 Punkten
        from numpy import polyfit
        x_vals = [volvo1, teil_volvo, volvo2]
        y_vals = [real1, teil_real, real2]
        a, b, c = polyfit(x_vals, y_vals, 2)
        return lambda v: a*v**2 + b*v + c
    elif volvo2 - volvo1 != 0:
        # Lineare Kalibrierung
        a = (real2 - real1) / (volvo2 - volvo1)
        b = real1 - a * volvo1
        return lambda v: a * v + b
    else:
        return lambda v: v  # Fallback: keine Kalibrierung möglich

kennzeichen = st.text_input("Kennzeichen eingeben:", value="W-12345")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

st.header("🔧 Kalibrierung – Leer, Voll und Teilbeladen")

with st.expander("Zugmaschine (Antriebsachse)"):
    leer_volvo_antrieb = st.number_input("Volvo Anzeige leer", value=daten["leer_volvo_antrieb"])
    leer_real_antrieb = st.number_input("Waage leer", value=daten["leer_real_antrieb"])
    voll_volvo_antrieb = st.number_input("Volvo Anzeige voll", value=daten["voll_volvo_antrieb"])
    voll_real_antrieb = st.number_input("Waage voll", value=daten["voll_real_antrieb"])
    teilbel_volvo_antrieb = st.number_input("Volvo Anzeige teilbeladen", value=daten["teilbel_volvo_antrieb"])
    teilbel_real_antrieb = st.number_input("Waage teilbeladen", value=daten["teilbel_real_antrieb"])

with st.expander("Auflieger"):
    leer_volvo_auflieger = st.number_input("Volvo Anzeige leer (Auflieger)", value=daten["leer_volvo_auflieger"])
    leer_real_auflieger = st.number_input("Waage leer (Auflieger)", value=daten["leer_real_auflieger"])
    voll_volvo_auflieger = st.number_input("Volvo Anzeige voll (Auflieger)", value=daten["voll_volvo_auflieger"])
    voll_real_auflieger = st.number_input("Waage voll (Auflieger)", value=daten["voll_real_auflieger"])
    teilbel_volvo_auflieger = st.number_input("Volvo Anzeige teilbeladen (Auflieger)", value=daten["teilbel_volvo_auflieger"])
    teilbel_real_auflieger = st.number_input("Waage teilbeladen (Auflieger)", value=daten["teilbel_real_auflieger"])

if st.button("💾 Kalibrierung speichern"):
    alle_daten[kennzeichen] = {
        "leer_volvo_antrieb": leer_volvo_antrieb,
        "leer_real_antrieb": leer_real_antrieb,
        "voll_volvo_antrieb": voll_volvo_antrieb,
        "voll_real_antrieb": voll_real_antrieb,
        "teilbel_volvo_antrieb": teilbel_volvo_antrieb,
        "teilbel_real_antrieb": teilbel_real_antrieb,
        "leer_volvo_auflieger": leer_volvo_auflieger,
        "leer_real_auflieger": leer_real_auflieger,
        "voll_volvo_auflieger": voll_volvo_auflieger,
        "voll_real_auflieger": voll_real_auflieger,
        "teilbel_volvo_auflieger": teilbel_volvo_auflieger,
        "teilbel_real_auflieger": teilbel_real_auflieger
    }
    speichere_daten(alle_daten)
    st.success("✅ Kalibrierung gespeichert")

st.header("📥 Eingabe aktueller Volvo-Werte")

volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Antriebsachse", value=voll_volvo_antrieb)
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=voll_volvo_auflieger)

# Umrechnung basierend auf vorhandenen Werten
f_antrieb = berechne_kalibrierung(
    leer_volvo_antrieb, leer_real_antrieb,
    voll_volvo_antrieb, voll_real_antrieb,
    teilbel_volvo_antrieb, teilbel_real_antrieb
)
f_auflieger = berechne_kalibrierung(
    leer_volvo_auflieger, leer_real_auflieger,
    voll_volvo_auflieger, voll_real_auflieger,
    teilbel_volvo_auflieger, teilbel_real_auflieger
)

real_antrieb = f_antrieb(volvo_now_antrieb)
real_auflieger = f_auflieger(volvo_now_auflieger)
real_gesamt = real_antrieb + real_auflieger

st.header("📊 Ergebnis")

st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
st.write(f"📦 Gesamtgewicht: **{real_gesamt:.2f} t**")

if real_antrieb > 11.5:
    st.error("⚠️ Achtung: Antriebsachse überladen (> 11.5 t)")
