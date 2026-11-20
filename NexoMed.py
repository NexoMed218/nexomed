import streamlit as st
from datetime import datetime, timedelta, timezone
from google import genai
from google.genai import types
import json

st.set_page_config(page_title="NexoMed - Triaje Multilingüe", page_icon="🏥", layout="wide")
ZONA_MX = timezone(timedelta(hours=-6))
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def obtener_cola_global():
    return []

cola_global = obtener_cola_global()

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
    "Náhuatl": {
        "bandera": "🇲🇽 Náhuatl", "subtitulo": "Motlahtolpalehuiliz tlen pahpatiliztli",
        "instruccion": "Xikpejpena kenijkatsa timokokoa:",
        "verde": "🟢 Tsikitsin kokolistli", "amarillo": "🟡 Tlahko kokolistli", "rojo": "🔴 NIMAN TLAPALEHUILISTLI",
        "msg_rojo": "🚨 YOTLATITLANKEH TLAHTOLI IPAN TEPATIANI. Ximokahua nikan.",
        "msg_mic": "🎙️ Xikijto tlen timokokoa ika motlahtol o xikijkuilo nikan:",
        "placeholder": "Ej. Nechkokoa notsontekon...", "btn_enviar": "Tlatitlani ipan tepatiani",
        "procesando": "⏳ Tikakij uan tikpatlaj motlahtol...",
        "msg_exito": "✅ Yotlatitlankeh motlahtol ipan tepatiani.", "msg_vacio": "⚠️ Xikijkuilo o xikijto tlen timokokoa."
    },
    "Hñähñu (Otomí)": {
        "bandera": "🇲🇽 Hñähñu", "subtitulo": "Ra ñäki pa ra 'ñethi",
        "instruccion": "Huahni te'ä gi tu:",
        "verde": "🟢 Ts'ʉtho ra ñ'u", "amarillo": "🟡 Madetho ra ñ'u", "rojo": "🔴 NT'A'MI PA RA 'ÑETHI",
        "msg_rojo": "🚨 XÄ MÄHNÄ RA 'ÑETHI. 'Bʉi gekua.",
        "msg_mic": "🎙️ Mää te gi tu ko ri ñäki o 'yot'i gekua:",
        "placeholder": "Ej. U ma ñäxu...", "btn_enviar": "Pehni ha ra 'ñethi",
        "procesando": "⏳ Di øde ne di pädihu ri ñäki...",
        "msg_exito": "✅ Xä mähni ha ra 'ñethi.", "msg_vacio": "⚠️ 'Yot'i o mää te gi tu."
    },
    "한국어 (Coreano)": {
        "bandera": "🇰🇷 한국어", "subtitulo": "언어 장벽 없는 의료 소통 다리",
        "instruccion": "불편함의 정도를 선택하세요:",
        "verde": "🟢 가벼운 증상 (일반 진료)", "amarillo": "🟡 중간 정도 증상 (지속적인 통증)", "rojo": "🔴 즉각적인 응급 상황",
        "msg_rojo": "🚨 의사에게 긴급 알림이 전송되었습니다. 제자리에 계세요.",
        "msg_mic": "🎙️ 음성으로 증상을 말씀하시거나 아래에 입력하세요:",
        "placeholder": "예: 어제부터 머리가 너무 아픕니다...", "btn_enviar": "의사에게 전송",
        "procesando": "⏳ 증상을 듣고 번역하는 중...",
        "msg_exito": "✅ 증상이 의사에게 전송 및 번역되었습니다.", "msg_vacio": "⚠️ 증상을 입력하거나 녹음해 주세요."
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
    },
    "العربية (Árabe)": {
        "bandera": "🇸🇦 العربية", "subtitulo": "جسر التواصل الطبي بدون حواجز لغوية",
        "instruccion": "اختر مستوى الألم أو الانزعاج:",
        "verde": "🟢 انزعاج خفيف", "amarillo": "🟡 ألم متوسط مستمر", "rojo": "🔴 حالة طوارئ فورية",
        "msg_rojo": "🚨 تم إرسال تنبيه للطبيب. ابق في مكانك.",
        "msg_mic": "🎙️ صف أعراضك بالصوت أو اكتبها أدناه:",
        "placeholder": "مثال: أعاني من صداع شديد منذ أمس...", "btn_enviar": "إرسال للطبيب",
        "procesando": "⏳ جاري الاستماع وترجمة الأعراض...",
        "msg_exito": "✅ تم إرسال الأعراض وترجمتها للطبيب.", "msg_vacio": "⚠️ يرجى كتابة أو تسجيل الأعراض."
    }
}

