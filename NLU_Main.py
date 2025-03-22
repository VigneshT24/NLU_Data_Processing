from quadra_nlu import QuadraNLU
from loadingModule_2 import loadingAnimation
import sys
import string
import time
import re

# method that returns the question-type like 'what', 'when', where' etc...
def printAllQuestionType(processed_data):
   if len(processed_data.get("QT")) == 1:
         return "'" + processed_data.get("QT").__getitem__(0) + "'"
   else:
         result = "mix of "
         try:
               for c in range(len(processed_data.get("QT")) - 1):
                     result += "'" + processed_data.get("QT").__getitem__(c) + "', "
               result += "and '" + processed_data.get("QT").__getitem__(len(processed_data.get("QT")) - 1) + "'"
         except IndexError:
               print("\nI had an issue processing your query. Please re-run the program and rephrase your sentence.")
               sys.exit()
   return result

# method that returns any possible places that the user mentioned in their original statement ~ improves specific contextualization
def printPossibleMentions(saved_input, list):
  matches = [place for place in list if re.search(rf'\b{re.escape(place.lower())}\b', saved_input.lower())]
  if len(matches) == 1:
      return matches[0]
  elif matches:
      return ", ".join(matches)
  else:
      return ""

# method that checks if the given word is in the possibleList matrix to ensure that it can proceed with "what is"
def validateItemAbsent(word, data_instance):
   if not word:
       return False
   for q in range(len(data_instance.possibleList)):
         for w in range(len(data_instance.possibleList[q])):
               for e in word:
                   if e == data_instance.possibleList[q][w]:
                         return False
   return True

# method that returns True if the saved_input's first word is not "if", "would", or "could", else it returns False
def checkFirstWord(saved_input):
   if not saved_input:
       return False
   return (saved_input.split()[0].lower() != "if" and saved_input.split()[0].lower() != "would" and saved_input.split()[0].lower() != "could")

# introductory instructions and terms/conditions
print("QUADRA MODEL SIMULATOR: \n1.) Enter a question that you might ask a robotic/AI system."
   "\n2.) The system will process your response.\n3.) It will give you it's understanding of the question by categorizing it using entry-level Natural Language Understander (NLU) algorithm.\n")
print("Why is this crucial you might ask -> this is the first and most important step taken for many familiar systems like Alexa, ChatGPT, etc to process human language to then take action upon it.\n"
     "This Quadra Engine uses a form of NLU to interpret the query that the user inputs to then explain back to the user what the system understood and deciphered.")
print("The NLU model has recently exited BETA development. While it performs well in tests, it may occasionally misinterpret queries or miss some inputs. "
     "Ongoing improvements are underway based on user feedback. [Version: 4.0]\n\n")
user_input = input("Ask me anything: ")
data_instance = QuadraNLU()
rowCategory = None
BLUE = '\033[34m'
RESET = '\033[0m'

# timer started - to be used to calculate how long this program was used
start_time = time.time()

