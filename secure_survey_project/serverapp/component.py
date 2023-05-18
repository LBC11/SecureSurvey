from typing import Dict, List, Tuple
from queue import Queue
import piheaan as heaan
from piheaan.math import approx
from pathlib import Path
from tqdm.auto import tqdm


class Survey():
    def __init__(cls):
        cls.questions = []
        cls.answers = []


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

            # Initialization
            self.encrypted_personal_info: Queue[Tuple[int, heaan.Ciphertext]] = Queue(
            )
            self.encrypted_personal_condition: Queue[Tuple[List, List[heaan.Ciphertext]]] = Queue(
            )
            self.survey: Queue[Survey] = Queue()
            self.encrypted_survey_result: Queue = Queue()
            self.aggregated_survey_results: Queue = Queue()

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
            self.encrypted_personal_info.put(user_info)

        print(self.encrypted_personal_info.qsize())

    def encrypt_personal_info(self, id, data):
        message = heaan.Message(self.log_slots)
        for i in range(len(data)):
            message[i] = data[i]

        ciphertext = heaan.Ciphertext(self.context)
        self.encryptor.encrypt(message, self.public_key, ciphertext)

        # cipher text 저장
        file_path = self.user_dir / f"{id}.ctxt"
        ciphertext.save(str(file_path))

        # Queue 에도 저장
        user_info = (id, ciphertext)
        self.encrypted_personal_info.put(user_info)

    def find_target_user(self):
        number_of_elements_per_column, encrypted_personal_conditions = self.encrypted_personal_conditions
        user_idx = [x for x in range(len(self.user_table.index))]
        target_user_idx = []

        count = 0
        for i, number_of_elements in enumerate(number_of_elements_per_column):
            print(f"Selected number of users: {len(user_idx)}")
            for _ in tqdm(range(number_of_elements)):
                current_personal_condition = encrypted_personal_conditions[count]
                for idx in user_idx:
                    current_personal_info = self.user_table.iloc[
                        idx]['encrypted_personal_info']

                    result_discrete_equal = heaan.Ciphertext(
                        self.context)
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
            target_user_idx = []
            print("------------------------------------")
        print(f"Selected number of users: {len(user_idx)}")
        print("------------------------------------")
        return user_idx

    def send_survey_to_target_user(self):
        return

    def get_encrypted_survey_result(self):
        return

    def aggregate_survey_result(self):
        return

    def send_aggregated_survey_result_to_company(self):
        return
