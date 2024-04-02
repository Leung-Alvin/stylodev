import model
import os

def test_on_text(text):
    bag_of_words, punc_ratio, avg_word_len, avg_sen_len, cap_rat, scores = model.predict(text, 30, os.path.join(os.getcwd(), "send\\survey"))
    print("Scores: ", scores)
def test_on_file(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
    bag_of_words, punc_ratio, avg_word_len, avg_sen_len, cap_rat, scores = model.predict(text, 30, os.path.join(os.getcwd(), "send\\survey"))
    # print("Bag of Words: ", bag_of_words)
    # print("Punctuation Ratio: ", punc_ratio)
    # print("Average Word Length: ", avg_word_len)
    # print("Average Sentence Length: ", avg_sen_len)
    # print("Capital Ratio: ", cap_rat)
    print("Scores: ", scores)



if __name__ == "__main__":
    text = ""
    # test_on_text(text)
    
    test_on_file(os.getcwd() + "\\send\\test.txt")