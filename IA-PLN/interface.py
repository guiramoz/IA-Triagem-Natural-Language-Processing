import streamlit as st
import joblib
import spacy
import pandas as pd
from pathlib import Path

#configuração de página (título e icone)
st.set_page_config(page_title="Triagem de chamados",page_icon="👨🏽‍💻")

#carregamento de recursos -> em cache para que não seja nescessário
#recarregar a cada clique
@st.cache_resource
def carregar_modelo():
    caminho_modelo = Path(__file__).resolve().parent / "modelo_triagem_suporte.pkl"
    return joblib.load(caminho_modelo) #carregamento do modelo ML treinado

@st.cache_resource
def carregar_nlp():
    nlp_model = spacy.load("pt_core_news_sm")
    if nlp_model is None:
        raise ValueError("Erro ao carregar o modelo")
    return nlp_model
    
try:
    modelo = carregar_modelo()
    nlp = carregar_nlp()
    
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    st.stop()


#lógica de processamento
def analisar_chamado(texto_usuario):

    #1.processamento linguistico com spacy
    doc = nlp(texto_usuario)

    #2.extração de entidades nomeadas (ex.: AWS, locais, equipamentos e etc.)
    entidades = [(ent.text,ent.label_) for ent in doc.ents]
    #texto | rótulo
    #VPN   | acesso
    #notebook | hardware 

    #limpeza de texto pro modelo: lematizar, converter pra minusculo e remover pontuação
    texto_limpo = " ".join ([
        token.lemma_.lower()
        for token in doc
        if not token.is_punct
    ])

    #2. predição com o modelo de machine learning

    #prevê a categoria do chamado
    categoria_predita = modelo.predict([texto_limpo])[0]

    #probabilidade de cada categoria / classe
    probs = modelo.predict_proba([texto_limpo])[0]

    #pega a maior probabilidade como resultado da analise
    confianca = max(probs)*100

    #retorna os resultados
    return categoria_predita, confianca, entidades
    #[infra - 80% (maior prob), acesso - 65%, software - 30%]


#-----interface gráfica------
st.title("Triagem de suporte") #titulo da página
st.markdown("Descreva o problema em poucas palavras e um por vez.") # descrição

#criando o chat
if "messages" not in st.session_state:
    st.session_state.messages = []

#exibe mensagens anteriores no chat
for message in st.session_state.messages: #cria um armazenamento temporário para cada mensagem
    with st.chat_message(message["role"]): #criar um botão de chat visual
        st.markdown(message["content"]) #exibe o texto da mensagem dentro do balão

#exibir o campo de entrada para o usuário (chat input)
if prompt:= st.chat_input("Ex.: O servidor AWS parou de responder..."):

    st.chat_message('user').markdown(prompt)

    st.session_state.messages.append({
        "role":"user",
        "content": prompt
    })

    #processar a resposta que a IA (modelo ML) vai retornar ao usuário
    categoria, confianca, ents = analisar_chamado(prompt)

    #montar/personalizar a resposta em um formato amigável
    #3x" -> string com quebra de linha direto na identação
    resposta_md = f"""
**Análise do chamado:**
**Categoria:** `{categoria}`
**Confiança:** `{confianca:.2f}%`
"""

    if ents:
        resposta_md += "\n\n**Entidades detectadas:**"
        for ent in ents:
            resposta_md += f"\n- *{ent[0]}* ({ent[1]})"

    #ações automáticas por categoria
    acoes = {
        "infraestrutura": "Encaminhando para equipe N2",
        "Acesso": "Verificando logs de autentificação.",
        "Hardware":"Abrindo ordem de serviço.",
        "Software":"Verificando disponibilidade de licenças."
    }

    #adicionar as ações sugestidas com base na categoria
    resposta_md += f"\n\n**Ação:** {acoes.get(categoria, 'Triagem manual necessária.')}"
    
    #3. exibir a resposta do assistente
    with st.chat_message('assistant'):
        st.markdown(resposta_md)
        
    #salvar resposta no histórico
    st.session_state.messages.append({
        "role":"assistant",
        "content": resposta_md
    })


#ULTIMO PASSO: RODAR O STREAMLIT COM O COMANDO: streamlit run interface.py
