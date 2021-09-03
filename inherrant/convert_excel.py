import pandas as pd
import stanza
import os
from pathlib import Path
import inherrant
import pickle


base_dir = Path(__file__).resolve().parent
annotator = inherrant.load("hi")
nlp = stanza.Pipeline('hi')
os.environ['KMP_DUPLICATE_LIB_OK']='True'


def eval_edit_extraction(s1, s2):
    doc1 = nlp(s1)
    doc2 = nlp(s2)
    print("here")
    target_iterator = iter(doc2.sentences)
    for i, orig in enumerate(doc1.sentences):
        cor = next(target_iterator)
        edits = annotator.annotate(orig, cor, lev=False, merging="rules")
        print("Number of edits: %d" % len(edits))
        list_edits = []
        for x in edits:
            # print(x)
            list_edits.append(x.__str__())
        return list_edits


def get_csv(error_type):
    extension = "pre_annotated"
    # base_path= os.path.join(base_dir,extension)
    base_path = os.path.join(base_dir, extension)
    csv_file = error_type + " - "+ error_type + ".csv"
    csv_file_path = os.path.join(base_path, csv_file)
    df = pd.read_csv(csv_file_path,encoding ='utf-8-sig' )
    return df


def get_pred_from_edit(proposed_edit):
    #print("here")
    #print(proposed_edit)
    tags = proposed_edit.split(",")
    pred = ((tags[-1].split(" "))[-1])[1:-1:]
    return pred


def convert_pred_ankur(pred_ankur):
    if ':' in pred_ankur:
        pred = pred_ankur.split(':')
        new_pred = pred[0] + '-' + pred[1]
    else:
        new_pred = pred_ankur
    return new_pred


def get_diff_other(error_type, df_cur):
    cnt_rows = len(df_cur.axes[0])
    annotation_match = []
    true_label = []
    edit_quality = []
    edit_ex_quality = []
    for num_row in range(cnt_rows):
        #pred_prev = get_pred_from_edit(df_prev[num_row])
        proposed_edit_cur = df_cur['Proposed Edit InHerrant'][num_row]
        cur_edit_quality = df_cur['Edit Quality Before (g,b,a)'][num_row]
        pred_cur = get_pred_from_edit(proposed_edit_cur)
        label = df_cur['True Label Before (Multi-Class)'][num_row]
        #print("label",label)
        #print("pred_cur",pred_cur)
        if pred_cur == label and cur_edit_quality == 'g':
            true_label.append(label)
            edit_quality.append(cur_edit_quality)
            edit_ex_quality.append(df_cur['Edit Extraction Quality Before(a,b)'][num_row])
            annotation_match.append("YES")
        else:
            #print("pred_cur", pred_cur)
            #print("pred-prev",pred_prev)
            if pred_cur[2:] == "MORPH":
                true_label.append("R:MORPH")
                edit_quality.append('g')
                edit_ex_quality.append(df_cur['Edit Extraction Quality Before(a,b)'][num_row])
                annotation_match.append("YES")
            else:
                true_label.append(pred_cur)
                edit_quality.append(cur_edit_quality)
                edit_ex_quality.append(df_cur['Edit Extraction Quality Before(a,b)'][num_row])
                annotation_match.append("NO")

    df_cur['True Label (Multi-Class)'] = true_label
    df_cur['Edit Quality (g,b,a)'] = edit_quality
    df_cur['Edit Extraction Quality (a,b)'] = edit_ex_quality
    df_cur['InHerrant Annotation Correct'] = annotation_match


