from pathlib import Path
import Levenshtein
from .hindi_stemmer import HindiStemmer


def get_gen(feats):
    if 'Gender' in feats:
        return feats['Gender']
    else:
        return ""


def get_tense(feats):
    if 'Tense' in feats:
        return feats['Tense']
    else:
        return ""


def get_num(feats):
    if 'Number' in feats:
        return feats['Number']
    else:
        return ""


def opposite_gen(o_feats, c_feats):
    """ Returns true if the two tokens have opposite genders"""
    if not o_feats or not c_feats:
        return False
    else:
        if {'Masc', 'Fem'}.issubset({get_gen(o_feats), get_gen(c_feats)}):
            return True
        else:
            return False


def opposite_num(o_feats, c_feats):
    """ Returns true if one of the tokens is singular and other plural"""
    if not o_feats or not c_feats:
        return False
    else:
        if {'Sing', 'Plur'}.issubset({get_num(o_feats), get_num(c_feats)}):
            return True
        else:
            return False


def opposite_tense(o_feats, c_feats):
    """ Returns true if the tense of both tokens is different, empty string included"""
    if get_tense(o_feats) != get_tense(c_feats):
        return True
    else:
        return False


def get_feats(Word):
    # returns features of a Stanza word as a dictionary
    feats = {}
    try:
        Feats = Word.feats
        if Feats:
            Feats = Feats.replace("feats: ", "")
            Feats = Feats.split('|')
            for pair in Feats:
                feat, val = pair.split("=")
                feats[feat] = val
            if 'Gender' not in feats:
                feats['Gender'] = ""
            if 'Number' not in feats:
                feats['Number'] = ""
            if 'Tense' not in feats:
                feats['Tense'] = ""
    except Exception as e:
        # print("e is", e)
        # print("Word is", Word)
        pass
    return feats


def are_stems_similar(o_stem, c_stem):
    """ Returns true if if two stems are similar"""
    f1 = lambda stem: stem.endswith('ी')
    f2 = lambda stem: stem.endswith('िय')
    f3 = lambda stem1, stem2: f1(stem1) and f2(stem2) and stem1[-1:] == stem2[-2:]
    f4 = lambda stem1, stem2: f3(stem1, stem2) or f3(stem2, stem1)
    if f4(o_stem, c_stem):
        return True
    c_stemchar_ratio = Levenshtein.ratio(o_stem, c_stem)
    c_stemchar_dist = Levenshtein.distance(o_stem, c_stem)
    return c_stemchar_dist <= 1 or c_stemchar_ratio >= 0.8


# Input 1: Spacy orig tokens
# Input 2: Spacy cor tokens
# Output: Boolean; the tokens are exactly the same but in a different order
def exact_reordering(o_toks, c_toks):
    # Sorting lets us keep duplicates.
    oset = {}
    cset = {}
    for tok in o_toks:
        if tok.text in oset:
            oset[tok.text] += 1
        else:
            oset[tok.text] = 1
    for tok in c_toks:
        if tok.text in cset:
            cset[tok.text] += 1
        else:
            cset[tok.text] = 1
    check = True
    for k in oset:
        if k in cset and oset[k] == cset[k]:
            continue
        else:
            check = False
            break
    if len(oset) == len(cset) and check:
        return True
    return False


def is_only_orth_change(o_toks: list, c_toks: list) -> bool:
    o_join = "".join(o_tok.text for o_tok in o_toks)
    c_join = "".join(c_tok.text for c_tok in c_toks)
    if o_join == c_join:
        return True
    return False


