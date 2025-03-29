import speech_recognition as sr
import pygame
import google.generativeai as genai
import pyttsx3
import time
import threading
import keyboard
# Google Gemini API
genai.configure(api_key="AIzaSyDcx39dpx5qe4OKSe6L7hi7W7s9bb_KVb0")  # Replace with your key
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
#system instructions
chat = model.start_chat(history=[
    {
        "role": "system",
        "parts":["You are ProHari AI, a virtual assistant. When Someone asks your name or identity , always respond with 'I am ProHari AI, a virtual assistant created by R Harinandan'"]
    }
])
response=model.generate_content([
    "you are ProHari AI, a virtual assistant. When Someone asks your name or identity , always respond with 'I am ProHari AI, a virtual assistant created by R Harinandan'",
    "Whats your name?"
])

system_instruction = "you are ProHari AI, a virtual assistant. When Someone asks your name or identity , always respond with 'I am ProHari AI, a virtual assistant created by R Harinandan'"

# Sound effects
pygame.mixer.init()

def play_sound(file_path):
    """Play a sound effect from the given file path."""
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(5)

# Speech Recognition
def listen_with_google():
    """Listen to the user's voice and convert it to text."""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nListening... Speak now!")
        
        # Play listening sound 
        play_sound(r"listen.mp3")  

        try:
            audio = recognizer.listen(source, timeout=15, phrase_time_limit=30)  # Supports long sentences
            play_sound(r"convert.mp3")  
            
            print("\nProcessing speech...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            
            text = recognizer.recognize_google(audio)
            print("You said: " + text)
            return text
        
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand what you said.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None
        except Exception as e:
            print("Error:", e)
            return None

# AI Response Generation
def gemini_api(text):
    """Generate AI response"""
    try:
        
        if is_asking_name(text):
            response = "I am ProHari AI, a virtual assistant created by R Harinandan"
            return response
        else:
            response = model.generate_content(text)
            return response.text.strip()  # Get only the AI-generated response
    except Exception as e:
        print("Error with Gemini API:", e)
        return "Sorry, I couldn't process your request."
    
# Identity related queries
def is_asking_name(text):
    keywords = ["your name", "who are you", "what's your name", "what is your name", "identity of you", "who is prohari", "who is prohari ai", "who is prohari assistant", "who is prohari robot", "who is prohari ai robot"]
    return any(word in text.lower() for word in keywords)

# Convert text to speech
def text_to_speech(text, voice_index=0, rate=170, volume=1.0):
    """Convert text to speech and speak it."""
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_index].id)   
    engine.setProperty('rate', rate)
    engine.setProperty('volume', volume)
    text1=text.replace("*","")
    print("\nAI: " + text1)  # Display the response
    #New code start
    
    speech_thread = threading.Thread(target=engine.say, args=(text1,))
    speech_thread.start()
    print("Press 'Enter' to stop speaking...")
    while speech_thread.is_alive():
        if keyboard.is_pressed('enter'):
            engine.stop()
            break
        threading.Event().wait(0.1)
    #new code ends 
    engine.runAndWait()

# Main function to run the AI robot
def prohai_robot():
    print("\nWelcome to ProHari AI! (Say 'exit' to stop)")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', 0)  
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    engine.say("Welcome to ProHari AI ! Say 'exit' to stop.")
    engine.runAndWait()

    while True:
        user_input = listen_with_google()
        if user_input:
            if user_input.lower() in ["exit", "quit", "stop"]:
                print("\nExiting AI Robot...")
                text_to_speech("Goodbye! and Have a great day!", voice_index=0)
                break

            ai_response = gemini_api(user_input)
            text_to_speech(ai_response, voice_index=0)  

            time.sleep(1)  # Small delay before next interaction

# Running
prohai_robot()
