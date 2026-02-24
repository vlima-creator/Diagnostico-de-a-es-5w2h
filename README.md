# 5W2H - Diagnóstico de Ações

Ferramenta Streamlit para planejamento estratégico em reuniões de start com clientes usando a metodologia 5W2H.

## Funcionalidades

- **Captura de Ações**: Seleção de 20 ações pré-definidas com customização
- **Cálculo Automático**: Score baseado em impacto vs esforço
- **Plano 5W2H**: Visualização completa com What, Why, Where, How
- **Análise**: Métricas e distribuição por categoria
- **Gestão**: Adicionar, visualizar e remover ações

## Como Usar

1. Digite o nome do cliente na barra lateral
2. Selecione uma ação do banco
3. Customize impacto, esforço, duração e responsável
4. Clique em "Adicionar Ação"
5. Visualize o plano completo na aba "Visualizar"
6. Analise métricas na aba "Análise"

## Instalação

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tecnologias

- Streamlit 1.28.1
- Pandas 2.0.3
- Python 3.8+

## Metodologia 5W2H

- **What**: O quê será feito?
- **Why**: Por quê fazer?
- **Where**: Onde será feito?
- **How**: Como será feito?
- **When**: Quando será feito?
- **Who**: Quem fará?
- **How Much**: Quanto custará?

## Score

Score = (Impacto × 10) - (Esforço × 2)

Quanto maior o score, maior a prioridade.
