from pathlib import Path
import Levenshtein


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
        print("e is",e)
        print("Word is",Word)
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
    # o_set = sorted([o.text.lower for o in o_toks])
    # c_set = sorted([c.text.lower for c in c_toks])
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
        if k in cset and oset[k]==cset[k]:
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
    print("Type", type(toks[0]))
    print(toks[0])
    if len(toks) == 1:
        if toks[0].pos == "NOUN":
            return "NOUN"
        if toks[0].pos == "PRON":
            return "PRON"
        if toks[0].pos == "VERB":
            return "VERB"
        if toks[0].pos == "ADP":
            return "ADP"
        if toks[0].pos in ["ADJ", "NUM"]:
            return "ADJ"
        if toks[0].deprel == "punct":
            return "PUNCT"
    if "NOUN" in pos:
        return "NOUN"
    if "VERB" in pos:
        return "VERB"
    if "PRON" in pos:
        return "PRON"
    if "ADJ" in pos:
        return "ADJ"
    if "ADP" in pos:
        return "ADP"
    else:
        return "OTHER"
        # Possessive noun suffixes; e.g. ' -> 's


# Input: Spacy tokens
# Output: A list of pos and dep tag strings
def get_edit_info(toks):
    pos = []
    dep = []
    for tok in toks:
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


# Input 1: Spacy orig tokens
# Input 2: Spacy cor tokens
# Output: An error type string based on orig AND cor
def get_two_sided_type(o_toks, c_toks):
    o_toks = [tok.words[0] for tok in o_toks]
    c_toks = [tok.words[0] for tok in c_toks]

    # Extract pos tags and parse info from the toks as lists
    o_pos, o_dep = get_edit_info(o_toks)
    c_pos, c_dep = get_edit_info(c_toks)

    o_feats = [get_feats(o_toks[0]) for tok in o_toks]
    c_feats = [get_feats(c_toks[0]) for tok in c_toks]

    # Orthography; i.e. whitespace and/or case errors.
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
            # Check if both sides have a common lemma
            if o_toks[0].lemma == c_toks[0].lemma:
                # Inflection; often count vs mass nouns or e.g. got vs getted
                if o_pos == c_pos and o_pos[0] in {"NOUN", "VERB"}:
                    return o_pos[0] + ":INFL"
                # Unknown morphology; i.e. we cannot be more specific.
                else:
                    return "MORPH"
            # Use string similarity to detect true spelling errors.
            else:
                char_ratio = Levenshtein.ratio(o_toks[0].text, c_toks[0].text)
                # Ratio > 0.5 means both side share at least half the same chars.
                # WARNING: THIS IS AN APPROXIMATION.
                if char_ratio > 0.5:
                    return "SPELL"
                # If ratio is <= 0.5, the error is more complex e.g. tolk -> say
                else:
                    # If POS is the same, this takes precedence over spelling.
                    if o_pos == c_pos and \
                            o_pos[0] not in rare_pos:
                        return o_pos[0]
                    # Tricky cases.
                    else:
                        return "OTHER"

        # 1. SPECIAL CASES
        # Possessive noun suffixes; e.g. ' -> 's

        # Gender Edits
        if c_toks[0].pos in main_pos and o_toks[0].lemma == c_toks[0].lemma and o_feats[0]['Gender'] != c_feats[0][
            'Gender']:
            return str(c_toks[0].pos) + "-GEN"
        # Single token replacement of a word with a upos tag of NOUN, different lemma
        if c_toks[0].pos == "NOUN" and o_toks[0].lemma != c_toks[0].lemma:
            return "NOUN"
        if c_toks[0].pos == "NOUN" and o_toks[0].lemma == c_toks[0].lemma and o_feats[0]['Number'] != c_feats[0][
            'Number']:
            return "NOUN-NUM"
        if c_toks[0].pos == "PRON":
            return "PRON"
        if o_toks[0].pos == "NOUN" and c_toks[0].pos == "PRON":  # unnecessary
            return "PRON"
        if c_toks[0].pos == "VERB" and o_toks[0].lemma != c_toks[0].lemma:
            return "VERB"
        if o_toks[0].pos == "NOUN" and c_toks[0].pos == "VERB":
            return "VERB"
        if c_toks[0].pos in ["ADJ", "NUM"] and o_toks[0].lemma != c_toks[0].lemma:
            return "ADJ"
        # Single token replacement, substituting a PRON with a ADJ
        # (might generalise to any POS tag being replaced with ADJ)
        if o_toks[0].pos != "ADJ" and c_toks[0].pos == "ADJ":
            return "ADJ"
        if c_toks[0].pos == "ADP":
            return "ADP"
        if o_toks[0].deprel == "punct" and c_toks[0].deprel == "punct":
            return "PUNCT"

    # Multi-token replacements (uncommon)
    for i in range(len(o_toks)):
        if o_toks[i].pos == "NOUN":
            for j in range(len(c_pos)):
                if c_toks[j].pos == "NOUN":
                    if o_toks[i].lemma == c_toks[j].lemma and o_feats[i]['Number'] != c_feats[j]['Number']:
                        return "NOUN-NUM"
                    if o_toks[i].lemma == c_toks[j].lemma and o_feats[i]['Gender'] != c_feats[j]['Gender']:
                        return "NOUN-GEN"
                    if o_toks[i].lemma != c_toks[j].lemma:
                        return "NOUN"
    for i in range(len(o_toks)):
        if o_toks[i].pos in ["PRON", "NOUN"]:
            for j in range(len(c_pos)):
                if c_toks[j].pos == "PRON":
                    if o_toks[i].lemma == c_toks[j].lemma and o_feats[i]['Gender'] != c_feats[j]['Gender']:
                        return "PRON-GEN"
                    if o_toks[i].lemma != c_toks[j].lemma:
                        return "PRON"
    for i in range(len(o_toks)):
        if o_toks[i].pos == "VERB":
            for j in range(len(c_pos)):
                if c_toks[j].pos == "VERB":
                    if o_toks[i].lemma == c_toks[j].lemma and o_feats[i]['Gender'] != c_feats[j]['Gender']:
                        return "VERB-GEN"
                    if o_toks[i].lemma != c_toks[j].lemma:
                        return "VERB"
    for i in range(len(o_toks)):
        if o_toks[i].pos == "ADP":
            for j in range(len(c_pos)):
                if c_toks[j].pos == "ADP":
                    if o_toks[i].lemma != c_toks[j].lemma:
                        return "ADP"
    # Tricky cases.
    else:
        return "OTHER"
