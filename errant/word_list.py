import stanza
from pathlib import Path


base_dir = Path(__file__).resolve().parent
nlp = stanza.Pipeline('hi')


def parse(f):
  res = set()
  c = 0
  for sen in f.readlines():
    print(c)
    c += 1
    doc = nlp(sen)
    s = set([word.text for sen in doc.sentences for word in sen.tokens])
    res = res.union(s)
    return res


if __name__ == "__main__":

    path_1 = base_dir/"hi"/"resources"/"btp_val_data"/"kram_new_kar.txt"
    path_2 = base_dir / "hi" / "resources" / "btp_val_data" / "noun_new_cor.txt"
    path_3 = base_dir / "hi" / "resources" / "btp_val_data" / "karak_new_cor.txt"
    path_4 = base_dir / "hi" / "resources" / "btp_val_data" / "ling_new_cor.txt"
    path_5 = base_dir / "hi" / "resources" / "btp_val_data" / "misc_new_cor.txt"
    path_6 = base_dir / "hi" / "resources" / "btp_val_data" / "pronoun_new_cor.txt"
    path_7 = base_dir / "hi" / "resources" / "btp_val_data" / "vachan_new_cor.txt"
    path_8 = base_dir / "hi" / "resources" / "btp_val_data" / "verb_new_cor.txt"
    path_9 = base_dir / "hi" / "resources" / "btp_val_data" / "visheshan_new_cor.txt"

    f_1 = open(path_1, "r")
    f_2 = open(path_2, "r")
    f_3 = open(path_3, "r")
    f_4 = open(path_4, "r")
    f_5 = open(path_5, "r")
    f_6 = open(path_5, "r")
    f_7 = open(path_5, "r")
    f_8 = open(path_5, "r")
    f_9 = open(path_5, "r")

    text_1 = set([sen for sen in f_1.readlines()])
    text_2 = set([w for sen in f_2.readlines() for w in sen.split()])
    text_3 = set([w for sen in f_3.readlines() for w in sen.split()])
    text_4 = set([w for sen in f_4.readlines() for w in sen.split()])
    text_5 = set([w for sen in f_5.readlines() for w in sen.split()])
    text_6 = set([w for sen in f_5.readlines() for w in sen.split()])
    text_7 = set([w for sen in f_5.readlines() for w in sen.split()])
    text_8 = set([w for sen in f_5.readlines() for w in sen.split()])
    text_9 = set([w for sen in f_5.readlines() for w in sen.split()])

    vocab = text_1.union(text_2)
    vocab = vocab.union(text_3)
    vocab = vocab.union(text_4)
    vocab = vocab.union(text_5)
    vocab = vocab.union(text_6)
    vocab = vocab.union(text_7)
    vocab = vocab.union(text_8)
    vocab = vocab.union(text_9)

    f_1.close()
    f_2.close()
    f_3.close()
    f_4.close()
    f_5.close()
    f_6.close()
    f_7.close()
    f_8.close()
    f_9.close()

    print(len(vocab))

    c = 0
    f = open(base_dir/"hi"/"resources"/"vocab.txt", "a")
    for v in vocab:
        if len(v) == 0:
            continue
        f.write(v)
        if v[-1] != '\n':
            f.write('\n')
        c += 1
    f.close()
