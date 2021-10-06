from unidecode import unidecode
class ContactService:
    def __init__(self):
        self.contacts_list = []

    def add(self, name, phone):
        self.contacts_list.append([name, phone])

    def add_pp(self, ruc="None", website="None", email="None", phone="None"):
        return [ruc, website, email, phone]

    def get_contacts_list(self):
        return self.contacts_list

    def validate_phone(self, phone):
        phone = str(phone).strip()
        return phone[0] == '9'

    def format_name(self, name):
        name = str(name)
        c = 0
        for ch in name:
            if ch == '.':
                break
            c += 1
        name = unidecode(name)
        return name[c + 1:len(name)]
