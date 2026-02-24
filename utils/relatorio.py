"""
Módulo para geração de relatórios em Excel.
"""
import io
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd


class GeradorRelatorio:
    """Classe para gerar relatórios em Excel."""
    
    def __init__(self):
        """Inicializa o gerador de relatórios."""
        pass
    
    def gerar_excel(
        self,
        cliente: str,
        acoes: List[Dict[str, Any]],
        metricas: Dict[str, Any]
    ) -> bytes:
        """
        Gera um relatório em Excel.
        
        Args:
            cliente: Nome do cliente
            acoes: Lista de ações do plano
            metricas: Métricas agregadas do plano
        
        Returns:
            Bytes do arquivo Excel gerado
        """
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Aba 1: Resumo
            resumo_df = pd.DataFrame([
                {"Métrica": "Total de Ações", "Valor": metricas.get("total_acoes", 0)},
                {"Métrica": "Score Total", "Valor": metricas.get("score_total", 0)},
                {"Métrica": "Score Médio", "Valor": metricas.get("score_medio", 0)},
                {"Métrica": "Custo Total (R$)", "Valor": metricas.get("custo_total", 0)},
                {"Métrica": "Duração Total (dias)", "Valor": metricas.get("duracao_total_dias", 0)},
                {"Métrica": "Impacto Total", "Valor": metricas.get("impacto_total", 0)},
                {"Métrica": "Esforço Total", "Valor": metricas.get("esforco_total", 0)}
            ])
            resumo_df.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Aba 2: Ações
            acoes_df = pd.DataFrame([
                {
                    "ID": idx,
                    "Ação": acao.get("acao", ""),
                    "Categoria": acao.get("categoria", ""),
                    "Responsável": acao.get("responsavel", ""),
                    "Data Início": acao.get("data_inicio", "").strftime("%d/%m/%Y") if isinstance(acao.get("data_inicio"), datetime) else "",
                    "Data Fim": acao.get("data_fim", "").strftime("%d/%m/%Y") if isinstance(acao.get("data_fim"), datetime) else "",
                    "Duração (dias)": acao.get("duracao_dias", ""),
                    "Custo (R$)": acao.get("custo", 0),
                    "Impacto": acao.get("impacto", ""),
                    "Esforço": acao.get("esforco", ""),
                    "Score": acao.get("score", ""),
                    "Prioridade": acao.get("prioridade", ""),
                    "Status": acao.get("status", ""),
                    "% Execução": acao.get("percentual_execucao", 0),
                    "Notas": acao.get("notas", "")
                }
                for idx, acao in enumerate(acoes, 1)
            ])
            acoes_df.to_excel(writer, sheet_name='Ações', index=False)
            
            # Aba 3: Detalhes 5W2H
            detalhes_data = []
            for acao in acoes:
                detalhes_data.append({
                    "Ação": acao.get("acao", ""),
                    "What": acao.get("what", ""),
                    "Why": acao.get("why", ""),
                    "Where": acao.get("where", ""),
                    "How": acao.get("how", ""),
                    "Indicadores": acao.get("indicadores", "")
                })
            
            detalhes_df = pd.DataFrame(detalhes_data)
            detalhes_df.to_excel(writer, sheet_name='5W2H Detalhes', index=False)
            
            # Aba 4: Distribuição por Categoria
            categoria_data = [
                {"Categoria": cat, "Quantidade": qtd}
                for cat, qtd in metricas.get("acoes_por_categoria", {}).items()
            ]
            categoria_df = pd.DataFrame(categoria_data)
            categoria_df.to_excel(writer, sheet_name='Por Categoria', index=False)
            
            # Aba 5: Distribuição por Prioridade
            prioridade_data = [
                {"Prioridade": pri, "Quantidade": qtd}
                for pri, qtd in metricas.get("acoes_por_prioridade", {}).items()
            ]
            prioridade_df = pd.DataFrame(prioridade_data)
            prioridade_df.to_excel(writer, sheet_name='Por Prioridade', index=False)
        
        buffer.seek(0)
        return buffer.getvalue()
