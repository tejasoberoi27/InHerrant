from pathlib import Path
import Levenshtein


def get_gen(feats):

    if 'Gender' in feats:
        return feats['Gender']
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


def opposite_num(o_feats,c_feats):
    """ Returns true if one of the tokens is singular and other plural"""
    if not o_feats or not c_feats:
        return False
    else:
        if {'Sing', 'Plur'}.issubset({get_num(o_feats), get_num(c_feats)}):
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
    except Exception as e:
        print("e is", e)
        print("Word is", Word)
    return feats


# Input 1: Spacy orig tokens
# Input 2: Spacy cor tokens
# Output: Boolean; the difference between orig and cor is only whitespace
def only_orth_change(o_toks, c_toks):
    o_join = "".join([o.text for o in o_toks])
    c_join = "".join([c.text for c in c_toks])
    if o_join == c_join:
        return True
    return False


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
        print("POS", tok.pos)
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
main_pos = ['NOUN', 'PRON', 'VERB', 'ADJ']
spell = load_word_list(base_dir / "resources" / "vocab.txt")
rare_pos = {"INTJ", "NUM", "SYM", "X"}
open_pos2 = {"ADJ", "ADV", "NOUN", "VERB"}
list_pos = ['NOUN', 'PRON', 'VERB', 'ADJ', 'ADP', 'ADV', 'PREP', 'DET','CONJ']


