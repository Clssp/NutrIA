import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import plotly.express as px
import json
from datetime import datetime, timedelta
import os
from elevenlabs.client import ElevenLabs

# --- Configuração da Página e das APIs ---
st.set_page_config(
    page_title="Nutri-Voz 🎙️",
    page_icon="🥗",
    layout="centered"
)

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    elevenlabs_client = ElevenLabs(api_key=st.secrets["ELEVENLABS_API_KEY"])
except Exception as e:
    st.error(f"Erro ao configurar chaves de API. Verifique seu arquivo secrets.toml. Detalhe: {e}")
    st.stop()

# --- Constantes, Vozes e Funções de Dados ---
CSV_FILE = 'diario_alimentar.csv'
PROFILE_FILE = 'perfil.json'
CSV_COLUMNS = ['timestamp','data','hora','tipo_refeicao','alimentos_identificados','peso_estimado_g','calorias_kcal','proteinas_g','carboidratos_g','gorduras_g','fibras_g','sodio_mg','resumo_ia']

# PERSONALIZAÇÃO: Altere os nomes e IDs para as vozes da SUA conta ElevenLabs
VOICE_OPTIONS = {
    "Bia (Coach Motivacional)": "Eyspt3SYhZzXd1Jd3J8O", # Exemplo
    "Dr. Arthur (Voz Sábia)": "x3mAOLD9WzlmrFCwA1S3",   # Exemplo
    "Carla (Clara e Profissional)": "oJebhZNaPllxk6W0LSBA" # Exemplo
}

def init_csv():
    if not os.path.exists(CSV_FILE): pd.DataFrame(columns=CSV_COLUMNS).to_csv(CSV_FILE, index=False)
    
def init_profile():
    if not os.path.exists(PROFILE_FILE):
        primeira_voz_valida = list(VOICE_OPTIONS.keys())[0]
        default_profile = {"peso_kg": 70.0, "altura_cm": 175, "genero": "Masculino", "objetivo": "Manter o Peso", "nivel_atividade": "Levemente Ativo", "voice_name": primeira_voz_valida}
        with open(PROFILE_FILE, 'w') as f: json.dump(default_profile, f)
    with open(PROFILE_FILE, 'r') as f: return json.load(f)
    
def save_profile(data):
    with open(PROFILE_FILE, 'w') as f: json.dump(data, f, indent=4)
    
def adicionar_refeicao_csv(data):
    pd.DataFrame([data]).to_csv(CSV_FILE, mode='a', header=False, index=False)
    
def calculate_goals(profile):
    activity_factors = {"Sedentário": 1.2, "Levemente Ativo": 1.375, "Ativo": 1.55, "Muito Ativo": 1.725}
    if profile.get('genero', 'Masculino') == 'Masculino': tmb = 88.362 + (13.397 * profile.get('peso_kg', 70.0)) + (4.799 * profile.get('altura_cm', 175)) - (5.677 * 30)
    else: tmb = 447.593 + (9.247 * profile.get('peso_kg', 70.0)) + (3.098 * profile.get('altura_cm', 175)) - (4.330 * 30)
    tdee = tmb * activity_factors.get(profile.get('nivel_atividade'), 1.375)
    if profile.get('objetivo') == 'Perder Peso': calorie_goal = tdee - 400
    elif profile.get('objetivo') == 'Ganhar Massa Muscular': calorie_goal = tdee + 400
    else: calorie_goal = tdee
    protein_g, carbs_g, fat_g = (calorie_goal * 0.30) / 4, (calorie_goal * 0.40) / 4, (calorie_goal * 0.30) / 9
    return {"calorias": int(calorie_goal), "proteinas": int(protein_g), "carboidratos": int(carbs_g), "gorduras": int(fat_g)}
    
def get_streak_count(df):
    if df.empty: return 0
    df['data'] = pd.to_datetime(df['data']).dt.date
    unique_dates = sorted(df['data'].unique(), reverse=True)
    streak, today, yesterday = 0, datetime.now().date(), datetime.now().date() - timedelta(days=1)
    current_day_for_check = today
    if today not in unique_dates:
        if yesterday in unique_dates: current_day_for_check = yesterday
        else: return 0
    for i, date in enumerate(unique_dates):
        if date == current_day_for_check - timedelta(days=i): streak += 1
        else: break
    return streak

