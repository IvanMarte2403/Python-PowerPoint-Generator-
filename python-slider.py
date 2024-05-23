from pptx import Presentation
from pptx.util import Pt
import openai
from config import api_key

openai.api_key = api_key


def generate_text(prompt):

    print(f"Prompt: {prompt}")

    messages = [
       
        {
            "role" : "user", "content" : prompt     
        },
    ]


    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # Asegúrate de verificar el modelo disponible más reciente
        messages= messages,
        temperature= 0
    )
    return response.choices[0].message.content


from pptx.util import Pt

def create_presentation(text, file_name="presentation.pptx"):
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[1])

    title = slide.shapes.title
    content = slide.placeholders[1]

    title.text = "Generated Slide"
    content.text = text

    # Ajustar el tamaño del texto
    for paragraph in content.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(12)

    # Dividir el texto entre varias diapositivas si es demasiado largo
    max_length = 1000  # Ajusta este valor según tus necesidades
    while len(content.text) > max_length:
        # Crear una nueva diapositiva
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        title = slide.shapes.title
        content = slide.placeholders[1]

        title.text = "Introducción a la Convergencia de Datos y Negocios"
        content.text = text[max_length:]
        text = text[:max_length]

        # Ajustar el tamaño del texto
        for paragraph in content.text_frame.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(12)

    prs.save(file_name)
    print(f"Presentation saved as {file_name}")


def main():
    prompt = "Te vas a convertir en instructor, ame vas a dar los textos, y código para una presentación de una clase de Introducción a la convergencia de Datos y Negocios . El lenguaje relajado para alumnos -Tienen que ser intermedio - básico -No code  -25 Slides como mínimo -5 Ejercicios mínimos incluidos  Algo que es muy importante, es el lenguaje para la presentación, ya que es una clase para gente que no ha tenido acercamiento a la programación antes. Entonces ¿Cómo se lo explicarías a alguien que no ha tenido acercamiento a la programación? Evita el lenguaje emocionante, son alumnos entre 20 - 26 años  Los textos son para un presentación de Power Point, entonces hazlos fáciles de leer e incluye ejemplos o dinámicas como mejor sea el tema "
    generated_text = generate_text(prompt)
    print(f"Prompt: {prompt}")
    print(f"Generated text: {generated_text}")

    create_presentation(generated_text)

if __name__ == "__main__":
    main()
