import sys
import re


def tokenize_line(line):
    tokens = []
    final_tokens = []
    punc = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '-',
            '"', "'", '{', '}', '[', ']', '_', '+', '=']

    if line != '':
        line.strip()
        line = '<s> ' + line + ' </s>'
        line.strip()
        tokens = line.split(" ")

    for token in tokens:
        if token == '<s>' or token == '</s>':
            final_tokens.append(token)
        elif re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', token):
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
        elif re.match('^[AaPp]\.?[Mm]\.?', token):
            if re.match('^([0-9]+)$', final_tokens[len(final_tokens) - 1]):
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


def ngrams(filename, n):
    f = open(filename, 'r')
    contents = f.read().lower().split('\n')
    list_ngrams = []
    for line in contents:
        tokens = tokenize_line(line)
        words = ''
        try:
            counts = {}
            for i in range(0, n):
                words = words + ' ' + tokens[i]
            words = words.strip()
            list_ngrams.append(words)
            for i in range(n, len(tokens)):
                words = words.split(' ', 1)[1]
                words = words + ' ' + tokens[i]
                words = words.strip()
                list_ngrams.append(words)
        except:
            pass

    for ng in list_ngrams:
        if ng in counts:
            counts[ng] += 1
        else:
            counts[ng] = 1

    counts_final = sorted(
        counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    for c in counts_final:
        print(c[0], ":", c[1])
    return counts_final


n = 4
filename = sys.argv[1]
counts_final = ngrams(filename, n)

out_file = filename + "_" + n + "grams.txt"
of = open(out_file, 'w')
for c in counts_final:
    of.write(c[0] + " : " + c[1])
