from serverapp.component import *


def start_server():

    key_dir_path = Path("keys")
    userdir_path = Path("users")

    network = Network(key_dir_path, userdir_path)
    network.load_encrypted_personal_info()

    pass
