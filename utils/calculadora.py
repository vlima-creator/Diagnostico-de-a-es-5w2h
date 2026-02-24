"""
Módulo de cálculo de score e lógica 5W2H.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any


class Calculadora5W2H:
    """Classe para calcular scores e gerenciar lógica 5W2H."""
    
    def __init__(self, peso_impacto: int = 10, peso_esforco: int = 2):
        """
        Inicializa a calculadora com os pesos padrão.
        
        Args:
            peso_impacto: Peso do impacto na fórmula de score (padrão: 10)
            peso_esforco: Peso do esforço na fórmula de score (padrão: 2)
        """
        self.peso_impacto = peso_impacto
        self.peso_esforco = peso_esforco
    
    def calcular_score(self, impacto: int, esforco: int) -> float:
        """
        Calcula o score baseado em impacto e esforço.
        
        Fórmula: Score = (Impacto × Peso_Impacto) - (Esforço × Peso_Esforço)
        
        Args:
            impacto: Valor de impacto (1-5)
            esforco: Valor de esforço (1-5)
        
        Returns:
            Score calculado (float)
        """
        return (impacto * self.peso_impacto) - (esforco * self.peso_esforco)
    
    def calcular_data_fim(self, data_inicio: datetime, duracao_dias: int) -> datetime:
        """
        Calcula a data de fim baseada na data de início e duração.
        
        Args:
            data_inicio: Data de início (datetime)
            duracao_dias: Duração em dias (int)
        
        Returns:
            Data de fim (datetime)
        """
        return data_inicio + timedelta(days=duracao_dias)
    
    def classificar_prioridade(self, score: float) -> str:
        """
        Classifica a prioridade baseada no score.
        
        Args:
            score: Score da ação (float)
        
        Returns:
            Classificação de prioridade (str)
        """
        if score >= 35:
            return "Crítica (P0)"
        elif score >= 25:
            return "Alta (P1)"
        elif score >= 15:
            return "Média (P2)"
        elif score >= 5:
            return "Baixa (P3)"
        else:
            return "Muito Baixa (P4)"
    
    def gerar_plano_5w2h(
        self,
        acao_template: Dict[str, Any],
        cliente: str,
        responsavel: str,
        notas: str,
        data_inicio: datetime,
        impacto_customizado: int = None,
        esforco_customizado: int = None,
        custo_customizado: float = None
    ) -> Dict[str, Any]:
        """
        Gera um plano 5W2H completo baseado em um template de ação.
        
        Args:
            acao_template: Template da ação do banco de dados
            cliente: Nome do cliente
            responsavel: Responsável pela execução
            notas: Notas da reunião
            data_inicio: Data de início da ação
            impacto_customizado: Impacto customizado (opcional)
            esforco_customizado: Esforço customizado (opcional)
            custo_customizado: Custo customizado (opcional)
        
        Returns:
            Dicionário com o plano 5W2H completo
        """
        impacto = impacto_customizado or acao_template.get("impacto_padrao", 3)
        esforco = esforco_customizado or acao_template.get("esforco_padrao", 3)
        custo = custo_customizado or acao_template.get("custo_padrao", 0)
        duracao = acao_template.get("duracao_dias", 7)
        
        score = self.calcular_score(impacto, esforco)
        data_fim = self.calcular_data_fim(data_inicio, duracao)
        prioridade = self.classificar_prioridade(score)
        
        return {
            "cliente": cliente,
            "acao": acao_template.get("acao", ""),
            "categoria": acao_template.get("categoria", ""),
            "what": acao_template.get("what", ""),
            "why": acao_template.get("why", ""),
            "where": acao_template.get("where", ""),
            "how": acao_template.get("how", ""),
            "indicadores": acao_template.get("indicadores", ""),
            "data_inicio": data_inicio,
            "data_fim": data_fim,
            "duracao_dias": duracao,
            "responsavel": responsavel,
            "custo": custo,
            "impacto": impacto,
            "esforco": esforco,
            "score": score,
            "prioridade": prioridade,
            "status": "Planejado",
            "notas": notas,
            "percentual_execucao": 0
        }
    
    def calcular_timeline_gantt(self, acoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Calcula a timeline de Gantt para múltiplas ações.
        
        Args:
            acoes: Lista de ações com data_inicio e duracao_dias
        
        Returns:
            Lista de ações com informações de timeline
        """
        timeline = []
        for acao in acoes:
            data_inicio = acao.get("data_inicio")
            duracao = acao.get("duracao_dias", 7)
            data_fim = self.calcular_data_fim(data_inicio, duracao)
            
            timeline.append({
                **acao,
                "data_fim": data_fim,
                "dias_decorridos": (datetime.now() - data_inicio).days,
                "dias_restantes": (data_fim - datetime.now()).days
            })
        
        return sorted(timeline, key=lambda x: x["data_inicio"])
    
    def calcular_metricas_plano(self, acoes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calcula métricas agregadas do plano.
        
        Args:
            acoes: Lista de ações do plano
        
        Returns:
            Dicionário com métricas agregadas
        """
        if not acoes:
            return {
                "total_acoes": 0,
                "score_total": 0,
                "score_medio": 0,
                "custo_total": 0,
                "impacto_total": 0,
                "esforco_total": 0,
                "duracao_total_dias": 0,
                "acoes_por_categoria": {},
                "acoes_por_prioridade": {}
            }
        
        total_acoes = len(acoes)
        score_total = sum(a.get("score", 0) for a in acoes)
        score_medio = score_total / total_acoes if total_acoes > 0 else 0
        custo_total = sum(a.get("custo", 0) for a in acoes)
        impacto_total = sum(a.get("impacto", 0) for a in acoes)
        esforco_total = sum(a.get("esforco", 0) for a in acoes)
        duracao_total = sum(a.get("duracao_dias", 0) for a in acoes)
        
        # Agrupar por categoria
        acoes_por_categoria = {}
        for acao in acoes:
            categoria = acao.get("categoria", "Sem categoria")
            if categoria not in acoes_por_categoria:
                acoes_por_categoria[categoria] = 0
            acoes_por_categoria[categoria] += 1
        
        # Agrupar por prioridade
        acoes_por_prioridade = {}
        for acao in acoes:
            prioridade = acao.get("prioridade", "Não definida")
            if prioridade not in acoes_por_prioridade:
                acoes_por_prioridade[prioridade] = 0
            acoes_por_prioridade[prioridade] += 1
        
        return {
            "total_acoes": total_acoes,
            "score_total": round(score_total, 2),
            "score_medio": round(score_medio, 2),
            "custo_total": custo_total,
            "impacto_total": impacto_total,
            "esforco_total": esforco_total,
            "duracao_total_dias": duracao_total,
            "acoes_por_categoria": acoes_por_categoria,
            "acoes_por_prioridade": acoes_por_prioridade
        }