def text_to_audio_elevenlabs(text: str, voice_id: str):
    try:
        response = elevenlabs_client.text_to_speech.convert(voice_id=voice_id, text=text, model_id="eleven_multilingual_v2")
        audio_bytes = b"".join(response)
        return audio_bytes
    except Exception as e:
        st.error(f"Erro ao gerar áudio com ElevenLabs: {e}")
        return None

# --- Cérebro da IA (Modelos e Prompts) ---
model = genai.GenerativeModel('gemini-1.5-flash')

# PERSONALIZAÇÃO: Defina a personalidade da sua IA aqui!
PROMPT_BASE_REFEICAO = """
Você é a "Bia", uma nutricionista virtual com especialização em nutrição esportiva. Seu tom é motivacional, amigável e direto, como uma coach. Comece sempre de forma energética, como "E aí, campeão(ã)!" ou "Bora analisar essa máquina!". Você deve analisar a imagem de uma refeição, fornecer uma análise nutricional DETALHADA e conversar com o usuário, sempre considerando o perfil e objetivo dele.

PERFIL E OBJETIVO DO USUÁRIO:
{profile_summary}

INSTRUÇÕES:
1. **Análise Conversacional:** Comece com sua saudação energética. Comente sobre a refeição levando em conta o objetivo do usuário. Se o prato está alinhado com o objetivo, elogie e reforce o bom trabalho. Se não, dê uma sugestão construtiva e motivacional para a próxima refeição. Lembre que suas estimativas são aproximações.
2. **Análise JSON:** Após a conversa, forneça um bloco de dados JSON, começando com "---JSON---". Não adicione comentários no JSON. Use 0 se não conseguir estimar um valor.

ESTRUTURA JSON EXATA:
---JSON---
{{"alimentos_identificados": ["item1", "item2", "item3"],"peso_estimado_g": valor_numerico,"analise_nutricional": {{"calorias_kcal": valor_numerico, "proteinas_g": valor_numerico,"carboidratos_g": valor_numerico, "gorduras_g": valor_numerico,"fibras_g": valor_numerico, "sodio_mg": valor_numerico}}}}
"""
PROMPT_HISTORICO = """
Você é a "Bia", uma IA coach de nutrição. Responda à PERGUNTA DO USUÁRIO de forma amigável e direta, usando o CONTEXTO DE DADOS fornecido para dar uma resposta inteligente.

CONTEXTO DE DADOS (Resumo do diário alimentar):
{data_context}

PERGUNTA DO USUÁRIO:
"{user_question}"
"""

init_csv()
user_profile = init_profile()
goals = calculate_goals(user_profile)
try:
    df_full = pd.read_csv(CSV_FILE, header=0, on_bad_lines='warn')
except (pd.errors.EmptyDataError, FileNotFoundError):
    df_full = pd.DataFrame(columns=CSV_COLUMNS)
if "messages" not in st.session_state: st.session_state.messages = []

def process_and_display_response(response_text: str, role: str = "assistant"):
    with st.chat_message(role, avatar="🤖"):
        st.markdown(response_text)
        selected_voice_name = user_profile.get("voice_name", list(VOICE_OPTIONS.keys())[0])
        voice_id = VOICE_OPTIONS[selected_voice_name]
        audio_data = text_to_audio_elevenlabs(response_text, voice_id)
        if audio_data:
            st.audio(audio_data, autoplay=True)
    if role == 'assistant':
        st.session_state.messages.append({"role": role, "content": response_text})

