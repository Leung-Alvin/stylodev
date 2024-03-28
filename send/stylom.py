import nltk
import os

nltk.download("punkt")
import pandas as pd
import pickle
from random import shuffle
from math import floor
import shutil
import nltk


def get_text_by_author(author, directory):
    ret = []
    for file in os.listdir(directory):
        if author in file:
            ret.append(file)
    return ret


def get_string_from_filename(directory, author, filename):
    with open(directory + "/" + author + "_-_" + filename + ".txt", "r") as f:
        return f.read()


def read_files_into_string(directory, filenames):
    strings = []
    for filename in filenames:
        with open(directory + "/" + filename, "r", encoding="utf-8") as f:
            strings.append(f.read())
    return "\n".join(strings)


def merge_all_prints(author, directory):
    return read_files_into_string(directory, get_text_by_author(author, directory))


def get_all_files(directory):
    files = os.listdir(directory)
    if ".ipynb_checkpoints" in files:
        files.remove(".ipynb_checkpoints")
    return files


def get_all_authors(directory):
    ret = []
    files = os.listdir(directory)
    if ".ipynb_checkpoints" in files:
        files.remove(".ipynb_checkpoints")
    for file in files:
        author = file.split("_-_")[0]
        if author not in ret:
            ret.append(author)
    return ret


def merge(dict1, dict2):
    res = dict1 or dict2
    return res


def get_prints(authors, directory):
    prints = {}
    for author in authors:
        prints[author] = merge_all_prints(author, directory)
    return prints

#This prediction algorithm was sourced from https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python
#All other functions were written by us.
def predict(db, string, authors, N):
    author_tokens = {}
    for author in authors:
        tokens = nltk.word_tokenize(db[author])
        # Filter out punctuation
        author_tokens[author] = [
            token for token in tokens if any(c.isalpha() for c in token)
        ]
    # for author in authors:
    #     author_tokens[author] = ([tok.lower() for tok in author_tokens[author]])

    corpus = []
    for author in authors:
        corpus += author_tokens[author]

    corpus_freq_dist = list(nltk.FreqDist(corpus).most_common(N))
    # corpus_freq_dist[:10]

    features = [word for word, freq in corpus_freq_dist]
    feature_freqs = {}

    for author in authors:
        # A dictionary for each candidate's features
        feature_freqs[author] = {}

        # A helper value containing the number of tokens in the author's subcorpus
        overall = len(db[author])

        # Calculate each feature's presence in the subcorpus
        for feature in features:
            presence = author_tokens[author].count(feature)
            feature_freqs[author][feature] = presence / overall
    import math

    # The data structure into which we will be storing the "corpus standard" statistics
    corpus_features = {}

    # For each feature...
    for feature in features:
        # Create a sub-dictionary that will contain the feature's mean
        # and standard deviation
        corpus_features[feature] = {}

        # Calculate the mean of the frequencies expressed in the subcorpora
        feature_average = 0
        for author in authors:
            feature_average += feature_freqs[author][feature]
        feature_average /= len(authors)
        corpus_features[feature]["Mean"] = feature_average

        # Calculate the standard deviation using the basic formula for a sample
        feature_stdev = 0
        for author in authors:
            diff = feature_freqs[author][feature] - corpus_features[feature]["Mean"]
            feature_stdev += diff * diff
        feature_stdev /= len(authors) - 1
        feature_stdev = math.sqrt(feature_stdev)
        corpus_features[feature]["StdDev"] = feature_stdev
    feature_zscores = {}
    for author in authors:
        feature_zscores[author] = {}
        for feature in features:
            feature_val = feature_freqs[author][feature]
            feature_mean = corpus_features[feature]["Mean"]
            feature_stdev = corpus_features[feature]["StdDev"]
            feature_zscores[author][feature] = (
                feature_val - feature_mean
            ) / feature_stdev
    # db['TestCase'] = string
    # Tokenize the test case
    testcase_tokens = nltk.word_tokenize(string)

    # Filter out punctuation and lowercase the tokens

    # testcase_tokens = [token.lower() for token in testcase_tokens
    #                    if any(c.isalpha() for c in token)]

    testcase_tokens = [
        token for token in testcase_tokens if any(c.isalpha() for c in token)
    ]

    # Calculate the test case's features
    overall = len(testcase_tokens)
    testcase_freqs = {}
    for feature in features:
        presence = testcase_tokens.count(feature)
        testcase_freqs[feature] = presence / overall

    # Calculate the test case's feature z-scores
    testcase_zscores = {}
    for feature in features:
        feature_val = testcase_freqs[feature]
        feature_mean = corpus_features[feature]["Mean"]
        feature_stdev = corpus_features[feature]["StdDev"]
        testcase_zscores[feature] = (feature_val - feature_mean) / feature_stdev
    min_author = ""
    min_delta = 100000
    predictions = {}
    for author in authors:
        delta = 0
        for feature in features:
            delta += math.fabs(
                (testcase_zscores[feature] - feature_zscores[author][feature])
            )
        delta /= len(features)
        predictions[author] = delta
        if delta < min_delta:
            min_delta = delta
            min_author = author
        # print(author,delta)
    predictions = {
        k: v for k, v in sorted(predictions.items(), key=lambda item: item[1])
    }
    return min_author, predictions, features


