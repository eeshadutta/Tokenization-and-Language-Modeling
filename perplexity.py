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


def perplexity(line, n, ngram_counts):
    tokens = tokenize_line(line)
    length = len(tokens)
    words = ''
    list_ngrams = []

    for i in range(0, n):
        words = words + ' ' + tokens[i]
    words = words.strip()
    list_ngrams.append(words)
    for i in range(n, len(tokens)):
        words = words.split(' ', 1)[1]
        words = words + ' ' + tokens[i]
        words = words.strip()
        list_ngrams.append(words)

    total_prob = 1.0
    for ng in list_ngrams:
        num = 0
        den = 0
        w = ng.split(' ')
        for present_ng in ngram_counts:
            ww = present_ng[0].strip().split(' ')
            if w[:(n-1)] == ww[:(n-1)]:
                den += 1
            if w == ww:
                num += 1
        if num != 0 and den != 0:
            total_prob = total_prob * num / den

    perp = 1 / total_prob
    perp = perp**(float(1/length))

    return perp


def calculate_perplexity_file(filename, n, ngram_counts):
    file = open(filename, 'r')
    contents = file.read().split('\n')
    for line in contents:
        # try:
        perp = perplexity(line, n, ngram_counts)
        print(line, ":", perp)
        # except:
        # pass


n = 4

ngrams_file = "corpus1_4grams.txt"
f = open(ngrams_file, 'r')
contents = f.read().split('\n')
ngram_counts = []
for line in contents:
    if line != '':
        c = line.rsplit(":", 1)[1]
        ng = line.rsplit(":", 1)[0]
        ngram_counts.append((ng, c))

calculate_perplexity_file(sys.argv[1], n, ngram_counts)
