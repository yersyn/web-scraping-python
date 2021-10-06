import pandas as pd
import datetime


class FileContacts:
    def __init__(self, prefix):
        self.df_contacts = list()
        self.prefix = prefix

    def create_csv(self, contacts_list):
        date_now = datetime.datetime.now().timestamp()
        name_file = f'{self.prefix}-{date_now}'
        self.df_contacts = pd.DataFrame(contacts_list, columns=['name', 'phone'])
        self.df_contacts.to_csv(f'./{name_file}.csv')

    def create_pp_csv(self, contacts_list):
        date_now = datetime.datetime.now().timestamp()
        name_file = f'{self.prefix}-{date_now}'
        self.df_contacts = pd.DataFrame(contacts_list, columns=['ruc', 'website', 'email', 'phone'])
        self.df_contacts.to_csv(f'./{name_file}.csv')
