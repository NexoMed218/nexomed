import streamlit as st
from datetime import datetime

st.set_page_config(page_title="NexoMed - Sistema de Triaje Multilingüe", page_icon="🏥", layout="wide")

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
        "msg_exito": "✅ Sus datos fueron enviados al panel del doctor.",
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
        "msg_exito": "✅ Your data was sent to the doctor's dashboard.",
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
        "msg_exito": "✅ Vos données ont été envoyées au panneau du médecin.",
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
        "msg_exito": "✅ 您的数据已发送至医生面板。",
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
        "msg_exito": "✅ Ihre Daten wurden an das Arzt-Dashboard gesendet.",
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
        "msg_exito": "✅ Seus dados foram enviados para o painel do médico.",
        "msg_vacio": "⚠️ Por favor, escreva ou grave seus sintomas antes de enviar.",
        "disclaimer": "Aviso: NexoMed é uma ferramenta de comunicação e triagem. Não substitui avaliação médica."
    }
}

RECOMENDACIONES_OPERATIVAS = {
    "ROJO": "🚨 Atención inmediata en sala de choque. Solicitar intérprete urgente si el idioma no es local.",
    "AMARILLO": "🟡 Pasar a toma de signos vitales en menos de 15 min. Preparar traducción básica.",
    "VERDE": "🟢 Asignar turno en sala de espera general. Comunicación estándar."
}

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
            "sintomas": "Severe stomach pain and nausea since morning.",
            "recomendacion": RECOMENDACIONES_OPERATIVAS["AMARILLO"]
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
            "hora": datetime.now().strftime("%H:%M"),
            "nivel": "ROJO",
            "idioma": st.session_state.idioma,
            "sintomas": "⚠️ ALERTA ROJA ACTIVADA POR EL PACIENTE (Sin texto adicional)",
            "recomendacion": RECOMENDACIONES_OPERATIVAS["ROJO"]
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
                texto_final = sintomas.strip() if sintomas.strip() else "🎙️ [Nota de voz grabada por el paciente]"
                
                st.session_state.cola_pacientes.append({
                    "hora": datetime.now().strftime("%H:%M"),
                    "nivel": st.session_state.nivel,
                    "idioma": st.session_state.idioma,
                    "sintomas": texto_final,
                    "recomendacion": RECOMENDACIONES_OPERATIVAS[st.session_state.nivel]
                })
                st.success(t["msg_exito"])
            else:
                st.warning(t["msg_vacio"])

    st.divider()
    st.caption(f"⚕️ {t['disclaimer']}")

with tab_doctor:
    st.title("💻 NexoMed — Panel de Recepción Médica")
    st.write("Lista de pacientes ordenada automáticamente por prioridad de color e idioma detectado.")

    if not st.session_state.cola_pacientes:
        st.info("No hay pacientes en espera en este momento.")
    else:
        prioridad = {"ROJO": 1, "AMARILLO": 2, "VERDE": 3}
        pacientes_ordenados = sorted(
            st.session_state.cola_pacientes,
            key=lambda x: prioridad[x["nivel"]]
        )

        for idx, p in enumerate(pacientes_ordenados):
            with st.container(border=True):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if p["nivel"] == "ROJO":
                        st.error(f"🔴 **ROJO**\n\n🕒 {p['hora']}")
                    elif p["nivel"] == "AMARILLO":
                        st.warning(f"🟡 **AMARILLO**\n\n🕒 {p['hora']}")
                    else:
                        st.success(f"🟢 **VERDE**\n\n🕒 {p['hora']}")
                
                with col2:
                    st.markdown(f"**Idioma del paciente:** {p['idioma']}")
                    st.markdown(f"**Síntomas reportados:**\n> {p['sintomas']}")
                
