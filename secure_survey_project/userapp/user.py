from serverapp.component import Network


class PersonalInfo():
    def __init__(self):
        self.gender: int = -1
        self.age: int = -1
        self.marriage: int = -1
        self.income: int = -1
        self.education: int = -1
        self.job: int = -1
        self.phone_type: int = -1
        self.phone_maker: int = -1

    def __str__(self):
        return ""

    def set_personal_info(self, gender, age, marriage, income, education, job, phone_type, phone_maker):
        self.gender: int = gender
        self.age: int = age
        self.marriage: int = marriage
        self.income: int = income
        self.education: int = education
        self.job: int = job
        self.phone_type: int = phone_type
        self.phone_maker: int = phone_maker

    def return_list(self):
        return [self.gender, self.age, self.marriage, self.income, self.education, self.job, self.phone_type, self.phone_maker]


class User():
    def __init__(self, personal_info: PersonalInfo):
        self.personal_info = personal_info

    def encrypt_personal_info(self, id: int, network: Network):
        data = self.personal_info.return_list()

        data_complex = [complex(x, 0) if not isinstance(
            x, str) else complex(x) for x in data]
        network.encrypt_personal_info(id, data_complex)
