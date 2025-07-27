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
    "voll_volvo_antrieb": 7.9,
    "voll_real_antrieb": 11.3,
    "leer_volvo_auflieger": 6.6,
    "leer_real_auflieger": 8.5,
    "voll_volvo_auflieger": 19.0,
    "voll_real_auflieger": 27.5,
    "mid_volvo_antrieb": 0.0,
    "mid_real_antrieb": 0.0,
    "mid_volvo_auflieger": 0.0,
    "mid_real_auflieger": 0.0
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
    # Punkte = Liste von (volvo, real)
    if len(punkte) < 2:
        return 1.0, 0.0
    x = [p[0] for p in punkte]
    y = [p[1] for p in punkte]
    n = len(punkte)
    a = (n * sum(xi * yi for xi, yi in zip(x, y)) - sum(x) * sum(y)) / \
        (n * sum(xi**2 for xi in x) - sum(x)**2)
    b = (sum(y) - a * sum(x)) / n
    return a, b

kennzeichen = st.text_input("Kennzeichen eingeben:", value="W-12345")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

st.header("🔧 Kalibrierung – Leer / Teil / Voll")

with st.expander("Zugmaschine (Antriebsachse)"):
    leer_volvo_antrieb = st.number_input("Volvo Anzeige leer", value=daten.get("leer_volvo_antrieb", 0.0))
    leer_real_antrieb = st.number_input("Waage leer", value=daten.get("leer_real_antrieb", 0.0))
    mid_volvo_antrieb = st.number_input("Volvo Anzeige teilbeladen (optional)", value=daten.get("mid_volvo_antrieb", 0.0))
    mid_real_antrieb = st.number_input("Waage teilbeladen (optional)", value=daten.get("mid_real_antrieb", 0.0))
    voll_volvo_antrieb = st.number_input("Volvo Anzeige voll", value=daten.get("voll_volvo_antrieb", 0.0))
    voll_real_antrieb = st.number_input("Waage voll", value=daten.get("voll_real_antrieb", 0.0))

with st.expander("Auflieger"):
    leer_volvo_auflieger = st.number_input("Volvo Anzeige leer (Auflieger)", value=daten.get("leer_volvo_auflieger", 0.0))
    leer_real_auflieger = st.number_input("Waage leer (Auflieger)", value=daten.get("leer_real_auflieger", 0.0))
    mid_volvo_auflieger = st.number_input("Volvo Anzeige teilbeladen (optional)", value=daten.get("mid_volvo_auflieger", 0.0))
    mid_real_auflieger = st.number_input("Waage teilbeladen (optional)", value=daten.get("mid_real_auflieger", 0.0))
    voll_volvo_auflieger = st.number_input("Volvo Anzeige voll (Auflieger)", value=daten.get("voll_volvo_auflieger", 0.0))
    voll_real_auflieger = st.number_input("Waage voll (Auflieger)", value=daten.get("voll_real_auflieger", 0.0))

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

# Dynamisch Messpunkte sammeln
punkte_antrieb = [(leer_volvo_antrieb, leer_real_antrieb), (voll_volvo_antrieb, voll_real_antrieb)]
if mid_volvo_antrieb > 0 and mid_real_antrieb > 0:
    punkte_antrieb.insert(1, (mid_volvo_antrieb, mid_real_antrieb))

punkte_auflieger = [(leer_volvo_auflieger, leer_real_auflieger), (voll_volvo_auflieger, voll_real_auflieger)]
if mid_volvo_auflieger > 0 and mid_real_auflieger > 0:
    punkte_auflieger.insert(1, (mid_volvo_auflieger, mid_real_auflieger))

# Kalibrierung berechnen
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
