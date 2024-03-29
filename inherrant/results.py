from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from pathlib import Path
import pandas
import os
import collections
from sklearn.metrics import plot_confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def make_confusion_matrix(cf,
                          group_names=None,
                          categories='auto',
                          count=True,
                          percent=True,
                          cbar=True,
                          xyticks=True,
                          xyplotlabels=True,
                          sum_stats=True,
                          fig_size=None,
                          cmap='Blues',
                          title=None):
    '''
    This function will make a pretty plot of an sklearn Confusion Matrix cm using a Seaborn heatmap visualization.

    Arguments
    ---------
    cf:            confusion matrix to be passed in

    group_names:   List of strings that represent the labels row by row to be shown in each square.

    categories:    List of strings containing the categories to be displayed on the x,y axis. Default is 'auto'

    count:         If True, show the raw number in the confusion matrix. Default is True.

    normalize:     If True, show the proportions for each category. Default is True.

    cbar:          If True, show the color bar. The cbar values are based off the values in the confusion matrix.
                   Default is True.

    xyticks:       If True, show x and y ticks. Default is True.

    xyplotlabels:  If True, show 'True Label' and 'Predicted Label' on the figure. Default is True.

    sum_stats:     If True, display summary statistics below the figure. Default is True.

    fig_size:       Tuple representing the figure size. Default will be the matplotlib rcParams value.

    cmap:          Colormap of the values displayed from matplotlib.pyplot.cm. Default is 'Blues'
                   See http://matplotlib.org/examples/color/colormaps_reference.html

    title:         Title for the heatmap. Default is None.

    '''

    # CODE TO GENERATE TEXT INSIDE EACH SQUARE
    blanks = ['' for i in range(cf.size)]

    if group_names and len(group_names) == cf.size:
        group_labels = ["{}\n".format(value) for value in group_names]
    else:
        group_labels = blanks

    if count:
        group_counts = ["{0:0.0f}\n".format(value) for value in cf.flatten()]
    else:
        group_counts = blanks

    if percent:
        group_percentages = ["{0:.2%}".format(value) for value in cf.flatten() / np.sum(cf)]
    else:
        group_percentages = blanks

    box_labels = [f"{v1}{v2}{v3}".strip() for v1, v2, v3 in zip(group_labels, group_counts, group_percentages)]
    box_labels = np.asarray(box_labels).reshape(cf.shape[0], cf.shape[1])

    # CODE TO GENERATE SUMMARY STATISTICS & TEXT FOR SUMMARY STATS
    if sum_stats:
        # Accuracy is sum of diagonal divided by total observations
        accuracy = np.trace(cf) / float(np.sum(cf))

        # if it is a binary confusion matrix, show some more stats
        if len(cf) == 2:
            # Metrics for Binary Confusion Matrices
            precision = cf[1, 1] / sum(cf[:, 1])
            recall = cf[1, 1] / sum(cf[1, :])
            f1_score = 2 * precision * recall / (precision + recall)
            stats_text = "\n\nAccuracy={:0.3f}\nPrecision={:0.3f}\nRecall={:0.3f}\nF1 Score={:0.3f}".format(
                accuracy, precision, recall, f1_score)
        else:
            stats_text = "\n\nAccuracy={:0.3f}".format(accuracy)
    else:
        stats_text = ""

    # SET FIGURE PARAMETERS ACCORDING TO OTHER ARGUMENTS
    if fig_size is None:
        # Get default figure size if not set
        fig_size = plt.rcParams.get('figure.figsize')

    if xyticks == False:
        # Do not show categories if xyticks is False
        categories = False

    # MAKE THE HEATMAP VISUALIZATION
    plt.figure(figsize=fig_size)
    sns.heatmap(cf, annot=box_labels, fmt="", cmap=cmap, cbar=cbar, xticklabels=categories, yticklabels=categories)

    if xyplotlabels:
        plt.ylabel('True label')
        plt.xlabel('Predicted label' + stats_text)
    else:
        plt.xlabel(stats_text)

    if title:
        plt.title(title)
    plt.show()
    print("Done")


base_dir = Path(__file__).resolve().parent


