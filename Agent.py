class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.username = None
        self.password = None
        self.created_at = None
        self.f_name = None
        self.l_name = None
        self.gender = None
        self.age = None
        self.contact_number = None
        self.added_at = None

    def agent_credential(self, username, password, created_at):
        self.agent_id = self.agent_id
        self.username = username
        self.password = password
        self.created_at = created_at
        return {
            "agent_id": self.agent_id,
            "username": self.username,
            "password": self.password,
            "created_at": self.created_at
        }

    def agent_details(self, f_name, l_name, gender, age,contact_number, added_at):
        self.agent_id = self.agent_id
        self.f_name = f_name
        self.l_name = l_name
        self.gender = gender
        self.age = age
        self.contact_number = contact_number
        self.added_at = added_at
        return {
            "agent_id": self.agent_id,
            'f_name': self.f_name,
            "l_name": self.l_name,
            "gender": self.gender,
            "age": self.age,
            "contact_number": self.contact_number,
            "added_at": self.added_at
        }