def measure(db, di, authors, N):
    ret = pd.DataFrame(
        columns=[
            "actual_author",
            "work",
            "prediction_1",
            "delta_1",
            "prediction_2",
            "delta_2",
            "prediction_3",
            "delta_3",
            "correct",
            "in_top_3",
        ]
    )
    test_files = get_all_files(di)
    for file in test_files:
        parts = file.split("_-_")
        author = parts[0]
        name = parts[1].replace(".txt", "")
        min_author, predictions, features = predict(
            db, get_string_from_filename(di, author, name), authors, N
        )
        predictions = {
            k: v for k, v in sorted(predictions.items(), key=lambda item: item[1])
        }
        predictions_list = list(predictions.keys())
        # print(predictions)
        ret.loc[len(ret.index)] = [
            author,
            name,
            predictions_list[0],
            predictions[predictions_list[0]],
            predictions_list[1],
            predictions[predictions_list[1]],
            predictions_list[2],
            predictions[predictions_list[2]],
            predictions_list[0] == author,
            author in predictions_list[:3],
        ]
    return ret



def evaluate(df):
    num_rows = df.shape[0]
    value_counts = df["correct"].value_counts()
    corr_true_count = value_counts.get(True, 0)
    value_counts = df["in_top_3"].value_counts()
    in_top_3_true_count = value_counts.get(True, 0)
    print(corr_true_count / num_rows)
    print(in_top_3_true_count / num_rows)


def save_db(prints, db_name):
    with open(db_name + ".pkl", "wb") as f:
        pickle.dump(prints, f)


def read_db(db_name):
    with open(db_name + ".pkl", "rb") as f:
        loaded_dict = pickle.load(f)
        return loaded_dict


def update_db(db_name, directory):
    authors = get_all_authors(directory)
    prints = get_prints(authors, directory)
    save_db(prints, db_name)


def train_test_split(files, training_perc):
    shuffle(files)
    split_index = floor(len(files) * training_perc)
    training = files[:split_index]
    testing = files[split_index:]
    return training, testing


def copy_files(source_directory, destination_directory, filenames):
    for filename in filenames:
        source_path = os.path.join(source_directory, filename)
        destination_path = os.path.join(destination_directory, filename)
        try:
            shutil.copy2(source_path, destination_path)
        except FileNotFoundError:
            print(f"File '{filename}' not found in the source directory.")
        except PermissionError:
            print(f"Permission error while copying '{filename}'.")
        except Exception as e:
            print(f"An error occurred while copying '{filename}': {e}")


def create_train_test_dirs():
    try:
        os.mkdir("tr")
        os.mkdir("te")
    except FileExistsError:
        print("Directories are already created!")


def delete_train_test_dirs():
    shutil.rmtree("tr", ignore_errors=True, onerror=None)
    shutil.rmtree("te", ignore_errors=True, onerror=None)


def generate_corpus_dict(utterances):
    spkrs = {}
    for utt in utterances:
        spkr = utt.speaker.id
        if (
            utt.text == "[deleted]"
            or utt.text == "[removed]"
            or utt.text == ""
            or utt.speaker.id == "[deleted]"
        ):
            continue
        if spkr not in list(spkrs.keys()):
            spkrs[spkr] = ""
        spkrs[spkr] += "\n" + utt.text
    return spkrs


def predict_formatted(prints, text, authors, N):
    min_auth, sorted_dict, features = predict(prints, text, authors, N)
    preds = list(sorted_dict.keys())
    deltas = list(sorted_dict.values())
    num_features = len(features)
    percentages = [x / num_features * 100 for x in deltas]
    string = (
        "My top three guesses are:\n"
        + "Candidates: "
        + str(preds[:3])
        + "\n"
        + "Deltas: "
        + str(deltas[:3])
        + "\n"
    )
    return string


def predict_on_test_text(prints, authors, N):
    file = "tester_-_test.txt"
    string = ""
    with open(file, "r") as f:
        string = f.read()
        print("Input:\n\n" + string + "\n")
    return predict_formatted(prints, string, authors, N)


def observe_N(prints, test_dir, authors, N):
    x = []
    y = []
    while N <= 100:
        # print(str(N/(200)*100)+"%")
        x.append(N)
        y.append(evaluate(measure(prints, test_dir, authors, N)))
        N += 2
    max_y_index = y.index(max(y))
    x_value_for_max_y = x[max_y_index]
    return x_value_for_max_y, max(y)


def percent_top_three_correct(df):
    num_rows = df.shape[0]
    count = 0
    for index, row in df.iterrows():
        true_ans = row["actual_author"]
        pred_1 = row["prediction_1"]
        pred_2 = row["prediction_2"]
        pred_3 = row["prediction_3"]
        predictions = [pred_1, pred_2, pred_3]
        if true_ans in predictions:
            count += 1
    return count / num_rows


def observe_N_top_3(prints, test_dir, authors, N):
    x = []
    y = []
    while N <= 100:
        # print(str(N/(200)*100)+"%")
        x.append(N)
        y.append(percent_top_three_correct(measure(prints, test_dir, authors, N)))
        N += 2
    max_y_index = y.index(max(y))
    x_value_for_max_y = x[max_y_index]
    return x_value_for_max_y, max(y)