# Input: takes in a csv file and returns arrays y_true,y_pred
def get_labels(error_type, df):
    cnt_rows = len(df.axes[0])
    # cnt_rows = 1
    y_true = []
    y_pred = []
    pred_quality = []
    extract_quality = []
    broad_types = []
    prev_correct_sentence = ""
    for num_row in range(cnt_rows):
        proposed_edit = df['Proposed Edit'][num_row]

        curr_correct_sentence = str(df['Correct Sentence'][num_row])
        new_sentence = True
        curr_extract_quality = str(df['Edit Extraction Quality (a,b)'][num_row])

        if prev_correct_sentence == curr_correct_sentence:
            new_sentence = False
        else:
            # if this sentence is new or this is the last sample of the file
            # newSentence remains True
            if curr_correct_sentence != "" and curr_extract_quality in ['a', 'b']:
                extract_quality.append(curr_extract_quality)
            prev_correct_sentence = curr_correct_sentence

        try:
            tags = proposed_edit.split(",")
        except:
            print("not working")
            print(proposed_edit)
        pred = ((tags[-1].split(" "))[-1])[1:-1:]
        pred = pred[pred.find(':') + 1:]
        label = df['True Label (Multi-Class)'][num_row]
        if not new_sentence:
            if curr_extract_quality == 'b':
                extract_quality[-1] = curr_extract_quality
        if pandas.isnull(label):
            continue
        else:
            pred_quality_label = df['Edit Quality (g,b,a)'][num_row]
            label = str(label)
            broad_type = label[:label.find(':')]
            # print("label:",label,"broad_type:",broad_type)
            label = label[label.find(':') + 1:]
            if (label == 'ORTH'):
                print("ORTH", error_type, num_row)
                continue
            # exit()
            if (pred_quality_label in ['g', 'b', 'a']):
                pred_quality.append(pred_quality_label)
            else:
                print("pos", error_type, num_row)
            y_pred.append(pred)
            y_true.append(label)
            broad_types.append(broad_type)

    return broad_types, extract_quality, pred_quality, y_true, y_pred


def combine_labels(labels_list):
    n = len(labels_list)
    for i in range(n):
        label_name = labels_list[i]
        p1 = label_name.find('-')
        if p1 != -1:
            label_name = label_name[:p1]
            labels_list[i] = label_name
    return labels_list


def get_data_stats(broad_types, y_true, combine=False, error_type_broad=False,error_type = False):
    # If combine=True, the subdivisions of Noun and gen shall be clubbed
    if combine:
        broad_types = combine_labels(broad_types)
        y_true = combine_labels(y_true)
    ctr_labels = collections.Counter(y_true)
    ctr_broad_types = collections.Counter(broad_types)
    total_labels = sum(ctr_labels.values())
    total_broad_types = sum(ctr_broad_types.values())
    desc_label = ctr_labels.most_common()
    desc_broad_types = ctr_broad_types.most_common()
    label_count = []
    broad_type_count = []
    label_num = 0
    broad_type_num = 0
    for k, v in desc_label:
        broad_type_num += 1
        broad_type_count.append([broad_type_num, str(k), str(v)])
        print(str(k) + '\t' + str(v))
    for k, v in desc_broad_types:
        label_num += 1
        label_count.append([label_num, str(k), str(v)])
        print(str(k) + '\t' + str(v))

    if error_type_broad:
        df = pandas.DataFrame(broad_type_count, columns=['S.No.', 'Broad Error Type', 'Frequency'])
        csv_file = "error_type_broad_distr.csv"
        df.to_csv(base_dir / "hi" / "resources" / "results" / csv_file, encoding="utf-8-sig")

    if error_type:
        df = pandas.DataFrame(label_count, columns=['S.No.', 'Error Type', 'Frequency'])
        csv_file = "error_type_distr.csv"
        df.to_csv(base_dir / "hi" / "resources" / "results" / csv_file, encoding="utf-8-sig")


