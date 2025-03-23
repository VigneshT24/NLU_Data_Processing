# NLU Engine Name: Quadra
# This can be used in any program to naturally analyze human languages - ENGLISH ONLY
# INTENT RECOGNITION MODEL
import re
import random

class QuadraNLU:

    # to utilize these datasets: make QuadraNLU object and then call any or all of these data structures in appropriate places (e.g. to check if user_input contains any of the elements from these datasets)
    # purpose of these lists are for the computer to recognize words or patterns from user_input to better decipher queries

    # list of possible type of questions ~ truncated for flexibility [non-exhaustive]
    __possibleList = [

    # direct-answer question
    ["capital", "distanc", "weather", "movi", "forecast", "cit", "length", "climat", "humidit", "director", "actor"],

    # health-related questions
    ["exercis", "diet", "cook", "workout", "routin", "gym", "activit", "nutri", "wellness", "recipi", "fitnes", "yoga", "meditat", "stretch", "cardio", "strength", "vitamin", "calori", "symptom"],

    # productivity questions
    ["calendar", "remind", "task", "schedul", "event", "deadlin", "project", "checklist", "alert", "notif", "organ", "priorit", "goal", "plann", "timelin", "focus", "track", "habit", "workflow"],

    # entertainment questions
    ["scor", "gam", "jok", "song", "challeng", "puzzl", "music", "lyric", "match", "adventur", "humor", "quiz", "fun", "comed", "story", "celebr", "sport", "trend"],

    # mathematical questions
    ["plu", "minus", "multipl", "divid", "formula", "concept", "ratio", "algebra", "geometr", "calculus", "integrat", "deriv", "vector", "probabil", "statist", "measur", "equation", "matrix", "quantit"],

    # knowledge-building question
    ["pric", "mean", "fact", "happen", "latest", "explain", "differenc", "orig", "reason", "impact", "histor", "overview", "background", "going on"],

    # advice-seeking questions
    ["best", "advic", "help", "tip", "plan", "stuck", "assist", "recommend", "suggest", "guid", "strategy", "solv", "improv", "overcom", "choic", "option", "suicid", "therap"],

    # economic questions
    ["cost", "valu", "budget", "cheap", "expens", "discount", "sale", "offer", "stock", "inventor", "demand", "suppl", "quot", "deal", "order", "purchas", "rent", "bill", "econom", "buy"]
    ]

    # list of possible geographical cities/states/countries [mildly-exhaustive]
    __specificPlaceList = [

    # United States - States
    "California", "Texas", "Florida", "New York", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina",
    "Michigan", "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts", "Tennessee", "Indiana", "Missouri",
    "Maryland", "Wisconsin", "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana", "Kentucky",
    "Oregon", "Oklahoma", "Connecticut", "Utah", "Iowa", "Nevada", "Arkansas", "Mississippi", "Kansas", "New Mexico",
    "Nebraska", "West Virginia", "Idaho", "Hawaii", "New Hampshire", "Maine", "Montana", "Rhode Island", "Delaware",
    "South Dakota", "North Dakota", "Alaska", "Vermont", "Wyoming",

    # United States - Cities
    "Los Angeles", "Chicago", "San Francisco", "Miami", "Austin", "Las Vegas", "New York City", "Houston", "Seattle",
    "Boston", "Atlanta", "Phoenix", "Philadelphia", "San Diego", "Denver", "Dallas", "Orlando", "Tampa", "Minneapolis",
    "Detroit", "Portland", "St. Louis", "San Antonio", "Charlotte", "Pittsburgh", "Cleveland", "Kansas City",
    "Indianapolis", "Nashville", "Salt Lake City", "Honolulu", "Albuquerque", "Buffalo", "Sacramento", "Birmingham",

    # Global Cities (Major Capitals and Hubs)
    "London", "Paris", "Berlin", "Madrid", "Rome", "Amsterdam", "Brussels", "Vienna", "Prague", "Moscow",
    "Tokyo", "Seoul", "Beijing", "Shanghai", "Mumbai", "Delhi", "Bangalore", "Jakarta", "Manila", "Bangkok",
    "Singapore", "Hong Kong", "Kuala Lumpur", "Dubai", "Riyadh", "Cairo", "Cape Town", "Johannesburg", "Lagos",
    "Nairobi", "Addis Ababa", "Casablanca", "Buenos Aires", "São Paulo", "Rio de Janeiro", "Santiago",
    "Lima", "Bogotá", "Caracas", "Mexico City", "Toronto", "Vancouver", "Sydney", "Melbourne", "Brisbane",
    "Wellington", "Auckland", "Dublin", "Edinburgh", "Cardiff", "Belfast", "Helsinki", "Stockholm", "Oslo",
    "Copenhagen", "Warsaw", "Budapest", "Belgrade", "Athens", "Istanbul", "Tel Aviv", "Jerusalem",

    # Countries
    "United States", "Canada", "United Kingdom", "France", "Italy", "Germany", "Spain", "Mexico", "Brazil",
    "Argentina", "South Africa", "Japan", "India", "China", "Russia", "Australia", "New Zealand", "South Korea",
    "Vietnam", "Thailand", "Philippines", "Malaysia", "Indonesia", "Singapore", "Saudi Arabia", "United Arab Emirates",
    "Egypt", "Morocco", "Kenya", "Nigeria", "Turkey", "Greece", "Portugal", "Sweden", "Norway", "Denmark",
    "Netherlands", "Belgium", "Austria", "Switzerland", "Poland", "Czech Republic", "Hungary", "Romania",
    "Bulgaria", "Serbia", "Croatia", "Slovenia", "Bosnia and Herzegovina", "Montenegro", "North Macedonia",
    "Albania", "Ukraine", "Belarus", "Kazakhstan", "Uzbekistan", "Turkmenistan", "Kyrgyzstan", "Armenia", "Georgia",
    "Azerbaijan", "Israel", "Jordan", "Iraq", "Iran", "Pakistan", "Afghanistan", "Bangladesh", "Nepal",
    "Sri Lanka", "Bhutan", "Maldives", "Fiji", "Papua New Guinea", "Samoa", "Tonga", "Tuvalu",

    # Regions
    "North America", "South America", "Europe", "Asia", "Africa", "Oceania", "Caribbean", "Middle East", "Arctic",
    "Antarctica", "Southeast Asia", "Central Asia", "Eastern Europe", "Western Europe", "Southern Africa",
    "East Africa", "West Africa", "North Africa", "Central America", "Pacific Islands", "Scandinavia", "Balkan Peninsula",
    "Iberian Peninsula", "Himalayas", "Sahara Desert", "Amazon Rainforest", "Great Plains", "Rocky Mountains",
    "Andes Mountains", "Alps", "Pyrenees", "Mediterranean", "Atlantic Ocean", "Pacific Ocean", "Indian Ocean",
    "Arctic Ocean", "Baltic Sea", "Caribbean Sea", "Gulf of Mexico", "Bering Strait", "Panama Canal", "Suez Canal"
    ]

    # list of possible pop-culture references [mildly-exhaustive]
    __specificPopCultureList = [

    # Movies
    "The Avengers", "Star Wars", "The Matrix", "Harry Potter", "Jurassic Park", "Titanic", "The Godfather", "Pulp Fiction",
    "Back to the Future", "The Lion King", "Avatar", "Inception", "Frozen", "The Dark Knight", "Forrest Gump", "The Shawshank Redemption",
    "The Lord of the Rings", "Spider-Man", "Iron Man", "Black Panther", "Top Gun", "Wonder Woman", "Captain America",
    "Finding Nemo", "Toy Story", "Shrek", "Cinderella", "Beauty and the Beast", "Aladdin", "Pirates of the Caribbean",
    "The Hunger Games", "The Twilight Saga", "The Fast and the Furious", "Transformers", "The Bourne Identity", "Rocky",
    "Creed", "A Quiet Place", "The Social Network", "The Joker", "Interstellar", "Goodfellas", "La La Land", "Coco",
    "Encanto", "Zootopia", "Minions", "Moana", "Despicable Me", "The Little Mermaid", "Dune", "Oppenheimer", "Barbie", "Mission Impossible",

    # Brands
    "Apple", "Nike", "Tesla", "Coca-Cola", "McDonald’s", "Amazon", "Google", "Adidas", "Disney", "Microsoft", "Nvidia",
    "Samsung", "Sony", "Intel", "Pepsi", "Starbucks", "Walmart", "Gucci", "Louis Vuitton", "Chanel", "Hermès", "Prada",
    "Zara", "H&M", "Patagonia", "North Face", "Rolex", "Omega", "Lego", "Spotify", "Netflix", "YouTube", "Meta",
    "TikTok", "Snapchat", "Bose", "PlayStation", "Xbox", "Nintendo", "Uber", "Lyft", "FedEx", "UPS", "Airbnb", "Balenciaga",
    "Booking.com", "American Express", "Visa", "Mastercard", "Gucci", "Dior", "Cartier", "Burberry", "Versace", "Tiffany & Co.",

    # TV Shows
    "Friends", "Game of Thrones", "The Office", "Stranger Things", "Breaking Bad", "The Simpsons", "The Mandalorian",
    "The Crown", "The Walking Dead", "Westworld", "How I Met Your Mother", "Seinfeld", "Parks and Recreation", "Brooklyn Nine-Nine",
    "Big Bang Theory", "Schitt’s Creek", "Succession", "House of the Dragon", "Euphoria", "Wednesday", "Squid Game",
    "The Witcher", "Better Call Saul", "Mad Men", "Lost", "Grey’s Anatomy", "Dexter", "Buffy the Vampire Slayer",
    "The Sopranos", "True Detective", "The Boys", "Vikings", "The Umbrella Academy", "Arrested Development", "Fargo",
    "American Horror Story", "Ozark", "Supernatural", "Glee", "Suits", "Yellowstone", "The Last of Us", "Peaky Blinders",

    # Artists
    "The Beatles", "Beyoncé", "Kanye West", "Taylor Swift", "Elvis Presley", "Michael Jackson", "Ariana Grande", "Drake",
    "Lady Gaga", "Eminem", "Ed Sheeran", "Justin Bieber", "Adele", "Rihanna", "Billie Eilish", "The Rolling Stones",
    "Queen", "Pink Floyd", "Led Zeppelin", "Coldplay", "Bruno Mars", "Kendrick Lamar", "Harry Styles", "Doja Cat",
    "Lil Nas X", "Shawn Mendes", "Bad Bunny", "Karol G", "Shakira", "Jennifer Lopez", "Mariah Carey", "Celine Dion",
    "Taylor Swift", "Frank Sinatra", "Whitney Houston", "Prince", "ABBA", "Bee Gees", "Fleetwood Mac", "John Legend",
    "Post Malone", "The Weeknd", "Selena Gomez", "BTS", "Blackpink", "Twice", "EXO", "Stray Kids", "Gorillaz", "Imagine Dragons",

    # Video Games
    "Super Mario Bros.", "Minecraft", "Fortnite", "The Legend of Zelda", "Call of Duty", "Grand Theft Auto", "Pokémon",
    "League of Legends", "FIFA", "The Witcher", "Overwatch", "World of Warcraft", "Roblox", "Valorant", "Apex Legends",
    "Counter-Strike", "Elden Ring", "Dark Souls", "Halo", "Assassin's Creed", "God of War", "Red Dead Redemption",
    "The Sims", "Animal Crossing", "Among Us", "Tetris", "Pac-Man", "Donkey Kong", "Fall Guys", "Candy Crush", "Diablo",
    "Horizon Zero Dawn", "Cyberpunk 2077", "Battlefield", "Street Fighter", "Tekken", "PUBG", "Clash of Clans", "Clash Royale",

    # Automotive Brands
    "Rolls-Royce", "Ferrari", "Lamborghini", "Porsche", "Maserati", "Bentley", "Aston Martin", "Bugatti", "McLaren",
    "Mercedes-Benz", "Lexus", "BMW", "Audi", "Toyota", "Honda", "Ford", "Chevrolet", "Jeep", "Hyundai", "Kia", "Mazda",
    "Subaru", "Volkswagen", "Jaguar", "Land Rover", "Tesla", "Rivian", "Lucid Motors", "Volvo", "Peugeot", "Renault",
    "Fiat", "Alfa Romeo", "Citroën", "Dodge", "Chrysler", "Cadillac", "Acura", "Infiniti", "GMC", "Nissan", "Suzuki"
    ]

    # following 3 lists are used to detect specific type of incomplete sentences
    __conjunctions = [
        "if", "but", "and", "so", "because", "or", "then", "although", "though", "whereas", "while", "unless", "until",
        "for", "nor", "yet", "after", "as", "as if", "as long as", "as much as", "as soon as", "as though",
        "before", "even if", "even though", "if only", "in order that", "once",
        "provided that", "rather than", "since", "so that", "than", "that",
        "where", "wherever", "whenever", "whether", "why"
    ]

    __auxiliary_verbs = [
        "is", "was", "were", "am", "are", "be", "being", "been", "will", "shall", "should", "would",
        "can", "could", "may", "might", "must", "do", "does", "did", "has", "have", "had",
        "ought", "need", "dare", "used",
    ]

    __prepositions = [
        "in", "on", "at", "for", "with", "about", "of", "by", "to", "from", "under", "over",
        "between", "into", "onto", "without", "through", "among", "beside", "around", "before",
        "after", "against", "during", "within", "beyond", "beneath", "behind", "above", "below",
        "towards", "along", "across", "throughout", "into", "upon", "through", "out", "up"
    ]

    # helper list that is used for REDUCING autocorrect misinterpretations
    # already implemented, no need to worry
    __autocorrectExceptions = [

    # Common question words
    "what", "who", "why", "where", "when", "how",

    # Modal verbs and auxiliaries
    "will", "can", "shall", "should", "could", "would", "may", "might", "must", "do", "does", "did", "is", "are",
    "was", "were", "be",

    # Common commands and suggestions
    "play", "lets", "let", "go", "stop", "run", "walk", "come", "get", "give", "tell", "show", "find", "make",
    "take",

    # Logical words
    "if", "and", "or", "but", "nor", "yet", "so", "because", "since", "as", "while", "though", "although", "unless",
    "until",

    # Frequently used pronouns and identifiers
    "this", "that", "these", "those", "it", "they", "them", "we", "us", "he", "she", "him", "her", "you", "I", "me",

    # Short confirmation or negation words
    "yes", "no", "not", "ok", "okay", "yeah", "nah",

    # Time-related words
    "today", "tomorrow", "yesterday", "now", "then", "soon", "later", "always", "never", "sometimes", "often",

    # Prepositions and conjunctions
    "in", "on", "at", "with", "by", "for", "to", "of", "off", "about", "above", "below", "before", "after", "during",

    # Miscellaneous
    "why", "try", "ask", "fix", "put", "set", "read", "write", "say", "speak", "think", "feel", "know", "see", "hear",
    "want"
    ]

    # words that are autocorrected
    # to utilize correctedWord: once a word is implicitly autocorrected, you can call this variable to get access to the autocorrected word(s) for any purpose (e.g. access and print the autocorrected word(s) to make it more explicit)
    correctedWord = []

    def __removeDuplicate(self, list):
        """
            __removeDuplicate Method {private}
            =======================

            Description:
            Removes duplicate elements from a list while preserving the order.

            Parameters:
            list: A list of elements to remove duplicates from.

            Returns:
            New List: A list with duplicates removed.

            Raises:
            TypeError: If 'list' is not a list.
        """
        accList = []
        for i in list:
            if i not in accList:
                accList.append(i)
        return accList

    def __stemWord(self, userInput):
        """
            __stemWord Method {private}
            =======================

            Description:
            Removes all instances of suffixes in userInput to achieve base word for easy interpretation

            Parameters:
            userInput: An input from the user that will be stemmed

            Returns:
            Modified Input: A modified input after removing suffixes from userInput

            Raises:
            TypeError: If 'userInput' is not a string
        """
        predefined_exclusions = ["is", "going on"]
        ignored_words = predefined_exclusions + self.__specificPlaceList + self.__specificPopCultureList
        ignored_pattern = '|'.join(map(re.escape, ignored_words))

        regex = rf'\b(?!(?:{ignored_pattern})\b)' \
        r'(e|es|ing|ed|s|se|ication|ization|isation|ized|ised|ied|ous|y|' \
        r'ies|tion|ent|ents|er|ers|ic|ation|ating|ize|ian|ate|ative|atives|' \
        r'ity|ics|in|inate|ance|ive|al|ist|ists)\b'

        return re.sub(regex, '', userInput, flags=re.IGNORECASE)

    def __autoCorrect(self, userInput, c_list):
        """
            __autoCorrect Method {private}
            =======================

            Description:
            Spellchecks and corrects words in userInput in accordance to c_list

            Parameters:
            userInput: An input by the user that will be autocorrect
            c_list: a dictionary list used to compare possibly misspelled words against it to replace it

            Returns:
            result: A list with all corrected words (identifier) for proper interpretation

            Raises:
            TypeError: If 'userInput' is not a string and 'c_list' is not a list.
        """
        inputList = userInput.split()
        inputList = [word for word in inputList if word.lower() not in self.__autocorrectExceptions]
        count = 0
        result = []
        for r in range(len(c_list)):
            for c in range(len(c_list[r])):
                for n in inputList:
                    iter = min(len(n), len(c_list[r][c]))
                    for i in range(iter):
                        if list(n).__getitem__(i) == list(c_list[r][c]).__getitem__(i):
                            count += 1
                        elif (i + 1) < len(c_list[r][c]):
                            if list(n).__getitem__(i) == list(c_list[r][c]).__getitem__(i + 1):
                                count += 1
                    if (count / max(len(n), len(c_list[r][c]))) * 100 >= 70:
                        result.append(c_list[r][c])
                count = 0
        return result if result else None

    def parsedData(self, userInput):
        """
            parsedData Method
            =======================

            Description:
            The most important method as it returns parsed and proper "Question Type" [QT] and "Identifier" [I] for other programs using this engine for NLU

            Parameters:
            userInput: An input from user that is used to parse and extract information from

            Returns:
            result: A dictionary (hash-map) that includes Question Type and Identifier that other programs can process

            Raises:
            TypeError: If 'userInput' is not a string.
        """
        orig_userInput = userInput
        userInput = self.__stemWord(userInput)
        question_type = self.__removeDuplicate(re.findall(r"(what|who|why|where|when|how|will|can|play|lets|let|should|is|tell|give|if|are|would|could|i)", userInput))
        identifier = self.__removeDuplicate(re.findall(r"(capital|best|cit|length|climat|humidit|director|actor|task|schedul|event|deadlin|project|checklist|alert|notif|organ|advic|stuck|help|tip|distanc|plan|weather|forecast|latest"
                      r"|happen|movi|exercis|song|diet|workout|explain|differenc|routin|gym|activit|nutri|wellness|recipi|fitnes|calendar|remind|cook|scor|pric|mean|plu|ratio|minus|multipl|divid|"
                      r"jok|gam|fact|formula|concept|algebra|geometr|challeng|puzzl|music|lyric|match|adventur|humor|yoga|meditat|stretch|cardio|"
                      r"strength|vitamin|calori|priorit|goal|plann|timelin|focus|track|habit|workflow|quiz|fun|comedi|story|celebr|sport|trend|"
                      r"calculus|integrat|deriv|vector|probabil|statist|measur|equation|symptom|matrix|quantit|orig|reason|impact|histor|overview|background|assist|recommend|suggest|guid|strategy|solv|improv|overcom|choic|option"
                      r"cost|valu|budget|cheap|expens|discount|sale|offer|stock|inventor|demand|suppl|quot|deal|order|purchas|rent|bill|suicid|going on|econom|buy|therap)", userInput))

        # assigns "result" dictionary its appropriate question_type and identifier
        # only execute this statement if userInput is not incomplete
        if (self.__isIncomplete(orig_userInput, self.__conjunctions, self.__auxiliary_verbs, self.__prepositions) == None):
            if not identifier:
                if self.__autoCorrect(userInput, self.__possibleList) is not None:
                    identifier.extend(self.__autoCorrect(userInput, self.__possibleList))
                    identifier = self.__removeDuplicate(identifier)

        # if multiple "identifier" was found, it only considers one
        if identifier:
            identifier = random.sample(identifier, 1)
            self.correctedWord.extend(identifier)
        else:
            identifier = self.__isIncomplete(orig_userInput, self.__conjunctions, self.__auxiliary_verbs, self.__prepositions)
            question_type = None
        result =  {"QT": question_type, "I": identifier}
        return result

    def sentimentAnalysis(self, saved_input):
        """
            sentimentAnalysis Method
            =======================

            Description:
            Uses saved_input to determine the tone of the given input and returns the analysis

            Parameters:
            saved_input: An input from the user that will be analyzed

            Returns:
            result: A dictionary [hash-map] that contains the type of sentiment analyzed

            Raises:
            TypeError: If 'saved_input' is not a string
        """
        result = {False: []}
        if saved_input.__contains__("!") and saved_input.__contains__("?"):
            result = {True: ["exclamation", "question"]}
        elif saved_input.__contains__("!"):
            result = {True: ["exclamation"]}
        elif saved_input.__contains__("?"):
            result = {True: ["question"]}
        elif saved_input.__contains__("...") or saved_input.__contains__(".."):
            result = {True: ["uncertainty"]}
        if saved_input.isupper():
            if True in result:
                result[True].append("caps-lock")
            else:
                result = {True: ["caps-lock"]}
        return result
    def __isIncomplete(self, userInput, conjunctions, auxiliary_verbs, prepositions):
        """
            __isIncomplete Method {private}
            =======================

            Description:
            goes through one of the three lists from the parameter to detect if userInput is incomplete or not

            Parameters:
            userInput: An input by the user that will be checked for possible incompleteness
            conjunctions: a list of conjunction words to detect
            auxiliary_verbs: a list of auxiliary verbs to detect
            prepositions: a list of preposition words to detect

            Returns:
            result: A phrase that lets the user know, with a personalized message, that their input was incomplete

            Raises:
            TypeError: If 'userInput' is not a string
        """
        result = None
        lastWord = userInput.split()[-1]

        # list of possible personalized responses to incomplete queries that will be chosen at random
        responses = [
            f"Your sentence got cut off. You were saying: '{lastWord}', but what? Try again or type 'stop': ",
            f"It looks like your question is incomplete. You ended with '{lastWord}', which suggests there's more to say. Could you clarify or type 'stop': ",
            f"Hmm… your sentence stops at '{lastWord}', making it feel unfinished. What were you about to say. Try again or type 'stop': ",
            f"You left me hanging! You said: '{lastWord}', but I think there’s more to it. Could you rephrase or type 'stop': ",
            f"Your message seems incomplete—it ended with '{lastWord}', which usually means there's more to follow. Could you complete it or type 'stop': ",
            f"Oops! It looks like your message trails off at '{lastWord}'. Can you finish your thought or type 'stop': ",
            f"Uh-oh, sentence cliffhanger detected! 😆 You stopped at '{lastWord}'—but what? Don’t keep me in suspense! Try again or type 'stop': ",
            f"It feels like you were about to say something important! You ended with '{lastWord}', but I think there’s more. Fill me in or type 'stop': ",
        ]
        if (any(lastWord.lower() == word.lower() for word in conjunctions)):
            result = random.choice(responses)
        elif (any(lastWord.lower() == word.lower() for word in auxiliary_verbs)):
            result = random.choice(responses)
        elif (any(lastWord.lower() == word.lower() for word in prepositions)):
            result = random.choice(responses)
        return result
