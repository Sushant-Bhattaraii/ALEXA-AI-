import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import googlesearch
import time

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)  # Adjust for noise
            audio = listener.listen(source, timeout=10)  # Allow 5 seconds for response
            command = listener.recognize_google(audio)
            command = command.lower()
            print(f"You said: {command}")
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print("Command after removing 'alexa':", command)
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Please try again.")
    except sr.RequestError:
        print("Speech Recognition service unavailable. Check your internet connection.")
    except Exception as e:
        print(f"Error recognizing voice: {e}")
    
    return command

def search_google(query):
    # Perform Google search and return the first result
    try:
        results = googlesearch.search(query, num_results=1)
        return next(results)  # Get the first result
    except Exception as e:
        print(f"Error with Google search: {e}")
        return None

def run_alexa():
    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk('Playing ' + song)
        pywhatkit.playonyt(song)

    elif 'stop' in command or 'close' in command:
        talk("Stopping the music.")
        pywhatkit.stop()  # This stops the music

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk('The current time is ' + current_time)

    elif 'who is' in command or 'what is' in command or 'tell me something about' in command:
        query = command.replace('who is', '').replace('what is', '').replace('tell me something about', '')
        query = query.strip()  # Remove extra spaces if any
        if query:  # Check if there's something to search
            try:
                # First, try Wikipedia for specific answers
                info = wikipedia.summary(query, sentences=1)
                print(info)
                talk(info)
            except wikipedia.exceptions.DisambiguationError as e:
                talk("There are multiple results, can you be more specific?")
            except wikipedia.exceptions.PageError:
                # If no result in Wikipedia, fall back to Google search
                talk("Sorry, I couldn't find information on Wikipedia. Let me search on Google.")
                google_result = search_google(query)
                if google_result:
                    talk(f"Here is what I found: {google_result}")
                else:
                    talk("Sorry, I couldn't find any information on that.")
            except Exception as e:
                talk("Sorry, I couldn't fetch the information. Please try again.")
        else:
            talk("Sorry, I didn't catch that. Please specify what you'd like to know.")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        print(joke)
        talk(joke)

    elif 'are you single' in command:
        talk('I am in a relationship with WiFi.')

    else:
        talk("I didn't understand. Please say it again.")

# Run the assistant in a loop
while True:
    run_alexa()
    time.sleep(1)  # Delay to prevent it from repeating too quickly
