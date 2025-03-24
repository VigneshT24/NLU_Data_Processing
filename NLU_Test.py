from quadra_nlu import QuadraNLU

while True:
    botEngine = QuadraNLU()
    userInput = input("Query: ")

    # all possible intel that could be gathered
    filteredData = botEngine.parsedData(userInput)
    sentimentType = botEngine.sentimentAnalysis(userInput)
    placesMentioned = botEngine.printPlacesMentioned(userInput)
    popCultureMentioned = botEngine.printPopCulturesMentioned(userInput)
    correctedWords = botEngine.getCorrectedWords()
    isHypothetical = botEngine.is_hypothetical(userInput)

    print("\n")
    print(f"User Input : {userInput}\n")
    print(f"Parsed Input: {filteredData}\n")
    print(f"Sentiment Type : {sentimentType}\n")
    print(f"Places Mentioned : {placesMentioned}\n")
    print(f"Pop Cultures Mentioned : {popCultureMentioned}\n")
    print(f"Corrected Words: {correctedWords}\n")
    print(f"Hypothetical Statement? : {isHypothetical}\n")

