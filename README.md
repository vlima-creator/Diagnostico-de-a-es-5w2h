# 📋 Diagnóstico de Ações 5W2H

Uma ferramenta Streamlit para diagnóstico e planejamento de ações utilizando a metodologia **5W2H** em reuniões de start com clientes.

## 🎯 Objetivo

Este aplicativo permite que consultores e gestores:

1. **Capturem ações** durante reuniões de start com clientes
2. **Apliquem a metodologia 5W2H** automaticamente a cada ação
3. **Calculem scores de prioridade** baseados em impacto e esforço
4. **Visualizem o plano completo** em diferentes formatos
5. **Gerem relatórios** em PDF e Excel para apresentação ao cliente

## 📊 Metodologia 5W2H

A metodologia 5W2H responde a 7 perguntas fundamentais para cada ação:

- **What (O quê)?** - Descrição clara da ação
- **Why (Por quê)?** - Justificativa e benefício esperado
- **Where (Onde)?** - Local ou contexto de execução
- **How (Como)?** - Passo a passo da execução
- **How Much (Quanto custa)?** - Custo estimado
- **When (Quando)?** - Data de início e duração
- **Who (Quem)?** - Responsável pela execução

## 🚀 Funcionalidades

### 📝 Captura de Ações
- Seleção de ações pré-definidas em um banco de dados
- Customização de impacto, esforço e custo
- Preenchimento de informações adicionais (responsável, notas, status)
- Cálculo automático de datas de início e fim

### 📊 Plano 5W2H
- Visualização completa de todas as ações capturadas
- Tabela resumida com informações principais
- Detalhes expandidos de cada ação com 5W2H completo
- Remoção de ações do plano

### 📈 Análise
- Distribuição de ações por categoria
- Distribuição de ações por prioridade
- Timeline das ações (Gantt simplificado)
- Análise de scores (máximo, mínimo, médio, total)

### 📥 Relatórios
- **PDF**: Relatório profissional com resumo executivo e detalhes de cada ação
- **Excel**: Múltiplas abas com resumo, ações, 5W2H, categorias e prioridades

## 📦 Banco de Ações

O aplicativo inclui um banco pré-configurado com 20 ações em categorias:

- **Precificação**: Ajustar precificação
- **Pessoas**: Contratar colaborador, Contratar RP
- **Canais**: Utilização de canal, Entrada em novo canal
- **Operação**: Ativar fulfillment, Gestão de atendimento, Expedição, Entrada de produtos
- **Mídia**: Ativar publicidade, Ads e campanhas
- **Comercial**: Trabalhar com promoções
- **Catálogo**: Melhorar conteúdo, Padronização de anúncios, Padronização de cadastros
- **Gestão**: Implantar rotina de indicadores, Rotinas e processos, Analisar curva ABC
- **Compras**: Gestão de compras, Compras

## 🔧 Fórmula de Score

O score de cada ação é calculado como:

```
Score = (Impacto × Peso_Impacto) - (Esforço × Peso_Esforço)
```

**Pesos padrão:**
- Peso Impacto: 10
- Peso Esforço: 2

**Classificação de Prioridade:**
- **Crítica (P0)**: Score ≥ 35
- **Alta (P1)**: Score ≥ 25
- **Média (P2)**: Score ≥ 15
- **Baixa (P3)**: Score ≥ 5
- **Muito Baixa (P4)**: Score < 5

## 📋 Estrutura do Projeto

```
Diagnostico-de-a-es-5w2h/
├── app.py                    # Aplicação principal Streamlit
├── requirements.txt          # Dependências do projeto
├── README.md                 # Este arquivo
├── .gitignore               # Arquivo de exclusão Git
├── data/
│   └── acoes.json          # Banco de ações em JSON
└── utils/
    ├── __init__.py
    ├── calculadora.py      # Lógica de cálculo de score e 5W2H
    └── relatorio.py        # Geração de relatórios PDF e Excel
```

## 🛠️ Instalação

### Pré-requisitos
- Python 3.8+
- pip ou conda

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/vlima-creator/Diagnostico-de-a-es-5w2h.git
cd Diagnostico-de-a-es-5w2h
```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 🚀 Como Usar

### Executar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`.

### Fluxo de Uso

1. **Configure o cliente** na barra lateral
2. **Selecione a data da reunião**
3. **Vá para a aba "Captura de Ações"**
4. **Selecione uma ação** do banco de dados
5. **Customize** impacto, esforço e custo (se necessário)
6. **Preencha** responsável e notas
7. **Clique em "Adicionar Ação"**
8. **Repita** para todas as ações da reunião
9. **Visualize** o plano na aba "Plano 5W2H"
10. **Analise** na aba "Análise"
11. **Gere relatórios** na aba "Relatórios"

## 📊 Exemplo de Saída

### Relatório PDF
- Título com nome do cliente e data
- Resumo executivo com métricas
- Distribuição por categoria
- Detalhes completos de cada ação com 5W2H

### Relatório Excel
- **Aba Resumo**: Métricas agregadas
- **Aba Ações**: Tabela com todas as ações
- **Aba 5W2H Detalhes**: Detalhes completos de cada ação
- **Aba Por Categoria**: Distribuição por categoria
- **Aba Por Prioridade**: Distribuição por prioridade

## 🎨 Customização

### Modificar Pesos de Score

Na barra lateral, ajuste os pesos de impacto e esforço em tempo real.

### Adicionar Novas Ações

Edite o arquivo `data/acoes.json` e adicione novas ações ao array `acoes`:

```json
{
  "id": 21,
  "acao": "Nome da Ação",
  "categoria": "Categoria",
  "what": "O quê?",
  "why": "Por quê?",
  "where": "Onde?",
  "how": "Como?",
  "indicadores": "Indicadores",
  "dia_inicio_padrao": 1,
  "duracao_dias": 7,
  "custo_padrao": 0,
  "impacto_padrao": 3,
  "esforco_padrao": 3
}
```

### Modificar Configurações

Edite o arquivo `data/acoes.json` e ajuste a seção `config`:

```json
"config": {
  "peso_impacto": 10,
  "peso_esforco": 2,
  "dias_ciclo": 30,
  "horas_por_dia": 8
}
```

## 📚 Dependências

- **streamlit**: Framework web para criar aplicações interativas
- **pandas**: Manipulação e análise de dados
- **openpyxl**: Criação de arquivos Excel
- **reportlab**: Geração de relatórios PDF
- **python-dateutil**: Utilitários para datas

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Fazer commit das mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Fazer push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.

## 👤 Autor

Desenvolvido para otimizar reuniões de start com clientes e planejamento estratégico.

## 📧 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório GitHub.

---

**Versão**: 1.0  
**Última atualização**: Fevereiro de 2026
