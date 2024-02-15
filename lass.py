import lassdb
import config
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('vader_lexicon')
except LookupError:
    nltk.download('vader_lexicon')

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('wordnet')
except LookupError:
    nltk.download('wordnet')

# nltk.download('punkt')
# nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string


DIRECTORY = 'prints/survey'
FIELDS_FILE = 'table_fields.txt'

def break_file_into_paragraphs(file_path):
    with open(file_path, 'r', encoding = "utf8") as file:
        text = file.read()
    paragraphs = text.split('\n\n')
    paragraphs = [substring for substring in paragraphs if substring.strip()]
    return paragraphs

def get_file_author(file_path):
    return file_path.split("/")[-1].split("_-_")[0]

def clean(paragraph):
    stop = set(stopwords.words('english'))
    exclude = set(string.punctuation)
    lemma = WordNetLemmatizer()
    stop_free = " ".join([i for i in paragraph.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

def analyze_sentiment(paragraph):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(paragraph)
    # for key in sorted(scores):
        # print('{0}: {1}, '.format(key, scores[key]), end='')
    # print()
    if scores['compound'] > 0.05:
        return "positive"
    elif scores['compound'] < -0.05:
        return "negative"
    else:
        return "neutral"

if __name__ == '__main__':
    configurations = config.load_config()
    conn = lassdb.connect(configurations)
    cursor = conn.cursor()
    table_name = 'prints'
    lassdb.drop_table(conn, table_name)
    lassdb.initialize_sample_table(conn, table_name, FIELDS_FILE, DIRECTORY)
    works = lassdb.select_all_in_table(conn, table_name)
    print(works[3])
    # lassdb.drop_table(conn, table_name)
    # sample = works[0][2]
    # print(sample)
    # print(analyze_sentiment(sample))