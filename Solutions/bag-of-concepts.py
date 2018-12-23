'''
FILE NAME: bag-of-concepts
AUTHOR(S): Shabnam naz
DATE     : 23 July 2018
EMAIL    : naz.reshmi@gmail.com
'''

#----------------------------------------------------------------------------

                            # Imports Section

#python libraries
import urllib.request
import re
import os
import string
import nltk
import http.client
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
from readability.readability import Document
from spellchecker import SpellChecker
from vocabulary.vocabulary import Vocabulary as vb
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from textblob.classifiers import NaiveBayesClassifier

#----------------------------------------------------------------------------
                            # Global Variables Section

log_file_handler = 'null'

#----------------------------------------------------------------------------


#----------------------------------------------------------------------------

# training data set
train = [
    ("browser", "technology"),
    ("science", "technology"),
    ("automation", "technology"),
    ("machine", "technology"),
    ("computer", "technology"),
    ("malware", "technology"),
    ("spam", "technology"),
    ("artificial intelligence", "technology"),
    ("internet", "technology"),
    ("virus", "technology"),
    ("employment employee", "business"),
    ("corporation", "business"),
    ("startup startups", "business"),
    ("company companies", "business"),
    ("shop shopping", "business"),
    ("factory factories", "business"),
    ("market marketing", "business"),
    ("setup transaction", "business"),
    ("sale sales industry", "business"),
    ("import export","business"),
    ("watch watches", "gadget"),
    ("device", "gadget"),
    ("phones smartphone smartphones", "gadget"),
    ("laptop", "gadget"),
    ("tv television", "gadget"),
    ("alarm clock clock", "gadget"),
    ("camera ipod", "gadget"),
    ("pendrive", "gadget"),
    ("headphone headphones", "gadget"), 
    ("engineer engineering scientist", "occupation"),
    ("player artist", "occupation"),
    ("intern journalist", "occupation"),
    ("professor", "occupation"),
    ("entrepreneur farmer", "occupation"),
    ("actor", "occupation"),
    ("doctor lawyer","occupation"),
    ("law", "politics"),
    ("elections rights", "politics"),
    ("government parliament", "politics"),
    ("party public", "politics"),
    ("votes assembly", "politics"),
    ("ministers bill legal", "politics"),
    ("politician political", "politics"),
    ("politics policy", "politics"),
    ("research", "study"),
    ("degree", "study"),
    ("education", "study"),
    ("athletics badminton", "sports"),
    ("ball scores", "sports"),
    ("batsman basketball", "sports"),
    ("cricket", "sports"),
    ("game goal", "sports"),
    ("football", "sports"),
    ("players", "sports"),
    ("hockey running  bowler", "sports"),
    ("tennis chess score scored", "sports"),
    ("sports stadium stadiums", "sports"),
    ("world cup winner", "sports"),
    ("cakes cake candies", "foods"),
    ("chocolates fruits", "foods"),
    ("sweets tofee vegetables", "foods"),
    ("restuarent spices", "foods"),
    ("australia egypt country", "country"),
    ("germany german", "country"),
    ("usa us nations", "country"),
    ("uk canada", "country"),
    ("india", "country"),
    ("airplane cycle bus", "vehicles"),
    ("cab ship", "vehicles"),
    ("bikes bike motorcycle", "vehicles"),
    ("cars car plane", "vehicles"),
    ("train railway", "vehicles"),
    ("awards acheivements", "famous"),
    ("personality characters", "famous"),
    ("legends inspirational", "famous"),
    ("inspriers positive", "famous"),
    ("mens man kids", "famous"),
    ("articles", "study"),
    ("news", "study"),
    ("university universities", "study"),
    ("analysis", "study"),
    ("college colleges", "study"),
    ("schools school", "study"),
    ("happiness knowledge", "study"),
    ("womens woman childrens", "famous"),
    ("born birthday", "famous")
    ]

# Naive Bayesian classification on train data set
cl = NaiveBayesClassifier(train)

#----------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# FUNCTION NAME : create_log
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Opens a log file to log the program execution details. 
#           
# ---------------------------------------------------------------------------
def create_log():
    # global variables are used with the keyword 'global' when
    # they are used inside functions
    global log_file_handler
    log_file_handler = open("Bag_of_Concepts_log.txt", "a")
    log_file_handler.write(str(datetime.datetime.now()) + " Log file opened."+ "\n")
    
    
    
