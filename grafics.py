from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt


def add_header_bar(slide, color):
    # Añadir una barra en el encabezado de la diapositiva
    header_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,  # Forma rectangular
        Inches(2),  # Posición x (izquierda)
        0,  # Posición y (arriba)
        Inches(10),  # Ancho (igual al ancho de la diapositiva)
        Pt(10),  # Alto (3 puntos)go
    )

    # Configurar el color de la barra
    fill = header_bar.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(color)
