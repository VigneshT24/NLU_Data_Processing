# NLU Engine Name: Quadra
# This can be used in any program to naturally analyze human languages - ENGLISH ONLY
# INTENT RECOGNITION MODEL
import re
import random

class QuadraNLU:

    # constructor that resets some member variable for fresh start
    def __init__(self):
        self.__correctedWords = []
        self.__identifier = ""
        self.__question_type = ""

    # to utilize these datasets: make QuadraNLU object and then call any or all of these data structures in appropriate places (e.g. to check if user_input contains any of the elements from these datasets)
    # purpose of these lists are for the computer to recognize words or patterns from user_input to better decipher queries

    # list of possible type of questions ~ truncated for flexibility [non-exhaustive]
    __possibleList = [

        # direct-answer question
        ["capital", "distanc", "weather", "movi", "forecast", "cit", "length", "climat", "humidit", "director", "actor", "far", "rain", "snow", "windy", "thunderstorm"],

        # health-related questions
        ["exercis", "diet", "cook", "workout", "routin", "gym", "activit", "nutri", "wellness", "recipi", "fitnes", "yoga", "meditat", "stretch", "cardio", "strength", "vitamin", "calori", "symptom"],

        # productivity questions
        ["calendar", "remind", "product", "task", "schedul", "event", "deadlin", "project", "checklist", "alert", "notif", "organ", "priorit", "goal", "plann", "timelin", "focus", "track", "habit", "workflow"],

        # entertainment questions
        ["scor", "gam", "jok", "song", "challeng", "puzzl", "music", "lyric", "match", "adventur", "humor", "quiz", "fun", "comed", "story", "celebr", "sport", "trend"],

        # mathematical questions
        ["plu", "minus", "multipl", "divid", "formula", "concept", "ratio", "square", "root", "cube", "algebra", "geometr", "calculus", "integr", "deriv", "vector", "probabil", "statist", "measur", "equation", "matrix", "quantit"],

        # knowledge-building question
        ["pric", "mean", "fact", "happen", "latest", "explain", "differenc", "orig", "reason", "impact", "histor", "overview", "background", "going on"],

        # advice-seeking questions
        ["best", "advic", "help", "tip", "plan", "stuck", "assist", "recommend", "suggest", "guid", "strategy", "solv", "improv", "overcom", "choic", "option", "suicid", "therap"],

        # economic questions
        ["cost", "valu", "money", "budget", "cheap", "expens", "discount", "sale", "offer", "stock", "inventor", "demand", "suppl", "quot", "deal", "order", "purchas", "rent", "bill", "econom", "buy"]
    ]

    # list of possible geographical cities/states/countries [mildly-exhaustive]
    __specificPlaceList = [

        # United States - States
        "California", "Texas", "Florida", "New York", "Illinois", "Pennsylvania", "Ohio", "Georgia", "North Carolina",
        "Michigan", "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts", "Tennessee", "Indiana",
        "Missouri",
        "Maryland", "Wisconsin", "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana", "Kentucky",
        "Oregon", "Oklahoma", "Connecticut", "Utah", "Iowa", "Nevada", "Arkansas", "Mississippi", "Kansas",
        "New Mexico",
        "Nebraska", "West Virginia", "Idaho", "Hawaii", "New Hampshire", "Maine", "Montana", "Rhode Island", "Delaware",
        "South Dakota", "North Dakota", "Alaska", "Vermont", "Wyoming",

        # United States - Cities
        "Los Angeles", "Chicago", "San Francisco", "Miami", "Austin", "Las Vegas", "New York City", "Houston",
        "Seattle",
        "Boston", "Atlanta", "Phoenix", "Philadelphia", "San Diego", "Denver", "Dallas", "Orlando", "Tampa",
        "Minneapolis",
        "Detroit", "Portland", "St. Louis", "San Antonio", "Charlotte", "Pittsburgh", "Cleveland", "Kansas City",
        "Indianapolis", "Nashville", "Salt Lake City", "Honolulu", "Albuquerque", "Buffalo", "Sacramento", "Birmingham",
        "Anchorage", "Omaha", "Des Moines", "Boise", "Little Rock", "Jacksonville", "Charleston", "Raleigh",
        "Louisville",
        "Riverside", "Lake Forest", "Irvine", "Anaheim", "Santa Ana", "Chula Vista", "Fresno", "Bakersfield",
        "Stockton",
        "Modesto", "Oxnard", "Fontana", "Moreno Valley", "Huntington Beach", "Glendale", "San Bernardino", "Irvine",
        "Fremont", "San Jose", "Santa Clarita", "Oceanside", "Garden Grove", "Ontario", "Rancho Cucamonga",
        "Santa Rosa",
        "Chandler", "Scottsdale", "Gilbert", "Tempe", "Peoria", "Surprise", "Tucson", "Mesa",

        # Global Cities (Major Capitals and Hubs)
        "London", "Paris", "Berlin", "Madrid", "Rome", "Amsterdam", "Brussels", "Vienna", "Prague", "Moscow",
        "Tokyo", "Seoul", "Beijing", "Shanghai", "Mumbai", "Delhi", "Bangalore", "Jakarta", "Manila", "Bangkok",
        "Singapore", "Hong Kong", "Kuala Lumpur", "Dubai", "Riyadh", "Cairo", "Cape Town", "Johannesburg", "Lagos",
        "Nairobi", "Addis Ababa", "Casablanca", "Buenos Aires", "São Paulo", "Rio de Janeiro", "Santiago",
        "Lima", "Bogotá", "Caracas", "Mexico City", "Toronto", "Vancouver", "Sydney", "Melbourne", "Brisbane",
        "Wellington", "Auckland", "Dublin", "Edinburgh", "Cardiff", "Belfast", "Helsinki", "Stockholm", "Oslo",
        "Copenhagen", "Warsaw", "Budapest", "Belgrade", "Athens", "Istanbul", "Tel Aviv", "Jerusalem", "Doha",
        "Kuwait City", "Muscat", "Hanoi", "Yangon", "Tashkent", "Almaty", "Ulaanbaatar", "Dhaka",

        # Countries
        "United States", "Canada", "United Kingdom", "France", "Italy", "Germany", "Spain", "Mexico", "Brazil",
        "Argentina", "South Africa", "Japan", "India", "China", "Russia", "Australia", "New Zealand", "South Korea",
        "Vietnam", "Thailand", "Philippines", "Malaysia", "Indonesia", "Singapore", "Saudi Arabia",
        "United Arab Emirates",
        "Egypt", "Morocco", "Kenya", "Nigeria", "Turkey", "Greece", "Portugal", "Sweden", "Norway", "Denmark",
        "Netherlands", "Belgium", "Austria", "Switzerland", "Poland", "Czech Republic", "Hungary", "Romania",
        "Bulgaria", "Serbia", "Croatia", "Slovenia", "Bosnia and Herzegovina", "Montenegro", "North Macedonia",
        "Albania", "Ukraine", "Belarus", "Kazakhstan", "Uzbekistan", "Turkmenistan", "Kyrgyzstan", "Armenia", "Georgia",
        "Azerbaijan", "Israel", "Jordan", "Iraq", "Iran", "Pakistan", "Afghanistan", "Bangladesh", "Nepal",
        "Sri Lanka", "Bhutan", "Maldives", "Fiji", "Papua New Guinea", "Samoa", "Tonga", "Tuvalu", "Mongolia",

        # Regions
        "North America", "South America", "Europe", "Asia", "Africa", "Oceania", "Caribbean", "Middle East", "Arctic",
        "Antarctica", "Southeast Asia", "Central Asia", "Eastern Europe", "Western Europe", "Southern Africa",
        "East Africa", "West Africa", "North Africa", "Central America", "Pacific Islands", "Scandinavia",
        "Balkan Peninsula",
        "Iberian Peninsula", "Himalayas", "Sahara Desert", "Amazon Rainforest", "Great Plains", "Rocky Mountains",
        "Andes Mountains", "Alps", "Pyrenees", "Mediterranean", "Atlantic Ocean", "Pacific Ocean", "Indian Ocean",
        "Arctic Ocean", "Baltic Sea", "Caribbean Sea", "Gulf of Mexico", "Bering Strait", "Panama Canal", "Suez Canal",
        "Mount Everest", "Mount Kilimanjaro", "Grand Canyon", "Great Barrier Reef", "Serengeti",
        "Yellowstone National Park",
        "Yosemite National Park", "Victoria Falls", "Niagara Falls", "Amazon River", "Nile River", "Mississippi River",
        "Danube River", "Volga River", "Ganges River", "Mekong River", "Lake Victoria", "Great Lakes"
    ]

    # list of possible pop-culture references [mildly-exhaustive]
    __specificPopCultureList = [

        # Movies (Classic & Modern)
        "The Avengers", "Star Wars", "The Matrix", "Harry Potter", "Jurassic Park", "Titanic", "The Godfather", "Pulp Fiction",
        "Back to the Future", "The Lion King", "Avatar", "Inception", "Frozen", "The Dark Knight", "Forrest Gump",
        "The Shawshank Redemption", "The Lord of the Rings", "Spider-Man", "Iron Man", "Black Panther", "Top Gun",
        "Wonder Woman", "Captain America", "Finding Nemo", "Toy Story", "Shrek", "Cinderella", "Beauty and the Beast",
        "Aladdin", "Pirates of the Caribbean", "The Hunger Games", "The Twilight Saga", "The Fast and the Furious",
        "Transformers", "The Bourne Identity", "Rocky", "Creed", "A Quiet Place", "The Social Network", "The Joker",
        "Interstellar", "Goodfellas", "La La Land", "Coco", "Encanto", "Zootopia", "Minions", "Moana", "Despicable Me",
        "The Little Mermaid", "Dune", "Oppenheimer", "Barbie", "Mission Impossible", "The Incredibles", "It", "Scream",
        "The Conjuring", "Paranormal Activity", "The Exorcist", "Jaws", "A Nightmare on Elm Street", "Halloween",
        "The Texas Chainsaw Massacre", "The Silence of the Lambs", "Get Out", "Us", "Nope", "The Batman", "Deadpool",
        "Logan", "Doctor Strange", "Thor", "Guardians of the Galaxy", "Ant-Man", "Venom", "X-Men", "Justice League",
        "Man of Steel", "The Flash", "Aquaman", "Shazam!", "The Suicide Squad", "John Wick", "Mad Max: Fury Road",
        "Everything Everywhere All at Once", "The Grand Budapest Hotel", "Whiplash", "The Revenant", "Gladiator",
        "Fight Club", "The Truman Show", "The Departed", "Django Unchained", "Kill Bill", "Reservoir Dogs",
        "The Green Mile", "The Pianist", "Saving Private Ryan", "Full Metal Jacket", "Platoon", "Apocalypse Now",
        "Casablanca", "Citizen Kane", "12 Angry Men", "2001: A Space Odyssey", "A Clockwork Orange", "Blade Runner",
        "Scarface", "Taxi Driver", "The Big Lebowski", "American Psycho", "Requiem for a Dream", "Eternal Sunshine of the Spotless Mind",
        "The Sixth Sense", "Se7en", "Memento", "Donnie Darko", "Pan’s Labyrinth", "Oldboy", "Spirited Away", "Your Name",
        "Akira", "Princess Mononoke", "My Neighbor Totoro", "Ghost in the Shell", "The Iron Giant", "Coraline",

        # TV Shows
        "Friends", "Game of Thrones", "House of the Dragon", "Breaking Bad", "Better Call Saul", "The Sopranos",
        "Mad Men", "Stranger Things", "The Office", "Parks and Recreation", "Brooklyn Nine-Nine", "Seinfeld",
        "How I Met Your Mother", "Big Bang Theory", "The Mandalorian", "Andor", "The Book of Boba Fett", "Ahsoka",
        "The Walking Dead", "Fear the Walking Dead", "Westworld", "The Crown", "Euphoria", "Wednesday", "Squid Game",
        "The Witcher", "The Umbrella Academy", "The Boys", "Vikings", "The Last of Us", "American Horror Story",
        "Fargo", "Supernatural", "Glee", "Suits", "Yellowstone", "Peaky Blinders", "True Detective", "Dexter",
        "Lost", "Grey’s Anatomy", "Buffy the Vampire Slayer", "Arrested Development", "Futurama", "Family Guy",
        "South Park", "BoJack Horseman", "Rick and Morty", "Gravity Falls", "Adventure Time", "Steven Universe",
        "Invincible", "Arcane", "One Piece", "Black Mirror", "Doctor Who", "Sherlock", "Merlin",
        "The Twilight Zone", "X-Files", "Hannibal", "Chernobyl", "Band of Brothers", "The Wire",

        # Tech & Electronics
        "Apple", "Samsung", "Google", "Microsoft", "Intel", "Nvidia", "AMD", "Sony", "LG", "Huawei", "Oppo", "OnePlus",
        "Xiaomi", "Motorola", "Lenovo", "Asus", "Acer", "Dell", "HP", "Razer", "Logitech", "Corsair", "Alienware",
        "MSI", "Western Digital", "Seagate", "Kingston", "Crucial", "HyperX", "Bose", "Beats", "JBL", "Sennheiser",
        "Harman Kardon", "Bang & Olufsen", "GoPro", "DJI", "Garmin", "Tesla", "Rivian", "Lucid Motors", "SpaceX",
        "Blue Origin", "Qualcomm", "Cisco", "IBM", "Oracle", "SAP", "Adobe", "Dropbox", "Slack", "Zoom", "Spotify",
        "Netflix", "YouTube", "Meta", "TikTok", "Snapchat", "Twitter", "Reddit", "Discord", "Twitch", "Pinterest",
        "PayPal", "Square", "Stripe", "Robinhood", "Coinbase", "OpenAI", "Salesforce", "Amazon Web Services",
        "Google Cloud", "IBM Watson", "Cloudflare", "Red Hat", "Docker", "GitHub", "GitLab", "Unity", "Unreal Engine",

        # Fashion & Luxury Brands
        "Nike", "Adidas", "Puma", "Reebok", "Under Armour", "New Balance", "Champion", "Fila", "Asics", "Converse",
        "Vans", "Timberland", "The North Face", "Columbia", "Patagonia", "Arc'teryx", "Helly Hansen", "Salomon",
        "Canada Goose", "Gucci", "Louis Vuitton", "Chanel", "Dior", "Hermes", "Prada", "Versace", "Burberry",
        "Balenciaga", "Givenchy", "Valentino", "Dolce & Gabbana", "Fendi", "Yves Saint Laurent", "Tiffany & Co.",
        "Cartier", "Rolex", "Omega", "Tag Heuer", "Patek Philippe", "Hublot", "Breguet", "Montblanc", "Ermenegildo Zegna",
        "Tom Ford", "Hugo Boss", "Ralph Lauren", "Calvin Klein", "Lacoste", "Armani", "Tommy Hilfiger", "Michael Kors",
        "Coach", "Kate Spade", "Marc Jacobs", "Chloe", "Miu Miu", "Celine", "Salvatore Ferragamo", "Bottega Veneta",

        # Food & Beverage
        "McDonald's", "Burger King", "Wendy's", "Taco Bell", "KFC", "Popeyes", "Chick-fil-A", "Subway", "Pizza Hut",
        "Domino's", "Papa John's", "Little Caesars", "Starbucks", "Dunkin'", "Krispy Kreme", "Cinnabon", "Chipotle",
        "Panera Bread", "Five Guys", "In N Out", "Shake Shack", "Carl’s Jr.", "Arby's", "Jack in the Box", "Panda Express",
        "Wingstop", "Jersey Mike’s", "Jimmy John's", "Pepsi", "Coca Cola", "Dr Pepper", "Red Bull", "Monster Energy",
        "Gatorade", "Nestle", "Hershey's", "Mars", "Snickers", "M&M's", "Skittles", "Kit Kat", "Twix", "Oreo",
        "Doritos", "Lay’s", "Pringles", "Ruffles", "Frito-Lay", "Tostitos", "Ben & Jerry's", "Haagen Dazs", "Magnum",

        # Retail & E-commerce
        "Amazon", "Walmart", "Target", "Costco", "Best Buy", "Home Depot", "Lowe’s", "IKEA", "Wayfair", "Macy's",
        "Nordstrom", "Bloomingdale’s", "Saks Fifth Avenue", "Neiman Marcus", "Burlington", "Ross", "TJ Maxx",
        "Marshalls", "Dollar Tree", "Dollar General", "CVS", "Walgreens", "Kroger", "Publix", "Whole Foods", "Trader Joe’s",
        "Aldi", "7-Eleven", "Costco", "Sam’s Club", "eBay", "Etsy", "Zara", "H&M", "Uniqlo", "Shein", "ASOS", "Boohoo",

        # Finance & Banking
        "Visa", "Mastercard", "American Express", "PayPal", "Venmo", "Cash App", "Square", "Stripe", "Bank of America",
        "Chase", "Wells Fargo", "Citibank", "Goldman Sachs", "Morgan Stanley", "JP Morgan", "HSBC", "Barclays", "UBS",
        "Credit Suisse", "Deutsche Bank", "BNP Paribas", "Santander", "Ally Bank", "SoFi", "Robinhood", "Fidelity",
        "Vanguard", "Charles Schwab", "E-Trade", "TD Ameritrade", "Coinbase", "Binance", "Kraken", "FTX",

        # Automotive
        "Tesla", "Toyota", "Honda", "Ford", "Chevrolet", "Dodge", "Jeep", "Ram", "Subaru", "Mazda", "Nissan", "Hyundai",
        "Kia", "Volkswagen", "Audi", "BMW", "Mercedes-Benz", "Porsche", "Jaguar", "Land Rover", "Lexus", "Volvo",
        "Ferrari", "Lamborghini", "McLaren", "Bugatti", "Rolls-Royce", "Bentley", "Aston Martin", "Maserati",
        "Rivian", "Lucid Motors", "Polestar", "Genesis", "Chrysler", "Fiat", "Alfa Romeo", "GMC", "Suzuki"
    
        # Entertainment & Media
        "Disney", "Warner Bros.", "Universal", "Paramount", "Sony Pictures", "20th Century Studios", "Netflix",
        "HBO", "Hulu", "Amazon Prime Video", "Apple TV", "Peacock", "Crunchyroll", "Funimation", "Discovery",
        "National Geographic", "BBC", "CNN", "Fox News", "MTV", "VH1", "Nickelodeon", "Cartoon Network", "Disney Channel",
        "ESPN", "NBA", "NFL", "MLB", "NHL", "WWE", "UFC", "Formula 1", "NASCAR",

        # Airlines & Travel
        "Delta", "American Airlines", "United Airlines", "Southwest", "JetBlue", "Alaska Airlines", "Air Canada",
        "Lufthansa", "British Airways", "Qatar Airways", "Emirates", "Singapore Airlines", "Japan Airlines",
        "Cathay Pacific", "Turkish Airlines", "Air France", "KLM", "Etihad Airways", "Virgin Atlantic", "Ryanair",
        "EasyJet", "Aeromexico", "Qantas", "LATAM", "Norwegian Air", "WestJet", "Hawaiian Airlines",

        # Artists
        "The Beatles", "Beyonce", "Kanye West", "Taylor Swift", "Elvis Presley", "Michael Jackson", "Ariana Grande", "Drake",
        "Lady Gaga", "Eminem", "Ed Sheeran", "Justin Bieber", "Adele", "Rihanna", "Billie Eilish", "The Rolling Stones",
        "Queen", "Pink Floyd", "Led Zeppelin", "Coldplay", "Bruno Mars", "Kendrick Lamar", "Harry Styles", "Doja Cat",
        "Lil Nas X", "Shawn Mendes", "Bad Bunny", "Karol G", "Shakira", "Jennifer Lopez", "Mariah Carey", "Celine Dion",
        "Taylor Swift", "Frank Sinatra", "Whitney Houston", "Prince", "ABBA", "Bee Gees", "Fleetwood Mac", "John Legend",
        "Post Malone", "The Weeknd", "Selena Gomez", "BTS", "Blackpink", "Twice", "EXO", "Stray Kids", "Gorillaz", "Imagine Dragons",
        "Yo Yo Honey Singh", "Anirudh Ravichandran", "Arjith Singh",

        # Video Games
        "Super Mario Bros.", "Minecraft", "Fortnite", "The Legend of Zelda", "Call of Duty", "Grand Theft Auto", "Pokémon",
        "League of Legends", "FIFA", "The Witcher", "Overwatch", "World of Warcraft", "Roblox", "Valorant", "Apex Legends",
        "Counter-Strike", "Elden Ring", "Dark Souls", "Halo", "Assassin's Creed", "God of War", "Red Dead Redemption",
        "The Sims", "Animal Crossing", "Among Us", "Tetris", "Pac-Man", "Donkey Kong", "Fall Guys", "Candy Crush", "Diablo",
        "Horizon Zero Dawn", "Cyberpunk 2077", "Battlefield", "Street Fighter", "Tekken", "PUBG", "Clash of Clans", "Clash Royale"
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
    __correctedWords = []

    __identifier = ""

    __question_type = ""

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
        predefined_exclusions = ["is", "going on", "ate"]
        ignored_words = predefined_exclusions + self.__specificPlaceList + self.__specificPopCultureList
        ignored_pattern = '|'.join(map(re.escape, ignored_words))

        regex = rf'\b(?!(?:{ignored_pattern})\b)' \
        r'(e|es|ing|ed|s|se|ication|ization|isation|ized|ised|ied|ous|y|' \
        r'ies|tion|ent|ents|er|ers|ic|ation|ating|ize|ian|ate|ative|atives|' \
        r'ity|ics|in|inate|ance|ive|al|ist|ists|ivity|ate|al)\b'

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
        lastWord = userInput.strip().split()[-1]

        if (any(lastWord.lower() == word.lower() for word in conjunctions)):
            result = "Incomplete. Ends with a conjunction."
        elif (any(lastWord.lower() == word.lower() for word in auxiliary_verbs)):
            result = "Incomplete. Ends with a auxiliary verb."
        elif (any(lastWord.lower() == word.lower() for word in prepositions)):
            result = "Incomplete. Ends with a preposition."
        return result

    def __getInputCategory(self):
        """
            __getInputCategory Method {private}
            =======================

            Description:
            finds out which category the identifier belongs to by taking advantage of the structural manner of possibleList

            Returns:
            list of string: gives a brief description of the type of categories identifier belongs to

            Raises:
            TypeError: If member variable is not a proper data type
        """
        rowCategory = []
        result = []
        if self.__identifier is not None:
            for row in range(len(self.__possibleList)):
                for column in range(len(self.__possibleList[row])):
                    for a in self.__identifier:
                        if a.strip().lower() == self.__possibleList[row][column].strip().lower():
                            rowCategory.append(row)

        # Iterate through rowCategory and append all possible matches
        for r in rowCategory:
            if r == 0:
                result.append("Direct-Answer Question")
            elif r == 1:
                result.append("Health-Related Question")
            elif r == 2:
                result.append("Productivity Question")
            elif r == 3:
                result.append("Entertainment Question")
            elif r == 4:
                result.append("Mathematical Question")
            elif r == 5:
                result.append("Knowledge-Building Question")
            elif r == 6:
                result.append("Advice-Seeking Question")
            elif r == 7:
                result.append("Economic-Based Question")
        return [] if not result else result

    def parsedData(self, userInput):
        """
            parsedData Method
            =======================

            Description:
            The most important method as it returns parsed and proper "Question Type" [QT], "Identifier" [I], and "Categories" [C] for other programs using this engine for NLU

            Parameters:
            userInput: An input from user that is used to parse and extract information from

            Returns:
            result: A dictionary (hash-map) that includes Question Type and Identifier that other programs can process

            Raises:
            TypeError: If 'userInput' is not a string.
        """
        orig_userInput = userInput
        userInput = self.__stemWord(userInput).lower()
        self.__question_type = self.__removeDuplicate(re.findall(r"(what|who|why|where|when|how|will|can|play|lets|let|should|is|tell|give|if|are|would|could|i)", userInput))
        self.__identifier = self.__removeDuplicate(re.findall(r"(capital|best|cit|length|climat|humidit|director|actor|task|schedul|event|deadlin|project|checklist|alert|notif|organ|advic|stuck|help|tip|distanc|plan|weather|forecast|latest"
                      r"|happen|movi|exercis|song|diet|workout|explain|differenc|routin|gym|activit|nutri|wellness|recipi|fitnes|calendar|remind|cook|scor|pric|mean|plu|ratio|minus|multipl|divid|"
                      r"jok|gam|fact|formula|concept|algebra|geometr|challeng|puzzl|music|lyric|match|adventur|humor|yoga|meditat|stretch|cardio|square|root|cube|"
                      r"strength|vitamin|calori|priorit|goal|plann|timelin|focus|track|habit|workflow|quiz|fun|comedi|story|celebr|sport|trend|"
                      r"calculus|integr|deriv|vector|probabil|statist|measur|equation|symptom|matrix|quantit|orig|reason|impact|histor|overview|background|assist|recommend|suggest|guid|strategy|solv|improv|overcom|choic|option"
                      r"cost|valu|budget|cheap|expens|discount|sale|offer|money|stock|inventor|demand|suppl|quot|deal|order|purchas|rent|bill|suicid|going on|econom|buy|therap|product|far|rain|snow|windy|thunderstorm)", userInput))

        # assigns "result" dictionary its appropriate question_type and identifier
        # only execute this statement if userInput is not incomplete
        if (self.__isIncomplete(orig_userInput, self.__conjunctions, self.__auxiliary_verbs, self.__prepositions) == None):
            if not self.__identifier:
                if self.__autoCorrect(userInput, self.__possibleList) is not None:
                    self.__identifier.extend(self.__autoCorrect(userInput, self.__possibleList))
                    self.__identifier = self.__removeDuplicate(self.__identifier)

        # if multiple "identifier" was found, it only considers one
        if self.__identifier:
            identifier = random.sample(self.__identifier, 1)
            self.__correctedWords.extend(identifier)
        else:
            self.__identifier = self.__isIncomplete(orig_userInput, self.__conjunctions, self.__auxiliary_verbs, self.__prepositions)
            self.__question_type = None
        result =  {"Question Type": self.__question_type, "Identifier": self.__identifier, "Categories": self.__getInputCategory()}
        return result

    def sentimentAnalysis(self, userInput):
        """
            sentimentAnalysis Method
            =======================

            Description:
            Uses userInput to determine the tone of the given input and returns the analysis

            Parameters:
            userInput: An input from the user that will be analyzed

            Returns:
            result: A dictionary [hash-map] that contains the type of sentiment analyzed

            Raises:
            TypeError: If 'userInput' is not a string
        """
        description = ""
        result = {description: []}
        if userInput.__contains__("!") and userInput.__contains__("?"):
            description = "excitement/thrill/confusion"
            result = {description: ["exclamation", "question"]}
        elif userInput.__contains__("!"):
            description = "excitement/thrill"
            result = {description: ["exclamation"]}
        elif userInput.__contains__("?"):
            description = "confusion/clarification"
            result = {description: ["question"]}
        elif userInput.__contains__("...") or userInput.__contains__(".."):
            description = "uncertainty/hesitation"
            result = {description: ["ellipsis"]}
        if userInput.isupper():
            if True in result:
                result[description].append("caps-lock")
            else:
                description = "aggression/frustration"
                result = {description: ["caps-lock"]}
        return result

    # method that returns any possible places that the user mentioned in their original statement ~ improves specific contextualization
    def printPlacesMentioned(self, userInput):
        matches = [place for place in self.__specificPlaceList if
                   re.search(rf'\b{re.escape(place.lower())}\b', userInput.lower())]
        if len(matches) == 1:
            return matches[0]
        elif matches:
            return ", ".join(matches)
        else:
            return ""

    # method that returns any possible pop-culture that the user mentioned in their original statement ~ improves specific contextualization
    def printPopCulturesMentioned(self, userInput):
        matches = [place for place in self.__specificPopCultureList if
                   re.search(rf'\b{re.escape(place.lower())}\b', userInput.lower())]
        if len(matches) == 1:
            return matches[0]
        elif matches:
            return ", ".join(matches)
        else:
            return ""

    # method the returns the correctWords list for public access
    def getCorrectedWords(self):
        return self.__correctedWords

    # method that returns True if the userInput's first word is "if", "would", or "could", indicating hypothetical statement, else false
    def is_hypothetical(self, userInput):
        if not userInput:
            return False
        if len(userInput.split()) >= 2:
            return userInput.split()[0] == "what" and userInput.split()[1] == "if"
        return (userInput.split()[0].lower() == "if" or userInput.split()[0].lower() == "would" or
                userInput.split()[0].lower() == "could")
