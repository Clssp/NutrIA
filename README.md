Nutri-Voz: Seu Assistente de Nutrição com IA 🥗🎙️
Nutri-Voz é um assistente de nutrição pessoal, construído com Python e Streamlit, que utiliza a IA multimodal do Google Gemini para analisar refeições a partir de fotos e a API da ElevenLabs para fornecer feedback por voz de alta qualidade.
Este projeto funciona como um diário alimentar inteligente, permitindo que o usuário registre suas refeições, receba análises nutricionais detalhadas e acompanhe seu progresso em direção a metas de saúde personalizadas.
(Dica: Tire uma screenshot da sua aplicação funcionando, suba para um site como o Imgur e cole o link direto da imagem aqui)
✨ Funcionalidades Principais
Análise de Refeições por Imagem: Envie uma foto do seu prato e a IA do Gemini identificará os alimentos, estimando calorias e macronutrientes.
Assistente por Voz Personalizado: Receba feedback e relatórios com uma voz natural e de alta qualidade, fornecida pela ElevenLabs. O usuário pode escolher a voz do seu assistente.
Dashboard de Acompanhamento: Um painel de controle na barra lateral mostra o progresso diário em relação às metas de calorias e proteínas.
Perfil de Usuário e Metas: Defina seu peso, altura, nível de atividade e objetivos (perder peso, manter, ganhar massa) para receber conselhos personalizados.
Gamificação: Mantenha-se motivado com um contador de "sequência" (streak) de registros diários e conquistas ao atingir metas.
Histórico e Relatórios: Converse com seu histórico alimentar ("Quantas calorias consumi ontem?") e gere relatórios semanais com pontos positivos e de melhoria.
Design Responsivo: A interface é otimizada para uma excelente experiência tanto em desktops quanto em dispositivos móveis.
🛠️ Tecnologias Utilizadas
Frontend: Streamlit
IA (Análise de Imagem e Texto): Google Gemini (API)
Síntese de Voz (TTS): ElevenLabs (API)
Manipulação de Dados: Pandas
Linguagem: Python 3.11+
🚀 Como Executar o Projeto Localmente
Siga estes passos para configurar e rodar o Nutri-Voz em sua máquina local.
1. Pré-requisitos
Python 3.11 ou superior instalado.
pip (gerenciador de pacotes do Python).
Uma conta e chave de API do Google AI Studio (Gemini).
Uma conta e chave de API da ElevenLabs.
Git instalado (para clonar o repositório).
2. Clonar o Repositório
Generated bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
Use code with caution.
Bash
3. Instalar as Dependências
É altamente recomendado usar um ambiente virtual para evitar conflitos de pacotes.
Generated bash
# Criar um ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ativar o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

# Instalar os pacotes necessários
pip install -r requirements.txt
Use code with caution.
Bash
4. Configurar as Chaves de API (Secrets)
Este projeto usa o gerenciador de segredos do Streamlit para proteger suas chaves de API.
Crie uma pasta chamada .streamlit na raiz do projeto, caso ela não exista.
Dentro da pasta .streamlit, crie um arquivo chamado secrets.toml.
Adicione suas chaves de API a este arquivo:
Generated toml
# .streamlit/secrets.toml

GOOGLE_API_KEY = "SUA_CHAVE_API_DO_GEMINI_AQUI"
ELEVENLABS_API_KEY = "SUA_CHAVE_API_DA_ELEVENLABS_AQUI"
Use code with caution.
Toml
5. Executar a Aplicação
Com as dependências instaladas e as chaves configuradas, inicie a aplicação com o seguinte comando:
Generated bash
streamlit run app.py
Use code with caution.
Bash
A aplicação será aberta automaticamente no seu navegador padrão no endereço http://localhost:8501.
☁️ Deploy no Streamlit Community Cloud
Para tornar seu assistente acessível de qualquer lugar, você pode fazer o deploy gratuito na nuvem do Streamlit.
Envie seu código para o GitHub: Certifique-se de que seu código (incluindo app.py, requirements.txt e um .gitignore que ignore os arquivos de dados e secrets) está em um repositório do GitHub.
Crie uma conta: Acesse share.streamlit.io e crie uma conta.
"New app": Clique para criar uma nova aplicação, conecte seu repositório do GitHub e selecione o arquivo principal (app.py).
Adicione os Secrets: Nas configurações avançadas, cole o conteúdo do seu arquivo secrets.toml na caixa de texto "Secrets".
Clique em "Deploy!" e aguarde a mágica acontecer.
🎨 Personalização
Este projeto foi feito para ser seu! Sinta-se à vontade para personalizar:
Aparência: Modifique o arquivo .streamlit/config.toml (crie-o se não existir) para alterar o tema de cores.
Personalidade da IA: Edite as variáveis PROMPT_BASE_REFEICAO e PROMPT_HISTORICO no arquivo app.py para dar um novo tom e personalidade ao seu assistente.
Vozes: Adicione suas próprias vozes (clonadas ou da biblioteca) da ElevenLabs ao dicionário VOICE_OPTIONS no app.py.