with st.sidebar:
    st.title("🤖 Painel do Nutri-Voz")
    with st.expander("👤 Meu Perfil e Metas", expanded=True):
        f_peso = st.number_input("Meu Peso (kg)", value=float(user_profile.get('peso_kg', 70.0)), min_value=30.0, max_value=300.0, step=0.5, format="%.1f")
        f_altura = st.number_input("Minha Altura (cm)", value=user_profile.get('altura_cm', 175), min_value=100, max_value=250)
        f_genero = st.radio("Gênero Biológico", ["Masculino", "Feminino"], index=["Masculino", "Feminino"].index(user_profile.get('genero', 'Masculino')))
        f_objetivo = st.selectbox("Meu Objetivo", ["Perder Peso", "Manter o Peso", "Ganhar Massa Muscular"], index=["Perder Peso", "Manter o Peso", "Ganhar Massa Muscular"].index(user_profile.get('objetivo', 'Manter o Peso')))
        f_atividade = st.selectbox("Nível de Atividade", ["Sedentário", "Levemente Ativo", "Ativo", "Muito Ativo"], index=["Sedentário", "Levemente Ativo", "Ativo", "Muito Ativo"].index(user_profile.get('nivel_atividade', 'Levemente Ativo')))
        
        voice_keys = list(VOICE_OPTIONS.keys())
        current_voice_name = user_profile.get("voice_name", voice_keys[0])
        if current_voice_name not in voice_keys: current_voice_name = voice_keys[0]
        f_voice_name = st.selectbox("Voz do Assistente", options=voice_keys, index=voice_keys.index(current_voice_name))

        if st.button("Salvar Perfil"):
            user_profile = {"peso_kg": f_peso, "altura_cm": f_altura, "genero": f_genero, "objetivo": f_objetivo, "nivel_atividade": f_atividade, "voice_name": f_voice_name}
            save_profile(user_profile)
            st.success("Perfil salvo!")
            st.rerun()

    st.markdown("---")
    st.markdown("##### Suas Metas Diárias:")
    st.markdown(f"**Calorias:** `{goals.get('calorias', 0)}` kcal | **Proteínas:** `{goals.get('proteinas', 0)}` g")
    st.markdown(f"**Carboidratos:** `{goals.get('carboidratos', 0)}` g | **Gorduras:** `{goals.get('gorduras', 0)}` g")
    
    st.markdown("---")
    st.subheader("📊 Dashboard do Dia")
    if not df_full.empty: df_full['data'] = pd.to_datetime(df_full['data']).dt.date
    today = datetime.now().date()
    df_today = df_full[df_full['data'] == today] if not df_full.empty else pd.DataFrame(columns=CSV_COLUMNS)

    if df_today.empty: st.info("Nenhuma refeição registrada hoje.")
    else:
        cals_today, prot_today = df_today['calorias_kcal'].sum(), df_today['proteinas_g'].sum()
        st.markdown("**Calorias**")
        st.progress(min(cals_today / goals.get('calorias', 1), 1.0), text=f"{int(cals_today)} / {goals.get('calorias', 'N/A')} kcal")
        st.markdown("**Proteínas**")
        st.progress(min(prot_today / goals.get('proteinas', 1), 1.0), text=f"{int(prot_today)} / {goals.get('proteinas', 'N/A')} g")

    st.markdown("---")
    st.subheader("🏆 Gamificação")
    streak = get_streak_count(df_full)
    st.metric("🔥 Sequência de Registros", f"{streak} Dias")
    if not df_today.empty:
      if (cals_today >= goals.get('calorias', float('inf'))): st.success("🏆 Conquista: Meta de calorias batida!")
      if (prot_today >= goals.get('proteinas', float('inf'))): st.success("💪 Conquista: Meta de proteínas batida!")

    st.markdown("---")
    if st.button("📜 Gerar Relatório Semanal"):
        with st.spinner("Analisando sua semana..."):
            if df_full.empty: st.warning("Não há dados para gerar o relatório.")
            else:
                seven_days_ago = today - timedelta(days=7)
                df_week = df_full[df_full['data'] >= seven_days_ago]
                if df_week.empty: st.warning("Não há dados suficientes na última semana.")
                else:
                    avg_cals = df_week.groupby('data')['calorias_kcal'].sum().mean()
                    avg_prot = df_week.groupby('data')['proteinas_g'].sum().mean()
                    contexto_semanal = f"- Média de calorias: {int(avg_cals)} kcal (Meta: {goals['calorias']} kcal)\n- Média de proteínas: {int(avg_prot)} g (Meta: {goals['proteinas']} g)\n- Refeições na semana: {len(df_week)}"
                    prompt_relatorio = PROMPT_HISTORICO.format(data_context=contexto_semanal, user_question="Crie um relatório semanal amigável para mim com base nestes dados, destacando um ponto positivo e um ponto a melhorar.")
                    report_response = model.generate_content(prompt_relatorio)
                    st.session_state.last_response_text = report_response.text
                    st.rerun()

