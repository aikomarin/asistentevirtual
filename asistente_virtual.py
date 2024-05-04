import pyttsx3  # Importar la librería pyttsx3 para sintetizar voz
import speech_recognition as sr  # Importar la librería speech_recognition para reconocimiento de voz
import pywhatkit
import yfinance as yf  # Importar la librería yfinance para obtener información financiera
import pyjokes  # Importar la librería pyjokes para obtener chistes
import webbrowser  # Importar la librería webbrowser para controlar el navegador web
import datetime  # Importar la librería datetime para trabajar con fechas y horas
import wikipedia  # Importar la librería wikipedia para buscar información en Wikipedia

# Voces existentes en el equipo para el idioma
id1 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0'
id2 = r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


def transformar_audio_en_texto():  # Función para transformar audio en texto
    r = sr.Recognizer()  # Inicializar el reconocedor de voz
    with sr.Microphone() as origen:  # Configurar el micrófono
        r.pause_threshold = 0.8  # Tiempo de espera
        print('Ya puedes hablar')  # Informar que está listo para grabar
        audio = r.listen(origen)  # Grabar audio desde el micrófono

        try:
            pedido = r.recognize_google(audio, language='es-mx')  # Reconocer el audio usando Google
            print('Dijiste: ' + pedido)  # Mostrar lo que se dijo
            return pedido  # Devolver el texto reconocido
        except sr.UnknownValueError:  # Manejar error si no se entendió el audio
            print('No entendí')
            return 'Sigo esperando'  # Devolver indicación de que sigue esperando
        except sr.RequestError:  # Manejar error si no se pudo procesar el pedido
            print('No hay servicio')
            return 'Sigo esperando'
        except Exception as e:  # Manejar error genérico
            print(f'Algo ha salido mal: {e}')
            return 'Sigo esperando'


def hablar(mensaje):  # Función para sintetizar voz
    engine = pyttsx3.init()  # Inicializar el motor de síntesis de voz
    engine.setProperty('voice', id1)  # Fijar la voz que va a hablar
    engine.say(mensaje)  # Decir el mensaje
    engine.runAndWait()  # Esperar hasta que se complete la reproducción del mensaje


def pedir_dia():  # Función para obtener el día de la semana
    dia = datetime.date.today()  # Obtener la fecha de hoy
    print(dia)

    dia_semana = dia.weekday()  # Obtener el número del día de la semana
    print(dia_semana)

    # Diccionario con nombres de días
    calendario = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'}

    hablar(f'Hoy es {calendario[dia_semana]}')  # Decir el día de la semana


def pedir_hora():  # Función para obtener la hora actual
    hora = datetime.datetime.now()  # Obtener la hora actual
    hora = f'En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos'
    print(hora)
    hablar(hora)  # Decir la hora


def saludo_inicial():  # Función para saludar al usuario al inicio
    hora = datetime.datetime.now()  # Obtener la hora actual
    if hora.hour < 6 or hora.hour > 20:  # Determinar el momento del día
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'
    hablar(f'Hola{momento}, soy Sabina, tu asistente personal. Por favor, dime en qué te puedo ayudar')


def pedir_cosas():  # Función principal del asistente
    saludo_inicial()  # Saludar al usuario al inicio
    comenzar = True  # Variable para controlar el bucle
    while comenzar:  # Iniciar bucle principal
        pedido = transformar_audio_en_texto().lower()  # Obtener pedido del usuario

        if 'abrir youtube' in pedido:  # Abrir YouTube si se solicita
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abrir el navegador' in pedido:  # Abrir el navegador web si se solicita
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com/')
            continue
        elif 'qué día es hoy' in pedido:  # Obtener el día de la semana si se solicita
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:  # Obtener la hora actual si se solicita
            pedir_hora()
            continue
        elif 'buscar en wikipedia' in pedido:  # Buscar en Wikipedia si se solicita
            hablar('Buscando eso en wikipedia')
            pedido = pedido.replace('buscar en wikipedia', '')  # Buscar directamente lo que se dice
            wikipedia.set_lang('es')  # Lenguaje en el que se va a buscar
            resultado = wikipedia.summary(pedido, sentences=1)  # Resumen de la información, solo 1 oración
            hablar('Wikipedia dice lo siguiente')
            hablar(resultado)
            continue
        elif 'buscar en internet' in pedido:  # Buscar en internet si se solicita
            hablar('Ya mismo estoy en eso')
            pedido = pedido.replace('buscar en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproducir' in pedido:
            hablar('Buena idea, ya comienzo a reproducirlo')
            pywhatkit.playonyt(pedido)  # Reproducir un video de YouTube si se solicita
            continue
        elif 'broma' in pedido:  # Decir un chiste si se solicita
            hablar(pyjokes.get_joke('es'))  # Determinar el lenguaje
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()  # Obtener el nombre de la acción eliminando la parte 'de'
            # Crear diccionario con nombres de acciones y sus símbolos
            cartera = {'apple': 'APPL', 'amazon': 'AMZN', 'google:': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]  # Obtener el símbolo de la acción
                accion_buscada = yf.Ticker(accion_buscada)  # Crear objeto Ticker para la acción
                precio_actual = accion_buscada.info['regularMarketPrice']  # Obtener el precio actual de la acción
                hablar(f'La encontré, el precio de {accion} es {precio_actual}')
                continue
            except KeyError:  # Error si la acción no se encuentra en la cartera
                hablar('Perdón pero no la he encontrado')
                continue
        elif 'adiós' in pedido:  # Despedirse y finalizar el asistente si se solicita
            hablar('Me voy a descansar, cualquier cosa me avisas')
            break  # Salir del bucle


pedir_cosas()  # Llamar a la función principal para ejecutar el asistente
