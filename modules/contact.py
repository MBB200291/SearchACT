"""
To manage dictionary update operations.

"""
import pickle
import pandas as pd
from sys import argv
from os import path, listdir

def save_obj_to_pickle(path, obj): # will end with pickle
    print('# saving file to:', '%s.pickle'%path)
    with open('%s.pickle'%path, 'wb') as f_pkl:
        pickle.dump(obj, f_pkl)

def read_pickle(path_):
    with open(path_, 'rb') as file:
        return pickle.load(file)

def locate_contact_file(path_script):
    cwd = path.dirname(path.abspath(path_script))
    print(cwd)
    path_contact = sorted([x for x in listdir(cwd) if ".xlsx" in x and not x.startswith('~$')])[-1]
    #print([x for x in os.listdir(cwd) if ".xlsx" in x])
    print('# Read file:', path_contact )
    return path.join(cwd, path_contact)

def remove_blank(tab):
    #First, find NaN entries in first column
    blank_row_bool = tab.iloc[:,4].isna()
    #Next, get index of first NaN entry
    blank_row_index =  [i for i, x in enumerate(blank_row_bool) if x][0]
    #Finally, restrict dataframe to rows before the first NaN entry
    return tab.iloc[:(blank_row_index)]

def read_excel(path_contact):
    if path.isfile(path_contact):
        #contacts = pd.read_excel(path_contact, nrows=nrows)
        contacts = remove_blank(pd.read_excel(path_contact))
        contacts.dropna(how="all", inplace=True)
#        contacts = contacts.loc[(~contacts['信     箱'].isna()) & (contacts['信     箱'].str.contains("@"))]
        return contacts, path.splitext(path_contact)[-1]
    else:
        print('*** Contact file not exist')
        return None

def make_dict(path_contact):#, _nrows):
    ## Read excel
    contacts, excel_file_name = read_excel(path_contact)
    if type(contacts)!=pd.core.frame.DataFrame:
        return None
    ## Make dictionary
    dict_terms_key = {} #
    dict_key_contacts = {'*version':excel_file_name, '*ver':excel_file_name}
    
    DI_Apartment_Abbrev = {  ### 欸欸那個大家如果有知道這些部門的縮寫，麻煩幫忙補一下 ###
        "執行長室": "CEO", 
        #"技術中心": "", 
        #"營運中心": "", 
        #"Group CFO": "", 
        "研究開發處": "RD", 
        "研究開發部": "RD", 
        #"技術移轉部": "", 
        #"智慧財產部": "", 
        #"商業卓越處": "", 
        #"系統整合部": "", 
        #"產品管理部": "", 
        "生物資訊暨人工智慧處": "BI", 
        "生物資訊部": "BI", 
        "人工智慧部": "AI", 
        "數據分析部": "DA", 
        "數據智能部": "DI", 
        "資料科學處": "DS", 
        #"分子檢驗處": "", 
        "次世代定序部": "NGS", 
        #"轉譯醫學處": "", 
        "癌症基因體部": "", 
        #"專案管理部": "", 
        "醫藥資訊部": "MI", 
        #"臨床醫學部": "", 
        "品保與環境監控部": "QA", 
        "法規事務處": "RA", 
        #"銷售業務處": "", 
        #"銷售業務部": "", 
        #"業務行政部": "", 
        #"臨床衛教部": "", 
        #"行政資源處": "", 
        #"行政資源部": "", 
        #"會計處": "", 
        #"財務與出納部": "", 
        "事業暨企業發展處": "BD", 
        "資訊處": "IT", 
        "人力資源處": "HR", 
    }
    for i,R in contacts.iterrows():

        PhoneNum = str(R['分機']).strip()
        ChnName = R['姓名'].strip()
        Department2 = R['所屬處級名稱'].strip()
        Department = R['部門名稱'].strip()
        EngName = str(R['英文名']).strip()
        EngName_dd = EngName.replace('-', ' ').strip()
        EngName_dd2 = EngName.replace('-', '').strip()
        MailAress = R['信箱'].strip()
        CellPhone = str(R['手機']).strip()
        
        print(ChnName, EngName)
        
        KEY = MailAress.split('@')[0]

        ## first part: key to result
        dict_key_contacts[KEY] = [str(x) for x in [ChnName, EngName, Department2, Department, MailAress, PhoneNum, CellPhone]]

        ## second part: query items to key
        
        ### eng-name or ch-name
        dict_terms_key.setdefault(ChnName, set()).add(KEY)
        dict_terms_key.setdefault(ChnName[:-1], set()).add(KEY)
        dict_terms_key.setdefault(ChnName[-1], set()).add(KEY)
        dict_terms_key.setdefault(EngName, set()).add(KEY)
        dict_terms_key.setdefault(EngName.lower(), set()).add(KEY)
        dict_terms_key.setdefault(EngName_dd, set()).add(KEY)
        dict_terms_key.setdefault(EngName_dd.lower(), set()).add(KEY)
        dict_terms_key.setdefault(EngName_dd2, set()).add(KEY)
        dict_terms_key.setdefault(EngName_dd2.lower(), set()).add(KEY)
        
        ### create key of name abbreviation --> in uppercase form
        dict_terms_key.setdefault(''.join([x[0].upper() for x in EngName.split(' ')]), set()).add(KEY)
        dict_terms_key.setdefault(''.join([x[0].upper() for x in EngName_dd.split(' ')]), set()).add(KEY)
        dict_terms_key.setdefault(''.join([x[0].upper() for x in EngName_dd2.split(' ')]), set()).add(KEY)
        ### create key of name abbreviation --> in uppercase form, order by first name then second name
        dict_terms_key.setdefault(EngName[-1].upper()+''.join([x[0].upper() for x in EngName.split(' ')[:-1]]), set()).add(KEY)
        dict_terms_key.setdefault(EngName[-1].upper()+''.join([x[0].upper() for x in EngName_dd.split(' ')[:-1]]), set()).add(KEY)
        dict_terms_key.setdefault(EngName[-1].upper()+''.join([x[0].upper() for x in EngName_dd2.split(' ')[:-1]]), set()).add(KEY)

        ### by email id
        dict_terms_key.setdefault(MailAress.split('@')[0].lower(), set()).add(KEY)
        ### by Phone num
        dict_terms_key.setdefault(str(PhoneNum), set()).add(KEY)
        ### by cell phone num
        dict_terms_key.setdefault(str(CellPhone), set()).add(KEY)
        ### by department
        dict_terms_key.setdefault(str(Department), set()).add(KEY)
        ### by department2
        dict_terms_key.setdefault(str(Department2), set()).add(KEY)
        ### by department's abbreviation
        dict_terms_key.setdefault(DI_Apartment_Abbrev.get(str(Department), str(Department)), set()).add(KEY)
        dict_terms_key.setdefault(DI_Apartment_Abbrev.get(str(Department2), str(Department2)), set()).add(KEY)


    #print(os.path.split(sys.path[0])[0])
    #'''
    path_term_key = path.join(path.dirname(path_contact), '_dict_terms_key')
    path_key_contact = path.join(path.dirname(path_contact), '_dict_key_contacts')
    save_obj_to_pickle(path_term_key, dict_terms_key)
    save_obj_to_pickle(path_key_contact, dict_key_contacts)
    #'''
    path_term2key_key2contact = path.join(path.dirname(path_contact), '_dict_contacts')
    save_obj_to_pickle(path_term2key_key2contact, [dict_terms_key, dict_key_contacts])


