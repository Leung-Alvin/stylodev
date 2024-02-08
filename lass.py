def break_file_into_paragraphs(file_path):
    with open(file_path, 'r', encoding = "utf8") as file:
        text = file.read()
    paragraphs = text.split('\n\n')
    paragraphs = [substring for substring in paragraphs if substring.strip()]
    return paragraphs

def get_file_author(file_path):
    return file_path.split("/")[-1].split("_-_")[0]

