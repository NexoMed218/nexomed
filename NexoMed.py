import streamlit as st
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai import types
import json

st.set_page_config(page_title="NexoMed - Triaje Multilingüe", page_icon="🏥", layout="wide")
ZONA_MX = timezone(timedelta(hours=-6))
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

TRADUCCIONES = {
    "Español": {
        "bandera": "🇲🇽 Español", "subtitulo": "Tu puente de comunicación médica",
        "instruccion": "Seleccione su nivel de malestar:",
        "verde": "🟢 Malestar Leve", "amarillo": "🟡 Malestar Moderado", "rojo": "🔴 EMERGENCIA INMEDIATA",
        "msg_rojo": "🚨 ALERTA ENVIADA AL MÉDICO. Permanezca en su lugar.",
        "msg_mic": "🎙️ Describa sus síntomas por voz o escríbalos abajo:",
        "placeholder": "Ej. Me duele mucho la cabeza...", "btn_enviar": "Enviar al médico",
        "procesando": "⏳ Escuchando y traduciendo síntomas...",
        "msg_exito": "✅ Síntomas enviados y traducidos al doctor.", "msg_vacio": "⚠️ Escriba o grabe sus síntomas."
    },
    "English": {
        "bandera": "🇺🇸 English", "subtitulo": "Your medical communication bridge",
        "instruccion": "Select your level of discomfort:",
        "verde": "🟢 Mild Discomfort", "amarillo": "🟡 Moderate Discomfort", "rojo": "🔴 IMMEDIATE EMERGENCY",
        "msg_rojo": "🚨 ALERT SENT TO DOCTOR. Stay where you are.",
        "msg_mic": "🎙️ Describe your symptoms by voice or text:",
        "placeholder": "E.g. Severe headache...", "btn_enviar": "Send to doctor",
        "procesando": "⏳ Listening and translating symptoms...",
        "msg_exito": "✅ Symptoms sent and translated.", "msg_vacio": "⚠️ Write or record symptoms."
    },
    "Français": {
        "bandera": "🇫🇷 Français", "subtitulo": "Votre pont de communication médicale",
        "instruccion": "Sélectionnez votre niveau d'inconfort :",
        "verde": "🟢 Inconfort Léger", "amarillo": "🟡 Inconfort Modéré", "rojo": "🔴 URGENCE IMMÉDIATE",
        "msg_rojo": "🚨 ALERTE ENVOYÉE AU MÉDECIN. Restez sur place.",
        "msg_mic": "🎙️ Décrivez vos symptômes :",
        "placeholder": "Ex. Mal à la tête...", "btn_enviar": "Envoyer",
        "procesando": "⏳ Écoute et traduction des symptômes...",
        "msg_exito": "✅ Symptômes envoyés et traduits.", "msg_vacio": "⚠️ Écrivez ou enregistrez vos symptômes."
    },
    "Mandarin": {
        "bandera": "🇨🇳 中文 (Mandarín)", "subtitulo": "医疗沟通桥梁",
        "instruccion": "请选择您的不适程度：",
        "verde": "🟢 轻度不适", "amarillo": "🟡 中度不适", "rojo": "🔴 紧急情况",
        "msg_rojo": "🚨 已向医生发送警报。请留在原地。",
        "msg_mic": "🎙️ 请语音或文字描述症状：",
        "placeholder": "例如：头疼...", "btn_enviar": "发送",
        "procesando": "⏳ 正在翻译症状...",
        "msg_exito": "✅ 已发送给医生。", "msg_vacio": "⚠️ 请填写或录制症状。"
    },
    "Deutsch": {
        "bandera": "🇩🇪 Deutsch", "subtitulo": "Medizinische Kommunikationsbrücke",
        "instruccion": "Wählen Sie Ihren Beschwerdegrad:",
        "verde": "🟢 Leichte Beschwerden", "amarillo": "🟡 Mäßige Beschwerden", "rojo": "🔴 NOTFALL",
        "msg_rojo": "🚨 ALARM GESENDET. Bleiben Sie hier.",
        "msg_mic": "🎙️ Beschreiben Sie Ihre Symptome:",
        "placeholder": "Z.B. Kopfschmerzen...", "btn_enviar": "Senden",
        "procesando": "⏳ Symptome werden übersetzt...",
        "msg_exito": "✅ An den Arzt gesendet.", "msg_vacio": "⚠️ Bitte Symptome angeben."
    },
    "Português": {
        "bandera": "🇧🇷 Português", "subtitulo": "Ponte de comunicação médica",
        "instruccion": "Selecione o nível de desconforto:",
        "verde": "🟢 Desconforto Leve", "amarillo": "🟡 Desconforto Moderado", "rojo": "🔴 EMERGÊNCIA",
        "msg_rojo": "🚨 ALERTA ENVIADO. Permaneça no local.",
        "msg_mic": "🎙️ Descreva os sintomas:",
        "placeholder": "Ex. Dor de cabeça...", "btn_enviar": "Enviar",
        "procesando": "⏳ Traduzindo sintomas...",
        "msg_exito": "✅ Enviado ao médico.", "msg_vacio": "⚠️ Escreva ou grave os sintomas."
    }
}