# loop helps the user continue asking more questions for system categorization
while user_input != "stop":
   saved_input = user_input
   user_input = user_input.lower()
   if not user_input:
       user_input = input(f"{BLUE}Sorry, empty input is not processable, please try again or type 'stop':{RESET} ")
   else:
       processed_data = data_instance.parsedData(user_input)

       # ensures there are no error, else, redirect the issue
       if processed_data.get("QT") != None:
             loadingAnimation()
             print("\n\n")
             for row in range(len(data_instance.possibleList)):
                   for column in range(len(data_instance.possibleList[row])):
                         for a in processed_data.get("I"):
                               if data_instance.possibleList[row][column] == a:
                                     rowCategory = str(row)
             if rowCategory == None and not saved_input.__contains__("what if") and checkFirstWord(saved_input) and not saved_input.__contains__("what is"):
                   user_input = input(f"\n{BLUE}I wasn't able to understand your input. There might not exist any question type or identifier that I can use to process your query.{RESET}\nTry again or type 'stop': ")
             else:
                   # check for any basic sentiment in the given input
                   additive = ""
                   if next(iter(data_instance.sentimentAnalysis(saved_input))):
                       if "caps-lock" in data_instance.sentimentAnalysis(saved_input).get(True):
                           print(f"{BLUE}The first thing I sensed is that your input is in ALL CAPS, which is a strong indicator of urgency, frustration, or excitement of some form.{RESET}")
                           additive = "also "
                       if len(data_instance.sentimentAnalysis(saved_input).get(True)) > 1:
                           print(f"{BLUE}I {additive}sensed the combination of {str(data_instance.sentimentAnalysis(saved_input).get(True)[0])} and {str(data_instance.sentimentAnalysis(saved_input).get(True)[1])} mark, which makes me recognize a mix of confusion and excitement in the given input.{RESET}")
                       elif data_instance.sentimentAnalysis(saved_input).get(True)[0] == "exclamation":
                           print(f"{BLUE}I {additive}sensed the inclusion of an {data_instance.sentimentAnalysis(saved_input).get(True)[0]} mark, which {additive}makes me recognize either an excitement or frustration in the given input.{RESET}")
                       elif data_instance.sentimentAnalysis(saved_input).get(True)[0] == "question":
                           print(f"{BLUE}I {additive}sensed the inclusion of a {data_instance.sentimentAnalysis(saved_input).get(True)[0]} mark, which makes me recognize that your given input wants me to clarify a confusion.{RESET}")
                       elif data_instance.sentimentAnalysis(saved_input).get(True)[0] == "uncertainty":
                           print(f"{BLUE}I {additive}sensed the inclusion of an {data_instance.sentimentAnalysis(saved_input).get(True)[0]} mark, which makes me recognize that you are uncertain about a given topic.{RESET}")
                   print(f"{BLUE}I understand that your input starts with a {printAllQuestionType(processed_data)} and I am supposed to give a(n) {RESET}")
                   place_mentions = printPossibleMentions(saved_input, data_instance.specificPlaceList)
                   pop_culture_mentions = printPossibleMentions(saved_input, data_instance.specificPopCultureList)

                   # list of possible type of questions extracted from user input [mildly-exhaustive]
                   if saved_input.__contains__("what if") or saved_input.split()[0] == "if" or saved_input.split()[0] == "would" or saved_input.split()[0] == "could":
                         if pop_culture_mentions != "":
                            print(f"{BLUE}thoughtful, speculative answer based on logical reasoning, established facts, and potential scenarios of {str(pop_culture_mentions)}.{RESET}")
                         elif place_mentions != "" and pop_culture_mentions == "":
                            print(f"{BLUE}thoughtful, speculative answer based on logical reasoning, established facts, and potential scenarios of {str(place_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}thoughtful, speculative answer based on logical reasoning, established facts, and potential scenarios.{RESET}")
                   elif (saved_input.__contains__("what is") and (validateItemAbsent(data_instance.correctedWord, data_instance) or len(saved_input.split()) == 3)) or saved_input.__contains__("definition"):
                         clean_text = saved_input.translate(str.maketrans('', '', string.punctuation))
                         if clean_text.split().__getitem__(len(clean_text.split()) - 1).isupper():
                            clean_text = clean_text.upper()
                         if not saved_input.__contains__("definition"):
                            print(f"{BLUE}definition and explanation for{clean_text.split("is", 1)[-1]}.{RESET}")
                         elif saved_input.__contains__("definition"):
                            print(f"{BLUE}definition and explanation for{clean_text.split("of", 1)[-1]}.{RESET}")
                         else:
                            print(f"{BLUE}definition and explanation for the given identifier.{RESET}")
                   elif rowCategory == "0":
                         if place_mentions != "" and pop_culture_mentions != "":
                            print(f"{BLUE}clear and succinct response providing general insights into situations, activities, individuals, or weather conditions and forecasts for locations like {str(place_mentions)} and Iconic References like {str(pop_culture_mentions)}.{RESET}")
                         elif place_mentions != "":
                             print(f"{BLUE}clear and succinct response providing general insights into situations, activities, individuals, or weather conditions and forecasts for locations like {str(place_mentions)}.{RESET}")
                         elif pop_culture_mentions != "":
                             print(f"{BLUE}clear and succinct response providing general insights into situations, activities, individuals, or weather conditions and forecasts for Iconic References like {str(pop_culture_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}clear and succinct response providing general insights into locations, situations, activities, individuals, or weather conditions and forecasts, grounded in established facts.{RESET}")
                   elif rowCategory == "1":
                            print(f"{BLUE}insightful, evidence-based response addressing personal or health-related inquiries about diet, lifestyle, and well-being.{RESET}")
                            if place_mentions != "" or pop_culture_mentions != "":
                               print(f"{BLUE}You mentioned places and/or Iconic References like, yet I don't see any relevancy of these mentions to the personal or health-related inquires you asked.{RESET}")
                   elif rowCategory == "2":
                         if place_mentions != "" and pop_culture_mentions != "":
                            print(f"{BLUE}productivity-focused response designed to enhance health, work, or performance efficiency, based on logical reasoning, proven strategies, and relevancy to the following places: {str(place_mentions)} and Iconic References: {str(pop_culture_mentions)}.{RESET}")
                         elif place_mentions != "":
                             print(f"{BLUE}productivity-focused response designed to enhance health, work, or performance efficiency, based on logical reasoning, proven strategies, and relevancy to the following places: {str(place_mentions)}.{RESET}")
                         elif pop_culture_mentions != "":
                             print(f"{BLUE}productivity-focused response designed to enhance health, work, or performance efficiency, based on logical reasoning, proven strategies, and relevancy to the following Iconic References: {str(pop_culture_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}productivity-focused response designed to enhance health, work, or performance efficiency, based on logical reasoning and proven strategies.{RESET}")
                   elif rowCategory == "3":
                         if place_mentions != "" and pop_culture_mentions != "":
                            print(f"{BLUE}engaging, mood-enhancing response tailored to improving your leisure and overall well-being, based on entertainment preferences and refined for the following places: {str(place_mentions)} and Iconic References: {str(pop_culture_mentions)}.{RESET}")
                         elif place_mentions != "":
                             print(f"{BLUE}engaging, mood-enhancing response tailored to improving your leisure and overall well-being, based on entertainment preferences and refined for the following places: {str(place_mentions)}.{RESET}")
                         elif pop_culture_mentions != "":
                             print(f"{BLUE}engaging, mood-enhancing response tailored to improving your leisure and overall well-being, based on entertainment preferences and refined for the following Iconic References: {str(pop_culture_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}engaging, mood-enhancing response tailored to improving your leisure and overall well-being, based on entertainment preferences.{RESET}")
                   elif rowCategory == "4":
                         print(f"{BLUE}concise or detailed mathematical response addressing a concept or calculation, based on established principles and logical reasoning.{RESET}")
                         if place_mentions != "" or pop_culture_mentions != "":
                             print(f"{BLUE}You mentioned places and/or Iconic References, although I am not sure the relevancy of this in the context of mathematical calculation, therefore, I am disregarding them.{RESET}")
                   elif rowCategory == "5":
                         if place_mentions != "" and pop_culture_mentions != "":
                            print(f"{BLUE}informative response aimed at enhancing your understanding of key details related to current or past events and information for places like {str(place_mentions)} and Iconic References like {str(pop_culture_mentions)}.{RESET}")
                         elif place_mentions != "":
                            print(f"{BLUE}informative response aimed at enhancing your understanding of key details related to current or past events and information for places like {str(place_mentions)}.{RESET}")
                         elif pop_culture_mentions != "":
                             print(f"{BLUE}informative response aimed at enhancing your understanding of key details related to current or past events and information for Iconic References like {str(pop_culture_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}informative response aimed at enhancing your understanding of key details related to current or past events and information, grounded in factual accuracy and context.{RESET}")
                   elif rowCategory == "6":
                         if place_mentions != "" and pop_culture_mentions != "":
                            print(f"{BLUE}practical and insightful advice designed to offer you the most effective guidance for better decision-making and results regarding the following places: {str(place_mentions)} and Iconic References like: {str(pop_culture_mentions)}.{RESET}")
                         elif place_mentions != "":
                            print(f"{BLUE}practical and insightful advice designed to offer you the most effective guidance for better decision-making and results in the following places: {str(place_mentions)}.{RESET}")
                         elif pop_culture_mentions != "":
                            print(f"{BLUE}practical and insightful advice designed to offer you the most effective guidance for better decision-making and results regarding Iconic References like: {str(pop_culture_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}practical and insightful advice designed to offer you the most effective guidance for better decision-making and results.{RESET}")
                   elif rowCategory == "7":
                         if place_mentions != "" and pop_culture_mentions != "":
                            print(f"{BLUE}accurate and comprehensive explanation tailored to your inquiries about financial costs, pricing, and availability, designed to provide economic and actionable insights in relevancy to {str(place_mentions)} and Iconic References like {pop_culture_mentions}.{RESET}")
                         elif place_mentions != "":
                            print(f"{BLUE}accurate and comprehensive explanation tailored to your inquiries about financial costs, pricing, and availability, designed to provide economic and actionable insights in relevancy to {str(place_mentions)}.{RESET}")
                         elif pop_culture_mentions != "":
                            print(f"{BLUE}accurate and comprehensive explanation tailored to your inquiries about financial costs, pricing, and availability, designed to provide economic and actionable insights in relevancy to {str(pop_culture_mentions)}.{RESET}")
                         else:
                            print(f"{BLUE}accurate and comprehensive explanation tailored to your inquiries about financial costs, pricing, and availability, designed to provide economic and actionable insights grounded in real-world relevance.{RESET}")
                   user_input = input("\nIs my understanding right? Type 'Y' for Yes or 'N' for No: ").lower()
                   print("Glad I am doing it right. Data has been noted!") if user_input.__contains__("y") else input("In what way should I have interpreted the response: ")
                   print("Thank you for your feedback!\n")
                   user_input = input("\nAsk me anything (or type 'stop' to end): ")
       else:
             if processed_data.get("I") != None:  # the sentence is rather incomplete, let the user know about this
                 user_input = input (f"\n{BLUE}{processed_data.get("I")}{RESET}")
             else:  # query is not recognizable at all
                 user_input = input(f"\n{BLUE}This question is unrecognizable. Try again or type 'stop':{RESET} ")

# post-program time display and feedback system
end_time = time.time()
total_time = int(end_time - start_time)
min = str(int(total_time / 60))
sec = f"0{int(total_time % 60)}" if (total_time % 60) < 10 else str(int(total_time % 60))
user_input = input(f"Now that you have used the program for {min}:{sec}, let me know how well I did: ")
print("Your feedback will help in improving this Quadra Model. Thank you.")
