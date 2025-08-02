
import streamlit as st
import json
import os

st.set_page_config(page_title="LKW Gewicht Rechner", page_icon="🚛")
st.title("🚛 LKW-Gewicht aus Volvo-Anzeige")

DATEI = "kalibrierung.json"

default_values = {
    "leer_volvo_antrieb": 4.7,
    "leer_real_antrieb": 7.5,
    "voll_volvo_antrieb": 11.0,
    "voll_real_antrieb": 11.5,
    "teilbeladung_volvo_antrieb": 0.0,
    "teilbeladung_real_antrieb": 0.0,
    "leer_volvo_auflieger": 6.6,
    "leer_real_auflieger": 8.5,
    "voll_volvo_auflieger": 23.0,
    "voll_real_auflieger": 27.5,
    "teilbeladung_volvo_auflieger": 0.0,
    "teilbeladung_real_auflieger": 0.0
}

def lade_daten():
    if os.path.exists(DATEI):
        with open(DATEI, "r") as f:
            return json.load(f)
    return {}

def speichere_daten(daten):
    with open(DATEI, "w") as f:
        json.dump(daten, f, indent=4)

def berechne_kalibrierung(volvo1, real1, volvo2, real2, optional_volvo=0.0, optional_real=0.0):
    if optional_volvo > 0 and optional_real > 0:
        x = [volvo1, optional_volvo, volvo2]
        y = [real1, optional_real, real2]
        xm = sum(x) / 3
        ym = sum(y) / 3
        nenner = sum((x[i] - xm)**2 for i in range(3))
        if nenner == 0:
            return 1.0, 0.0
        a = sum((x[i] - xm)*(y[i] - ym) for i in range(3)) / nenner
        b = ym - a * xm
        return a, b
    else:
        if volvo2 - volvo1 == 0:
            return 1.0, 0.0
        a = (real2 - real1) / (volvo2 - volvo1)
        b = real1 - a * volvo1
        return a, b

kennzeichen = st.text_input("Kennzeichen eingeben:", value="WL782GW")
alle_daten = lade_daten()
daten = alle_daten.get(kennzeichen, default_values)

# 📥 Eingabe aktueller Volvo-Werte
volvo_now_antrieb = st.number_input("Aktuelle Volvo-Anzeige – Zugmaschine", value=daten["voll_volvo_antrieb"])
volvo_now_auflieger = st.number_input("Aktuelle Volvo-Anzeige – Auflieger", value=daten["voll_volvo_auflieger"])

# ⚙️ Zusatzoptionen: Tank & Paletten
nutze_tank = st.checkbox("⛽ Tankfüllstand berücksichtigen?")
tank_kg = 0
if nutze_tank:
    tank_prozent = st.slider("Tankfüllstand", 0, 100, 100, step=10)
    max_tankgewicht = 320
    tank_kg = max_tankgewicht * (tank_prozent / 100)

nutze_paletten = st.checkbox("📦 Paletten im Palettenkorb berücksichtigen?")
paletten_kg = 0
if nutze_paletten:
    paletten_anzahl = st.slider("Anzahl Paletten im Korb", 0, 36, 0)
    gewicht_pro_palette = 25
    paletten_kg = paletten_anzahl * gewicht_pro_palette

a1, b1 = berechne_kalibrierung(daten["leer_volvo_antrieb"], daten["leer_real_antrieb"],
                               daten["voll_volvo_antrieb"], daten["voll_real_antrieb"],
                               daten["teilbeladung_volvo_antrieb"], daten["teilbeladung_real_antrieb"])
a2, b2 = berechne_kalibrierung(daten["leer_volvo_auflieger"], daten["leer_real_auflieger"],
                               daten["voll_volvo_auflieger"], daten["voll_real_auflieger"],
                               daten["teilbeladung_volvo_auflieger"], daten["teilbeladung_real_auflieger"])

real_antrieb = volvo_now_antrieb * a1 + b1
real_auflieger = volvo_now_auflieger * a2 + b2
real_gesamt = real_antrieb + real_auflieger
zusatzgewicht = (tank_kg + paletten_kg) / 1000
real_gesamt_korrigiert = real_gesamt + zusatzgewicht

st.header("📊 Ergebnis")
st.write(f"🚛 Zugmaschine: **{real_antrieb:.2f} t**")
st.write(f"🛻 Auflieger: **{real_auflieger:.2f} t**")
st.write(f"⚙️ Zusatzgewicht: **{zusatzgewicht:.2f} t**")
st.write(f"📦 Gesamtgewicht (inkl. Zusatz): **{real_gesamt_korrigiert:.2f} t**")

# Neue geführte Kalibrierung
st.header("🛠 Geführte Kalibrierung (Leer / Teil / Voll)")

def gefuehrte_kalibrierung(titel, key_prefix, feldnamen):
    with st.expander(titel):
        volvo_antrieb = st.number_input("📟 Volvo-Anzeige Zugmaschine (t)", key=f"{key_prefix}_volvo_antrieb")
        waage_antrieb = st.number_input("⚖️ Waagewert Zugmaschine (t)", key=f"{key_prefix}_waage_antrieb")
        volvo_auflieger = st.number_input("📟 Volvo-Anzeige Auflieger (t)", key=f"{key_prefix}_volvo_auflieger")
        waage_auflieger = st.number_input("⚖️ Waagewert Auflieger (t)", key=f"{key_prefix}_waage_auflieger")
        if st.button("💾 Speichern", key=f"{key_prefix}_save"):
            daten[feldnamen[0]] = volvo_antrieb
            daten[feldnamen[1]] = waage_antrieb
            daten[feldnamen[2]] = volvo_auflieger
            daten[feldnamen[3]] = waage_auflieger
            alle_daten[kennzeichen] = daten
            speichere_daten(alle_daten)
            st.success(f"✅ Kalibrierung '{titel}' gespeichert!")

st.subheader("📌 Bitte passende Kalibrierstufe wählen:")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🟢 Leer eingeben"):
        st.session_state["show_leer"] = True
with col2:
    if st.button("🟡 Teilbeladen eingeben"):
        st.session_state["show_teil"] = True
with col3:
    if st.button("🔵 Voll eingeben"):
        st.session_state["show_voll"] = True

if st.session_state.get("show_leer", False):
    gefuehrte_kalibrierung("🚛 Leer-Kalibrierung", "leer", [
        "leer_volvo_antrieb", "leer_real_antrieb",
        "leer_volvo_auflieger", "leer_real_auflieger"
    ])
if st.session_state.get("show_teil", False):
    gefuehrte_kalibrierung("📦 Teilbeladen-Kalibrierung", "teil", [
        "teilbeladung_volvo_antrieb", "teilbeladung_real_antrieb",
        "teilbeladung_volvo_auflieger", "teilbeladung_real_auflieger"
    ])
if st.session_state.get("show_voll", False):
    gefuehrte_kalibrierung("🏋️‍♂️ Voll-Kalibrierung", "voll", [
        "voll_volvo_antrieb", "voll_real_antrieb",
        "voll_volvo_auflieger", "voll_real_auflieger"
    ])
