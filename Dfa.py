import re

from os.path import abspath
from sys import argv


class DFA:

    class Rules:
        
        def __init__(self, path_to_rules):
            rules = load_language(path_to_rules)
            self.language = list()
            self.states = list()
            
        def _load_rules(rule_file):
            rules = {}
            rule_file = abspath(rule_file)
            with f as open(rule_file, 'r'):
                lang = f.readline()
                lang = lang.replace('\n', '')
                states = f.readline()
                states = lang.replace('\n', '')
                start = f.readline()
                start = lang.replace('\n', '')
                accept = f.readline()
                accept = lang.replace('\n', '')
                transfer = f.readlines()
                for t in transfer:
                    t = t.replace('\n', '')
            
    def __init__(self, path_to_rules):
        
        return

    def run(self):
        return

if __name__ == '__main__':
    if len(argv) != 2:
        print("Usage:\n\t python3 %s <dfa rule file>" % argv[0])
    else:
        dfa = DFA(argv[1])