'''

version:
- 1.3.0:
 - add phone number query key
- 1.4.0:
 - add department name
- 1.5.1:
 - new rule
 - 1.6.0: update contact by searching contact file("行動基因通訊錄") within same folder of this script
 - 1.7.0: modify some code for other os system
- 2.0.0:
 - using single pickle file to store contact data

next version:
 - keep customize content

'''
__version__ = '2.0.0'

from modules.contact import locate_contact_file, make_dict
    
def main():
    print('# Loading')
    make_dict(locate_contact_file(__file__))

if __name__ == '__main__':
    main()