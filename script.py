import os
import subprocess

files = ['xaa', 'xab', 'xac', 'xad', 'xae', 'xaf', 'xag', 'xah', 'xai', 'xaj', 'xak', 'xal', 'xam', 'xan', 'xao',
         'xap', 'xaq', 'xar', 'xas', 'xat', 'xau', 'xav', 'xaw', 'xax', 'xay', 'xaz', 'xba', 'xbb', 'xbc', 'xbd']

for f in files:
    os.system("python3 tokenizer.py " + f)
    print("Tokenized", f)

for f in files:
    os.system("python3 zipf.py " + f + "_tokenized.txt")
    print("Zipf graph", f)
