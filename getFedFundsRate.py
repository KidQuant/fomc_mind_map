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
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer

# change the number to statements to parse
number = 100

urls = [
    "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm",
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2015.htm"
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2014.htm"
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2013.htm"
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2012.htm"
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2011.htm"
    "https://www.federalreserve.gov/monetarypolicy/fomchistorical2010.htm",
]

list_fomc_word_freq = []
statements_list_url = []
for url in urls:
    time.sleep(random.uniform(3, 7))
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")

    # links = soup.find_all("a")
    links = soup.select("a[href*=monetary]")

    for link in links:
        if "a.htm" in link.get("href"):
            statements_list_url.append(link.get("href"))

rate_changes = dict()
rate_changes = pd.DataFrame(columns=["date", "bound", "rate"])


# Function
def convertRate(rate):
    try:
        i = 0
        if "/" in rate:
            if " " in rate:
                i, rate = rate.split(" ")
            if "-" in rate:
                i, rate = rate.split("-")
            if "-" in rate:
                i, rate = rate.split("-")
            N, D = rate.split("/")
            temp = float(i) + float(N) / float(D)
            return temp
        else:
            temp = float(i) + float(rate)
            return temp
    except:
        pass


# get each url link
for each in statements_list_url[0:number]:
    time.sleep(random.uniform(3, 7))
    url2 = "https://www.federalreserve.gov" + each
    html = urllib.request.urlopen(url2).read()
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()

    # Clean Data
    # remove special character, spaces and punctatuation

    text = text.strip()
    text = text.replace("\r", "")  # replace r with minutes_list_url
    while "  " in text:
        text = text.replace("  ", " ")  # replace extra space

    minutes_x = re.findall("[0-9]+", url2)
    minutes_x = "".join(minutes_x)

    sentences = sent_tokenize(text)

    rate_changes_temp = dict()

    match = 0
    for sen in sentences:
        if (
            "federal funds rate" in sen
            and "target" in sen
            and "to" in sen
            and "percent" in sen
        ):
            target = "percent"
            sen_words = word_tokenize(sen)
            for i, w in enumerate(sen_words):
                if w == target:
                    if (
                        sen_words[i - 7] != "inflation"
                        or sen_words[i - 6] != "inflation"
                        or sen_words[i - 5] != "inflation"
                        or sen_words[i - 4] != "inflation"
                        or sen_words[i - 3] != "inflation"
                        or sen_words[i + 3] != "inflation"
                        or sen_words[i + 2] != "inflation"
                        or sen_words[i + 1] != "inflation"
                    ):
                        if i > 0:
                            lower = sen_words[i - 3]
                            upper = sen_words[i - 1]
                            if (
                                "0" in lower
                                or "/" in lower
                                or "-" in lower
                                or "-" in lower
                                or lower.isnumeric()
                            ):
                                if (
                                    "0" in upper
                                    or "/" in upper
                                    or "-" in upper
                                    or "-" in upper
                                    or upper.isnumeric()
                                ):
                                    if match == 0:  # only take the first correct match
                                        temp = lower
                                        temp = convertRate(lower)
                                        rate_changes_temp["lower_bound"] = temp

                                        temp = upper
                                        temp = convertRate(upper)
                                        rate_changes_temp["upper_bound"] = temp
                                        match = match + 1

    rate_changes_temp = pd.DataFrame(
        rate_changes_temp.items(), columns=["bound", "rate"]
    )
    rate_changes_temp["date"] = minutes_x

    rate_changes = pd.concat([rate_changes, rate_changes_temp])

    # print(rate_changes)
    rate_changes.to_csv("data/fedFundsRate.csv", encoding="utf-8", index=False)