# Input 1: Stanza orig tokens
# Input 2: Stanza cor tokens
# Output: An error type string based on orig AND cor
def get_two_sided_type(o_toks, c_toks):
    o_toks = [tok.words[0] for tok in o_toks]
    c_toks = [tok.words[0] for tok in c_toks]
    print("Hello", o_toks, c_toks)

    # Extract pos tags and parse info from the toks as lists
    o_pos, o_dep = get_edit_info(o_toks)
    c_pos, c_dep = get_edit_info(c_toks)

    o_feats = [get_feats(o_toks[0]) for tok in o_toks]
    c_feats = [get_feats(c_toks[0]) for tok in c_toks]

    o_gen = [get_gen(o_feats[i]) for i in range(len(o_feats))]
    c_gen = [get_gen(c_feats[i]) for i in range(len(c_feats))]

    o_num = [get_num(o_feats[i]) for i in range(len(o_feats))]
    c_num = [get_num(c_feats[i]) for i in range(len(c_feats))]

    # Orthography; i.e. whitespace errors.
    if only_orth_change(o_toks, c_toks):
        return "ORTH"
    # Word Order; only matches exact reordering.
    if exact_reordering(o_toks, c_toks):
        return "WO"

    # 1:1 replacements (very common)
    if len(o_toks) == len(c_toks) == 1:

        # 2. SPELLING AND INFLECTION
        # Spelling errors take precedence over POS errors; this rule is ordered
        # Check a GB English dict for both orig and lower case.
        # E.g. "cat" is in the dict, but "Cat" is not.
        if o_toks[0].text not in spell:
            char_ratio = Levenshtein.ratio(o_toks[0].text, c_toks[0].text)
            print("Character Ratio ", char_ratio)
            # Ratio > 0.5 means both side share at least half the same chars.
            # WARNING: THIS IS AN APPROXIMATION.
            if char_ratio >= 0.5:
                return "SPELL"
            # If ratio is < 0.5, the error is more complex e.g. tolk -> say
            else:
                # If POS is the same, this takes precedence over spelling.
                if o_pos[0] == c_pos[0] and \
                        o_pos[0] in list_pos:
                    print("o_pos" + o_pos[0])
                    return o_pos[0]
                # Tricky cases.
                else:
                    return "OTHER"

        # 1. SPECIAL CASES

        # Gender Edits
        # if the edit has both tense and gender different, then classify as gender edit
        if (c_pos[0] in main_pos or c_pos[0] == 'AUX') and o_toks[0].lemma == c_toks[0].lemma \
                and opposite_gen(o_feats[0], c_feats[0]) and c_pos[0] != "NOUN":
            if c_pos[0] == 'AUX':
                c_pos[0] = 'VERB'
            return str(c_pos[0]) + "-GEN"
        if (c_pos[0] in main_pos or c_pos[0] == 'AUX') and o_toks[0].lemma == c_toks[0].lemma \
                and opposite_num(o_feats[0], c_feats[0]):
            if c_pos[0] == 'AUX':
                c_pos[0] = 'VERB'
            return str(c_pos[0]) + "-NUM"
        # Single token replacement of a word with a upos tag of NOUN, different lemma
        if c_pos[0] == "VERB" and o_toks[0].lemma != c_toks[0].lemma:
            return "VERB"
        if  c_pos[0] == "CONJ":
            return "CONJ"
        if c_pos[0] in ["ADJ", "NUM"]:
            return "ADJ"
        char_ratio = Levenshtein.ratio(o_toks[0].text, c_toks[0].text)
        if c_pos[0] == 'NOUN' and char_ratio >= 0.5 and opposite_gen(o_feats[0], c_feats[0]):
            return "NOUN-GEN"
        if c_pos[0] in list_pos:
            return c_pos[0]
        if o_toks[0].deprel == "punct" and c_toks[0].deprel == "punct":
            return "PUNCT"

        # 3. MORPHOLOGY
        if o_toks[0].lemma == c_toks[0].lemma:
            # Same POS on both sides
            if o_pos[0] == c_pos[0]:

                if o_pos[0] == "VERB":

                    # Of what's left, TENSE errors normally involved VBD.
                    if o_toks[0].xpos == "VBD" or c_toks[0].xpos == "VBD":
                        s = "if o_toks[0].tag_ == \"VBD\" or c_toks[0].tag_ == \"VBD\":"
                        print(s)
                        return "VERB-TENSE"
                    # Any remaining aux verbs are called TENSE.
                    if o_dep[0].startswith("aux") and \
                            c_dep[0].startswith("aux") and not opposite_gen(o_feats[0], c_feats[0]) \
                            and not opposite_num(o_feats[0],c_feats[0]):
                        s = "same lemma if o_dep[0].startswith(\"aux\") and \
                            c_dep[0].startswith(\"aux\"):"
                        print(s)
                        return "VERB-TENSE"
            if c_toks[0].xpos == "VBD":
                s = "c_toks[0].tag_ == \"VBD\""
                print(s)
                return "VERB-TENSE"

        # 4. GENERAL
        # Auxiliaries with different lemmas
        if o_dep[0].startswith("aux") and c_dep[0].startswith("aux"):
            s = "if o_dep[0].startswith(\"aux\") and c_dep[0].startswith(\"aux\"):"
            print(s)
            print("O_FEATS",o_feats[0])
            print("C_FEATS",c_feats[0])
            if not opposite_gen(o_feats[0], c_feats[0]) and not opposite_num(o_feats[0],c_feats[0]):
                return "VERB-TENSE"

    # Multi-token replacements (uncommon)

    if set(o_dep + c_dep).issubset({"aux", "aux:pass"}):
        s = "if set(o_dep+c_dep).issubset({\"aux\", \"aux:pass\"}): and o_gen = c_gen"
        print(s)
        if set(o_gen) == set(c_gen) and set(o_num) == set(c_num):
            return "VERB-TENSE"
    # All same POS
    if len(set(o_pos + c_pos)) <= 2 and ("VERB" in set(o_pos + c_pos) or "AUX" in set(o_pos + c_pos)):
        # Final verbs with the same lemma are tense; e.g. eat -> has eaten
        if o_pos[0] == "VERB" and \
                o_toks[0].lemma == c_toks[0].lemma and not opposite_gen(o_feats[0], c_feats[0])\
                and not opposite_num(o_feats[0],c_feats[0]):
            s = "if len(set(o_pos+c_pos)) == 1:," + "if o_pos[0] == VERB and o_toks[0].lemma == c_toks[0].lemma:"
            print(s)
            return "VERB-TENSE"

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
                    if o_toks[i].lemma == c_toks[j].lemma and opposite_gen(o_feats[i],c_feats[j]):
                        return "PRON-GEN"
                    if o_toks[i].lemma != c_toks[j].lemma:
                        return "PRON"
    for i in range(len(o_toks)):
        if o_pos[i] in ("VERB","AUX"):
            for j in range(len(c_pos)):
                if c_pos[j] == o_pos[i]:
                    if o_toks[i].lemma == c_toks[j].lemma and opposite_gen(o_feats[i],c_feats[j]):
                        # print("i =", "j =", i, j, o_toks[i], c_toks[j], o_feats[i], c_feats[j])
                        print("ling")
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
    # Tricky cases.
    else:
        return "OTHER"
