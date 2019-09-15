import sys
import re


def tokenize_line(line):
    # if line[-1] == '.' and (line[-2] != ' ' or line[-2] != '.'):
    #     line = line.rsplit(".", 1)[0]
    #     line = line + " ."
    tokens = []
    final_tokens = []
    punc = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '-',
            '"', "'", '{', '}', '[', ']', '_', '+', '=']

    if line != '':
        line.strip()
        line = '<s> ' + line + ' </s>'
        line = line.strip().lower()
        tokens = line.split(" ")

    for token in tokens:
        if token == '<s>' or token == '</s>':
            final_tokens.append(token)
        elif re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', token):
            final_tokens.append(token)
        elif re.match('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', token):
            final_tokens.append(token)
        elif re.match('^([0-9]+)\.([0-9]+)', token):
            final_tokens.append(token)
        elif re.match('^([0-9]+):([0-9]+)$', token) or re.match('^([0-9]+)/([0-9]+)$', token):
            final_tokens.append(token)
        elif re.match('^#([a-zA-Z0-9_\-\.]+)$', token):
            final_tokens.append(token)
        elif re.match('^@([a-zA-Z0-9_\-\.]+)$', token):
            final_tokens.append(token)
        elif re.match('^[AaPp]\.?[Mm]\.?$', token):
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
    contents = [line.rstrip() for line in open(filename, 'r')]
    list_ngrams = []
    nl = len(contents)
    print("Num lines", nl)
    for line in contents:
        # print(nl)
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
        # nl -= 1

    for ng in list_ngrams:
        if ng in counts:
            counts[ng] += 1
        else:
            counts[ng] = 1

    counts_final = sorted(
        counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return counts_final


n = 4
filename = sys.argv[1]
counts_final = ngrams(filename, n)

out_file = filename.split(".")[0] + "_" + str(n) + "grams.txt"
of = open(out_file, 'w')
tot = len(counts_final)
print("Num ngrams", tot)
for c in counts_final:
    print(tot)
    # print(tot, "::::", c[0], ":", c[1])
    of.write(c[0] + " : " + str(c[1]) + "\n")
    # print(c[0], c[1])
    tot -= 1
