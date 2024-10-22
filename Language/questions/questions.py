import nltk; nltk.download('stopwords')
import sys
import os
import string
import re
import math
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), 'r') as file:
            data[filename] = file.read()

    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    document = document.lower()

    regex = re.compile(f'[{string.punctuation}]', re.MULTILINE)
    document = regex.sub('', document)

    document = nltk.word_tokenize(document)

    stopwords = set(nltk.corpus.stopwords.words("english"))
    document = [word for word in document if word not in stopwords]

    return sorted(document)


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf = {}
    seen = set()
    docsets = {k: set(v) for k,v in documents.items()}
    for file, doc in documents.items():
        for word in doc:
            if word in seen:
                continue
            df = [1 if word in otherdoc else 0 for otherdoc in docsets.values()]
            df = sum(df)
            idf[word] = math.log(len(documents) / df)
            seen.add(word)

    return idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    word_count = {k: Counter(v) for k,v in files.items()}
    ranked = {fname: 0 for fname in word_count.keys()}
    for fname, count in word_count.items():
        for word in query:
            ranked[fname] += count.get(word, 0) * idfs.get(word, 0)

    ranked = dict(sorted(ranked.items(), key=lambda x: x[1], reverse=True))
    ranked = list(ranked.keys())[:n]

    return ranked


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    def qtd(sentence, query):
        """
        calculates the query term density.
        That is, proportion of terms in sentence that are also in query.
        """
        query = set(query)
        count = sum([1 if word in query else 0 for word in sentence.split()])
        return count / len(sentence.split())

    ranked = {}
    for sentence, wordlist in sentences.items():
        ranked[sentence] = 0
        for word in query:
            if word in wordlist:
                ranked[sentence] += idfs.get(word, 0)

    ranked = dict(sorted(ranked.items(), key=lambda x: x[1], reverse=True))
    ranked = list(ranked.items())[:n]

    # Tie breaker using query term density
    for index in range(n - 1):
        if ranked[index][1] == ranked[index+1][1]:
            left = qtd(ranked[index][0], query)
            right = qtd(ranked[index][0], query)
            if right > left:
                ranked[index], ranked[index + 1] = ranked[index + 1], ranked[index]

    ranked = [item[0] for item in ranked]
    return ranked

if __name__ == "__main__":
    main()