# Input: An Edit object
# Output: The same Edit object with an updated error type
def classify(edit):
    # Nothing to nothing is a detected but not corrected edit
    if not edit.o_toks and not edit.c_toks:
        edit.type = "UNK"
    # Missing
    elif not edit.o_toks and edit.c_toks:
        op = "M:"
        cat = get_one_sided_type(edit.c_toks)
        edit.type = op + cat
    # Unnecessary
    elif edit.o_toks and not edit.c_toks:
        op = "U:"
        cat = get_one_sided_type(edit.o_toks)
        edit.type = op + cat
    # Replacement and special cases
    else:
        # Same to same is a detected but not corrected edit
        if edit.o_str == edit.c_str:
            edit.type = "UNK"
        # Replacement
        else:
            op = "R:"
            cat = get_two_sided_type(edit.o_toks, edit.c_toks)
            edit.type = op + cat
    return edit


# Input: Spacy tokens
# Output: An error type string based on input tokens from orig or cor
# When one side of the edit is null, we can only use the other side
def get_one_sided_type(toks):
    # Special cases
    toks = [tok.words[0] for tok in toks]
    pos, dep = get_edit_info(toks)
    # Auxiliary verbs
    if set(dep).issubset({"aux", "aux:pass"}):
        return "VERB-TENSE"
    if len(toks) == 1:
        if pos[0] in list_pos:
            return pos[0]
        if pos[0] in ["NUM"]:
            return "ADJ"
        if toks[0].deprel == "punct":
            return "PUNCT"
    if len(set(pos)) == 1 and pos[0] in list_pos:
        return pos[0]
    else:
        return "OTHER"


# Input: Spacy tokens
# Output: A list of pos and dep tag strings
def get_edit_info(toks):
    pos = []
    dep = []
    for tok in toks:
        # print("POS", tok.pos)
        if tok.pos in ("CCONJ", "SCONJ"):
            pos.append("CONJ")
        else:
            pos.append(tok.pos)
        dep.append(tok.deprel)
    return pos, dep


def load_word_list(path):
    with open(path, encoding="utf8") as word_list:
        return set([word.strip() for word in word_list])


base_dir = Path(__file__).resolve().parent
stemmer = HindiStemmer()
main_pos = ['NOUN', 'PRON', 'VERB', 'ADJ']
spell = load_word_list(base_dir / "resources" / "hi_IN.txt")
# list_spell = list(spell)
# dict = sorted(list_spell)
# print(dict)
# print("रेह" in spell)
rare_pos = {"INTJ", "NUM", "SYM", "X"}
open_pos2 = {"ADJ", "ADV", "NOUN", "VERB"}
list_pos = ['NOUN', 'PRON', 'VERB', 'ADJ', 'ADP', 'ADV', 'PREP', 'DET', 'CONJ']
morph_list = ["ADJ", "ADV", "NOUN", "VERB", "ADP", "PRON"]


# Input 1: Stanza orig tokens
# Input 2: Stanza cor tokens
# Output: An error type string based on orig AND cor
def is_tense_aux(o_tok, c_tok):
    #checks if both the tokens belong to auxiliary verbs list responsible for tense changes
    set_tense_aux_lemma = {'लग', 'सक', 'खाना', 'चुक', 'है', 'लगा', 'दे', 'जा', 'चल', 'ले', 'चाहिए', 'कर', 'रह', 'सकूँग', 'खा', 'पड़', 'ला', 'हो', 'पा', 'गय', 'आ', 'पड', 'था', 'चाहि'}
    set_tense_aux_stem = {'थी', 'जाएँ', 'लग', 'पाए', 'सक', 'लिय', 'आई', 'दिय', 'चाह', 'चुक', 'है', 'पाओ', 'खाय', 'दे', 'जा', 'लगाएँग', 'जाओ', 'ले', 'चल', 'गईं', 'लाय', 'गए', 'लिए', 'लाएँग', 'थे', 'कर', 'हुईं', 'हुए', 'रह', 'हैं', 'किए', 'होग', 'खाए', 'खा', 'लाए', 'पड़', 'हुई', 'ला', 'ली', 'हो', 'लगाऊँ', 'पाय', 'चाहिएँ', 'थीं', 'लो', 'गय', 'आए', 'जाएँग', 'था', 'कीज', 'जाएग', 'हुआ', 'आय', 'लीं', 'होंग', 'किय', 'दी', 'पाएँग', 'आईं', 'गई', 'पाएँ', 'की'}
    o_stem = stemmer.stem(o_tok.text)
    c_stem = stemmer.stem(c_tok.text)
    o_lemma = o_tok.lemma
    c_lemma = c_tok.lemma
    if ({o_stem,c_stem}.issubset(set_tense_aux_stem)) or ({o_lemma,c_lemma}.issubset(set_tense_aux_lemma)):
        return True
    return False