def escuchar_y_traducir(texto, audio_file, idioma):
    prompt = (
        f"Eres un asistente de triaje hospitalario en México. El paciente habla '{idioma}'. "
        "Escucha el audio o lee el texto y devuelve un JSON con dos claves exactas: "
        "'sintomas' (transcripción exacta de lo que dijo el paciente traducida al español claro) y "
        "'rec' (acción operativa breve para enfermería en español, sin dar diagnósticos)."
    )
    contenidos = [prompt]
    if texto.strip():
        contenidos.append(texto.strip())
    if audio_file is not None:
        tipo_mime = audio_file.type or "audio/wav"
        contenidos.append(types.Part.from_bytes(data=audio_file.getvalue(), mime_type=tipo_mime))

    try:
        disponibles = [
            m.name.replace("models/", "")
            for m in client.models.list()
            if "flash" in m.name.lower() and "image" not in m.name.lower() and "tts" not in m.name.lower()
        ]
        if not disponibles:
            disponibles = ["gemini-2.5-flash", "gemini-2.0-flash"]
    except Exception:
        disponibles = ["gemini-2.5-flash", "gemini-2.0-flash"]

    ultimo_error = ""
    for modelo in disponibles:
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

    return f"🎙️ Audio grabado (Info: {ultimo_error[:70]})", "Preparar intérprete y tomar signos vitales."

if "idioma" not in st.session_state:
    st.session_state.idioma = "Español"
if "nivel" not in st.session_state:
    st.session_state.nivel = None

vista_actual = st.query_params.get("vista", "paciente")

if vista_actual == "doctor":
    st.title("💻 NexoMed — Panel Doctor")
    st.caption("Vista exclusiva para recepción médica y personal de salud.")
    
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("🔄 Actualizar lista", type="primary"):
        st.rerun()
    if col_btn2.button("🗑️ Limpiar toda la lista"):
        cola_global.clear()
        st.rerun()

    if not cola_global:
        st.info("No hay pacientes en espera en este momento.")
    else:
        prioridad = {"ROJO": 1, "AMARILLO": 2, "VERDE": 3}
        pacientes_ordenados = sorted(cola_global, key=lambda x: prioridad[x["nivel"]])
        
        for idx, p in enumerate(pacientes_ordenados):
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                if p["nivel"] == "ROJO":
                    c1.error(f"🔴 **ROJO**\n\n🕒 {p['hora']}")
                elif p["nivel"] == "AMARILLO":
                    c1.warning(f"🟡 **AMARILLO**\n\n🕒 {p['hora']}")
                else:
                    c1.success(f"🟢 **VERDE**\n\n🕒 {p['hora']}")
                c2.write(f"**Idioma:** {p['idioma']}\n\n**Síntomas traducidos:** {p['sintomas']}")
                if p["audio_bytes"] is not None:
                    c2.audio(p["audio_bytes"], format=p["audio_mime"])
                c3.info(p["rec"])
if c3.button("✅ Marcar como atendido", key=f"atender_{idx}{p['hora']}"):
    cola_global.remove(p)
    st.rerun()
else:
t = TRADUCCIONES[st.session_state.idioma]
st.title("🏥 NexoMed")
st.caption(t["subtitulo"])
cols = st.columns(5)
for i, lang in enumerate(TRADUCCIONES.keys()):
if cols[i % 5].button(TRADUCCIONES[lang]["bandera"], key=f"b{lang}", use_container_width=True):
st.session_state.idioma = lang
st.session_state.nivel = None
st.rerun()
st.divider()
st.subheader(t["instruccion"])
if st.button(t["rojo"], type="primary", use_container_width=True):
st.session_state.nivel = "ROJO"
cola_global.append({"hora": datetime.now(ZONA_MX).strftime("%H:%M:%S"), "nivel": "ROJO", "idioma": st.session_state.idioma, "sintomas": "⚠️ ALERTA ROJA INMEDIATA", "rec": "🚨 Atención inmediata en sala de choque.", "audio_bytes": None, "audio_mime": None})
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
b_audio = voz.getvalue() if voz is not None else None
m_audio = (voz.type or "audio/wav") if voz is not None else None
cola_global.append({"hora": datetime.now(ZONA_MX).strftime("%H:%M:%S"), "nivel": st.session_state.nivel, "idioma": st.session_state.idioma, "sintomas": sintomas_es, "rec": rec_es, "audio_bytes": b_audio, "audio_mime": m_audio})
st.success(t["msg_exito"])
else:
st.warning(t["msg_vacio"])
