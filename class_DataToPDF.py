from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import StyleSheet1, getSampleStyleSheet
from reportlab.platypus import Paragraph

""" Exports list of dictionaries to a PDF file using reportlab library. 
    Used to export Plant data and Garden data.
"""
class DataToPDF:
    def __init__(self, *args: list[dict], filename:str) -> None:
        """takes list of dictionary and exports it as table in pdf file
        Args:
            filename (str): name for the pdf file where data will be exported
        """
        self.data: tuple[list[dict]] = args
        self.filename: str = filename + ".pdf"
    
    def save_data_to_pdf(self) -> None:
        """Convers list of dictionaries to a list of lists
            formats it as table 
            saves to a pdf file
        """
        elements:list = []
        doc = SimpleDocTemplate(self.filename, pagesize=landscape(A4)) 
        for data_list in self.data:
            headers = list(data_list[0].keys())
            table_data: list[list] = [headers]
            for row in data_list:
                table_data.append([str(row[key]) for key in headers])
            
            if len(headers) == 11:
                column_widths:list[int] = [30, 40, 90, 60, 60, 45, 70, 70, 50, 70, 190]
            elif len(headers) == 4:
                column_widths:list[int] = [80, 100, 70, 300 ]
            else:    
                column_widths = [len(header) * 10 for header in headers]
            

            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.pink),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                ('WORDWRAP', (0, 0), (-1, -1), 'CJK'), 
            ])
            
            s: StyleSheet1 = getSampleStyleSheet()
            s = s["BodyText"]
            s.wordWrap = 'CJK'
            data2: list[list[Paragraph]] = [[Paragraph(cell, s) for cell in row] for row in table_data]
            table=Table(data2)
            table._argW = column_widths
            table.setStyle(style)
            elements.append(table)
        doc.build(elements)