from pptx import Presentation
from pptx.util import Pt
import openai
import requests
from config import api_key  
from grafics import add_header_bar
from pptx.util import Inches, Pt


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



def download_image(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as out_file:
        out_file.write(response.content)


def generate_dalle_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,  # Generate a single image
    )
    image_url = response.data[0].url
    return image_url

def create_presentation(prompts, file_name="presentation.pptx"):
    prs = Presentation()
    prs.slide_width = Inches(13.2)

    # Diapositiva de inicio
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Inicio"
    #Edición de la introducción de la clase
    slide.placeholders[1].text = generate_text("Dame una descripción de 7 palabras sobre Introducción a la convergencia de Datos y Negocios")
    #Añade Gráfico de Logo
    add_header_bar(slide, "FF0E68")

    
    # Añadir imagen al fondo de la diapositiva
    slide.shapes.add_picture('img/Background.png', Inches(0), prs.slide_height - Inches(5), prs.slide_width, Injches(5))
    
    slide.shapes.add_picture('img/logo-datarebels-rosa.png', Inches(1), Inches(2))
    slide.shapes.add_picture('img/logo-datarebels-portada.png', Inches(10), Inches(2), Inches(3), Inches(5))    
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Objetivos"
    #Edición de los objetivos de la clase
    slide.placeholders[1].text = generate_text("Objetivos de la clase")

    # Diapositivas de temas
    for i, prompt in enumerate(prompts, start=1):
        # Diapositiva del tema
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = f"Tema {i}"
        slide.placeholders[1].text = generate_text(prompt)

       
        #Add Grafic Bar 
        add_header_bar(slide, "FF0E68")

        # Diapositiva del ejemplo o analogía
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = f"Tema {i} - Ejemplo o analogía"
        slide.placeholders[1].text = generate_text(f"Ejemplo o analogía para {prompt}")

        add_header_bar(slide, "FF0E68")


        # Generate DALL-E image for analogy
        analogy_prompt = f"Ejemplo o analogía visual para {prompt}"
        analogy_image_url = generate_dalle_image(analogy_prompt)

        # Download DALL-E image
        image_filename = f"analogy_image_{i}.png"
        download_image(analogy_image_url, image_filename)

         # Add DALL-E image to analogy slide (after text)

        slide.shapes.add_picture(
            image_filename,
            left=prs.slide_width / 4,
            top=prs.slide_height / 3,
            width=prs.slide_width / 2,
            height=prs.slide_height / 2,
        )  # Adjust positioning as needed
        

    # Ajustar el tamaño del texto
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for paragraph in shape.text_frame.paragraphs:
                    for run in paragraph.runs:
                        run.font.size = Pt(16)
                        run.font.name = 'Open Sans'

    prs.save(file_name)
    print(f"Presentation saved as {file_name}")

def main():
    # Prompts para cada tema de la clase
    prompts = [
        "Generauna introducción a la convergencia de Datos y Negocios",
        
    ]

    # Generar texto para cada prompt
    generated_texts = [generate_text(prompt) for prompt in prompts]

    # Crear la presentación
    create_presentation(generated_texts)

if __name__ == "__main__":
    main()