# ---------------------------------------------------------------------------
# FUNCTION NAME : close_log
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Closes the log file.
#           
# ---------------------------------------------------------------------------
def close_log():
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " Log file closed."+ "\n")
    log_file_handler.close()
    

    
# ---------------------------------------------------------------------------
# CLASS NAME    : InvalidKeywordError
# ---------------------------------------------------------------------------
# PARAMETERS	: Exception
# ---------------------------------------------------------------------------
# RETURN	: Value
# ---------------------------------------------------------------------------
# DESCRIPTION	: User-defined exception class.
#           
# ---------------------------------------------------------------------------
class InvalidKeywordError(Exception):
    def _str_(self):
        return(repr(self.value))
    

    
# ---------------------------------------------------------------------------
# FUNCTION NAME : user_input
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Fetches search words from user to search.
#                 Pass keywords to spell_check function call.          
# ---------------------------------------------------------------------------    
def user_input():
    global log_file_handler       
    log_file_handler.write(str(datetime.datetime.now()) + " user_input function reach."+ "\n")
    
    # Collect words to search from user
    print("Enter the Keyword/s. [use - instead of space for more than one word]")
    key = [x for x in input("Search For :").split(',')]
    log_file_handler.write(str(datetime.datetime.now()) + " user input collected."+ "\n")

    log_file_handler.write(str(datetime.datetime.now()) + " user_input function terminate."+ "\n")
    #function call
    spell_check(key)
    
    
    
# ---------------------------------------------------------------------------
# FUNCTION NAME : spell_check
# ---------------------------------------------------------------------------
# PARAMETERS	: Key(keywords)
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Checks for spellings and grammer of keywords.
#                 Suggests correct word, asks for removal or replacement
#                 of words.
#                 Pass updated keywords to collect_urls function call.          
# --------------------------------------------------------------------------- 
def spell_check(key):
    global log_file_handler       
    log_file_handler.write(str(datetime.datetime.now()) + " spell_check function reach."+ "\n")
    
    newKeywords = []
    spell = SpellChecker()
    check = '[-@_!#$%^&*()<>?/\|+}{~:]+'
    
    # Splits each word in key and check for special characters and removes it
    for thisWord in key:
        # inputWord is a list consisting of spilted words
        inputWord = re.split(check, thisWord, flags=re.IGNORECASE)
        
        # loop checks each word for spellings and grammatical errors
        for word in inputWord:
            try:
                # raises error if word has no meaning meaning - word entered is invalid
                if vb.meaning(word) == False:
                    raise (InvalidKeywordError("\nImproper Input!"))
                
                # no error if word meaning exists
                elif spell.correction(word) == word or vb.meaning(word) != False:
                    continue
                
            # handles error                
            except InvalidKeywordError as error:
                log_file_handler.write(str(datetime.datetime.now()) + " error occured in spell_check."+ "\n")
                print(error)
                print(thisWord,'\t:',word)

                # asks user to enter choice for the word that caused error
                print("\nError Type:")
                print("1.Input Word has Spelling Error.")
                print("2.No Errors")
                print("3.Remove word")
                get_numb = int(input("Enter Error no. :"))
            
                if get_numb == 1:
                    # suggests near correct word
                    print("\nSuggestions:",spell.candidates(word))
                    pos = inputWord.index(word)

                    # pops error word,replace and insert correct word in the same position
                    inputWord.pop(pos)
                    inputWord.insert(pos,word.replace(word,input("Enter correct word:")))
                    #print(inputWord)
                    continue
                
                elif get_numb == 2:
                    print("Okay!!")
                    continue
                
                elif get_numb == 3:
                    # deletes irrelevant words 
                    pos = inputWord.index(word)
                    inputWord.pop(pos)
                    continue

                    
        if len(inputWord) >= 2:
            # joins the group of words that were spilt(if word more than 1 in list)
            #and appends in new list
            inputWord = "-".join(inputWord)
            newKeywords.append(inputWord)
            

        elif len(inputWord) <= 2:
            # add words to the list having length of the word in list less than or equal to 2  
            newKeywords.extend(inputWord)
    
    print("\n Final Check:")
    log_file_handler.write(str(datetime.datetime.now()) + " checking final keywords."+ "\n")
    print(newKeywords)
    # asks user to either 'remove/replace' or 'procceed' further
    option = int(input("Remove or Replace[with '-'] Keyword-[1]/procceed-[2] :"))
    if option == 1:
        log_file_handler.write(str(datetime.datetime.now()) + " modifications require for keywords."+ "\n")
        # clears the 'key' list and adds words from 'newKeywords'
        key.clear()
        key.extend(newKeywords)
        
        # shows position of each word in list
        print("Position of Words:-")
        for num in key:
            print(num,'\t :',key.index(num))
            
        # takes position number from user to edit word
        # in case word is wrongly entered or replaced in the list
        # takePos is a list of positions of wrong entered words
        takePos = [int(num) for num in input("Position to remove:").split(',')]
        for tp in takePos:
            for new_thisWord in key:
                keyPos = key.index(new_thisWord)

                # loops until word in 'key' list matches with position in 'takePos' list
                if tp != keyPos:
                    continue
                else:
                    # if found, pops the word
                    key.pop(keyPos)
                    print("\n",new_thisWord,'-> popped')

                    # asks either to replace or continue further
                    option = int(input("Replace - [Yes-(1)/No-(2)]:"))
                    if option == 1:
                        log_file_handler.write(str(datetime.datetime.now()) + " keyword is replaced."+ "\n")
                        # inserts new word in place of popped word
                        key.insert(keyPos,new_thisWord.replace(new_thisWord,input("Enter correct word:")))
                    elif option == 2:
                        log_file_handler.write(str(datetime.datetime.now()) + " no replacement, continue."+ "\n")
                        print("okay!")
                        break
        print(key)
        log_file_handler.write(str(datetime.datetime.now()) + " spell_check function terminate."+ "\n")
        #function call
        collect_urls(key)
                        
    elif option == 2:
        log_file_handler.write(str(datetime.datetime.now()) + " proceed further."+ "\n")
        
        print("Yes!")
        log_file_handler.write(str(datetime.datetime.now()) + " spell_check function terminate."+ "\n")
        
        # clears the 'key' list and adds words from 'newKeywords'
        key.clear()
        key.extend(newKeywords)
        #function call
        collect_urls(key)
        

        
