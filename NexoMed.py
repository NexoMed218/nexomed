import streamlit as st
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai import types
import json

st.set_page_config(page_title="NexoMed - Sistema de Triaje Multilingüe", page_icon="🏥", layout="wide")

ZONA_MX = timezone(timedelta(hours=-6))
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

TRADUCCIONES = {
    "Español": {
        "bandera": "🇲🇽 Español",
        "subtitulo": "Tu puente de comunicación médica en cualquier idioma",
        "instruccion": "Seleccione su nivel de malestar:",
        "verde": "🟢 Malestar Leve (Consulta General)",
        "amarillo": "🟡 Malestar Moderado (Dolor Persistente)",
        "rojo": "🔴 EMERGENCIA INMEDIATA",
        "msg_rojo": "🚨 ALERTA ENVIADA AL MÉDICO. Permanezca en su lugar, la ayuda va en camino.",
        "msg_mic": "🎙️ Describa sus síntomas por voz o escríbalos abajo:",
        "placeholder": "Ej. Me duele mucho la cabeza desde ayer...",
        "btn_enviar": "Enviar al médico",
        "procesando": "⏳ Procesando y traduciendo síntomas para el equipo médico...",
        "msg_exito": "✅ Sus datos fueron enviados y traducidos para el doctor.",
        "msg_vacio": "⚠️ Por favor, escriba o grabe sus síntomas antes de enviar.",
        "disclaimer": "Aviso: NexoMed es una herramienta de comunicación y triaje. No sustituye valoración médica."
    },
    "English": {
        "bandera": "🇺🇸 English",
        "subtitulo": "Your medical communication bridge in any language",
        "instruccion": "Select your level of discomfort:",
        "verde": "🟢 Mild Discomfort (General Checkup)",
        "amarillo": "🟡 Moderate Discomfort (Persistent Pain)",
        "rojo": "🔴 IMMEDIATE EMERGENCY",
        "msg_rojo": "🚨 ALERT SENT TO DOCTOR. Stay where you are, help is on the way.",
        "msg_mic": "🎙️ Describe your symptoms by voice or type them below:",
        "placeholder": "E.g. I have had a severe headache since yesterday...",
        "btn_enviar": "Send to doctor",
        "procesando": "⏳ Processing and translating symptoms for the medical team...",
        "msg_exito": "✅ Your data was sent and translated for the doctor.",
        "msg_vacio": "⚠️ Please write or record your symptoms before sending.",
        "disclaimer": "Disclaimer: NexoMed is a communication and triage tool. Does not replace medical evaluation."
    },
    "Français": {
        "bandera": "🇫🇷 Français",
        "subtitulo": "Votre pont de communication médicale dans toutes les langues",
        "instruccion": "Sélectionnez votre niveau d'inconfort :",
        "verde": "🟢 Inconfort Léger (Consultation Générale)",
        "amarillo": "🟡 Inconfort Modéré (Douleur Persistante)",
        "rojo": "🔴 URGENCE IMMÉDIATE",
        "msg_rojo": "🚨 ALERTE ENVOYÉE AU MÉDECIN. Restez sur place, les secours arrivent.",
        "msg_mic": "🎙️ Décrivez vos symptômes à la voix ou écrivez-les ci-dessous :",
        "placeholder": "Ex. J'ai très mal à la tête depuis hier...",
        "btn_enviar": "Envoyer au médecin",
        "procesando": "⏳ Traitement et traduction des symptômes pour l'équipe médicale...",
        "msg_exito": "✅ Vos données ont été envoyées et traduites pour le médecin.",
        "msg_vacio": "⚠️ Veuillez écrire ou enregistrer vos symptômes avant d'envoyer.",
        "disclaimer": "Avis : NexoMed est un outil de communication et de triage. Ne remplace pas un avis médical."
    },
    "Mandarin": {
        "bandera": "🇨🇳 中文 (Mandarín)",
        "subtitulo": "跨越语言障碍的医疗沟通桥梁",
        "instruccion": "请选择您的不适程度：",
        "verde": "🟢 轻度不适（常规检查）",
        "amarillo": "🟡 中度不适（持续疼痛）",
        "rojo": "🔴 紧急情况",
        "msg_rojo": "🚨 已向医生发送警报。请留在原地，救援人员正在赶来。",
        "msg_mic": "🎙️ 请语音描述您的症状或在下方输入：",
        "placeholder": "例如：从昨天开始我头疼得很厉害……",
        "btn_enviar": "发送给医生",
        "procesando": "⏳ 正在为医疗团队处理和翻译症状...",
        "msg_exito": "✅ 您的数据已发送并翻译给医生。",
        "msg_vacio": "⚠️ 发送前请填写或录制您的症状。",
        "disclaimer": "免责声明：NexoMed 是沟通与分诊工具，不能替代专业医疗评估。"
    },
    "Deutsch": {
        "bandera": "🇩🇪 Deutsch",
        "subtitulo": "Ihre medizinische Kommunikationsbrücke in jeder Sprache",
        "instruccion": "Wählen Sie Ihren Beschwerdegrad:",
        "verde": "🟢 Leichte Beschwerden (Allgemeine Untersuchung)",
        "amarillo": "🟡 Mäßige Beschwerden (Anhaltende Schmerzen)",
        "rojo": "🔴 SOFORTIGER NOTFALL",
        "msg_rojo": "🚨 ALARM AN DEN ARZT GESENDET. Bleiben Sie an Ihrem Platz, Hilfe ist unterwegs.",
        "msg_mic": "🎙️ Beschreiben Sie Ihre Symptome per Sprache oder Text:",
        "placeholder": "Z.B. Ich habe seit gestern starke Kopfschmerzen...",
        "btn_enviar": "An Arzt senden",
        "procesando": "⏳ Symptome werden für das Ärzteteam verarbeitet und übersetzt...",
        "msg_exito": "✅ Ihre Daten wurden gesendet und für den Arzt übersetzt.",
        "msg_vacio": "⚠️ Bitte geben Sie Ihre Symptome ein oder nehmen Sie sie auf.",
        "disclaimer": "Hinweis: NexoMed ist ein Kommunikations- und Triage-Tool. Ersetzt keine ärztliche Untersuchung."
    },
    "Português": {
        "bandera": "🇧🇷 Português",
        "subtitulo": "Sua ponte de comunicação médica em qualquer idioma",
        "instruccion": "Selecione o seu nível de desconforto:",
        "verde": "🟢 Desconforto Leve (Consulta Geral)",
        "amarillo": "🟡 Desconforto Moderado (Dor Persistente)",
        "rojo": "🔴 EMERGÊNCIA IMEDIATA",
        "msg_rojo": "🚨 ALERTA ENVIADO AO MÉDICO. Permaneça no seu lugar, a ajuda está a caminho.",
        "msg_mic": "🎙️ Descreva os seus sintomas por voz ou escreva abaixo:",
        "placeholder": "Ex. Estou com muita dor de cabeça desde ontem...",
        "btn_enviar": "Enviar ao médico",
        "procesando": "⏳ Processando e traduzindo sintomas para a equipe médica...",
        "msg_exito": "✅ Seus dados foram enviados e traduzidos para o médico.",
        "msg_vacio": "⚠️ Por favor, escreva ou grave seus sintomas antes de enviar.",
        "disclaimer": "Aviso: NexoMed é uma ferramenta de comunicação e triagem. Não substitui avaliação médica."
    }
}

