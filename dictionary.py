#!/usr/local/bin/python3
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import time
import pandas as pd 
import numpy as np
from termcolor import colored

# from io import StringIO
# import sys
# old_stdout = sys.stdout
# In[77]:


def get_url(url):
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        return None
    else:
        return r.text
    
def get_slowo_dnia():
    url_clean='https://sjp.pwn.pl/'
    bs = BeautifulSoup(get_url(url_clean),features="html.parser")
    out = bs.findAll("div", {"class": "sjp-slowo-dnia"})
    slowo_dnia = out[0].a.text
    slowo_dnia_href = out[0].a['href']
    return slowo_dnia, slowo_dnia_href

def get_znaczenia_slowa(slowo_href):
    bs = BeautifulSoup(get_url(slowo_href),features="html.parser")
    
    out = []

    output = bs.findAll("div", {"class": "znacz"})
    for item in output:
        print(item.text)
        out+=item.text
    output2 = bs.findAll("div", {"class": "ribbon-element type-187126"})
    for item in output2:
        print(item.text)
        out+=item.text

    return ''.join(out)

def get_random_spanish_word():
    df = pd.read_csv('./1k_spanish_words.txt',sep='\t',index_col='Number')
    x = df.sample(1)
    sp = x.loc[x.first_valid_index()].Spanish
    en = x.loc[x.first_valid_index()]['in English']
    #print('Słowo dnia: ',colored(sp,'magenta'),'-',en)
    return sp, en

def get_slowo_dnia_eng():
    url_clean='https://www.dictionary.com/e/word-of-the-day/'
    bs = BeautifulSoup(get_url(url_clean), features="html.parser")
    out = bs.findAll("div", {"class": "otd-item-headword__word"})
    out2 = bs.findAll("div", {"class": "otd-item-headword__pronunciation"})
    out3 = bs.findAll("div", {"class": "otd-item-headword__pos"})

    word = out[0].text.strip()
    pronon = out2[0].text.strip()
    partofspeech = out3[0].text.strip().split('\n\n')[0].split(' ')[0]
    definition = out3[0].text.strip().split('\n\n')[1].split('.')[0]

    return word, pronon, partofspeech, definition 

# In[75]:
# result = StringIO()
# sys.stdout = result
# result_string = result.getvalue()

def main():
    print('--------------------------------------------------------------------------------')

    print('-----------')
    print('|', colored('ESPAÑOL','yellow'),'|')
    print('-----------')

    get_random_spanish_word()

    print('----------')
    print('|', colored('POLSKI','red'),'|')
    print('----------')

    slowo_dnia, slowo_dnia_href  = get_slowo_dnia()

    print('Słowo dnia: ', colored(slowo_dnia,'magenta'))

    get_znaczenia_slowa(slowo_dnia_href)

    print('-----------')
    print('|', colored('ENGLISH','cyan'),'|')
    print('-----------')

    word, pronon, partofspeech, definition  = get_slowo_dnia_eng()

    print('Słowo dnia: ', colored(word,'magenta'), pronon , '\n')
    print("%s, «%s»"%(partofspeech,definition))

    print('--------------------------------------------------------------------------------')

# def get_output_string():
#     print(result_string)
#     return result_string

# sys.stdout = old_stdout




