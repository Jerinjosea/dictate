import pyttsx3
import time
import os
from pynput import keyboard

engine = pyttsx3.init()

#change basic properties here
engine.setProperty('rate', 120) #set speed here
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female

language = 'en-IN'
#change language here
#find supported languages here https://cloud.google.com/text-to-speech/docs/voices

N=4
#number of words spelled at a time

def splitTextToFour(string):
    words = string.split()
    grouped_words = [' '.join(words[i: i + N]) for i in range(0, len(words), N)]
    return grouped_words
#function to split lines to group of words


def isVowel(ch): 
    return (ch == 'a' or ch == 'e' or 
            ch == 'i' or ch == 'o' or 
            ch == 'u') 
  
# Function to calculate difficulty 
def calcDiff(str): 
    str = str.lower() 
    count_vowels = 0
    count_conso = 0
    consec_conso = 0
    hard_words = 0
    easy_words = 0
  
    # Start traversing the string 
    for i in range(0, len(str)): 
          
        # Check if current character is  
        # vowel or consonant 
        if(str[i]!= " " and isVowel(str[i])): 
              
            # Increment if vowel 
            count_vowels += 1
            consec_conso = 0
              
        # Increment counter for consonant 
        # also mainatin a separate counter for 
        # counting consecutive consonants  
        elif(str[i] != " "): 
            count_conso += 1
            consec_conso += 1
  
        # If we get 4 consecutive consonants 
        # then it is a hard word  
        if(consec_conso == 4): 
            hard_words += 1
  
            # Move to the next word 
            while(i < len(str) and str[i] != " "): 
                i += 1
                  
            # Reset all counts  
            count_conso = 0
            count_vowels = 0
            consec_conso = 0
        elif(i < len(str) and (str[i] == ' ' or
                          i == len(str) - 1)): 
                                
            # Increment hard_words, if no. of  
            # consonants are higher than no. of  
            # vowels, otherwise increment count_vowels 
            if(count_conso > count_vowels): 
                hard_words += 1
            else: 
                easy_words += 1
  
            # Reset all counts  
            count_conso = 0
            count_vowels = 0
            consec_conso = 0
              
    # Return difficulty of sentence      
    return (5 * hard_words + 3 * easy_words)

#for using pause
def on_press(key):
    if key == keyboard.Key.space:
        print("\n!!Paused!!\nEnter space to resume\n")
        input("enter r:")
            

f = open("text.txt",'r',encoding = 'utf-8')

st = f.read()

lines = st.split('.')

for line in lines:
    splited =  splitTextToFour(line)
    #split paragraph in to lines
    for word in splited:
        d=calcDiff(word) #calculate difficulty of words
        engine.say(word)
        engine.runAndWait()
        time.sleep(2)
        print(word)
        #to repeat if required
        if d>17: #change this value if required
            time.sleep(4)
            engine.say(word)
            engine.runAndWait()
    time.sleep(2)
time.sleep(2) #to give a pause after a line
engine.say('next sentence')


f.close()