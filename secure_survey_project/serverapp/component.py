from typing import List, Tuple
import piheaan as heaan
from piheaan.math import approx
from pathlib import Path


class Network:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Network, cls).__new__(cls)
        return cls._instance

    def __init__(self, key_dir: Path, user_dir: Path):
        if not hasattr(self, 'initialized'):
            self.log_slots = 3

            self.params = heaan.ParameterPreset.FGb
            self.context = heaan.make_context(self.params)
            heaan.make_bootstrappable(self.context)

            self.key_dir = key_dir
            self.user_dir = user_dir

            self.public_key = None
            self.private_key = None

            self.eval = None
            self.encryptor = None
            self.decryptor = None
            self._load_keys()

            # id, ciphertext
            self.encrypted_personal_info: List[Tuple[int, heaan.Ciphertext]] = [
            ]

            # 각 번호에서 중복 선택된 횟수, 각 항목의 ciphertext
            self.encrypted_personal_condition: List[Tuple[List, List[heaan.Ciphertext]]] = [
            ]
            self.encrypted_survey_result: List = []
            self.aggregated_survey_results: List = []

            self.initialized = True

    def _create_and_save_keys(self):
        # create secret key
        self.private_key = heaan.SecretKey(self.context)
        # create public key
        key_generator = heaan.KeyGenerator(
            self.context, self.private_key)
        key_generator.gen_common_keys()

        # make directory and save both keys
        self.key_dir.mkdir(mode=0o775, parents=True, exist_ok=True)
        self.private_key.save(
            str(self.key_dir / "secretkey.bin"))  # save secret key
        key_generator.save(str(self.key_dir / ""))  # save public key

    def _load_keys(self):

        if not self.key_dir.is_dir():
            self._create_and_save_keys()

        # load private key
        self.private_key = heaan.SecretKey(
            self.context, str(self.key_dir / "secretkey.bin"))
        # load public key
        self.public_key = heaan.KeyPack(
            self.context, str(self.key_dir / ""))
        self.public_key.load_enc_key()
        self.public_key.load_mult_key()

        # to load piheaan basic function
        self.eval = heaan.HomEvaluator(self.context, self.public_key)
        self.decryptor = heaan.Decryptor(self.context)  # for decrypt
        self.encryptor = heaan.Encryptor(self.context)  # for encrypt

    def load_encrypted_personal_info(self):

        userfilepaths = list(self.user_dir.glob("*.ctxt"))

        for userfilepath in userfilepaths:
            # create a new instance of heaan.Ciphertext
            temp_ctxt = heaan.Ciphertext(self.context)
            temp_ctxt.load(str(userfilepath))

            # get the user id from the file name and convert to int
            user_id = int(userfilepath.stem)

            # create a tuple with user id and ciphertext
            user_info = (user_id, temp_ctxt)

            # append to the Queue using put
            self.encrypted_personal_info.append(user_info)

        # print(len(self.encrypted_personal_info))

    def encrypt_personal_info(self, id, data):
        message = heaan.Message(self.log_slots)
        for i in range(len(data)):
            message[i] = data[i]

        ciphertext = heaan.Ciphertext(self.context)
        self.encryptor.encrypt(message, self.public_key, ciphertext)

        # cipher text 저장
        file_path = self.user_dir / f"{id}.ctxt"
        ciphertext.save(str(file_path))

        # List 에도 저장
        user_info = (id, ciphertext)
        self.encrypted_personal_info.append(user_info)

    def encrypt_personal_conditions(self, personal_conditions):
        ciphertext_list = []
        for personal_condition in personal_conditions:
            message = heaan.Message(self.log_slots)
            for i, condition_value in enumerate(personal_condition):
                # 값들을 complex 타입으로 변환
                complex_value = complex(condition_value, 0.0)
                message[i] = complex_value

            ciphertext = heaan.Ciphertext(self.context)
            self.encryptor.encrypt(message, self.public_key, ciphertext)
            ciphertext_list.append(ciphertext)
        return ciphertext_list

    def save_personal_conditions(self, personal_condition_dict):
        number_of_elements_per_column = []
        personal_conditions = []
        for column, selections in personal_condition_dict.items():
            number_of_elements_per_column.append(len(selections))

            for selection in selections:
                condition = [0] * (2 ** self.log_slots)
                condition_value = selection
                column_index = int(column)  # 문자열 열 인덱스 값을 정수로 변환
                condition[column_index] = int(condition_value)
                personal_conditions.append(condition)

        encrypted_personal_conditions = self.encrypt_personal_conditions(
            personal_conditions)
        temp = (number_of_elements_per_column, encrypted_personal_conditions)

        self.encrypted_personal_condition.append(temp)

        # print("data: ", self.encrypted_personal_condition)

        # print(len(self.encrypted_personal_condition))

    def find_target_user(self):
        number_of_elements_per_column, encrypted_personal_conditions = self.encrypted_personal_condition[
            len(self.encrypted_personal_condition) - 1]

        # id 를 기준으로 오름차순으로 정렬
        self.encrypted_personal_info = sorted(
            self.encrypted_personal_info, key=lambda x: x[0])

        # user_idx = [x for x in range(len(self.user_table.index))]
        user_idx = [e[0]
                    for e in self.encrypted_personal_info]  # (id, encrypted_info)

        target_user_idx = []

        count = 0
        for i, number_of_elements in enumerate(number_of_elements_per_column):
            print(f"Selected number of users: {len(user_idx)}")

            target_user_idx = []
            for _ in range(number_of_elements):
                current_personal_condition = encrypted_personal_conditions[count]

                for idx in user_idx:

                    # current_personal_info = self.user_table.iloc[idx]['encrypted_personal_info']
                    current_personal_info = self.encrypted_personal_info[idx - user_idx[0]][1]

                    result_discrete_equal = heaan.Ciphertext(self.context)
                    approx.discrete_equal(
                        self.eval, current_personal_info, current_personal_condition, result_discrete_equal)

                    result_discrete_equal_message = heaan.Message(
                        self.log_slots)
                    self.decryptor.decrypt(
                        result_discrete_equal, self.private_key, result_discrete_equal_message)

                    if round(result_discrete_equal_message[i].real) == 1:
                        target_user_idx.append(idx)
                count += 1
            user_idx = target_user_idx.copy()

            print("------------------------------------")
        print(f"Selected number of users: {len(user_idx)}")
        print("------------------------------------")
        return user_idx
