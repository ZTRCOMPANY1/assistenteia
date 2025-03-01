import speech_recognition as sr
import webbrowser
import pyttsx3
import wikipedia
import datetime

#inicializa o motor de voz
engine = pyttsx3.init()
engine.setProperty('rate', 180) #velocidade de fala
engine.setProperty('volume', 1) #volume maximo

def falar(texto):
    """Faz o assistente falar"""
    engine.say(texto)
    engine.runAndWait()
    
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
        
    elif "pesquisar" in comando:
        comando = comando.replace("pesquisar", "").strip()
        resultado = wikipedia.summary(comando, sentences=2, lang="pt")  
        falar(resultado)
    
    elif "abrir youtube" in comando:
        falar("abrindo o Youtube")
        webbrowser.open("https://www.youtube.com")
        
    elif "abrir dj" in comando:
        falar("abrindo o Youtube no canal dj julio beat")
        webbrowser.open("https://www.youtube.com/@DJJULIOBEAT/featured")
     
    elif "tocar" in comando:
        falar("abrindo o Youtube no canal dj julio beat")
        webbrowser.open("https://www.youtube.com/watch?v=AtYuKryoKoI")            
        
    elif "pesquisar" in comando:
        comando = comando.replace("pesquisar", "").strip()
        resultado = wikipedia.summary(comando, sentences=2, lang="pt")
        falar(f"Aqui está o que encontreis na Wikipédia sobre {comando}:")
        falar(resultado)    
        
    elif "abrir Google" in comando:
        falar("abrindo Google")
        webbrowser.open("https://www.google.com")       
        
    elif "sair" in comando or "fechar" in comando:
        falar("Até mais")
        exit()
    
    else:
        falar("Desculpe, Não entendi o comando")
        
# Loop do assistente
falar("Olá! Como posso te ajudar?")
while True:
    comando_usuario = ouvir_comando()
    if comando_usuario:
        executar_comando(comando_usuario)                
        
          