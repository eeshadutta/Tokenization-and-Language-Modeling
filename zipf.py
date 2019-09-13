import sys
import re
import matplotlib.pyplot as plt


# def tokenize(filename):
#     file = open(filename, "r")
#     contents = file.read().split('\n')
#     tokens = []
#     for line in contents:
#         if line != '':
#             line.strip()
#             tokens = tokens + line.split(" ")

#     punc = ['(', ')', '?', ':', ';', ',', '.', '!', '/', '-',
#             '"', "'", '{', '}', '[', ']', '_', '+', '=']

#     final_tokens = []
#     for token in tokens:
#         if re.match('^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$', token):
#             final_tokens.append(token)
#         elif re.match('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', token):
#             final_tokens.append(token)
#         elif re.match('^([0-9]+)\.([0-9]+)$', token):
#             final_tokens.append(token)
#         elif re.match('^([0-9]+):([0-9]+)$', token) or re.match('^([0-9]+)/([0-9]+)$', token):
#             final_tokens.append(token)
#         elif re.match('^#([a-zA-Z0-9_\-\.]+)$', token):
#             final_tokens.append(token)
#         elif re.match('^@([a-zA-Z0-9_\-\.]+)$', token):
#             final_tokens.append(token)
#         elif re.match('^[AaPp]\.[Mm]\.', token):
#             final_tokens.append(token)
#         else:
#             token_list = re.sub(
#                 r'[]!"$%&()+,./:;=?[\\^_`{|}~-]+', r' \g<0> ', token).strip().split(' ')
#             for t in token_list:
#                 if re.match('.[\w].', t):
#                     for s in t:
#                         if s in punc:
#                             t1 = t.split(s, 1)[0]
#                             t2 = t.split(s, 1)[1]
#                             if t1 != '':
#                                 final_tokens.append(t1)
#                             final_tokens.append(s)
#                             t = t2
#                 if t != '':
#                     final_tokens.append(t)

#     return final_tokens


# filename = sys.argv[1]
# final_tokens = tokenize(filename)
# counts = {}
# for token in final_tokens:
#     if token in counts:
#         counts[token] += 1
#     else:
#         counts[token] = 1

# counts_list = []
# for c in counts:
#     counts_list.append(counts[c])
# counts_list.sort(reverse=True)
# num = len(counts_list)
# x = []
# for i in range(1, num+1):
#     x.append(i)
# plt.scatter(x, counts_list)
# plt.title("Zipf graph of " + filename)
# # plt.show()
# plt.savefig("zipf.png")

def zipf_graph(tokens, filename):
    counts = {}
    for token in tokens:
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1

    distinct_counts = set()
    for c in counts:
        distinct_counts.add(counts[c])

    counts_list = sorted(distinct_counts, reverse=True)
    num = len(counts_list)
    x = [i for i in range(1, num+1)]
    plt.scatter(x, counts_list)
    plt.xlabel("Rank")
    plt.ylabel("Frequency")
    plt.savefig(filename + "_zipf.png")


tokenized_file = sys.argv[1]
tokens = [line.rstrip() for line in open(tokenized_file, 'r')]
zipf_graph(tokens, tokenized_file.split("_")[0])
