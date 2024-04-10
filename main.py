import google.generativeai as genai
import os
from dotenv import load_dotenv


def main():
    assistente_falante = True
    ligar_microfone = True

    load_dotenv()

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])

    ###CONFIGURANDO A VOZ
    if assistente_falante:
        import pyttsx3
        engine = pyttsx3.init()

        voices = engine.getProperty('voices')
        engine.setProperty('rate', 180)  # VELOCIDADE 120 = LENTO

        print("\nLista de Vozes - Verifique o número\n")
        for indice, vozes in enumerate(voices):  # LISTAR VOZES
            print(indice, vozes.name)

        voz = 0
        engine.setProperty('voice', voices[voz].id)

    if ligar_microfone:
        import speech_recognition as sr
        r = sr.Recognizer()
        mic = sr.Microphone()

    bem_vindo = "# Bem Vindo ao Assistente Mil Grau com Gemini AI #"
    print("")
    print(len(bem_vindo) * "#")
    print(bem_vindo)
    print(len(bem_vindo) * "#")
    print("###   Digite 'desligar' para encerrar    ###")
    print("")

    while True:
        if ligar_microfone:
            with mic as fonte:
                r.adjust_for_ambient_noise(fonte)
                print("Fale alguma coisa (ou diga 'desligar')")
                audio = r.listen(fonte)
                print("Enviando para reconhecimento")
                try:
                    texto = r.recognize_google(audio, language="pt-BR")
                    print("Você disse: {}".format(texto))
                except Exception as e:
                    print("Não entendi o que você disse. Erro", e)
                    texto = ""
        else:
            texto = input("Escreva sua mensagem (ou #sair): ")

        if texto.lower() == "desligar":
            break

        if texto.strip():
            response = chat.send_message(texto)
            print("Gemini:", response.text, "\n")

            if assistente_falante:
                texto_fala = response.text.replace('*', '')
                engine.say(texto_fala)
                engine.runAndWait()
        else:
            print("Mensagem vazia, não enviando.")

    print("Encerrando Chat")


if __name__ == '__main__':
    main()