# ---------------------------------------------------------------------------
# FUNCTION NAME : collect_urls
# ---------------------------------------------------------------------------
# PARAMETERS	: Key
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Collects the relevant urls from the search engine for the
#                 user supplied keyword. 
#                 Writes all the results into a file.
# ---------------------------------------------------------------------------
def collect_urls(key):
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " collect_urls function reach."+ "\n")
    try:
        #urllib.request.build_opener() returns an OpenerDirector instance, which chains the handlers in the order given.
        #The OpenerDirector class opens URLs.
        opener = urllib.request.build_opener()

        #headers are dictionary that accepts a key and a value.
        #User-agent header is used by a browser to identify itself.
        #here Mozilla5.0 is used as a browser.
        opener.addheaders = [('User-agent', 'Chrome/35.0.1916.47')]

        #opens the text file links.txt in write mode which is assigned to a file-object file
        file = open("links.txt", "w",encoding="utf-8")
        
        for searchWord in key:
            #url format appended with the keyword to be searched
            url = "http://www.google.com/search?q="+ searchWord +"&start="

            #opens the webpage in the browser with the above url
            page = opener.open(url)
            log_file_handler.write(str(datetime.datetime.now()) + " url opened successfully."+ "\n")

            #specifies that the html parser is used to parse the data returned from the page
            soup = BeautifulSoup(page, "html.parser")

            #soup.find_all() method will perform a match against that of argument provided
            #here each match is the url of the cite which is written in the file links.txt
            for cite in soup.find_all('cite'):
                file.write(cite.text)
                file.write("\n")
            file.write("----------------------------------------------------------------------------")
            file.write("\n")
            log_file_handler.write(str(datetime.datetime.now()) + " links upadated in file - links.txt."+ "\n")

        file.close()
        log_file_handler.write(str(datetime.datetime.now()) + " collect_urls function terminate."+ "\n")
    
    except (urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, BaseException):
        log_file_handler.write(str(datetime.datetime.now()) + " failed to open url."+ "\n")
        pass
    
    

