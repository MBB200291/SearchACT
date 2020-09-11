 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  3 23:52:45 2019

@author: linbangqi
@Co-author: bruce

Version log:
- 1.0.0
- 1.1.0:
    - organize by id to value
    - include more keys
- 1.3.0
- 1.3.1
- 1.4.0: add calculator
- 1.5.0: calculator triggering part
- 1.6.0:
    - caculator loop inside until exit
    - modify a file name for other OS
- 1.7.0:
    - multiple rule syntax
    - calculator re-implement
    - search key by string matching
- 1.8.0:
    - new structure
- 1.8.1:
    - calculator re-implement

Next version
- include removing function

"""

__version__ = '1.8.1'


from sys import argv
from os import path
### custom functions
from modules.search import SearchACT
import modules.calculator as cal
from modules.contact import Contact
from modules.help_info import help_
###

PATH_OF_SCRIPT = path.dirname(argv[0])
PATH_DICT_KEY_CONTACT = path.join(PATH_OF_SCRIPT, '_dict_key_contacts.pickle')
PATH_DICT_TERM_KEY = path.join(PATH_OF_SCRIPT, '_dict_terms_key.pickle')

LI_EXIST_WORDS = ['exit', 'bye', 'ex', 'bye bye', 'quit']

# main process
def main():
    print('Type part of name to search ACT contact. Type "*help" to get detail instruction. Type "exit" to leave.\nType *cal to enter caculation mode.')
#    global DICT_KEY_CONTACT, DICT_TERM_KEY,  PATH_DICT_KEY_CONTACT, PATH_DICT_TERM_KEY
    calculator = cal.Calculator(cal.names, cal.ops)
    while True:
        str_input = input('\nSeach >>> ')#.lower()
        Contact_ = Contact(PATH_DICT_KEY_CONTACT, PATH_DICT_TERM_KEY)
        SearchACT_ = SearchACT(Contact_.DICT_TERM_KEY)
        '''
        if str_input in DICT_TERM_KEY:
            ## matched
            for k in DICT_TERM_KEY[str_input]:
                print('\n', '>'+'\t'.join(DICT_KEY_CONTACT[k]))
        '''
        # add search term function
        if str_input in ['*addterm', '*add1']:
            print('into adding mode')
            str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit. >>> ').lower()
            if str_input_KEY in LI_EXIST_WORDS:
                break
            elif str_input_KEY not in Contact_.DICT_KEY_CONTACT.keys():
                print('*** The ID not exist. ***')
                continue
            str_input_Term = input('Type the new search term or type "exit" to exit.\n>>> ').lower()
            if str_input_Term in LI_EXIST_WORDS:
                break
            ans = Contact_.add_searchTerm_to_key(str_input_Term, str_input_KEY)
            if ans == 0:
                pass
            else:
                break
        # add contact info function
        elif str_input in ['*addinfo', '*add2']:
            str_input_KEY = input('Type the E-mail ID (for example, type "benlin" for "benlin@actgenomics.com") or type "exit" to exit.\n>>> ').lower()
            if str_input_KEY in LI_EXIST_WORDS:
                break
            elif str_input_KEY not in Contact_.DICT_KEY_CONTACT.keys():
                print('*** The ID not exist. ***')
                continue
            str_add_info = input('Type the new info of the person or type "exit" to exit.\n>>> ').lower()
            if str_add_info in LI_EXIST_WORDS:
                break
            ans = Contact_.add_contactInfo(str_input_KEY, str_add_info)
            if ans == 0:
                pass
            else:
                break
        # remove contact info function
        elif str_input in ['*rminfo', '*rm2']:
            pass
            #Contact_.rm_ifno()
        elif str_input in ['*rebuild', '*rb']:
            pass
            #Contact_.re_build()
        elif str_input.startswith('$'):
            print(eval(str_input[1:]))
        elif str_input in LI_EXIST_WORDS:
            break
        elif str_input in ['hi', 'hello']:
            print('HI')
            #break
        elif str_input in ['*cal', '*c']:
            print('Caculation_mode:')
            while True:
                str_input = input('\nCalculator >>> ')
                if str_input in LI_EXIST_WORDS:
                    break
                else:
                    try:
                        cal_ans = parse(str_input)
                        if cal_ans != eval(str_input):
                            print('error')
                            pass
                        else:
                            print('answer: ', cal_ans)
                    except:
                        print('formula error !')
                        pass
        elif str_input in ['*help', '*h']:
            print(f' version:{__version__}')
            print(help_())
        else:
            #raw_match(str_input, DICT_TERM_KEY, DICT_KEY_CONTACT)
            try:
                #set_matches = search(str_input)
                #set_matches = parse_formula(str_input)
                set_matches = SearchACT_.parse_formula(str_input)
            except:
                print('formula error !')
                set_matches = None
                pass
            if not set_matches:
                print(f'\n "{str_input}" not found. Retry or type "exit" to exit.')
            else:
                for r in set_matches:
                    print('\n', '>'+'\t'.join(Contact_.DICT_KEY_CONTACT[r]))
if __name__ == '__main__':
    main()