def get_diff(error_type, df_cur):
    cnt_rows = len(df_cur.axes[0])
    annotation_match = []
    quality_ankur = []
    copied = []
    true_label = []
    edit_quality = []
    edit_ex_quality = []
    for num_row in range(cnt_rows):
        #pred_prev = get_pred_from_edit(df_prev[num_row])
        proposed_edit_cur = df_cur['Proposed Edit InHerrant'][num_row]
        proposed_edit_ankur = df_cur['Proposed Edit Ankur\'s Errant'][num_row]
        cur_edit_quality = df_cur['Edit Quality Before (g,b,a)'][num_row]
        pred_ankur = get_pred_from_edit(proposed_edit_ankur)
        pred_cur = get_pred_from_edit(proposed_edit_cur)
        label = df_cur['True Label Before (Multi-Class)'][num_row]
        #print("label",label)
        #print("pred_cur",pred_cur)
        if pred_cur == label and cur_edit_quality == 'g':
            true_label.append(label)
            edit_quality.append(cur_edit_quality)
            edit_ex_quality.append(df_cur['Edit Extraction Quality Before(a,b)'][num_row])
            annotation_match.append("YES")
        else:
            #print("pred_cur", pred_cur)
            #print("pred-prev",pred_prev)
            if pred_cur[2:] == "MORPH":
                true_label.append("R:MORPH")
                edit_quality.append('g')
                edit_ex_quality.append(df_cur['Edit Extraction Quality Before(a,b)'][num_row])
                annotation_match.append("YES")
            else:
                true_label.append(pred_cur)
                edit_quality.append(cur_edit_quality)
                edit_ex_quality.append(df_cur['Edit Extraction Quality Before(a,b)'][num_row])
                annotation_match.append("NO")

        pred_ankur = pred_ankur[:2] + convert_pred_ankur(pred_ankur[2:])
        #print("pred ankur",pred_ankur)
        #print("pred cur",pred_cur)
        pos_list = ['ADJ', 'NOUN', 'PRON', 'VERB']
        flag=0
        for pos in pos_list:
            if (pred_cur[2:] == pos+'-GEN' or pred_cur[2:] == pos+'-NUM') and pred_ankur[2:] == pos+'-INFL' and cur_edit_quality == 'g':
                quality_ankur.append('a')
                copied.append("YES")
                flag=1
                break
        if flag==1:
            continue
        if pred_cur[2:] == 'ADP-INFL' and pred_ankur[2:] == pred_cur[2:]:
            quality_ankur.append(cur_edit_quality)
            copied.append("YES")
        elif pred_cur[2:] == 'VERB-TENSE' and pred_ankur[2:] == 'VERB-FORM' and cur_edit_quality == 'g':
            quality_ankur.append('a')
            copied.append("YES")
        elif pred_ankur[2:] == 'MULTI':
            quality_ankur.append('b')
            copied.append("YES")
        else:
            quality_ankur.append(cur_edit_quality)
            copied.append("NO")
    df_cur['True Label (Multi-Class)'] = true_label
    df_cur['Edit Quality (g,b,a)'] = edit_quality
    df_cur['Edit Extraction Quality (a,b)'] = edit_ex_quality
    df_cur['InHerrant Annotation Correct'] = annotation_match
    df_cur['Edit Quality (g,b,a) Ankur'] = quality_ankur
    df_cur['Ankur Annotation Correct'] = copied

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
    for i in range(len(text_incorr)):
        print("Sample No: ", i + 1)
        if text_incorr[i] == "\n":
            continue
        edits = eval_edit_extraction(text_incorr[i], text_corr[i])
        print(edits)
        for edit in edits:
            d.append([edit, text_incorr[i], text_corr[i]])
    return d


def loadData(file_path):
    # for reading also binary mode is important
    dbfile = open(file_path, 'rb')
    list_edits = pickle.load(dbfile)
    dbfile.close()
    return list_edits


