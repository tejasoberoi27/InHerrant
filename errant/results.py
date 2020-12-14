from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from pathlib import Path
import pandas
import os
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt

base_dir = Path(__file__).resolve().parent

#Input: takes in a csv file and returns arrays y_true,y_pred
def get_labels(csv_file_path):
    df = pandas.read_csv(csv_file_path)
    cnt_rows = len(df.axes[0])
    # cnt_rows = 1
    y_true = []
    y_pred = []
    for num_row in range(cnt_rows):
        proposed_edit = df['Proposed Edit'][num_row]
        tags = proposed_edit.split(",")
        pred = ((tags[-1].split(" "))[-1])[1:-1:]
        label = df['True Label (Multi-Class)'][num_row]
        y_pred.append(pred)
        y_true.append(label)
    return y_true,y_pred
        # print(tags)
    # print(proposed_edit)
    # print(df)


def compute_metrics():
    # error_types = ['adverb','karak','kram','ling','misc','noun','pronoun','vachan','verb','visheshan']
    error_types = ['vachan']
    y_true = []
    y_pred = []

    for error_type in error_types:
        print("base_dir", base_dir)
        # extension = os.path.normpath("/hi/resources/btp_val_data")
        extension = "hi/resources/sample_edits_annotated"
        # base_path= os.path.join(base_dir,extension)
        base_path = os.path.join(base_dir, extension)
        print("base_path", base_path)
        csv_file = error_type + ".csv"
        csv_file_path = os.path.join(base_path, csv_file)
        y_true_cur, y_pred_cur = get_labels(csv_file_path)
        y_true.extend(y_true_cur)
        y_pred.extend(y_pred_cur)
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='micro')
    recall = recall_score(y_true, y_pred, average='micro')
    cf_matrix = confusion_matrix(y_true, y_pred)
    print("Accuracy : % .3f" % (accuracy))
    print("Precision : % .3f" % (precision))
    print("Recall : % .3f" % (recall))
    print(cf_matrix)
    class_names = []
    disp = plot_confusion_matrix(classifier, X_test, y_test,
                                     display_labels=class_names,
                                     cmap=plt.cm.Blues,
                                     normalize=normalize)
if __name__ == "__main__":
    compute_metrics()



        # path_corr = base_dir/"hi"/"resources"/"btp_val_data"/"kram_new_kar.txt"
