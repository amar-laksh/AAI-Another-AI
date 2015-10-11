################# OUR MAIN CLASS #################################
class NI():
   
   def __init__(self):
      self.flag1 = 0
      self.rate = 0
      self.questions = []
      self.nouns = []
      self.pronouns = []
      self.posw = []
      self.negw = []
      self.verbs = []
      self.adverbs = []
      self.subjects = []
      self.sbjtree= []
      self.sent = ""
      self.messages = [
         "Hello Sir, Give me a sentence",
         "Hola Boss, Provide me with something",
         "Shoot me a sentence will ya?",
         "Tell me something please!"
         ]

   def message(self):
      import random as r
      choice=r.choice(self.messages)
      self.speak(choice)
      
   
   
   def greetings(self):
      import time as t
      import re
      datematch=re.findall(r'.*?=(.*?),',str(t.localtime()))
      hours = int(datematch[3])
      if(hours <= 12 and hours > 00):
         self.speak("Good Morning Sir")
      elif(hours > 12 and hours <= 18 ):
         self.speak("Good Afternoon Sir")
      elif(hours > 18 and hours < 24):
         self.speak("Good night Sir")         
      
   def find_in(self,sentence,string):
       import os
       import nltk
       import sys

       tokens = nltk.word_tokenize(sentence)
       tagged = nltk.pos_tag(tokens)
       if string == "verb":
           for verb in tagged:
               if 'VB' in str(verb[1:]):
                   self.verbs.append(str(verb[0]))
       elif string == "noun":
           for noun in tagged:
               if ('NN' in str(noun[1:])):
                   self.nouns.append(str(noun[0]))
       elif string == "pronoun":
           for pronoun in tagged:
               if ('PRP' in str(pronoun[1:])) or ('PRP$' in str(pronoun[1:])):
                   self.pronouns.append(str(pronoun[0]))
       elif string == "adverb":
           for adverb in tagged:
               if 'RB' in str(adverb[1:]):
                   self.adverbs.append(str(adverb[0]))
       elif string == "question":
           for question in tagged:
              if question[0] == "why":
                 self.questions.append(str(question[0]))
              elif ('WP' in str(question[1:])) or ('WRB' in str(question[1:])) or ('WDT' in str(question[1:])):
                    self.questions.append(str(question[0]))


   def sbj_tree(self):
       
       nothing_variable = 0
       #print "question, nouns, pronouns, adverbs, verbs = ",self.questions,self.nouns,self.pronouns,self.adverbs,self.verbs
       if (self.adverbs != [] or self.verbs != []):
          if self.nouns != []:
             try:
                if len(self.nouns) == 1:
                   self.sbjtree.append(str(self.nouns))
                else:
                   self.sbjtree.append(str(self.nouns[0]))
             except:
                self.speak("I couldn't find any subjects")
          if self.pronouns != []:
             try:
                if len(self.pronouns) == 1:
                   self.sbjtree.append(str(self.pronouns))
                else:
                   self.sbjtree.append(str(self.pronouns[0]))
             except:
                self.speak("I couldn't find any subjects")
       else:
          self.speak("Don't give me such complicated sentences!")
       
       try:
              self.subjects.append(self.sbjtree[-1])
              self.speak("The subject of the sentence should be,"+str(self.subjects))

       except:
          nothing_variable = 1
       """
       print "RESULTING SUBJECT TREE -"
       print self.sbjtree
       print "##################"
       print " "
       print "##################"
       """
       print "SUBJECT LIST"
       print self.subjects
       print "##################"
        
   def response(self,word):
       import os
       import nltk
       import sys
       tokens = nltk.word_tokenize(word)
       tagged = nltk.pos_tag(tokens)
       """
       print "################"
       print tagged
       print "##################"
       """
       self.find_in(word,"question")
       self.find_in(word,"verb")
       self.find_in(word,"noun")
       self.find_in(word,"pronoun")
       self.find_in(word,"adverb")
       self.sbj_tree()
       #print self.verbs, self.nouns, self.pronouns, self.adverbs
       


   def speak(self,sent):
       import pyttsx
       engine = pyttsx.init()
       engine.setProperty('rate',self.rate)
       voiceid = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0'
       engine.setProperty('voice', voiceid)
       engine.say(sent)
       engine.runAndWait()
       engine.stop()
       
   def goodbye(self):
       if self.sent == "goodbye dear":
           self.speak("Goodbye to you too sir.")
           exit()

   def learn(self,this):
      import mmap
      f = open('learning.txt')
      s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
      if s.find(this) != -1:
         self.speak("I already know the law that "+this)
      else:
         h = open('learning.txt','a')
         h.write(this+"\n")
         h.close
         self.speak("Now I know this law that is "+this)

   def learn_this(self):
      if self.sent[0:][:5] == "learn" or self.sent[0:][:5] == "Learn":
         self.learn(self.sent[5:][1:])
         self.sent = self.sent[5:][1:]

   def STT(self):
      import speech_recognition as sr
      r = sr.Recognizer()
      m = sr.Microphone()
      with m as source:
         r.adjust_for_ambient_noise(source)
         print("Set minimum energy threshold to {}".format(r.energy_threshold))
         print(" \a Listening...")
         audio = r.listen(source)
         print(" \a Recognizing...")
         try:
            self.sent = r.recognize(audio)
            self.flag1 = 0
         except LookupError:
            print("Oops! Didn't catch that")
            self.flag1 = 1

   def read(self):   #(,index):
      #sentences = []
      self.sent = raw_input("Please enter your sentence -> ")
      """
      f = open('learning.txt','r')
      for i in f.readlines():
         sentences.append(i)
      self.sent = sentences[index]
      """
      
############################### NOW THE PROGRAM STARTS #########################
if __name__ == "__main__":
   import time
   ni = NI()
   ni.greetings()
   i = 0 
   while True:
      try:
         ni = NI()
         ni.message()
         #ni.speak("Please speak something to me sir:")
         ni.STT()
         #ni.read()
         #ni.learn_this()
         if ni.flag1 == 0:
             ni.goodbye()
             #print ni.sent
             ni.speak("So you told me,"+str(ni.sent))
             #ni.sent = open('a.txt')
             ni.response(ni.sent)
             i = i + 1
      except:
         break




