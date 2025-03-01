import speech_recognition as sr
import webbrowser
import pyttsx3
import wikipedia
import datetime
import requests
import os
import time
import pywhatkit
import pyautogui

# Inicializa o motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 180)  # Velocidade de fala
engine.setProperty('volume', 1)  # Volume máximo

def falar(texto):
    
    """Faz o assistente falar"""
    engine.say(texto)
    engine.runAndWait()
    
    
def criar_bloco_notas(nome_arquivo, conteudo):
    """Cria e abre um bloco de notas com o nome e conteúdo informados."""
    caminho = f"{nome_arquivo}.txt"
    
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    
    os.system(f"notepad {caminho}")
    falar(f"Arquivo {nome_arquivo} criado e aberto.")
    
    
def enviar_whatsapp(nome, mensagem):
    """Envia uma mensagem no WhatsApp Web para um contato salvo."""
    contatos = {
        "coroa": "+554799713750",
        "pai": "+55XXXXXXXXXXX",
        "amigo": "+55XXXXXXXXXXX"
    }
    
    time.sleep(2)
    pyautogui.press("enter")
    
    if nome in contatos:
        numero = contatos[nome]
        pywhatkit.sendwhatmsg_instantly(numero, mensagem)
        falar(f"Mensagem enviada para {nome}")
    else:
        falar("Contato não encontrado, adicione à lista primeiro.")   

def obter_clima(cidade):
    """Obtém a previsão do tempo para a cidade"""
    api_key = "a0b18a9b527b49e4bfc8b6164eb0cce7"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br"
    resposta = requests.get(url)
    dados = resposta.json()

    if dados["cod"] == 200:
        clima = dados["weather"][0]["description"]
        temp = dados["main"]["temp"] - 273.15
        falar(f"A previsão do tempo em {cidade} é {clima} com temperatura de {temp:.1f}°C")
    else:
        falar("Não consegui obter as informações do clima")

def ouvir_comando():
    """Escuta o microfone e reconhece a fala"""
    recognizer = sr.Recognizer()  
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")  
        return comando.lower()
    except sr.UnknownValueError:
        print("Não entendi, pode repetir?")
        return ""
    except sr.RequestError:
        print("Erro ao conectar com a API") 
        return "" 

def executar_comando(comando):
    """Executa ações baseadas no comando""" 
    if "horas" in comando:
        hora = datetime.datetime.now().strftime("%H:%M")  
        falar(f"Agora são {hora}")
        
    elif "data" in comando:
        hoje = datetime.datetime.now().strftime("%d/%m/%Y")    
        falar(f"Hoje é {hoje}")

    elif "qual o clima" in comando:
        cidade = comando.replace("qual o clima em", "").strip()
        obter_clima(cidade)  # Chamando a função corretamente

    elif "pesquisar" in comando:
        comando = comando.replace("pesquisar", "").strip()
        resultado = wikipedia.summary(comando, sentences=2, lang="pt")  
        falar(resultado)
        

    elif "bloco de notas" in comando:
        os.system("notepad")
        falar("Abrindo Bloco de Notas")   
        
        
    elif "nota" in comando:
       falar("Qual o nome do arquivo?")
       nome_arquivo = ouvir_comando()

       falar("O que devo escrever no bloco de notas?")
       conteudo = ouvir_comando()

       criar_bloco_notas(nome_arquivo, conteudo)    
        
    elif "enviar mensagem" in comando:
        falar("Para quem devo enviar?")
        contato = ouvir_comando()

        falar("Qual a mensagem?")
        mensagem = ouvir_comando()
        
        enviar_whatsapp(contato, mensagem)   


    elif "alarme" in comando:
       falar("Que hora você quer definir para o alarme?")
       hora_alarme = ouvir_comando()  # Suponha que o usuário fala a hora
       hora_alarme = hora_alarme.split("hora")  # Processando a hora
       tempo_alarme = int(hora_alarme[0].strip()) * 60  # Converte para minutos
       falar(f"Alarme definido para {hora_alarme[0].strip()} minutos")
       time.sleep(tempo_alarme)
       falar("Alarme tocando!")

    elif "abrir youtube" in comando:
        falar("Abrindo o Youtube")
        webbrowser.open("https://www.youtube.com")

    elif "abrir dj" in comando:
        falar("Abrindo o Youtube no canal DJ Julio Beat")
        webbrowser.open("https://www.youtube.com/@DJJULIOBEAT/featured")

    elif "tocar" in comando:
        falar("Tocando música no canal DJ Julio Beat")
        webbrowser.open("https://www.youtube.com/watch?v=AtYuKryoKoI")            

    elif "abrir google" in comando:
        falar("Abrindo o Google")
        webbrowser.open("https://www.google.com")    
             

    elif "sair" in comando or "fechar" in comando:
        falar("Até mais")
        exit()
        
    else:
        falar("Desculpe, não entendi o comando")

# Loop do assistente
falar("Olá! Como posso te ajudar?")
while True:
    comando_usuario = ouvir_comando()
    if comando_usuario:
        executar_comando(comando_usuario)
