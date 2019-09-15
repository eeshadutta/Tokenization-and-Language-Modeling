import sys
import re


def tokenize(filename):
    contents = [line.rstrip() for line in open(filename, 'r')]
    init_tokens = [line.split(" ") for line in contents if line != '']
    tokens = [item for sublist in init_tokens for item in sublist]

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
        elif re.match('^[AaPp]\.?[Mm]\.?$', token):
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


def tokenize_line(line):
    if line[-1] == '.' and (line[-2] != ' ' or line[-2] != '.'):
        line = line.rsplit(".", 1)[0]
        line = line + " ."
    tokens = []
    final_tokens = []
    punc = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '-',
            '"', "'", '{', '}', '[', ']', '_', '+', '=']
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
        elif re.match('^([0-9]+):([0-9]+)', token) or re.match('^([0-9]+)/([0-9]+)$', token):
            final_tokens.append(token)
        elif re.match('^#([a-zA-Z0-9_\-\.]+)$', token):
            final_tokens.append(token)
        elif re.match('^@([a-zA-Z0-9_\-\.]+)$', token):
            final_tokens.append(token)
        elif re.match('^[AaPp]\.?[Mm]\.?$', token):
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
# Clean tokenize - one token on each line
# final_tokens = tokenize(filename)
# tokenized_file = filename.split(".")[0] + "_cleantokenized.txt"
# op = open(tokenized_file, "w")
# for token in final_tokens:
#     op.write(token + "\n")
# op.close()


# Tokenize - one line on each line
contents = [line.rstrip() for line in open(filename, 'r')]
# tokenized_file = filename.split(".")[0] + "_linetokenized.txt"
# op = open(tokenized_file, 'w')
for line in contents:
    if line != '':
        tokens = tokenize_line(line)
        st = ''
        for token in tokens:
            st = st + " " + token
        st = st.strip()
        print(st)
