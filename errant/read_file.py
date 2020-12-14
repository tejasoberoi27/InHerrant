import stanza
from errant.alignment import Alignment
import errant
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parent
nlp = stanza.Pipeline('hi')
annotator = errant.load("hi")


def eval_edit_extraction(s1, s2):
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    target_iterator = iter(doc2.sentences)
    for i, orig in enumerate(doc1.sentences):
        cor = next(target_iterator)
        edits = annotator.annotate(orig, cor, lev=False, merging="rules")
        print("Number of edits: %d" % len(edits))
        list_edits = []
        for x in edits:
            print(x)
            list_edits.append(x.__str__())
        return list_edits


if __name__ == "__main__":

    types = ['adverb','karak','kram','ling','misc','noun','pronoun','vachan','verb','visheshan']
    path_incorr = base_dir/"hi"/"resources"/"btp_val_data"/"kram_new_incor.txt"
    path_corr = base_dir/"hi"/"resources"/"btp_val_data"/"kram_new_kar.txt"

    f_incorr = open(path_incorr, "r",encoding="utf8")
    f_corr = open(path_corr, "r",encoding="utf8")

    text_incorr = [sen for sen in f_incorr.readlines()]
    text_corr = [sen for sen in f_corr.readlines()]

    f_incorr.close()
    f_corr.close()

    d = []
    for i in range(len(text_incorr)):
        print("Sample No: ", i + 1)
        if text_incorr[i]=="\n":
            continue
        edits = eval_edit_extraction(text_incorr[i], text_corr[i])
        print(edits)
        for edit in edits:
            d.append([edit, text_incorr[i], text_corr[i]])

    df = pd.DataFrame(d, columns=['Proposed Edit', 'Incorrect Sentence', 'Correct Sentence'])
    print(df)
    df.to_csv(base_dir/"hi"/"resources"/"sample_edits"/"kram.csv", encoding="utf-8-sig")