def filter_edits(error_type,df):
    list_replacement = []
    list_others = []
    list_edits_inherrant = loadData("pickle_files/"+error_type+".pt")
    list_edits_ankur = loadData("pickle_files_ankur/"+error_type+".pt")
    assert len(list_edits_ankur) == len(list_edits_inherrant)
    row = 0
    for i in range(len(list_edits_inherrant)):
        sent_incor = list_edits_inherrant[i][0]
        sent_cor = list_edits_inherrant[i][1]
        assert sent_incor == list_edits_ankur[i][0]
        assert sent_cor == list_edits_ankur[i][1]
        edits_inherrant = list_edits_inherrant[i][2]
        edits_ankur = list_edits_ankur[i][2]
        if len(edits_inherrant) == len(edits_ankur):
            for j in range(len(edits_inherrant)):
                pred_type = get_pred_from_edit(edits_inherrant[j])[0]
                if pred_type=='U' or pred_type=='M':
                    df_obj = [edits_inherrant[j], sent_incor, sent_cor]
                    assert df['Incorrect Sentence'][row] == sent_incor
                    df_obj.append(df['True Label Before (Multi-Class)'][row])
                    df_obj.append(df['Edit Quality Before (g,b,a)'][row])
                    df_obj.append(df['Edit Extraction Quality Before(a,b)'][row])
                    row += 1
                    list_others.append(df_obj)
                else:
                    df_obj = [edits_inherrant[j], edits_ankur[j], sent_incor, sent_cor]
                    assert df['Incorrect Sentence'][row] == sent_incor
                    df_obj.append(df['True Label Before (Multi-Class)'][row])
                    df_obj.append(df['Edit Quality Before (g,b,a)'][row])
                    df_obj.append(df['Edit Extraction Quality Before(a,b)'][row])
                    row += 1
                    list_replacement.append(df_obj)
        else:
            for j in range(len(edits_inherrant)):
                df_obj = [edits_inherrant[j], sent_incor, sent_cor]
                assert df['Incorrect Sentence'][row] == sent_incor
                df_obj.append(df['True Label Before (Multi-Class)'][row])
                df_obj.append(df['Edit Quality Before (g,b,a)'][row])
                df_obj.append(df['Edit Extraction Quality Before(a,b)'][row])
                row += 1
                list_others.append(df_obj)
    df_replacement = pd.DataFrame(list_replacement, columns=['Proposed Edit InHerrant', 'Proposed Edit Ankur\'s Errant', 'Incorrect Sentence', 'Correct Sentence','True Label Before (Multi-Class)', 'Edit Quality Before (g,b,a)', 'Edit Extraction Quality Before(a,b)'])
    df_others = pd.DataFrame(list_others, columns=['Proposed Edit InHerrant', 'Incorrect Sentence', 'Correct Sentence','True Label Before (Multi-Class)', 'Edit Quality Before (g,b,a)', 'Edit Extraction Quality Before(a,b)'])
    return df_replacement,df_others


def write_to_csv():
    error_types = ['adverb','conj','extra','karak','kram','ling','misc','noun','pronoun','vachan','verb','visheshan','new','New-Samples']
    #error_types = ["adverb"]
    for error_type in error_types:
        df_v1_csv = get_csv(error_type)
        d = get_hypo(error_type)
        #print(d)
        df = pd.DataFrame(d, columns=['Proposed Edit InHerrant', 'Incorrect Sentence', 'Correct Sentence'])
        #print(df)
        #df.to_csv("csv_files/"+error_type+".csv",encoding="utf-8-sig")
        #df_prev = df_v1_csv['Proposed Edit InHerrant']
        df_v1_csv['Proposed Edit InHerrant'] = df['Proposed Edit InHerrant']
        # print(df)
        # print(df_v1_csv)
        df_replacement, df_others = filter_edits(error_type,df_v1_csv)
        get_diff(error_type, df_replacement)
        get_diff_other(error_type,df_others)
        csv_file = error_type+".csv"
        df_replacement = df_replacement.drop(['Edit Quality Before (g,b,a)',
                             'Edit Extraction Quality Before(a,b)'],axis=1)
        df_others = df_others.drop(['Edit Quality Before (g,b,a)',
                                            'Edit Extraction Quality Before(a,b)'], axis=1)
        df_replacement.to_csv(base_dir/"final_replacement_csv"/csv_file, encoding="utf-8-sig")
        df_others.to_csv(base_dir / "final_other_csv" / csv_file, encoding="utf-8-sig")


if __name__=="__main__":
    write_to_csv()