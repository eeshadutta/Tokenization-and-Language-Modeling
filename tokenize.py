import sys
import re


file = open(sys.argv[1], "r")
contents = file.read().split('\n')
tokens = []
for line in contents:
    if line != '':
        line.strip()
        tokens = tokens + line.split(" ")

punc = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '-', '"', "'", '{', '}', '[', ']', '_', '+', '=']

final_tokens = []
for token in tokens:
    if re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', token):
        final_tokens.append(token)
    # ^(?:http:\/\/|https:\/\/)?[\w.\-]+(?:\.[\w\-]+)+[\w\-.,@?^=%&:;/~\\+#]+$ : also for url
    elif re.match('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', token):
        final_tokens.append(token)
    elif re.match('^([0-9]+)\.([0-9]+)$', token):
        final_tokens.append(token)
    elif re.match('^#([a-zA-Z0-9_\-\.]+)$', token):
        final_tokens.append(token)
    elif re.match('^@([a-zA-Z0-9_\-\.]+)$', token):
        final_tokens.append(token)
    elif re.match('^[AaPp]\.?[Mm]\.?', token):
        final_tokens.append(token)
    else:
        if re.match('(.*\.)+.*', token):
            token1 = token.split('.', 1)[0]
            token2 = token.rsplit('.', 1)[1]
            if token1 != '':
                final_tokens.append(token1)
            punc_token = token.replace(token1, '').replace(token2, '')
            final_tokens.append(punc_token)
            if token2 != '':
                final_tokens.append(token2)
        elif re.match('(.*\!)+(\?)+.*', token):
            token1 = token.split('!', 1)[0]
            token2 = token.rsplit('?', 1)[1]
            if token1 != '':
                final_tokens.append(token1)
            punc_token = token.replace(token1, '').replace(token2, '')
            final_tokens.append(punc_token)
            if token2 != '':
                final_tokens.append(token2)
        elif re.match('(.*\!)+.*', token):
            token1 = token.split('!', 1)[0]
            token2 = token.rsplit('!', 1)[1]
            if token1 != '':
                final_tokens.append(token1)
            punc_token = token.replace(token1, '').replace(token2, '')
            final_tokens.append(punc_token)
            if token2 != '':
                final_tokens.append(token2)
        elif re.match('(.*\?)+.*', token):
            token1 = token.split('?', 1)[0]
            token2 = token.rsplit('?', 1)[1]
            if token1 != '':
                final_tokens.append(token1)
            punc_token = token.replace(token1, '').replace(token2, '')
            final_tokens.append(punc_token)
            if token2 != '':
                final_tokens.append(token2)
        else:
            for s in token:
                if s in punc:
                    token1 = token.split(s, 1)[0]
                    token2 = token.split(s, 1)[1]
                    if token1 != '':
                        final_tokens.append(token1)
                    final_tokens.append(s)
                    token = token2
            if token != '':
                final_tokens.append(token)
                

for token in final_tokens:
    print(token)