# --- Layout Principal Otimizado para Mobile ---
# PERSONALIZAÇÃO: Adicione seu logo aqui. Crie um arquivo 'logo.png'
if os.path.exists("logo.png"):
    st.image("logo.png", width=100)

st.title("🥗 Nutri-Voz")
st.markdown("`Seu assistente de nutrição pessoal com IA`")

with st.expander("➕ Registrar Nova Refeição", expanded=True):
    with st.form(key="meal_form", clear_on_submit=True):
        tipo_refeicao = st.selectbox("Qual refeição é esta?", ("Café da Manhã", "Almoço", "Jantar", "Lanche"))
        uploaded_file = st.file_uploader("Envie a foto do seu prato", type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Analisar e Registrar Refeição")
        
        if submitted and uploaded_file is not None:
            image = Image.open(uploaded_file)
            user_message_content = f"Analisando meu **{tipo_refeicao}**..."
            st.session_state.messages.append({"role": "user", "content": user_message_content, "image": image})
            with st.spinner("Análise completa em andamento..."):
                profile_summary = f"- Gênero: {user_profile.get('genero')}\n- Objetivo: {user_profile['objetivo']}\n- Meta de Calorias: {goals['calorias']} kcal\n- Meta de Proteínas: {goals['proteinas']} g"
                prompt_final_refeicao = PROMPT_BASE_REFEICAO.format(profile_summary=profile_summary)
                try:
                    response = model.generate_content([prompt_final_refeicao, image])
                    parts = response.text.split("---JSON---")
                    if len(parts) == 2:
                        conversational_part, json_part_str = parts[0].strip(), parts[1].strip()
                        st.session_state.last_response_text = conversational_part
                        try:
                            json_data = json.loads(json_part_str)
                            now = datetime.now()
                            nutri_data = json_data.get('analise_nutricional', {})
                            new_row = {'timestamp': now, 'data': now.strftime('%Y-%m-%d'), 'hora': now.strftime('%H:%M:%S'), 'tipo_refeicao': tipo_refeicao, 'alimentos_identificados': ', '.join(json_data.get('alimentos_identificados', [])), 'peso_estimado_g': json_data.get('peso_estimado_g', 0), 'calorias_kcal': nutri_data.get('calorias_kcal', 0), 'proteinas_g': nutri_data.get('proteinas_g', 0), 'carboidratos_g': nutri_data.get('carboidratos_g', 0), 'gorduras_g': nutri_data.get('gorduras_g', 0), 'fibras_g': nutri_data.get('fibras_g', 0), 'sodio_mg': nutri_data.get('sodio_mg', 0), 'resumo_ia': conversational_part}
                            adicionar_refeicao_csv(new_row)
                        except json.JSONDecodeError:
                            print(f"Aviso: A IA não retornou um JSON válido. Resposta recebida: {json_part_str}")
                    else:
                        st.session_state.last_response_text = response.text
                        print(f"Aviso: A IA não seguiu o formato de resposta com '---JSON---'. Resposta completa: {response.text}")
                except Exception as e:
                    st.session_state.last_response_text = f"Ocorreu um erro na chamada da API do Gemini: {e}"
            st.rerun()

st.markdown("---")

st.header("💬 Histórico da Conversa")
if "last_response_text" in st.session_state:
    process_and_display_response(st.session_state.last_response_text)
    del st.session_state.last_response_text

with st.container(height=400, border=False): # Container com scroll para o chat
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "🤖"):
            if "image" in message:
                st.image(message["image"], width=150)
            st.markdown(message["content"])

if prompt := st.chat_input("Pergunte sobre seu histórico..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Atualiza o display imediatamente para melhor UX
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    with st.spinner("Consultando seu diário e preparando a resposta..."):
        contexto_dados = "Não há  no histórico." if df_full.empty else df_full.tail(20).to_string()
        prompt_final = PROMPT_HISTORICO.format(data_context=contexto_dados, user_question=prompt)
        response = model.generate_content(prompt_final)
        st.session_state.last_response_text = response.text
        st.rerun()