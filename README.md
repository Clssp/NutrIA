🥗🎙️ Nutri-Voz: Seu Assistente de Nutrição com IA

Nutri-Voz é um assistente de nutrição pessoal, construído com Python e Streamlit, que usa a IA multimodal do Google Gemini para analisar refeições a partir de fotos e a API da ElevenLabs para fornecer feedback por voz de alta qualidade.

Este projeto funciona como um diário alimentar inteligente: permite registrar suas refeições, receber análises nutricionais detalhadas e acompanhar seu progresso em direção a metas de saúde personalizadas.

Dica: Tire uma screenshot da aplicação funcionando, hospede em um site como Imgur e cole o link direto aqui para ilustrar o README!

✨ Funcionalidades Principais
✅ Análise de Refeições por Imagem
Envie uma foto do seu prato e a IA do Gemini identificará os alimentos, estimando calorias e macronutrientes.

✅ Assistente por Voz Personalizado
Receba feedback e relatórios com voz natural, fornecida pela ElevenLabs. O usuário pode escolher a voz do assistente.

✅ Dashboard de Acompanhamento
Painel na barra lateral mostra o progresso diário em relação às metas de calorias e proteínas.

✅ Perfil de Usuário e Metas
Defina peso, altura, nível de atividade e objetivos (perder peso, manter, ganhar massa) para conselhos personalizados.

✅ Gamificação
Mantenha-se motivado com contador de sequência (streak) de registros diários e conquistas ao atingir metas.

✅ Histórico e Relatórios
Converse com seu histórico alimentar ("Quantas calorias consumi ontem?") e gere relatórios semanais.

✅ Design Responsivo
Interface otimizada para uso em desktops e dispositivos móveis.

🛠️ Tecnologias Utilizadas
Frontend: Streamlit

IA (Imagem e Texto): Google Gemini (API)

Síntese de Voz (TTS): ElevenLabs (API)

Manipulação de Dados: Pandas

Linguagem: Python 3.11+

🚀 Como Executar o Projeto Localmente
Pré-requisitos
Python 3.11 ou superior

pip (gerenciador de pacotes do Python)

Conta e chave de API do Google AI Studio (Gemini)

Conta e chave de API do ElevenLabs

Git instalado

1️⃣ Clonar o Repositório
bash
Copiar
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
2️⃣ Instalar as Dependências
É altamente recomendado usar um ambiente virtual:

bash
Copiar
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Windows:
venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
3️⃣ Configurar as Chaves de API (Secrets)
Use o gerenciador de segredos do Streamlit para proteger suas chaves:

Crie a pasta .streamlit na raiz do projeto (se não existir).

Crie o arquivo .streamlit/secrets.toml com o conteúdo:

toml
Copiar
GOOGLE_API_KEY = "SUA_CHAVE_API_DO_GEMINI_AQUI"
ELEVENLABS_API_KEY = "SUA_CHAVE_API_DA_ELEVENLABS_AQUI"
4️⃣ Executar a Aplicação
bash
Copiar
streamlit run app.py
A aplicação será aberta automaticamente no navegador em http://localhost:8501.

☁️ Deploy no Streamlit Community Cloud
Suba seu código para o GitHub:
Inclua app.py, requirements.txt e um .gitignore que exclua dados e arquivos de secrets.

Crie uma conta em Streamlit Community Cloud:
Clique em “New app”, conecte seu repositório e selecione app.py como arquivo principal.

Adicione os Secrets:
Cole o conteúdo do seu secrets.toml na caixa "Secrets" nas configurações avançadas.

Clique em "Deploy!" e aguarde a mágica acontecer.

🎨 Personalização
Este projeto foi feito para ser seu! Personalize como quiser:

Aparência: Modifique .streamlit/config.toml para alterar o tema de cores.

Personalidade da IA: Edite PROMPT_BASE_REFEICAO e PROMPT_HISTORICO em app.py para mudar o tom do assistente.

Vozes: Adicione vozes personalizadas no dicionário VOICE_OPTIONS em app.py.

💡 Pronto! Agora é só começar a usar o Nutri-Voz e acompanhar sua evolução nutricional de forma prática e divertida.
