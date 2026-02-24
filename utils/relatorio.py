"""
Módulo para geração de relatórios em PDF e Excel.
"""
import io
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT


class GeradorRelatorio:
    """Classe para gerar relatórios em PDF e Excel."""
    
    def __init__(self):
        """Inicializa o gerador de relatórios."""
        self.styles = getSampleStyleSheet()
        self._criar_estilos_customizados()
    
    def _criar_estilos_customizados(self):
        """Cria estilos customizados para o relatório."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f2937'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#4b5563'),
            spaceAfter=6
        ))
    
    def gerar_pdf(
        self,
        cliente: str,
        acoes: List[Dict[str, Any]],
        metricas: Dict[str, Any],
        data_reuniao: datetime = None
    ) -> bytes:
        """
        Gera um relatório em PDF.
        
        Args:
            cliente: Nome do cliente
            acoes: Lista de ações do plano
            metricas: Métricas agregadas do plano
            data_reuniao: Data da reunião (opcional)
        
        Returns:
            Bytes do PDF gerado
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Título
        titulo = Paragraph(
            f"Plano de Ações 5W2H<br/>{cliente}",
            self.styles['CustomTitle']
        )
        story.append(titulo)
        
        # Data da reunião
        if data_reuniao is None:
            data_reuniao = datetime.now()
        
        data_str = data_reuniao.strftime("%d de %B de %Y")
        subtitulo = Paragraph(
            f"Reunião de Start - {data_str}",
            self.styles['CustomHeading']
        )
        story.append(subtitulo)
        story.append(Spacer(1, 0.3*inch))
        
        # Resumo executivo
        story.append(Paragraph("Resumo Executivo", self.styles['CustomHeading']))
        
        resumo_data = [
            ["Métrica", "Valor"],
            ["Total de Ações", str(metricas.get("total_acoes", 0))],
            ["Score Total", str(metricas.get("score_total", 0))],
            ["Score Médio", str(metricas.get("score_medio", 0))],
            ["Custo Total (R$)", f"R$ {metricas.get('custo_total', 0):,.2f}"],
            ["Duração Total (dias)", str(metricas.get("duracao_total_dias", 0))],
            ["Impacto Total", str(metricas.get("impacto_total", 0))],
            ["Esforço Total", str(metricas.get("esforco_total", 0))]
        ]
        
        resumo_table = Table(resumo_data, colWidths=[3*inch, 2*inch])
        resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        
        story.append(resumo_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Distribuição por categoria
        if metricas.get("acoes_por_categoria"):
            story.append(Paragraph("Distribuição por Categoria", self.styles['CustomHeading']))
            
            categoria_data = [["Categoria", "Quantidade"]]
            for cat, qtd in metricas.get("acoes_por_categoria", {}).items():
                categoria_data.append([cat, str(qtd)])
            
            categoria_table = Table(categoria_data, colWidths=[3*inch, 2*inch])
            categoria_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
            ]))
            
            story.append(categoria_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Quebra de página
        story.append(PageBreak())
        
        # Detalhes das ações
        story.append(Paragraph("Detalhes das Ações", self.styles['CustomHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        for idx, acao in enumerate(acoes, 1):
            # Cabeçalho da ação
            acao_titulo = Paragraph(
                f"{idx}. {acao.get('acao', 'Ação sem nome')} ({acao.get('categoria', 'N/A')})",
                self.styles['CustomHeading']
            )
            story.append(acao_titulo)
            
            # Dados da ação
            acao_data = [
                ["Campo", "Valor"],
                ["What (O quê)", acao.get('what', '')],
                ["Why (Por quê)", acao.get('why', '')],
                ["Where (Onde)", acao.get('where', '')],
                ["How (Como)", acao.get('how', '')],
                ["Indicadores", acao.get('indicadores', '')],
                ["Responsável", acao.get('responsavel', '')],
                ["Data Início", acao.get('data_inicio', '').strftime("%d/%m/%Y") if isinstance(acao.get('data_inicio'), datetime) else ''],
                ["Data Fim", acao.get('data_fim', '').strftime("%d/%m/%Y") if isinstance(acao.get('data_fim'), datetime) else ''],
                ["Duração (dias)", str(acao.get('duracao_dias', ''))],
                ["Custo (R$)", f"R$ {acao.get('custo', 0):,.2f}"],
                ["Impacto", str(acao.get('impacto', ''))],
                ["Esforço", str(acao.get('esforco', ''))],
                ["Score", str(acao.get('score', ''))],
                ["Prioridade", acao.get('prioridade', '')],
                ["Status", acao.get('status', '')],
                ["Notas", acao.get('notas', '')]
            ]
            
            acao_table = Table(acao_data, colWidths=[1.5*inch, 4*inch])
            acao_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
            ]))
            
            story.append(acao_table)
            story.append(Spacer(1, 0.2*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    
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