def escuchar_y_traducir(texto, audio_file, idioma):
    prompt = (
        f"Eres un asistente de triaje hospitalario. El paciente habla '{idioma}'. "
        "Escucha el audio o lee el texto y devuelve un JSON con dos claves exactas: "
        "'sintomas' (transcripción exacta de lo que dijo el paciente traducida al español) y "
        "'rec' (acción operativa breve para enfermería en español, sin dar diagnósticos)."
    )
    contenidos = [prompt]
    if texto.strip():
        contenidos.append(texto.strip())
    if audio_file is not None:
        tipo_mime = audio_file.type or "audio/wav"
        contenidos.append(types.Part.from_bytes(data=audio_file.getvalue(), mime_type=tipo_mime))

    modelos_a_probar = ["gemini-2.0-flash", "gemini-flash-latest", "gemini-2.5-flash", "gemini-2.0-flash-lite"]
    ultimo_error = ""

    for modelo in modelos_a_probar:
        try:
            resp = client.models.generate_content(
                model=modelo,
                contents=contenidos,
                config=types.GenerateContentConfig(response_mime_type="application/json")
            )
            datos = json.loads(resp.text)
            return datos.get("sintomas", texto), datos.get("rec", "Valorar en enfermería.")
        except Exception as e:
            ultimo_error = str(e)
            continue

    return f"🎙️ Audio grabado (Detalle: {ultimo_error[:70]})", "Preparar intérprete y tomar signos vitales."

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"
if "nivel" not in st.session_state:
    st.session_state.nivel = None
if "cola" not in st.session_state:
    st.session_state.cola = []

tab1, tab2 = st.tabs(["🧑‍⚕️ Pantalla Paciente", "💻 Pantalla Doctor"])

with tab1:
    t = TRADUCCIONES[st.session_state.idioma]
    st.title("🏥 NexoMed")
    st.caption(t["subtitulo"])
    cols = st.columns(3)
    for i, lang in enumerate(TRADUCCIONES.keys()):
        if cols[i % 3].button(TRADUCCIONES[lang]["bandera"], key=f"b_{lang}", use_container_width=True):
            st.session_state.idioma = lang
            st.session_state.nivel = None
            st.rerun()
    st.divider()
    st.subheader(t["instruccion"])
    if st.button(t["rojo"], type="primary", use_container_width=True):
        st.session_state.nivel = "ROJO"
        st.session_state.cola.append({"hora": datetime.now(ZONA_MX).strftime("%H:%M"), "nivel": "ROJO", "idioma": st.session_state.idioma, "sintomas": "⚠️ ALERTA ROJA INMEDIATA", "rec": "🚨 Atención inmediata en sala de choque.", "audio": None})
    if st.button(t["amarillo"], use_container_width=True):
        st.session_state.nivel = "AMARILLO"
    if st.button(t["verde"], use_container_width=True):
        st.session_state.nivel = "VERDE"
    if st.session_state.nivel == "ROJO":
        st.error(t["msg_rojo"])
    elif st.session_state.nivel in ["AMARILLO", "VERDE"]:
        st.info(t["msg_mic"])
        voz = st.audio_input("Voz / Voice")
        txt = st.text_area("Síntomas", placeholder=t["placeholder"], label_visibility="collapsed")
        if st.button(t["btn_enviar"], type="primary"):
            if txt.strip() or voz is not None:
                with st.spinner(t["procesando"]):
                    sintomas_es, rec_es = escuchar_y_traducir(txt, voz, st.session_state.idioma)
                    st.session_state.cola.append({"hora": datetime.now(ZONA_MX).strftime("%H:%M"), "nivel": st.session_state.nivel, "idioma": st.session_state.idioma, "sintomas": sintomas_es, "rec": rec_es, "audio": voz})
                st.success(t["msg_exito"])
            else:
                st.warning(t["msg_vacio"])

with tab2:
    st.title("💻 NexoMed — Panel Doctor")
    prioridad = {"ROJO": 1, "AMARILLO": 2, "VERDE": 3}
    for p in sorted(st.session_state.cola, key=lambda x: prioridad[x["nivel"]]):
        with st.container(border=True):
            c1, c2, c3 = st.columns(3)
            if p["nivel"] == "ROJO":
                c1.error(f"🔴 **ROJO**\n\n🕒 {p['hora']}")
            elif p["nivel"] == "AMARILLO":
                c1.warning(f"🟡 **AMARILLO**\n\n🕒 {p['hora']}")
            else:
                c1.success(f"🟢 **VERDE**\n\n🕒 {p['hora']}")
            c2.write(f"**Idioma:** {p['idioma']}\n\n**Síntomas traducidos:** {p['sintomas']}")
            if p["audio"] is not None:
                c2.audio(p["audio"])
            c3.info(p["rec"])
