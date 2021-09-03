import os
from pathlib import Path
import stanza
import pandas as pd
import pickle
import inherrant

base_dir = Path(__file__).resolve().parent
annotator = inherrant.load("hi")
nlp = stanza.Pipeline('hi')

def eval_edit_extraction(s1, s2):
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    target_iterator = iter(doc2.sentences)
    # edits = annotator.annotate(doc1, doc2, lev=False, merging="rules")
    # list_edits = []
    # for x in edits:
    #     # print(x)
    #     list_edits.append(x.__str__())
    # return list_edits
    for i, orig in enumerate(doc1.sentences):
        cor = next(target_iterator)
        edits = annotator.annotate(orig, cor, lev=False, merging="rules")
        # print("Number of edits: %d" % len(edits))
        list_edits = []
        for x in edits:
            # print(x)
            list_edits.append(x.__str__())
        return list_edits

def get_csv(error_type):
    # extension = os.path.normpath("/hi/resources/btp_val_data")
    extension = "hi/resources/sample_edits_annotated/csv_files"
    # base_path= os.path.join(base_dir,extension)
    base_path = os.path.join(base_dir, extension)
    csv_file = error_type + ".csv"
    csv_file_path = os.path.join(base_path, csv_file)
    # print("csv_file_path", csv_file_path)
    df = pd.read_csv(csv_file_path,encoding ='utf-8-sig' )
    return df


def get_pred_from_edit(proposed_edit):
    tags = proposed_edit.split(",")
    pred = ((tags[-1].split(" "))[-1])[1:-1:]
    return pred

def modify_df_gen(df):
    cnt_rows = len(df.axes[0])
    for num_row in range(cnt_rows):
        proposed_edit = df['Proposed Edit'][num_row]
        pred = get_pred_from_edit(proposed_edit)
        original_pred = pred
        pred = pred[pred.find(':')+1:]
        broad_type = pred[:pred.find(':')]
        label = df['True Label (Multi-Class)'][num_row]
        if pd.isnull(label):
            continue
        else:
            if(pred in ["ADJ-NUM","VERB-NUM","PRON-NUM"]):
                df.loc[num_row,'True Label (Multi-Class)'] = original_pred
            label = df['True Label (Multi-Class)'][num_row]
            label = str(label)
            label = label[label.find(':') + 1:]
            print("num_row: ",num_row,"pred: ",pred,"label: ",label)
            print("pred==label",pred==label)
            if(pred==label):
                #change edit quality to g where true label and pred match
                # df['Edit Extraction Quality (a,b)'][num_row] = 'g'
                df.loc[num_row,'Edit Quality (g,b,a)'] = 'g'
    return df

def get_diff(error_type,df_prev,df_cur):
    cnt_rows = len(df_prev.axes[0])
    assert (len(df_cur.axes[0])==cnt_rows)
    rows = []
    for num_row in range(cnt_rows):
        proposed_edit_prev = df_prev['Proposed Edit'][num_row]
        proposed_edit_cur = df_cur['Proposed Edit'][num_row]
        cur_edit_quality = df_cur['Edit Quality (g,b,a)'][num_row]
        pred_prev = get_pred_from_edit(proposed_edit_prev)
        pred_cur= get_pred_from_edit(proposed_edit_cur)
        label = df_cur['True Label (Multi-Class)'][num_row]
        diff_pairs= []
        sent_prev = df_prev["Correct Sentence"][num_row]
        sent_cur = df_cur["Correct Sentence"][num_row]
        assert(sent_prev==sent_cur)
        print()
        if pd.isnull(label):
            continue
        else:
            if pred_cur!=pred_prev and cur_edit_quality!='g':
                rows.append(num_row)
                diff_pairs.append([str(num_row),str(pred_prev),str(pred_cur)])
                print("num_row :",num_row, "pred_prev: ",pred_prev,"pred_cur: ",pred_cur)
    if(len(rows)>0):
        print("Error type:",error_type)
        print("Rows: ",rows)
        print(diff_pairs)
        print("---------------")


def get_hypo(error_type):
    d = []
    print("base_dir",base_dir)
    #extension = os.path.normpath("btp_val_data")
    extension = "btp_val_data"
    # base_path= os.path.join(base_dir,extension)
    base_path = os.path.join(base_dir,extension)
    # print("base_path",base_path)
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
    d_sen = []
    for i in range(len(text_incorr)):
        print("Sample No: ", i + 1)
        if text_incorr[i] == "\n":
            continue
        edits = eval_edit_extraction(text_incorr[i], text_corr[i])
        print(edits)
        for edit in edits:
            d.append([edit, text_incorr[i], text_corr[i]])
        d_sen.append([text_incorr[i],text_corr[i],edits])
    return d,d_sen

def write_to_csv():
    error_types = ['adverb','conj','extra','karak','kram','ling','misc','noun','pronoun','vachan','verb','visheshan','new','New-Samples']
    #error_types = ["adverb"]
    for error_type in error_types:
        #df_v1_csv = get_csv(error_type)
        #df_prev = df_v1_csv.copy()
        d, d_sen = get_hypo(error_type)
        df = pd.DataFrame(d, columns=['Proposed Edit', 'Incorrect Sentence', 'Correct Sentence'])
        df.to_csv("csv_files/"+error_type+".csv",encoding="utf-8-sig")
        with open('pickle_files/'+error_type+".pt", 'wb') as pickle_file:
            pickle.dump(d_sen, pickle_file)
        #df_v1_csv['Proposed Edit'] = df['Proposed Edit']
        # print(df)
        # print(df_v1_csv)
        #df_v1_csv = modify_df_gen(df_v1_csv)
        #get_diff(error_type,df_prev,df_v1_csv)
        #csv_file = error_type+".csv"
        #df_v1_csv.to_csv(base_dir/"hi"/"resources"/"sample_edits_3"/csv_file, encoding="utf-8-sig")



if __name__ == "__main__":
    write_to_csv()