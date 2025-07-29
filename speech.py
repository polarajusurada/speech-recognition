import speech_recognition as sr
import pyttsx3
import openai

# Set your OpenAI API key
openai.api_key = "your-api-key-here"  # 🔑 Replace with your actual API key

# Initialize recognizer and TTS engine
recognizer = sr.Recognizer()
tts = pyttsx3.init()
tts.setProperty("rate", 150)

# Roleplay scenarios
roleplay_data = {
    "school": ["Good morning! What’s your name?", "Do you like school?"],
    "store": ["Welcome! What do you want to buy today?", "One banana coming right up!"],
    "home": ["Who do you live with?", "Do you help them at home?"]
}

def speak(text):
    print(f"🤖 AI: {text}")
    tts.say(text)
    tts.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        print(f"👧 You said: {user_input}")
        return user_input.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Couldn't reach the speech service.")
        return ""

def chat_with_gpt(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly English tutor for kids aged 6 to 16."},
            {"role": "user", "content": message}
        ]
    )
    return response['choices'][0]['message']['content']

def roleplay(mode):
    if mode in roleplay_data:
        for prompt in roleplay_data[mode]:
            speak(prompt)
            child_response = listen()
            if child_response == "":
                break
    else:
        speak("Sorry, I don't know that roleplay.")

# MAIN
speak("Hi! I'm your Genie. Say 'chat' for questions or 'school', 'store', or 'home' for roleplay.")

while True:
    mode = listen()
    
    if "chat" in mode:
        speak("Okay! Ask me anything.")
        question = listen()
        if question:
            reply = chat_with_gpt(question)
            speak(reply)
    
    elif any(keyword in mode for keyword in ["school", "store", "home"]):
        roleplay(mode)
    
    elif "stop" in mode or "exit" in mode:
        speak("Goodbye! Keep practicing!")
        break
    
    else:
        speak("Please say 'chat' or choose a roleplay: school, store, or home.")
