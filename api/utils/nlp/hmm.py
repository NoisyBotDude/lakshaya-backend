import requests
import json
import re
import random
from pywsd.similarity import max_similarity
from pywsd.lesk import adapted_lesk
from pywsd.lesk import simple_lesk
from pywsd.lesk import cosine_lesk
from nltk.corpus import wordnet as wn

import pprint
import itertools
import re
import pke
import string
from nltk.corpus import stopwords
    
import re
import random

def make_filtered_keys(keywords,summarized_text):
    filtered_keys=[]
    for keyword in keywords:
        if keyword.lower() in summarized_text.lower():
            filtered_keys.append(keyword)
    return filtered_keys

def generate_question_options(key_distractor_list, keyword_sentence_mapping):
    index = 1
    question_options = []
    for each in key_distractor_list:
        sentence = keyword_sentence_mapping[each][0]
        pattern = re.compile(each, re.IGNORECASE)
        output = pattern.sub(" _ ", sentence)
        question_options.append(f"{index}) {output}")
        choices = [each.capitalize()] + key_distractor_list[each]
        top4choices = choices[:4]
        random.shuffle(top4choices)
        optionchoices = ['a', 'b', 'c', 'd']
        for idx, choice in enumerate(top4choices):
            question_options.append(f"\t{optionchoices[idx]}) {choice}")
        question_options.append(f"\nMore options: {choices[4:20]}\n\n")
        index = index + 1
    return question_options

# full_text='''The Nile River fed Egyptian civilization for hundreds of years. It begins near the equator in Africa and flows north to the Mediterranean Sea. A delta is an area near a river’s mouth where the water deposits fine soil called silt.......................'''


# summarized_text='''The Nile River fed Egyptian civilization for hundreds of years. It begins near the equator in Africa and flows north to the Mediterranean Sea.'''



def get_nouns_multipartite(text):
    out=[]
    extractor = pke.unsupervised.MultipartiteRank()
    extractor.load_document(input=text)
    #    not contain punctuation marks or stopwords as candidates.
    pos = {'PROPN'}


    #pos = {'VERB', 'ADJ', 'NOUN'}
    stoplist = list(string.punctuation)
    stoplist += ['-lrb-', '-rrb-', '-lcb-', '-rcb-', '-lsb-', '-rsb-']
    stoplist += stopwords.words('english')
    extractor.candidate_selection(pos=pos)#, stoplist=stoplist)
    # 4. build the Multipartite graph and rank candidates using random walk,
    #    alpha controls the weight adjustment mechanism, see TopicRank for
    #    threshold/method parameters.
    extractor.candidate_weighting(alpha=1.1,
                                  threshold=0.75,
                                  method='average')
    keyphrases = extractor.get_n_best(n=20)
    for key in keyphrases:
        out.append(key[0])
    return out







from nltk.tokenize import sent_tokenize
from flashtext import KeywordProcessor
def tokenize_sentences(text):
    sentences = [sent_tokenize(text)]
    sentences = [y for x in sentences for y in x]
    # Remove any short sentences less than 20 letters.
    sentences = [sentence.strip() for sentence in sentences if len(sentence) > 20]
    return sentences
def get_sentences_for_keyword(keywords, sentences):
    keyword_processor = KeywordProcessor()
    keyword_sentences = {}
    for word in keywords:
        keyword_sentences[word] = []
        keyword_processor.add_keyword(word)
    for sentence in sentences:
        keywords_found = keyword_processor.extract_keywords(sentence)
        for key in keywords_found:
            keyword_sentences[key].append(sentence)
    for key in keyword_sentences.keys():
        values = keyword_sentences[key]
        values = sorted(values, key=len, reverse=True)
        keyword_sentences[key] = values
    return keyword_sentences



# summarized_text="""The Nile River fed Egyptian civilization for hundreds of years. It begins near the equator in Africa and flows north to the Mediterranean Sea."""
# sentences = tokenize_sentences(summarized_text)
# keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)
        
# print (keyword_sentence_mapping)

# from api.utils.nlp.sentence_mapping import get_nouns_multipartite, get_sentences_for_keyword,tokenize_sentences
#1. getting keyword using multipartite rank

#2. making filtered keys on keywords
# 3. getting distractors using wordnet
# 4. getting distractors using conceptnet
#5.
#  



