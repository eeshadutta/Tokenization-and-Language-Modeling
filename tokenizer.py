import sys
import re


def tokenize(filename):
    file = open(filename, "r")
    contents = file.read().split('\n')
    tokens = []
    for line in contents:
        if line != '':
            line.strip()
            tokens = tokens + line.split(" ")

    punc = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '-',
            '"', "'", '{', '}', '[', ']', '_', '+', '=']

    final_tokens = []
    for token in tokens:
        if re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', token):
            final_tokens.append(token)
        elif re.match('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', token):
            final_tokens.append(token)
        elif re.match('^([0-9]+)\.([0-9]+)$', token):
            final_tokens.append(token)
        elif re.match('^([0-9]+):([0-9]+)$', token) or re.match('^([0-9]+)/([0-9]+)$', token):
            final_tokens.append(token)
        elif re.match('^#([a-zA-Z0-9_\-\.]+)$', token):
            final_tokens.append(token)
        elif re.match('^@([a-zA-Z0-9_\-\.]+)$', token):
            final_tokens.append(token)
        elif re.match('^[AaPp]\.[Mm]\.', token):
            final_tokens.append(token)
        else:
            token_list = re.sub(
                r'[]!"$%&()+,./:;=?[\\^_`{|}~-]+', r' \g<0> ', token).strip().split(' ')
            for t in token_list:
                if re.match('.[\w].', t):
                    for s in t:
                        if s in punc:
                            t1 = t.split(s, 1)[0]
                            t2 = t.split(s, 1)[1]
                            if t1 != '':
                                final_tokens.append(t1)
                            final_tokens.append(s)
                            t = t2
                if t != '':
                    final_tokens.append(t)

    return final_tokens


filename = sys.argv[1]
final_tokens = tokenize(filename)
for token in final_tokens:
    print(token)