# ---------------------------------------------------------------------------
# FUNCTION NAME : validate_urls
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Removes the irrelevant urls from the text file. 
#                 Writes all the results into a new file.
#                 Removes the previous file.
# ---------------------------------------------------------------------------
def validate_urls():
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " validate_urls function reach."+ "\n")
    
    # opens new file to store only valid links
    forWrite = open("validlinks.txt", "w")
    log_file_handler.write(str(datetime.datetime.now()) + " check for invalid urls in file - links.txt."+ "\n")
    with open('links.txt') as forRead:
        for eachLine in forRead:
            if eachLine.find("www") >= 0 and \
               eachLine.find("youtube") == -1 and \
               eachLine.find("facebook") == -1 and \
               eachLine.find("imdb") == -1 and \
               eachLine.find("...") == -1:
                forWrite.write(eachLine)
                
    forWrite.close()
    forRead.close()
    log_file_handler.write(str(datetime.datetime.now()) + " valid links updated in file - validlinks.txt."+ "\n")
    print("Check the file validlinks.txt for results!")

    # deletes 'links.txt' file
    if os.path.exists("links.txt"):
        os.remove("links.txt")
        log_file_handler.write(str(datetime.datetime.now()) + " links.txt - file removed."+ "\n")
    else:
        print("File does not exists!!")
        log_file_handler.write(str(datetime.datetime.now()) + " error occured to remove file - links.txt ."+ "\n")

    log_file_handler.write(str(datetime.datetime.now()) + " validate_urls function terminate."+ "\n")

    

# ---------------------------------------------------------------------------
# FUNCTION NAME : fetch_text
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Removes formatting of the text and collects plain text and
#                 titles. 
#                 Writes all the results into new files.
# ---------------------------------------------------------------------------
def fetch_text():
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " fetch_text function reach."+ "\n")
    
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-agent', 'Chrome/35.0.1916.47')]

    # opens text file to store data from each links
    forWrite = open("web_data.txt", "w")
    forRead = open("validlinks.txt", "r")
    forTitle = open("titles.txt","w")
    readable_title = []


    # removes HTML formatting of the text and collects only plain text/data 
    with open("validlinks.txt") as forRead:
        log_file_handler.write(str(datetime.datetime.now()) + " opens each url in file - validlinks.txt."+ "\n")
        for eachLine in forRead:
            try:
                if eachLine.startswith("http"):
                    con = urlopen(eachLine).read()
                    readable_article = Document(con).summary()
                    readable_title = Document(con).title()
                    forTitle.write(readable_title)
                    forTitle.write("\n")
                    
                    
                else:
                    con = urlopen("http://"+eachLine).read()
                    readable_article = Document(con).summary()
                    readable_title = Document(con).title()
                    forTitle.write(readable_title)
                    forTitle.write("\n")

                soup = BeautifulSoup(readable_article,"lxml")

            except(urllib.request.HTTPError, urllib.request.URLError, http.client.HTTPException, http.client.IncompleteRead, BaseException):
                log_file_handler.write(str(datetime.datetime.now()) + " failed to open url."+ "\n")
                continue

            try:
                # adds delimeter at the end of portion of text from each link
                result = soup.text[:600]+'...\"'
                forWrite.write(result)

            except (SystemError, UnicodeEncodeError):
                log_file_handler.write(str(datetime.datetime.now()) + " failed to collect text."+ "\n")
                continue
    log_file_handler.write(str(datetime.datetime.now()) + " formatting removed, text and titles collected in file - web_data.txt and titles.txt."+ "\n")
                
            
            
    forTitle.close()     
    forWrite.close()
    forRead.close()
    log_file_handler.write(str(datetime.datetime.now()) + " fetch_text function terminate."+ "\n")


    
