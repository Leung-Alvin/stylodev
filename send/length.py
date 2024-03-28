from string import punctuation
from collections import Counter
import re
from nltk.tokenize import sent_tokenize

def predict(prints, string, authors):
    # print(combine(prints['aleung']))
    
    keys = prints.keys()
    
    ret_ratio = {}
    ret_word_len = {}
    ret_sen_len = {}
    ret_capital_ratio = {}
    
    for key in keys:
        author = key
        punc_ratio = get_punctuation_ratio(prints[key])
        avg_word_len = get_average_word_length(prints[key])
        avg_sen_len = get_average_sentence_length(prints[key])
        cap_rat = capital_ratio(prints[key])
        
        string_punc_ratio = get_punctuation_ratio(string)
        string_avg_word_len = get_average_word_length(string)
        string_avg_sen_len = get_average_sentence_length(string)
        string_capital_ratio = capital_ratio(string)
        
        diff_punc_ratio = abs(punc_ratio - string_punc_ratio)
        diff_avg_word_len = abs(avg_word_len - string_avg_word_len)
        diff_avg_sen_len = abs(avg_sen_len - string_avg_sen_len)
        diff_capital_ratio = abs(cap_rat - string_capital_ratio)
        
        ret_ratio[author] = diff_punc_ratio
        ret_word_len[author] = diff_avg_word_len
        ret_sen_len[author] = diff_avg_sen_len
        ret_capital_ratio[author] = diff_capital_ratio
        
        ret_ratio = dict(sorted(ret_ratio.items(), key=lambda item: item[1]))
        ret_word_len = dict(sorted(ret_word_len.items(), key=lambda item: item[1]))
        ret_sen_len = dict(sorted(ret_sen_len.items(), key=lambda item: item[1]))
        ret_capital_ratio = dict(sorted(ret_capital_ratio.items(), key=lambda item: item[1]))
        
    
    return ret_ratio, ret_word_len, ret_sen_len, ret_capital_ratio
        
        
        
    

def get_punctuation(string):
    counts = Counter(string)
    return {k:v for k, v in counts.items() if k in punctuation}

def count_punctuation(string):
    return sum(list(get_punctuation(string).values()))

def combine(string):
    return string.replace('\t','').replace('\n','')

def break_apart(string):
    ret = re.split(',|\.|;|:|!|\?| ', string)
    return list(filter(None, ret))

def get_punctuation_ratio(string):
    return count_punctuation(string)/count_words(string)

def count_words(string):
    return len(string)

def capital_ratio(string):
    return sum([1 for c in string if c.isupper()])/len(string)

def get_average_word_length(string):
    ret = break_apart(string)
    return sum([len(word) for word in ret])/len(ret)

def get_average_sentence_length(string):
    sentences = sent_tokenize(string)
    counts = []
    for sentence in sentences:
        counts.append(len(break_apart(sentence)))
    return sum(counts)/len(counts)

