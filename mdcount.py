import re
import sys
import string
from optparse import OptionParser

def main():
    parser = OptionParser(usage ="Markdown Count, author: Ryan Riley, description: simple word counter customized for makdown syntax -- Does not count block quotes, citations, non-words, or code. Need to provide a file to count. Eg. type on the command line: mdcount.py <your filename>", version ="%prog 1.0")
    parser.add_option('-c', '--cut', help='Ends word counted at at specified name of words cited section, eg. "Citations" This option is case sensitive and assumes that the line begins with "#". To use this option, on the command line, type mdcount.py <your filename> -c <name of your works cited section>', dest='cut', action='store_true') 

    (opts, args) = parser.parse_args()
    if len(args)==0:
        parser.print_help()
        exit(-1)
    filename = args[0]
    findQuotes = re.compile(r"^>\w*.*",re.MULTILINE)
    with open(filename, 'r') as f:
        if opts.__dict__["cut"]:
            removeCitations = re.split(r"#.*"+args[1],f.read())
            removeBlockQuotes = reduce(lambda x, y: x + y, findQuotes.split(removeCitations[0]))
        else:  
            removeBlockQuotes = reduce(lambda x, y: x + y, findQuotes.split(f.read()))
        removeCode =reduce(lambda x, y: x + y, map(lambda x: re.split(r"~+", removeBlockQuotes)[x], filter(lambda i: i % 2 == 0, range(len(re.split(r"~+", removeBlockQuotes))))))                          
        wordCount = len(re.findall(r"\S?\w+\S?\w*", removeCode))
    print "word count of {}: {}".format(filename, wordCount)
    f.close()
                
                
if __name__== '__main__':
    main()

