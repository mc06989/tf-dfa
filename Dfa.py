import re

from os.path import abspath
from sys import argv


class DFA:
    class Rules:
        def __init__(self, rule_file):
            def read_list(list):
                if list[0] == '{':
                    list = list[1:]
                if list[-1] == '}':
                    list = list[:-1]
                list = list.split(',')
                return list
            
            rules = {}
            rule_file = abspath(rule_file)
            lang = list()
            states = list()
            start = str()
            accept = list()
            transfer = dict()
            with open(rule_file, 'r', newline=None) as f:
                
                # read the sections, and strip any newlines
                lang = f.readline()
                states = f.readline()
                start = f.readline()
                accept = f.readline()
                transfer = f.readlines()
            
            lang = lang.replace('\n', '')
            states = states.replace('\n', '')
            start = start.replace('\n', '')
            accept = accept.replace('\n', '')

            #print(lang)
            #print(states)
            #print(start)
            #print(accept)

            for index, t in enumerate(transfer):
                transfer[index] = t.replace('\n', '')
            #print(transfer)
            list_pattern = re.compile(r"\{[\w\d]+(?:,[\w\d]+)*\}")
            transfer_pattern = re.compile(r"\((?P<state>[\w\d]+),(?P<input>[\w\d])\)->(?P<next>[\w\d]+)")
            language_pattern = re.compile(r"\{[\w\d](?:,[\w\d])*\}")
            lfs = "Language not formatted properly"
            lcs = "Language must consist of individual symbols, not more than one"
            sfs = "States not formatted properly"
            afs = "Accepting states not formatted properly"
            tfs = "Transfer function %d is not formatted properly"

            # syntax checks
            assert re.fullmatch(list_pattern, lang), lfs
            assert re.fullmatch(language_pattern, lang), lcs
            assert re.fullmatch(list_pattern, states), sfs
            assert re.fullmatch(list_pattern, accept), afs

            # reformat
            lang = read_list(lang)
            states = read_list(states)
            accept = read_list(accept)
            for index, t in enumerate(transfer):
                match = re.fullmatch(transfer_pattern, t)
                assert match, tfs % index
                transfer[index] = match.groupdict()

            statechk = "%s is not an enumerated state"
            inputchk = "%s is not defined in the language %s"

            # now logical checks
            assert start in states, statechk % start
            for st in accept:
                assert st in states, statechk % st

            for item in transfer:
                assert item['state'] in states, statechk % item['state']
                assert item['input'] in lang, inputchk % (item['input'], str(lang))
                assert item['next'] in states, statechk % item['next']

            temp = {}
            for item in transfer:
                if not temp.setdefault(item['state']):
                    temp.update({item['state']: {}})
                temp[item['state']].update({item['input']: item['next']})
            #print(temp)
            
            self.language = lang
            self.states = states
            self.start = start
            self.accept = accept
            self.transfer = temp
   
    def __init__(self, path_to_rules):
        self.rules = DFA.Rules(path_to_rules)
        self.state = ''

    def run(self, input):
        self.state = self.rules.start
        for i in input:
            try:
                self.state = self.rules.transfer[self.state][i]
            except KeyError:
                print("KeyError")
                print("%s: %s" % (self.state, i))
                return "Reject"
        if self.state in self.rules.accept:
            return "Accept"
        else:
            return "Reject"

if __name__ == '__main__':
    if len(argv) != 3:
        print("Usage:\n\t python3 %s <dfa rule file> <input string>" % argv[0])
    else:
        dfa = DFA(argv[1])
        print(dfa.run(argv[2]))
