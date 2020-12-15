import os

import stanza
from inherrant.alignment import Alignment
import inherrant
import pandas as pd
from pathlib import Path,PureWindowsPath

base_dir = Path(__file__).resolve().parent
nlp = stanza.Pipeline('hi')
annotator = inherrant.load("hi")

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

def get_csv(error_type):
    # extension = os.path.normpath("/hi/resources/btp_val_data")
    extension = "hi/resources/sample_edits_annotated/csv_files"
    # base_path= os.path.join(base_dir,extension)
    base_path = os.path.join(base_dir, extension)
    csv_file = error_type + ".csv"
    csv_file_path = os.path.join(base_path, csv_file)
    print("csv_file_path", csv_file_path)
    df = pd.read_csv(csv_file_path)
    return df

def write_to_csv():
    error_types = ['karak','kram','ling','misc','noun','pronoun','vachan','verb','visheshan']
    for error_type in error_types:
        print("base_dir",base_dir)
        # extension = os.path.normpath("/hi/resources/btp_val_data")
        extension = "hi/resources/btp_val_data"
        # base_path= os.path.join(base_dir,extension)
        base_path = os.path.join(base_dir,extension)
        print("base_path",base_path)
        file_incorr = error_type+"_new_incor.txt"
        file_corr = error_type+"_new_cor.txt"
        # path_incorr = "kram_new_incor.txt"
        path_incorr = os.path.join(base_path,file_incorr)
        path_corr = os.path.join(base_path,file_corr)


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

        df_v1_csv = get_csv(error_type)
        df = pd.DataFrame(d, columns=['Proposed Edit', 'Incorrect Sentence', 'Correct Sentence'])
        df_v1_csv['Proposed Edit'] = df['Proposed Edit']
        print(df)
        print(df_v1_csv)
        csv_file =  error_type+".csv"
        df_v1_csv.to_csv(base_dir/"hi"/"resources"/"sample_edits_3"/csv_file, encoding="utf-8-sig")


if __name__ == "__main__":
    write_to_csv()