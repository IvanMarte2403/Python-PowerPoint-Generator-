from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt
import requests



def add_header_bar(slide, color):
    # Añadir una barra en el encabezado de la diapositiva
    header_bar = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,  # Forma rectangular
        Inches(0),  # Posición x (izquierda)
        Inches(0.1),  # Posición y (arriba)
        Inches(11),  # Ancho (igual al ancho de la diapositiva)
        Pt(10),  # Alto (3 puntos)
    )

    # Configurar el color de la barra
    fill = header_bar.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(color)

    # Eliminar bordes y sombras
    header_bar.line.fill.background()
    header_bar.shadow.inherit = False



#Función para descargar imagen generada por DALL-E
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as out_file:
        out_file.write(response.content)