# ---------------------------------------------------------------------------
# FUNCTION NAME : clean_fetched_data
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Cleans the fetched text file for newlines. 
#                 Writes all the results into a new file.
#                 Removes the previous file. 
# ---------------------------------------------------------------------------
def clean_fetched_data():
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " clean_fetch_text function reach."+ "\n")
    
    forRead = open("web_data.txt","r")
    newFile = open("WebData.txt", "w")

    # cleans the text file for newlines
    for eachLine in forRead:
        if eachLine.rstrip():
            newFile.write(eachLine)
    print("Fetched data modified.")
    log_file_handler.write(str(datetime.datetime.now()) + " fetched text in file - web_data.txt cleaned for newline."+ "\n")
    forRead.close()
    newFile.close()
    log_file_handler.write(str(datetime.datetime.now()) + " updated text in file - WebData.txt."+ "\n")

    #deletes 'web_data.txt' file
    if os.path.exists("web_data.txt"):
        os.remove("web_data.txt")
        log_file_handler.write(str(datetime.datetime.now()) + " web_data.txt - file removed."+ "\n")    
    else:
        print("File does not exists!!")
        log_file_handler.write(str(datetime.datetime.now()) + " error occured to remove file - web_data.txt ."+ "\n")

    log_file_handler.write(str(datetime.datetime.now()) + " clean_fetch_text function terminate."+ "\n")



# ---------------------------------------------------------------------------
# FUNCTION NAME : tokenize_text
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Splits text into sentences and writes sentences in each 
#                 line in the same file.
# ---------------------------------------------------------------------------        
def tokenize_text():
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " tokenize_text function reach."+ "\n")

    # read text from file 
    newFile = open("WebData.txt","r")
    readText = newFile.read()
    newFile.close()
    log_file_handler.write(str(datetime.datetime.now()) + " text read from file - WebData.txt."+ "\n")

    # tokenize each sentence in text file
    senTokens = nltk.sent_tokenize(readText)
    senTokens = [w.lower() for w in senTokens]
  
    newFile = open("WebData.txt","w")
    
    # stores in same file sentence-wise
    for stk in senTokens:
        stk = ' '.join(stk.split())
        newFile.write(stk)
        newFile.write("\n")
    newFile.close()
    log_file_handler.write(str(datetime.datetime.now()) + " sentence-wise, update in file - WebData.txt."+ "\n")

    log_file_handler.write(str(datetime.datetime.now()) + " tokenize_text function terminate."+ "\n")



    
# ---------------------------------------------------------------------------
# FUNCTION NAME : tokenize_words
# ---------------------------------------------------------------------------
# PARAMETERS	: tokens(empty list)
# ---------------------------------------------------------------------------
# RETURN	: tokens(list of lists)
# ---------------------------------------------------------------------------
# DESCRIPTION	: Splits and clean each sentence for stopwords and
#                 punctuation,appends words in a list and returns.
#                 Writes all the results into same file.
# --------------------------------------------------------------------------- 
def tokenize_words(tokens):
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " tokenize_words function reach."+ "\n")

    # reads text from file
    newFile = open("WebData.txt","r")
    text = newFile.readlines()
    newFile.close()
    log_file_handler.write(str(datetime.datetime.now()) + " text read from file - WebData.txt."+ "\n")

    for eachSent in text:
        wordTokens = nltk.word_tokenize(eachSent)
        
        # remove punctuation from each word
        table = str.maketrans('','',string.punctuation)
        stripped = [w.translate(table) for w in wordTokens]

        # remove remaining tokens that are not alphabetic/numeric
        checkWords = [word for word in stripped if word.isalnum()]

        # filter out stop words
        stopWords = set(stopwords.words('english'))
        textWords = [w for w in checkWords if not w in stopWords]
        
        tokens.append(textWords)
        
    # writes only tokens to the same file
    forWrite = open("WebData.txt","w")
    for eachList in tokens:
        sent = ' '.join(eachList)
        forWrite.write(sent)
        forWrite.write("\n")

    forWrite.close()
    log_file_handler.write(str(datetime.datetime.now()) + " text tokenize, updated in file - WebData.txt."+ "\n")
    
    print("Check the file WebData.txt for data!")
    log_file_handler.write(str(datetime.datetime.now()) + " tokenize_words function terminate."+ "\n")

    return tokens