def get_two_sided_type(o_toks, c_toks):
    o_toks = [tok.words[0] for tok in o_toks]
    c_toks = [tok.words[0] for tok in c_toks]

    # print("Hello", o_toks, c_toks)

    # Extract pos tags and parse info from the toks as lists
    o_pos, o_dep = get_edit_info(o_toks)
    c_pos, c_dep = get_edit_info(c_toks)

    o_feats = [get_feats(o_toks[0]) for tok in o_toks]
    c_feats = [get_feats(c_toks[0]) for tok in c_toks]

    o_gen = [get_gen(o_feats[i]) for i in range(len(o_feats))]
    c_gen = [get_gen(c_feats[i]) for i in range(len(c_feats))]

    o_num = [get_num(o_feats[i]) for i in range(len(o_feats))]
    c_num = [get_num(c_feats[i]) for i in range(len(c_feats))]

    o_stem = stemmer.stem(o_toks[0].text)
    c_stem = stemmer.stem(c_toks[0].text)
    c_stemchar_dist = Levenshtein.distance(o_stem, c_stem)
    c_stemchar_ratio = Levenshtein.ratio(o_stem, c_stem)
    print("o_stem", o_stem, "c_stem", c_stem, "c_stemchar_dist", c_stemchar_dist, "c_stemchar_ratio", c_stemchar_ratio)
    print("o_num", o_num, "c_num", c_num)
    print("lemma_o", o_toks[0].lemma, "lemma_c", c_toks[0].lemma)

    # Word Order; only matches exact reordering.
    if exact_reordering(o_toks, c_toks):
        return "WO"

    if is_only_orth_change(o_toks, c_toks):
        return "ORTH"

    # 1:1 replacements (very common)
    if len(o_toks) == len(c_toks) == 1:

        # 2. SPELLING AND INFLECTION
        # Spelling errors take precedence over POS errors; this rule is ordered
        # Check a GB English dict for both orig and lower case.
        # E.g. "cat" is in the dict, but "Cat" is not.
        if o_toks[0].text not in spell:
            char_ratio = Levenshtein.ratio(o_toks[0].text, c_toks[0].text)
            char_dist = Levenshtein.distance(o_toks[0].text, c_toks[0].text)
            print("Not in spell")
            # print("Character Ratio ", char_ratio)
            # Ratio > 0.5 means both side share at least half the same chars.
            # WARNING: THIS IS AN APPROXIMATION.
            if char_ratio >= 0.5 or char_dist == 1:
                return "SPELL"
            # If ratio is < 0.5, the error is more complex e.g. tolk -> say
            else:
                # If POS is the same, this takes precedence over spelling.
                if o_pos[0] == c_pos[0] and \
                        o_pos[0] in list_pos:
                    return o_pos[0]
                # Tricky cases.
                else:
                    return "OTHER"

        # 1. SPECIAL CASES
        # print("Reached")
        # Gender Edits
        # if the edit has both tense and gender different, then classify as gender edit
        if (c_pos[0] in (main_pos + ['AUX', 'ADP'])) and (o_toks[0].lemma == c_toks[0].lemma or are_stems_similar(o_stem,c_stem)):
            if c_pos[0]=='ADP':
                return "ADP-INFL"
            if opposite_gen(o_feats[0], c_feats[0]) and c_pos[0] != "NOUN":
                if c_pos[0] == 'AUX':
                    c_pos[0] = 'VERB'
                return str(c_pos[0]) + "-GEN"
            if c_pos[0] in main_pos or c_pos[0] == 'AUX':
                if c_pos[0] == 'AUX':
                    c_pos[0] = 'VERB'
            if opposite_num(o_feats[0], c_feats[0]):
                return str(c_pos[0]) + "-NUM"
            else:
                exceptions = (('है', 'हैं'), ('था', 'थे'), ('थी', 'थीं'), ('हुआ', 'हुए'), ('हुई', 'हुईं'),
                              ('रहा', 'रहे'), ('रही', 'रहीं'), ('चुका', 'चुके'), ('चुकी', 'चुकीं'),
                              ('लिया', 'लिए'), ('ली', 'लीं'), ('पाया', 'पाये'), ('पाया', 'पाए'), ('पायी', 'पायीं'),
                              ('गया', 'गए'), ('गयी', 'गई'), ('गया', 'गये'), ('गयीं', 'गईं'))
                exs_o = list(filter(lambda ex: o_toks[0].text in ex, exceptions))
                exs_c = list(filter(lambda ex: c_toks[0].text in ex, exceptions))
                if len(exs_o) != 0 and len(exs_c) != 0:
                    if set.intersection(set(exs_o), set(exs_c)):
                        return "VERB-NUM"

            if opposite_tense(o_feats[0], c_feats[0]):
                print("TENSE 1.1")
                return "VERB-TENSE"

        # Single token replacement of a word with a upos tag of NOUN, different lemma
        if o_pos[0]==c_pos[0]=="VERB" and o_toks[0].lemma != c_toks[0].lemma:
            print("Here, diff lemma")
            exceptions_tense = (
                ('है', 'था', 'होगा'), ('हैं', 'थे', 'होंगे'), ('है', 'थी', 'होगी'), ('हैं', 'थीं', 'होंगी'),
                ('हो', 'थे', 'होगे'), ('हूँ', 'था', 'होंगा'), ('गया', 'जाएगा'), ('गए', 'जाएँगे'), ('गयी', 'जाएगी'),
                ('गयीं', 'जाएँगी'),
                ('गई', 'जाएगी'), ('गईं', 'जाएँगी'), ('गया', 'जाऊँगा'))
            exs_o_tense = list(filter(lambda ex: o_toks[0].text in ex, exceptions_tense))
            exs_c_tense = list(filter(lambda ex: c_toks[0].text in ex, exceptions_tense))
            # print(exs_o_tense, exs_c_tense)
            if len(exs_o_tense) != 0 and len(exs_c_tense) != 0:
                if set.intersection(set(exs_o_tense), set(exs_c_tense)):
                    print("TENSE 1.2 c_pos[0] == VERB and o_toks[0].lemma != c_toks[0].lemma")
                    return "VERB-TENSE"

            # checking if stem is same but suffixes indicate change in tense
            if are_stems_similar(o_stem, c_stem) and opposite_tense(o_feats[0], c_feats[0]):
                print("TENSE 1.3 c_pos[0] == VERB and o_toks[0].lemma != c_toks[0].lemma")
                return "VERB-TENSE"
            return "VERB"
        # if c_pos[0] == "CONJ":
        #     return "CONJ"
        if o_pos in ["ADJ", "NUM"] and c_pos[0] in ["ADJ", "NUM"]:
            return "ADJ"
        char_ratio = Levenshtein.ratio(o_toks[0].text, c_toks[0].text)
        if o_pos[0] == 'NOUN' and c_pos[0] == 'NOUN' and char_ratio >= 0.5 and opposite_gen(o_feats[0], c_feats[0]):
            return "NOUN-GEN"
        if (c_pos[0] in list_pos or c_pos[0]=="AUX") and o_pos[0] == c_pos[0] and not opposite_tense(o_feats[0],c_feats[0]):
            # hai -> hoon
            print("I am here")
            print("o_pos[0]",o_pos[0],"c_pos[0]",c_pos[0])
            if(c_pos[0]=="AUX"):
                c_pos[0] = "VERB"
            if c_pos[0]=="VERB" and ((o_toks[0].lemma == c_toks[0].lemma) or (are_stems_similar(o_stem,c_stem))) :
                return "VERB-FORM"
            return c_pos[0]
        if o_toks[0].deprel == "punct" and c_toks[0].deprel == "punct":
            return "PUNCT"
        print("Morpho reached")
        # 3. MORPHOLOGY
        if o_toks[0].lemma == c_toks[0].lemma:
            print("Same lemma ")
            # Same POS on both sides
            if o_pos[0] == c_pos[0]:
                if o_pos[0] in ("VERB"):
                    # Of what's left, TENSE errors normally involved VBD.
                    if o_toks[0].xpos == "VBD" or c_toks[0].xpos == "VBD":
                        s = "if o_toks[0].tag_ == \"VBD\" or c_toks[0].tag_ == \"VBD\":"
                        # print(s)
                        print("TENSE 1.4")
                        return "VERB-TENSE"
                    # Any remaining aux verbs are called TENSE.
                    if o_dep[0].startswith("aux") and \
                            c_dep[0].startswith("aux") and not opposite_gen(o_feats[0], c_feats[0]) \
                            and not opposite_num(o_feats[0], c_feats[0]):
                        s = "same lemma if o_dep[0].startswith(\"aux\") and \
                            c_dep[0].startswith(\"aux\"):"
                        print(s)
                        exceptions = (('है', 'हैं'), ('था', 'थे', 'थी', 'थीं'), ('हुआ', 'हुई', 'हुए', 'हुईं'),
                                      ('रहा', 'रहे', 'रही', 'रहीं', 'रहो'), ('चुका', 'चुके', 'चुकी', 'चुकीं'),
                                      ('लिया', 'लिए', 'ली', 'लीं'), ('पाया', 'पाए', 'पायी', 'पायीं'),
                                      ('गया', 'गयी', 'गई', 'गए', 'गये', 'गयीं', 'गईं'))
                        exs_o = list(filter(lambda ex: o_toks[0].text in ex, exceptions))
                        exs_c = list(filter(lambda ex: c_toks[0].text in ex, exceptions))
                        if (len(exs_o) == 0 and len(exs_c) == 0) or exs_o != exs_c:
                            print("TENSE 1.5")
                            return "VERB-TENSE"
            if c_toks[0].xpos == "VBD":
                s = "c_toks[0].tag_ == \"VBD\""
                # print(s)
                print("TENSE 1.6")
                return "VERB-TENSE"

        # 4. GENERAL
        # Auxiliaries with different lemmas
        # Also checking that stems are not similar
        if (o_toks[0].lemma != c_toks[0].lemma and not are_stems_similar(o_stem, c_stem)) and o_dep[0].startswith("aux") and c_dep[0].startswith("aux"):
            s = "if o_dep[0].startswith(\"aux\") and c_dep[0].startswith(\"aux\"):"
            # print(s)
            if not opposite_gen(o_feats[0], c_feats[0]) and not opposite_num(o_feats[0], c_feats[0]):
                print("Tokens", o_toks[0], c_toks[0])
                if (is_tense_aux(o_toks[0],c_toks[0])):
                    print("TENSE 1.7")
                    return "VERB-TENSE"

        if (o_toks[0].lemma == c_toks[0].lemma or are_stems_similar(o_stem, c_stem)) and \
                o_pos[0] in morph_list and \
                c_pos[0] in morph_list:
            return "MORPH"

    # Multi-token replacements (uncommon)
    # All auxiliaries    
    if len(o_toks)+len(c_toks) > 2:
        if set(o_dep + c_dep).issubset({"aux", "aux:pass"}):
            # print("Hello")
            s = "if set(o_dep+c_dep).issubset({\"aux\", \"aux:pass\"}): and o_gen = c_gen"
            # print(s)
            if set(o_gen) == set(c_gen) and set(o_num) == set(c_num):
                if not opposite_gen(o_feats[0], c_feats[0]) and not opposite_num(o_feats[0], c_feats[0]):
                    print("Tokens", o_toks[0], c_toks[0])
                    if (is_tense_aux(o_toks[0],c_toks[0])):
                        print("TENSE 1.8")
                        return "VERB-TENSE"
    # All same POS
    # print("POS tags",o_pos + c_pos)
    # print(o_toks[0].lemma,c_toks[0].lemma)
    # print(not(opposite_gen(o_feats[0], c_feats[0])))
    # print(not(opposite_num(o_feats[0],c_feats[0])))
    if(len(o_toks)+len(c_toks)>2):
        if len(set(o_pos + c_pos)) <= 2 and set(o_pos + c_pos).issubset({"VERB", "AUX"}):
            print("len(set(o_pos + c_pos)) <= 2")
            # Final verbs with the same lemma are tense; e.g. eat -> has eaten
            if o_pos[0] in ("VERB", "AUX") and \
                    (o_toks[0].lemma == c_toks[0].lemma or are_stems_similar(o_stem, c_stem)) \
                    and not opposite_gen(o_feats[0], c_feats[0]) \
                    and not opposite_num(o_feats[0], c_feats[0]):
                s = "if len(set(o_pos+c_pos)) == 1:," + "if o_pos[0] == VERB and o_toks[0].lemma == c_toks[0].lemma:"
                print(s)
                print("TENSE 1.9")
                return "VERB-TENSE"

    if len(o_toks)+len(c_toks) > 2:
        for i in range(len(o_toks)):
            if o_pos[i] == "NOUN":
                for j in range(len(c_pos)):
                    if c_pos[j] == "NOUN":
                        if o_toks[i].lemma == c_toks[j].lemma and opposite_num(o_feats[i], c_feats[j]):
                            return "NOUN-NUM"
                        char_ratio = Levenshtein.ratio(o_toks[0].text, c_toks[0].text)
                        if char_ratio >= 0.5 and opposite_gen(o_feats[i], c_feats[j]):
                            return "NOUN-GEN"
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "NOUN"
        for i in range(len(o_toks)):
            if o_pos[i] in ["PRON", "NOUN"]:
                for j in range(len(c_pos)):
                    if c_pos[j] == "PRON":
                        if o_toks[i].lemma == c_toks[j].lemma and opposite_gen(o_feats[i], c_feats[j]):
                            return "PRON-GEN"
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "PRON"
        for i in range(len(o_toks)):
            if o_pos[i] in ("VERB", "AUX"):
                for j in range(len(c_pos)):
                    if c_pos[j] == o_pos[i]:
                        if o_toks[i].lemma == c_toks[j].lemma and opposite_gen(o_feats[i], c_feats[j]):
                            # print("i =", "j =", i, j, o_toks[i], c_toks[j], o_feats[i], c_feats[j])
                            # print("ling")
                            return "VERB-GEN"
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "VERB"
        for i in range(len(o_toks)):
            if o_pos[i] == "ADP":
                for j in range(len(c_pos)):
                    if c_pos[j] == "ADP":
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "ADP"
        for i in range(len(o_toks)):
            if o_pos[i] == "ADV":
                for j in range(len(c_pos)):
                    if c_pos[j] == "ADV":
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "ADV"
        for i in range(len(o_toks)):
            if o_pos[i] == "PREP":
                for j in range(len(c_pos)):
                    if c_pos[j] == "PREP":
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "PREP"
        for i in range(len(o_toks)):
            if o_pos[i] == "DET":
                for j in range(len(c_pos)):
                    if c_pos[j] == "DET":
                        if o_toks[i].lemma != c_toks[j].lemma:
                            return "DET"
    return "OTHER"