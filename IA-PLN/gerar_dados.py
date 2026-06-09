import pandas as pd
import random

# Categorias e seus vocabulários típicos
templates = {
    "Infraestrutura": [
        "O servidor {servidor} {problema_infra}",
        "Alta latência na {rede}",
        "Erro 500 na API de {servico}",
        "O cluster Kubernetes do {servico} caiu",
        "Disco cheio no servidor {servidor}"
    ],
    "Acesso": [
        "Esqueci minha senha do {sistema}",
        "Bloqueio de conta no {sistema}",
        "Preciso de permissão de admin no {sistema}",
        "Não consigo logar na VPN",
        "Token MFA inválido para o {sistema}"
    ],
    "Hardware": [
        "A impressora {lugar} está travada",
        "Meu monitor não liga",
        "Mouse parou de funcionar na estação {lugar}",
        "Notebook superaquecendo",
        "Preciso de um novo headset"
    ],
    "Software": [
        "Instalar o {soft} na minha máquina",
        "O {soft} fecha sozinho ao abrir",
        "Erro de licença no {soft}",
        "Atualizar versão do {soft}",
        "Tela azul ao abrir o {soft}"
    ]
}

variaveis = {
    "servidor": ["AWS Linux", "Azure DB", "Nginx", "Apache", "Tomcat"],
    "problema_infra": ["está fora do ar", "reiniciou sozinho", "não responde ping", "está com 100% CPU"],
    "rede": ["VLAN 10", "Subnet de Produção", "Rota do Firewall", "Conexão Wi-Fi"],
    "servico": ["Pagamento", "Auth", "Relatórios", "Logística"],
    "sistema": ["Jira", "Salesforce", "AD", "Email", "Slack"],
    "lugar": ["do 2º andar", "da recepção", "do financeiro", "da diretoria"],
    "soft": ["Excel", "VS Code", "Docker Desktop", "Photoshop", "Teams"]
}

def gerar_chamado_fake():
    categoria = random.choice(list(templates.keys()))
    template = random.choice(templates[categoria])
    
    # Preenche as variáveis do template aleatoriamente
    texto = template.format(
        servidor=random.choice(variaveis["servidor"]),
        problema_infra=random.choice(variaveis["problema_infra"]),
        rede=random.choice(variaveis["rede"]),
        servico=random.choice(variaveis["servico"]),
        sistema=random.choice(variaveis["sistema"]),
        lugar=random.choice(variaveis["lugar"]),
        soft=random.choice(variaveis["soft"])
    )
    return texto, categoria

# Gerar 3000 linhas
dados = [gerar_chamado_fake() for _ in range(3000)]
df = pd.DataFrame(dados, columns=["texto", "categoria"])

# Salvar em CSV
df.to_csv("dataset_chamados.csv", index=False)
print("✅ Arquivo 'dataset_chamados.csv' com 3000 registros criado com sucesso!")
