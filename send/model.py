import stylom as st
import length as ln

def predict(string, N, src):
    st.delete_train_test_dirs()
    dir_authors = st.get_all_authors(src)
    dir_prints = st.get_prints(dir_authors, src)
    
    bag_of_words = st.predict(dir_prints, string, dir_authors, N)[1]
    punc_ratio, avg_word_len, avg_sen_len, capital_ratio = ln.predict(dir_prints, string, dir_authors)
    tests = [bag_of_words, punc_ratio, avg_word_len, avg_sen_len, capital_ratio]
    placements = [get_names(test) for test in tests]
    scores = score(placements, dir_authors)
    return bag_of_words, punc_ratio, avg_word_len, avg_sen_len, capital_ratio, sorted(scores.items(), key=lambda x: x[1], reverse=True)

def get_names(dictionary):
    return list(dictionary.keys())

def score(placements, authors):
    scores = {}
    for author in authors:
        scores[author] = 0
    for placement in placements:
        for i in range(len(placement)):
            scores[placement[i]] += len(placement) - i
    return scores
