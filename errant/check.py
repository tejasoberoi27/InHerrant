import stanza
from errant.alignment import Alignment
import errant
import Levenshtein


if __name__ == '__main__':
    # stanza.download('hi')
    nlp = stanza.Pipeline('hi')
    s1 = "राम ने खाना खाया"
    # print(doc)
    annotator = errant.load("hi")
    doc1 = nlp(s1)
    target_iterator = iter(doc1.sentences)

    # for i, orig in enumerate(doc1.sentences):
    #     print(orig.words)
    orig = doc1.sentences[0].words
    print(orig)