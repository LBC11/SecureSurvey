from pathlib import Path
import json
import piheaan as heaan
from serverapp.component import Network


class Company():
    def __init__(self):
        self.personal_condition_dict = None
        self.personal_conditions = None

        self.log_slots = 3

        self.context = None
        self.public_key = None
        self.encryptor = None

    # def load_personal_condition_dict(self, personal_condition_dict_path: Path):
    #     with open(str(personal_condition_dict_path), 'r') as f:
    #         self.personal_condition_dict = json.load(f)

    def get_encryptor(self, network: Network):
        self.context, self.public_key, self.encryptor = network.encryptor.get()

    def encrypt_personal_conditions(self, personal_conditions):
        ciphertext_list = []
        for personal_condition in personal_conditions:
            message = heaan.Message(self.log_slots)
            for i in range(len(personal_condition)):
                message[i] = personal_condition[i]

            ciphertext = heaan.Ciphertext(self.context)
            self.encryptor.encrypt(message, self.public_key, ciphertext)
            ciphertext_list.append(ciphertext)
        return ciphertext_list

    def create_personal_conditions(self):
        number_of_elements_per_column = []
        personal_conditions = []
        for i, (column, selections) in enumerate(self.personal_condition_dict.items()):
            number_of_elements_per_column.append(len(selections))

            for selection in selections:
                condition = [0] * (2**self.log_slots)
                # print(selection, list(selection.values())[0])
                condition[i] = list(selection.values())[0]
                personal_conditions.append(condition)

        encrypted_personal_conditions = self.encrypt_personal_conditions(
            personal_conditions)
        self.personal_conditions = (
            number_of_elements_per_column, encrypted_personal_conditions)
        return

    def send_personal_conditions(self, network: Network):
        network.encrypted_personal_condition.put(self.personal_conditions)