def analizar_sintomas_ia(texto, audio_bytes, idioma_origen):
    prompt = (
        f"Eres un asistente de triaje y traducción hospitalaria. El paciente seleccionó el idioma '{idioma_origen}'. "
        "Escucha el audio o lee el texto proporcionado. "
        "Responde EXCLUSIVAMENTE en formato JSON válido con dos claves exactas: "
        "'sintomas_es' (transcripción y traducción clara al español de los síntomas que reporta el paciente) y "
        "'recomendacion' (una acción operativa breve de recepción o enfermería en español, sin dar diagnósticos médicos)."
    )
    contenidos = [prompt]
    if texto.strip():
        contenidos.append(f"Texto del paciente: {texto.strip()}")
    if audio_bytes is not None:
        contenidos.append(types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"))

    try:
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contenidos,
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )
        datos = json.loads(resp.text)
        return datos.get("sintomas_es", texto), datos.get("recomendacion", "Pasar a valoración de enfermería.")
    except Exception:
        fallback = texto.strip() if texto.strip() else "Nota de voz recibida (revisar audio)."
        return fallback, "Preparar intérprete y tomar signos vitales."

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"
if "nivel" not in st.session_state:
    st.session_state.nivel = None
if "cola_pacientes" not in st.session_state:
    st.session_state.cola_pacientes = [
        {
            "hora": "20:10",
            "nivel": "AMARILLO",
            "idioma": "English",
            "sintomas": "Dolor abdominal intenso y náuseas desde la mañana (Original: Severe stomach pain and nausea).",
            "recomendacion": "🟡 Pasar a toma de signos vitales en menos de 15 min y preparar traducción."
        }
    ]

tab_paciente, tab_doctor = st.tabs(["🧑‍⚕️ Pantalla Paciente", "💻 Pantalla Doctor"])

with tab_paciente:
    t = TRADUCCIONES[st.session_state.idioma]
    
    st.title("🏥 NexoMed")
    st.caption(t["subtitulo"])
    st.write("Seleccione su idioma / Select your language / 选择语言:")

    cols = st.columns(3)
    idiomas_lista = list(TRADUCCIONES.keys())

    for i, lang in enumerate(idiomas_lista):
        with cols[i % 3]:
            if st.button(TRADUCCIONES[lang]["bandera"], key=f"btn_{lang}", use_container_width=True):
                st.session_state.idioma = lang
                st.session_state.nivel = None
                st.rerun()

    st.divider()
    st.subheader(t["instruccion"])

    if st.button(t["rojo"], type="primary", use_container_width=True):
        st.session_state.nivel = "ROJO"
        st.session_state.cola_pacientes.append({
            "hora": datetime.now(ZONA_MX).strftime("%H:%M"),
            "nivel": "ROJO",
            "idioma": st.session_state.idioma,
            "sintomas": "⚠️ ALERTA ROJA ACTIVADA POR EL PACIENTE (Emergencia inmediata)",
            "recomendacion": "🚨 Atención inmediata en sala de choque. Solicitar intérprete urgente."
        })

    if st.button(t["amarillo"], use_container_width=True):
        st.session_state.nivel = "AMARILLO"

    if st.button(t["verde"], use_container_width=True):
        st.session_state.nivel = "VERDE"

    st.divider()

    if st.session_state.nivel == "ROJO":
        st.error(t["msg_rojo"])
    elif st.session_state.nivel in ["AMARILLO", "VERDE"]:
        st.info(t["msg_mic"])
        
        audio_voz = st.audio_input("Grabar voz / Record voice")
        sintomas = st.text_area("Síntomas", placeholder=t["placeholder"], label_visibility="collapsed")
        
        if st.button(t["btn_enviar"], type="primary"):
            if sintomas.strip() or audio_voz is not None:
