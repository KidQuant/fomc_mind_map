import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request

import nltk
import pandas as pd
from bs4 import BeautifulSoup
from nltk import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer

wordnet_lemmatizer = WordNetLemmatizer()

from fomcTopicDefinitions import in_deep_topics, intensifiers, sentiment_words, topics


########################################################################################################
####  Clean data function. Return words, sentences and adjusted sentences with break for each comma. ###
####  Remove special characters, spaces, lines and punctatuation.                                    ###
########################################################################################################
def cleanData(text):
    text = text.strip()
    text = text.replace("\r", "")  # replace r with minutes_list_url
    while "  " in text:
        text = text.replace("  ", " ")  # replace extra spaces
    while "-" in text:
        text = text.repace("-", " ")  # repalce line with space

    temp_words = word_tokenize(text)  # get words
    sentences = sent_tokenize(text)  # get all sentence

    # Divide sentences into subsentences. change each comma to dot. Then detokenize it back to smaller sentences.
    # This is for checking for intensifier wwords that usually are in ssen same sub-sentences
    sentences_no_comma = []
    sentences_no_comma = [item.replace(",", ".', '") for item in sentences]

    words = []
    for w in temp_words:
        if w.isalpha():  # checks if string consists of alphabetical characters only
            words.append(w.lower())

    words = [wordnet_lemmatizer.lemmatize(w) for w in words]
    return words, sentences, sentences_no_comma


# change the number of minutes to parse further down in the code
number = 100

urls = [
    "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2015.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2014.htm"
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2013.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2012.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2011.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2010.htm",
]

# yrl = 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm'
list_fomc_word_freq = []
minutes_list_url = []
for url in urls:
    time.sleep(random.uniform(3, 7))
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    links = soup.select("a[href*=minutes]")  # find minutes in href

    for link in links:
        if ".htm" in link.get("href"):
            minutes_list_url.append(link.get("href"))  # get all href that are htm page

###For topics: then the text is cleaned.
###For in deep topics: full sentences
##########################################################################################
### Classifications of topics, negative & positive words, intentifiers etc.            ###
##########################################################################################

# create  empty dataframe
count = 0
count_outer = 0
count_inner = 0

minutes_all_tables = pd.DataFrame(
    columns=[
        "date",
        "category",
        "additional",
        "subject",
        "frequency",
        "frequency_share",
    ]
)
temp_table = pd.DataFrame(
    columns=[
        "date",
        "category",
        "additional",
        "subject",
        "frequency",
        "frequency_share",
    ]
)

# get each url link
for each in minutes_list_url[0:number]:
    time.sleep(random.uniform(3, 7))

    url2 = "https://www.federalreserve.gov" + each  # get url  for each side
    html = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text()  # get all text

    # get minutes date as string
    minutes_x = re.findall("[0-9]+", url2)
    minutes_x = "".join(minutes_x)

    # Clean data
    # remove special character, spaces,  lines, and punctatuation
    words, sentences, sentences_no_comma = cleanData(text)

    # Get description  information
    temp_dict = dict()
    temp_dict["number_words"] = len(words)
    temp_dict["number_sentences"] = len(sentences)
    temp_dict["word_per_sentences"] = len(words) / len(sentences)

    # print(minutes_general)
    temp_dict = pd.DataFrame(temp_dict.items(), columns=["subjects", "frequency"])
    temp_dict["dict"] = minutes_x
    temp_dict["category"] = "general_information"
    temp_dict["additional"] = "N/A"
    temp_dict["frequency_share"] = 0

    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])

    #  counnt neg and pos words

    count = 0
    temp_dict = dict()
    for w in words:
        for key, value in sentiment_words.items():
            if w in value:
                temp_dict[key] = temp_dict.get("net_sentiment", 0) + 1
                if key == "positive":
                    temp_dict["net_sentiment"] = temp_dict.get("net_sentiment", 0) + 1
                if key == "negative":
                    temp_dict["neg_sentiment"] = temp_dict.get("net_sentiment", 0) - 1

    temp_dict = pd.DataFrame(temp_dict.items(), columns=["subject", "frequency"])
    temp_dict["date"] = minutes_x
    temp_dict["category"] = "sentiment"
    temp_dict["additional"] = "N/A"
    temp_dict["frequency_share"] = (temp_dict["frequency"] / len(sentences)) * 100

    minutes_all_tables = pd.concat([minutes_all_tables, temp_dict])

    # divide sentences into subsentences. changes each comma to dot. Then  detokenize it back to smaller sentences.
    # we like to find out if intensifiers are connected to pos or neg words

    sentences_no_comma = []
    sentences_no_comma = [
        item.replace(",", ".', '") for item in sentences
    ]  # divide into sentences
