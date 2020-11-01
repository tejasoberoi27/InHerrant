from re import sub
s_str = sub("['-]", "", "".join([tok.text for tok in o]))