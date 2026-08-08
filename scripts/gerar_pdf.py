from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Desenho-Tecnico-CAD-02J11-cronograma.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

MACKENZIE = colors.HexColor("#c90016")
WINE = colors.HexColor("#650014")
LIGHT_RED = colors.HexColor("#fff0f2")
PROVA = colors.HexColor("#ffcb3d")
COLETA = colors.HexColor("#315d78")
ENTREGA = colors.HexColor("#175c36")

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
    fontSize=20, leading=23, textColor=WINE, alignment=TA_CENTER, spaceAfter=4,
)
meta_style = ParagraphStyle(
    "Meta", parent=styles["Normal"], fontSize=10, leading=13,
    textColor=colors.HexColor("#493c40"), alignment=TA_CENTER,
)
cell_style = ParagraphStyle("Cell", parent=styles["BodyText"], fontSize=8.2, leading=10.3)
cell_bold = ParagraphStyle("CellBold", parent=cell_style, fontName="Helvetica-Bold", textColor=WINE)
white_style = ParagraphStyle("White", parent=cell_style, fontName="Helvetica-Bold", textColor=colors.white)
event_style = ParagraphStyle("Event", parent=cell_style, fontName="Helvetica-Bold", alignment=TA_CENTER)


def p(text, style=cell_style):
    return Paragraph(text, style)


rows = [
    ("12/08", "Apresentação da disciplina e das ferramentas", "Plano de Ensino, datas e critérios; Desenho Técnico no projeto de engenharia; normas ABNT; Inventor e AutoCAD; instalação dos programas.", "aula"),
    ("19/08", "Projeções planas e desenho à mão livre", "Projeções cônicas, paralelas e axonométricas; linhas, círculos, elipses, proporções e estilos de linha; exercícios à mão livre.", "aula"),
    ("26/08", "Inventor: modelagem básica", "Extrusão, recursos de desenho, planos de trabalho, visualização, restrições, fórmulas, fillet, array e chamfer.", "aula"),
    ("02/09", "Semana da Escola de Engenharia", "Atividade acadêmica institucional.", "evento"),
    ("09/09", "Atividade 1 - Coleta", "Coleta da folha de atividades individual e presencial. Cada aluno deve retirar sua própria folha; um colega não pode retirar por outro.", "coleta"),
    ("16/09", "Atividade 1 - Entrega", "Entrega individual e presencial pelo aluno. Cada aluno deve entregar a própria atividade; um colega não pode entregar por outro. Prova AVI institucional em 17/09.", "entrega"),
    ("23/09", "Prova 1", "Primeira prova da disciplina.", "prova"),
    ("30/09", "Devolutiva e vistas múltiplas", "Devolutiva; vistas múltiplas; convenções de linhas, interseções, tangências, arredondamentos e visualização.", "aula"),
    ("07/10", "AutoCAD: introdução", "Apresentação, zoom, erase, linhas, círculos e exercícios; desenhos propostos no AutoCAD.", "aula"),
    ("14/10", "Atividade 2 - Coleta", "Folha, escala, cotas, cortes e detalhes. Coleta individual e presencial; um colega não pode retirar a folha por outro.", "coleta"),
    ("21/10", "Atividade 2 - Entrega", "Entrega individual e presencial pelo aluno. Cada aluno deve entregar a própria atividade; um colega não pode entregar por outro.", "entrega"),
    ("28/10", "Inventor: desenho final", "Elaboração de um desenho completo no Inventor.", "aula"),
    ("04/11", "Prova Avalia", "Avaliação institucional.", "evento"),
    ("11/11", "Devolutiva e desenho final", "Devolutiva do trabalho e continuação do desenho final no Inventor.", "aula"),
    ("18/11", "Prova 2", "Segunda prova da disciplina.", "prova"),
    ("25/11", "Devolutiva e exercícios", "Devolutiva da avaliação e aplicação de exercícios.", "aula"),
    ("02/12", "SUB", "Período institucional de avaliação substitutiva.", "evento"),
    ("09/12", "PAFE", "Período institucional de PAFE.", "evento"),
]


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#73676c"))
    canvas.drawRightString(landscape(A4)[0] - 14 * mm, 9 * mm, f"Página {doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=landscape(A4),
    rightMargin=13 * mm, leftMargin=13 * mm, topMargin=9 * mm, bottomMargin=10 * mm,
    title="Cronograma - Desenho Técnico e CAD - Turma 02J11",
    author="Professor Gabriel Angelo",
)

story = [
    Paragraph("Desenho Técnico e CAD", title_style),
    Paragraph("Professor Gabriel Angelo | Turma 02J11 | 2º semestre de 2026", meta_style),
    Paragraph("<b>Atenção:</b> coleta e entrega são individuais e presenciais; um colega não pode retirar nem entregar por outro.", meta_style),
    Spacer(1, 4 * mm),
]

data = [[p("DATA", white_style), p("AULA / EVENTO", white_style), p("CONTEÚDO E ORIENTAÇÕES", white_style)]]
for date, topic, details, kind in rows:
    data.append([p(date, cell_bold), p(topic, cell_bold), p(details)])

table = Table(data, colWidths=[22 * mm, 61 * mm, 181 * mm], repeatRows=1, hAlign="CENTER")
table_style = [
    ("BACKGROUND", (0, 0), (-1, 0), WINE),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.45, colors.HexColor("#d8c8cc")),
    ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ("TOPPADDING", (0, 1), (-1, -1), 5),
    ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
]
for index, (_, _, _, kind) in enumerate(rows, start=1):
    background = colors.white if index % 2 else colors.HexColor("#fbf6f7")
    if kind == "prova":
        background = PROVA
    elif kind == "coleta":
        background = colors.HexColor("#dceaf2")
    elif kind == "entrega":
        background = colors.HexColor("#d9eee2")
    elif kind == "evento":
        background = LIGHT_RED
    table_style.append(("BACKGROUND", (0, index), (-1, index), background))
table.setStyle(TableStyle(table_style))
story.append(table)

doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(OUTPUT)