def get_standard_metrics(y_true, y_pred, class_labels):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    F1_score = f1_score(y_true, y_pred, average='macro')
    cf_matrix = confusion_matrix(y_true, y_pred, labels=class_labels)
    assert (len(y_true) == len(y_pred))
    print("Total number of samples : % d" % (len(y_true)))
    print("Accuracy : % .3f" % (accuracy))
    print("Precision : % .3f" % (precision))
    print("Recall : % .3f" % (recall))
    print("F1 score : % .3f" % (F1_score))
    print(cf_matrix)
    make_confusion_matrix(cf_matrix, categories=class_labels, fig_size=(14, 14), percent=False, sum_stats=False)
    # disp = plot_confusion_matrix(X_test, y_test,
    #                                  display_labels=class_names,
    #                                  cmap=plt.cm.Blues,
    #                                  normalize=normalize)


def get_classification_perc(pred_quality):
    cnt_good = pred_quality.count('g')
    cnt_acceptable = pred_quality.count('a')
    cnt_bad = pred_quality.count('b')
    total = len(pred_quality)
    perc_good = (cnt_good * 100.0 / total)
    perc_acceptable = ((cnt_acceptable) * 100.0 / total)
    perc_bad = (cnt_bad * 100.0 / total)
    print("Total number of samples : % d" % (total))
    print("Edit Classification Quality Percentages")
    print("Good : % d, Acceptable: % d, Bad: % d" % (cnt_good, cnt_acceptable, cnt_bad))
    print("Good percentage : % .3f" % (perc_good))
    print("Acceptable percentage : % .3f" % (perc_acceptable))
    print("Bad percentage : %.3f" % (perc_bad))


def get_extraction_perc(extract_quality):
    cnt_acceptable = extract_quality.count('a')
    cnt_bad = extract_quality.count('b')
    total = len(extract_quality)
    perc_acceptable = ((cnt_acceptable) * 100.0 / total)
    perc_bad = (cnt_bad * 100.0 / total)
    print("Number of sentences: %d" % (total))
    print("Edit Extraction Quality Percentages")
    print("Acceptable: % d, Bad: % d" % (cnt_acceptable, cnt_bad))
    print("Acceptable percentage : % .3f" % (perc_acceptable))
    print("Bad percentage : %.3f" % (perc_bad))


def compute_metrics(combine=False,error_type_broad=False,error_type=False):
    error_types = ['karak', 'kram', 'ling', 'misc', 'noun', 'pronoun', 'vachan', 'verb', 'visheshan', 'new', 'extra',
                   'New-Samples', 'conj']
    y_true = []
    y_pred = []
    pred_quality = []
    extract_quality = []
    broad_types = []
    for error_type in error_types:
        # extension = os.path.normpath("/hi/resources/btp_val_data")
        # extension = "hi/resources/sample_edits_annotated/csv_files"
        extension = "hi/resources/sample_edits_annotated_March_21/csv_files"

        # extension = "hi/resources/sample_edits_annotated"
        # base_path= os.path.join(base_dir,extension)
        base_path = os.path.join(base_dir, extension)
        csv_file = error_type + ".csv"
        csv_file_path = os.path.join(base_path, csv_file)
        print("csv_file_path", csv_file_path)
        df = pandas.read_csv(csv_file_path)
        broad_type_cur, extract_quality_cur, pred_quality_cur, y_true_cur, y_pred_cur = get_labels(error_type, df)
        y_true.extend(y_true_cur)
        y_pred.extend(y_pred_cur)
        pred_quality.extend(pred_quality_cur)
        extract_quality.extend(extract_quality_cur)
        broad_types.extend(broad_type_cur)

    if combine:
        y_true = combine_labels(y_true)
        y_pred = combine_labels(y_pred)

    set_labels = set(y_true)
    error_labels = list(set_labels)
    print("---------------------------------------------------")
    get_standard_metrics(y_true, y_pred, error_labels)
    print("---------------------------------------------------")
    get_classification_perc(pred_quality)
    print("---------------------------------------------------")
    get_extraction_perc(extract_quality)
    get_data_stats(y_true, broad_types, combine=combine,error_type_broad=error_type_broad,error_type=error_type)


if __name__ == "__main__":
    compute_metrics(combine=False, error_type_broad=True, error_type=False)

    # path_corr = base_dir/"hi"/"resources"/"btp_val_data"/"kram_new_kar.txt"
