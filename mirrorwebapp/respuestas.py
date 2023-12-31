from bs4 import BeautifulSoup
import requests
import re
import wikipedia
import random


def eliminar_etiquetas(texto):
    # Utiliza una expresión regular para encontrar y eliminar las etiquetas
    return re.sub(r'<.*?>', '', texto)


def google_answering(consulta):
    base_url = 'https://www.google.com/search?q='
    url = base_url + consulta

    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                            'AppleWebKit/537.36 (KHTML, like Gecko) '
                            'Chrome/80.0.3987.149 Safari/537.36'}

    try:
        response = requests.get(url, headers=header)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Intenta encontrar la respuesta en distintos elementos HTML
        answer_elements = soup.find_all(['div', 'span'], class_=[
                                        'Z0LcW t2b5Cf', 'hgKElc', 'wob_t q8U8x', 'co8aDb', 'vk_bk dDoNo FzvWSb'])

        for element in answer_elements:
            if element:
                if 'wob_t' in str(element):
                    answer = eliminar_etiquetas(str(element)) + 'ºC'
                    return answer
                else:
                    answer = eliminar_etiquetas(str(element))
                    return answer

        # Configura el idioma de búsqueda para Wikipedia en español
        wikipedia.set_lang('es')
        try:
            # Intenta buscar la respuesta en Wikipedia
            answer = wikipedia.summary(consulta, sentences=3)
            if answer:
                return answer
        except wikipedia.exceptions.PageError as e:
            print(f"Error al buscar la respuesta.")
            return "No he encontrado la respuesta."

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return 'ERROR'


def consulta(consulta):
    user_input = consulta

    # Utiliza la función para obtener la respuesta
    respuesta = responder_pregunta_o_conversacion(
        user_input)

    return str(respuesta)


def respuesta_tipo(entrada):
    entrada = entrada.lower()
    #quitar el punto final y las comas
    entrada = entrada.replace('.', '')
    entrada = entrada.replace(',', '')
    entrada = entrada.replace(';', '')
    entrada = entrada.replace(':', '')
    entrada = entrada.replace('!', '')
    entrada = entrada.replace('?', '')
    saludos = ['hola', 'buenos días', 'buenas tardes', 'buenas noches']
    despedidas = ['adiós', 'hasta luego', 'hasta pronto',
                  'hasta mañana', 'hasta la vista', 'hasta la próxima', 'nos vemos']
    agradecimientos = ['gracias', 'muchas gracias',
                       'gracias por todo', 'muchas gracias por todo']
    chistes = ['¿Por qué las focas del circo miran siempre hacia arriba? Porque es donde están los focos.',
               '¿Qué le dice un pez a otro? Nada.',
               '¿Qué le dice un jaguar a otro jaguar? Jaguar you.']

    trabalenguas = ['El cielo está enladrillado, ¿quién lo desenladrillará? El desenladrillador que lo desenladrille, buen desenladrillador será.',
                    'Tres tristes tigres comen trigo en un trigal.',
                    'Pablito clavó un clavito, ¿qué clavito clavó Pablito?']
    
    palabras_entrada = entrada.split()

    if entrada in saludos or any(palabra == 'hola' for palabra in palabras_entrada):
        return 'Hola Marcel, ¿en qué puedo ayudarte?'
    elif entrada in despedidas or any(palabra == 'adiós' for palabra in palabras_entrada) or any(palabra == 'adios' for palabra in palabras_entrada):
        return 'Hasta luego, que tengas un buen día.'
    elif entrada in agradecimientos or any(palabra == 'gracias' for palabra in palabras_entrada):
        return 'Un placer poder ayudarte.'
    elif any(palabra in ['cómo', 'tal', 'estás'] for palabra in palabras_entrada):
        return 'Estoy muy bien, gracias por preguntar.'
    elif any(palabra in ['chiste'] for palabra in palabras_entrada):
        return random.choice(chistes)
    elif any(palabra in ['trabalenguas'] for palabra in palabras_entrada):
        return random.choice(trabalenguas)
    elif any(palabra in ['nombre', 'llamas', 'llamo'] for palabra in palabras_entrada):
        return 'Por ahora no tengo un nombre'
    elif any(palabra in ['cabeza'] for palabra in palabras_entrada):
        return 'Analgésicos. Los analgésicos simples disponibles sin receta médica suelen ser la primera línea de tratamiento para reducir el dolor de cabeza.'
    elif any(palabra in ['analgesicos'] for palabra in palabras_entrada):
        return 'La dosis oral en adultos suele ser de 50 a 100 mg cada 6-8 h.'
    elif any(palabra in ['emergencias'] for palabra in palabras_entrada):
        return 'Es el número 112'
    elif any(palabra in ['ayunas'] for palabra in palabras_entrada):
        return 'Por lo general, usted necesita ayunar por 8 a 12 horas antes de una prueba.'
    else:
        return None


def responder_pregunta_o_conversacion(input_text):
    # Verifica si el input contiene una pregunta (termina con "?")
    es_pregunta = input_text.strip().endswith('?')

    respuesta = respuesta_tipo(input_text)

    if respuesta:
        # Si es una pregunta, utiliza google_answering para obtener la respuesta
        return respuesta
    else:
        if es_pregunta:
            # Si es una pregunta, utiliza google_answering para obtener la respuesta
            respuesta = google_answering(input_text)
        else:
            respuesta = "No te he entendido, ¿puedes repetirlo?"
        return respuesta