class Contact():
    #def __init__(self, PATH_DICT_KEY_CONTACT, PATH_DICT_TERM_KEY):
    def __init__(self, PATH_DICT_CONTACT):
        '''
        self.PATH_DICT_KEY_CONTACT = PATH_DICT_KEY_CONTACT
        self.PATH_DICT_TERM_KEY = PATH_DICT_TERM_KEY
        self.DICT_KEY_CONTACT = read_pickle(PATH_DICT_KEY_CONTACT)
        self.DICT_TERM_KEY = read_pickle(PATH_DICT_TERM_KEY)
        '''
        self.PATH_DICT_CONTACT = PATH_DICT_CONTACT
        self.DICT_TERM_KEY, self.DICT_KEY_CONTACT = read_pickle(PATH_DICT_CONTACT)
        
    def add_searchTerm_to_key(self, str_input_Term, str_input_KEY):
        self.DICT_TERM_KEY.setdefault(str_input_Term, set()).add(str_input_KEY)
        save_obj_to_pickle(path.splitext(self.PATH_DICT_TERM_KEY)[0], self.DICT_TERM_KEY)
        print(f'Successfuly add new search terms. "{str_input_Term}":"{str_input_KEY}"')
        return 0

    def add_contactInfo(self, str_input_KEY, str_add_info):
        self.DICT_KEY_CONTACT[str_input_KEY].append(str_add_info)
        save_obj_to_pickle(path.splitext(self.PATH_DICT_KEY_CONTACT)[0], self.DICT_KEY_CONTACT)
        print(f'Successfuly add new info terms. "{self.DICT_KEY_CONTACT[str_input_KEY]}"')
        return 0
    
    def re_build(self):
        pass
        '''
        import updata_contact
        print('** this operation will wipe out the term created by your own. Sure?')
        str_input = input('\n(Y/N) >>> ').lower()
        if str_input == 'y':
            updata_contact.MakeDict(updata_contact.locate_contact_file())
            DICT_KEY_CONTACT = read_pickle(PATH_DICT_KEY_CONTACT)
            DICT_TERM_KEY = read_pickle(PATH_DICT_TERM_KEY)
        else:
            pass
        '''
    def rm_ifno(self):
        pass