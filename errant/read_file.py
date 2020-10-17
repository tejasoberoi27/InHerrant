import stanza
from errant.alignment import Alignment
import errant
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
nlp = stanza.Pipeline('hi')
annotator = errant.load("hi")

def test_edit_extraction(s1, s2):

    doc1 = nlp(s1)
    doc2 = nlp(s2)
    target_iterator = iter(doc2.sentences)
    for i, orig in enumerate(doc1.sentences):
        cor = next(target_iterator)
        edits = annotator.annotate(orig, cor, lev=True, merging="rules")
        print("Number of edits: %d" % len(edits))
        list_edits = []
        for x in edits:
            print(x)
            list_edits.append(x.__str__())
        return list_edits

if __name__ == "__main__":

    path_incorr = base_dir/"hi"/"resources"/"incorr.txt"
    path_corr = base_dir/"hi"/"resources"/"corr.txt"

    f_incorr = open(path_incorr, "r")
    f_corr = open(path_corr, "r")

    text_incorr = [sen for sen in f_incorr.readlines()]
    text_corr = [sen for sen in f_corr.readlines()]

    f_incorr.close()
    f_corr.close()

    d = []
    for i in range(len(text_incorr)):
        print("Sample No: ", i + 1)
        edits = test_edit_extraction(text_incorr[i], text_corr[i])
        print(edits)
        d.append([text_incorr[i], text_corr[i], edits])

    df = pd.DataFrame(d, columns=['Incorrect Sentence', 'Correct Sentence', 'Proposed Edits'])

    df.to_csv(base_dir/"hi"/"resources"/"sample_edits.csv")


