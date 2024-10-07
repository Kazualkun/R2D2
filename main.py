import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import os
import webbrowser

# Configurações do Spotify
SPOTIPY_CLIENT_ID = 'be9df78c836c4838b4b0ad83fe363e9d'
SPOTIPY_CLIENT_SECRET = '953370717bff4553a1e7a977b4f7c5f2'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope="user-library-read user-read-playback-state user-modify-playback-state"))

# Função para listar compromissos
def listar_compromissos():
    compromissos = []
    if os.path.exists('agenda.txt'):
        with open('agenda.txt', 'r') as f:
            compromissos = f.readlines()
    return compromissos

# Inicializar reconhecimento de voz e conversão de texto em fala
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def talk(text):
    """Fala o texto passado como argumento"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Escuta o comando do usuário e retorna como texto"""
    try:
        with sr.Microphone() as source:
            print("As suas ordens senhor...")
            recognizer.adjust_for_ambient_noise(source)
            voice = recognizer.listen(source)
            command = recognizer.recognize_google(voice, language='pt-BR')
            command = command.lower()
            print(f"Você disse: {command}")
            return command
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return ""
    except sr.RequestError:
        print("Serviço de reconhecimento de fala indisponível")
        return ""

def play_spotify(song):
    """Toca uma música no Spotify"""
    results = sp.search(q=song, limit=1)
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        sp.start_playback(uris=[track['uri']])
        talk(f"Tocando {track['name']} por {track['artists'][0]['name']} no Spotify")
    else:
        talk("Não encontrei essa música no Spotify")

def execute_command(command):
    """Executa o comando reconhecido"""
    if 'tocar' in command:
        song = command.replace('tocar', '')
        talk(f"Procurando {song}")
        play_spotify(song)
    elif 'pesquisar' in command:
        query = command.replace('pesquisar', '')
        talk(f"Pesquisando por {query}")
        pywhatkit.search(query)
    elif 'marcar compromisso' in command:
        date_time_str = command.replace('marcar compromisso', '').strip()
        try:
            date_time = datetime.datetime.strptime(date_time_str, '%d/%m/%Y %H:%M')
            with open('agenda.txt', 'a') as f:
                f.write(f"Compromisso marcado para {date_time}\n")
            talk(f"Compromisso marcado para {date_time}")
        except ValueError:
            talk("Data ou hora inválida. Tente novamente.")
    elif 'listar compromissos' in command:
        compromissos = listar_compromissos()
        if compromissos:
            talk("Listando compromissos do mês:")
            for compromisso in compromissos:
                talk(compromisso.strip())
        else:
            talk("Você não tem compromissos marcados para este mês.")
    elif 'abrir' in command:
        app = command.replace('abrir', '').strip()
        if app == 'navegador':
            webbrowser.open("http://www.google.com")
            talk("Abrindo navegador")
        elif app == 'notepad':
            os.system("notepad")
            talk("Abrindo Bloco de Notas")
        # Adicione mais aplicações conforme necessário
    elif 'desligar' in command:
        talk("Tudo bem senhor, estarei aqui quando precisar.")
        return False  # Desativa o assistente até que 'EVA' seja dito novamente
    elif 'é hora do show' in command:
        # Substitua os nomes dos programas pelos programas específicos que você quer abrir
        os.system("start notepad")  # Exemplo de abrir o Bloco de Notas
        os.system("start chrome")  # Exemplo de abrir o Google Chrome
        play_spotify('Final Battle Elden Ring Tsukasa Saitoh')  # Substitua pela música que você quer tocar
        talk("Olá senhor, vai jogar o de sempre? Que tal subir de elo hoje?")
    elif 'acorda criança' in command:
        play_spotify('Should I Stay or Should I Go')
        talk(f"Bem-vindo senhor, hoje é dia {datetime.datetime.now().strftime('%d/%m/%Y')} e são {datetime.datetime.now().strftime('%H:%M')}.")
        compromissos = listar_compromissos()
        if compromissos:
            talk("Você tem os seguintes compromissos planejados para hoje:")
            for compromisso in compromissos:
                talk(compromisso.strip())
        else:
            talk("Você não tem compromissos planejados para hoje.")
        talk("O senhor está muito elegante hoje, é sempre um prazer vê-lo trabalhar. Quer fazer mais alguma coisa?")
    elif 'hora de trabalhar' in command:
        # Substitua os nomes dos programas pelos programas específicos que você quer abrir
        os.system("start notepad")  # Exemplo de abrir o Bloco de Notas
        os.system("start chrome")  # Exemplo de abrir o Google Chrome
        play_spotify('Malenia, Blade of Miquella Elden Ring Yuka Kitamura')  # Substitua pela música que você quer tocar
        talk(f"Olá senhor, tenha um ótimo dia de trabalho. Hoje é {datetime.datetime.now().strftime('%d/%m/%Y')} e são {datetime.datetime.now().strftime('%H:%M')}. Espero que tenha um ótimo dia de trabalho.")
    elif 'bom dia' in command:
        talk(f"Bom dia senhor, hoje é dia {datetime.datetime.now().strftime('%d/%m/%Y')} e são {datetime.datetime.now().strftime('%H:%M')}. Espero que tenha um ótimo dia de trabalho.")
    elif 'boa tarde' in command:
        talk(f"Boa tarde senhor, hoje é dia {datetime.datetime.now().strftime('%d/%m/%Y')} e são {datetime.datetime.now().strftime('%H:%M')}. Espero que tenha um ótimo dia de trabalho.")
    elif 'boa noite' in command:
        talk(f"Bom noite senhor, hoje é dia {datetime.datetime.now().strftime('%d/%m/%Y')} e são {datetime.datetime.now().strftime('%H:%M')}. Espero que tenha um ótimo dia de trabalho.")
    else:
        talk("Não entendi o comando. Pode repetir?")
    return True  # Mantém o assistente ativo

def check_microphone():
    """Verifica se o microfone está disponível"""
    print("Verificando microfones disponíveis...")
    mic_list = sr.Microphone.list_microphone_names()
    if not mic_list:
        print("Nenhum microfone encontrado.")
        return False
    
    print("Microfones disponíveis:")
    for i, mic in enumerate(mic_list):
        print(f"{i}: {mic}")

    # Tentando usar o primeiro microfone da lista
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Microfone está funcionando corretamente.")
            return True
    except OSError as e:
        print(f"Erro ao acessar o microfone: {e}")
        return False

# Verificar se o microfone está disponível antes de iniciar o assistente
if check_microphone():
    assistente_ativo = True
    while True:
        if not assistente_ativo:
            command = listen()
            if 'eva' in command:
                assistente_ativo = True
                talk("Estou ouvindo")
        else:
            command = listen()
            if 'eva' in command:
                command = command.replace('eva', '').strip()
                if command:
                    assistente_ativo = execute_command(command)
else:
    print("Por favor, conecte um microfone e tente novamente.")