# keywords = get_nouns_multipartite(full_text) 
# print (keywords)
# filtered_keys=[]
# for keyword in keywords:
#     if keyword.lower() in summarized_text.lower():
#         filtered_keys.append(keyword)
        
# print (filtered_keys)

# Distractors from Wordnet
def get_distractors_wordnet(syn,word):
    distractors=[]
    word= word.lower()
    orig_word = word
    if len(word.split())>0:
        word = word.replace(" ","_")
    hypernym = syn.hypernyms()
    if len(hypernym) == 0: 
        return distractors
    for item in hypernym[0].hyponyms():
        name = item.lemmas()[0].name()
        #print ("name ",name, " word",orig_word)
        if name == orig_word:
            continue
        name = name.replace("_"," ")
        name = " ".join(w.capitalize() for w in name.split())
        if name is not None and name not in distractors:
            distractors.append(name)
    return distractors

def get_wordsense(sent,word):
    word= word.lower()
    
    if len(word.split())>0:
        word = word.replace(" ","_")
    
    
    synsets = wn.synsets(word,'n')
    if synsets:
        wup = max_similarity(sent, word, 'wup', pos='n')
        adapted_lesk_output =  adapted_lesk(sent, word, pos='n')
        lowest_index = min (synsets.index(wup),synsets.index(adapted_lesk_output))
        return synsets[lowest_index]
    else:
        return None

# Distractors from http://conceptnet.io/
def get_distractors_conceptnet(word):
    word = word.lower()
    original_word= word
    if (len(word.split())>0):
        word = word.replace(" ","_")
    distractor_list = [] 
    url = "http://api.conceptnet.io/query?node=/c/en/%s/n&rel=/r/PartOf&start=/c/en/%s&limit=5"%(word,word)
    obj = requests.get(url).json()

    for edge in obj['edges']:
        link = edge['end']['term'] 

        url2 = "http://api.conceptnet.io/query?node=%s&rel=/r/PartOf&end=%s&limit=10"%(link,link)
        obj2 = requests.get(url2).json()
        for edge in obj2['edges']:
            word2 = edge['start']['label']
            if word2 not in distractor_list and original_word.lower() not in word2.lower():
                distractor_list.append(word2)
                   
    return distractor_list

key_distractor_list = {}
# from sentence_mapping import get_nouns_multipartite,full_text,summarized_text
# keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)

# # summarized_text="""The Nile River fed Egyptian civilization for hundreds of years. It begins near the equator in Africa and flows north to the Mediterranean Sea."""
# sentences = tokenize_sentences(summarized_text)
# keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)
    

def apply_wordsense_conceptnet_v1(keyword_sentence_mapping):
    for keyword in keyword_sentence_mapping:
        wordsense = get_wordsense(keyword_sentence_mapping[keyword][0],keyword)
        if wordsense:
            distractors = get_distractors_wordnet(wordsense,keyword)
        if len(distractors) ==0:
            distractors = get_distractors_conceptnet(keyword)
        if len(distractors) != 0:
            key_distractor_list[keyword] = distractors
    else:
        
        distractors = get_distractors_conceptnet(keyword)
        if len(distractors) != 0:
            key_distractor_list[keyword] = distractors
    return key_distractor_list


from making_mcq import apply_wordsense_conceptnet_v1
import uvicorn
import random
import re

from fastapi import FastAPI

app = FastAPI()

@app.post("/kuch_to_karta_hai")
async def process_text(text: str):
    result = model(text, min_length=60, max_length = 500 , ratio = 0.4)
    summarized_text = ''.join(result)
    keywords = get_nouns_multipartite(text)
    filtered_keys=make_filtered_keys(keywords)
    sentences = tokenize_sentences(summarized_text)
    keyword_sentence_mapping = get_sentences_for_keyword(filtered_keys, sentences)
    key_distractor_list= apply_wordsense_conceptnet_v1(keyword_sentence_mapping)
    # Create a dictionary to store the question and its options
    question_dict = {}
    answer=generate_question_options(key_distractor_list,keyword_sentence_mapping,question_dict)
    
    return {"processed_QA": summarized_text}

if __name__=="__main__":
    uvicorn.run(app,port = 8040)