# ---------------------------------------------------------------------------
# FUNCTION NAME : frequency_list
# ---------------------------------------------------------------------------
# PARAMETERS	: wordTokens(list of lists)
# ---------------------------------------------------------------------------
# RETURN	: wordList(list of frequent occuring words)
# ---------------------------------------------------------------------------
# DESCRIPTION	: Counts the frequent occuring words in titles and text.
#                 Appends in a list.
# ---------------------------------------------------------------------------
def frequency_list(wordTokens):
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " frequency_list function reach."+ "\n")
    
    countWord = []    
    wordFreq = []
    wordList = []

    # opens file containing titles
    forRead =  open("titles.txt","r" )
    text = forRead.read()
    forRead.close()
    log_file_handler.write(str(datetime.datetime.now()) + " titles read from file - titles.txt."+ "\n")

    # cleans data in the file
    words = text.split()
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in words]
    checkWords = [word.lower() for word in stripped if word.isalnum()]
    stopWords = set(stopwords.words('english'))
    textWords = [w for w in checkWords if not w in stopWords]

    # counts the most occurring words in title
    for eachWord in textWords:
        countNum = textWords.count(eachWord)
        if countNum > 1: 
            countWord.append(eachWord)
        else:
            continue
        
    # removes repeated words    
    listSet = set(countWord)
    wordFreq = list(listSet)
    log_file_handler.write(str(datetime.datetime.now()) + " frequent words in file - titles.txt fetched."+ "\n")

    # counts the most occurring words in tokens
    freqList = dict()
    # generates a dictionary of words with values
    for eachList in wordTokens:
        for theWord in eachList:
            for titleWord in textWords:
                if titleWord != theWord:
                    continue

                if titleWord == theWord:
                    if theWord in freqList:
                        freqList[theWord] += 1
                    else:
                        freqList[theWord] = 1
                        
    for keyWord in freqList:
        wordList.append(keyWord)
        
    wordFreq.extend(wordList)
    listSet = set(wordFreq)
    wordList = list(listSet)
  
    log_file_handler.write(str(datetime.datetime.now()) + " frequent words in file - WebData.txt fetched."+ "\n")

    log_file_handler.write(str(datetime.datetime.now()) + " frequency_list function terminate."+ "\n")

    return wordList



# ---------------------------------------------------------------------------
# FUNCTION NAME : concepts_classifier
# ---------------------------------------------------------------------------
# PARAMETERS	: wordTokens(list of lists),wordList(frequent occuring words)
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Converts each list into string.
#                 Matches frequent words in string.
#                 Based on Naive Bayes Classification, categorise into
#                 relevant concepts.
#                 Appends in a lists.
# ---------------------------------------------------------------------------
def concepts_classifier(wordTokens,wordList):
    global log_file_handler
    log_file_handler.write(str(datetime.datetime.now()) + " concepts_classifier function reach."+ "\n")

    # classify each sentence into concepts
    for eachList in wordTokens:

        # joins list to convert into string
        eachSent = ' '.join(eachList)
        for wf in wordList:

            # skips sentences if word from wordList is absent in sentence
                if re.search(wf,eachSent) == None or wf.isnumeric() == True:
                    continue
                else:
                    
                    # if match found, appends into relevant lists
                    case = cl.classify(eachSent)
                    if case == "technology":
                        forAppend = open("technology.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "business":
                        forAppend = open("business.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "gadget":
                        forAppend = open("gadget.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "famous":
                        forAppend = open("famous.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "study":
                        forAppend = open("study.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "sports":
                        forAppend = open("sports.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "occupation":
                        forAppend = open("occupation.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "vehicles":
                        forAppend = open("vehicles.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "politics":
                        forAppend = open("politics.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "foods":
                        forAppend = open("foods.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break
                    elif case == "country":
                        forAppend = open("country.txt","a")
                        forAppend.write(eachSent)
                        forAppend.write("\n")
                        forAppend.close()
                        break

    print("Check files in the directory!")                
    log_file_handler.write(str(datetime.datetime.now()) + " data classified into concepts."+ "\n")


    log_file_handler.write(str(datetime.datetime.now()) + " concepts_classifier fucntion terminate."+ "\n")


            
# ---------------------------------------------------------------------------
# FUNCTION NAME : main
# ---------------------------------------------------------------------------
# PARAMETERS	: NIL
# ---------------------------------------------------------------------------
# RETURN	: NIL
# ---------------------------------------------------------------------------
# DESCRIPTION	: Operates with the defined functions
# ---------------------------------------------------------------------------
def main():
    create_log()
    user_input()
    validate_urls()
    fetch_text()
    clean_fetched_data()
    tokenize_text()

    tokens = []
    wordTokens = tokenize_words(tokens)

    wordList = []
    wordList = frequency_list(wordTokens)
    concepts_classifier(wordTokens,wordList)

    close_log()
    
main()

