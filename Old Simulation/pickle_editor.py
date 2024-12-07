import pickle


def load(path):
    file = open(path, "rb")
    user_settings = pickle.load(file)
    file.close()
    return user_settings


def save(path, data):
    file = open(path, "wb")
    pickle.dump(data, file)
    file.close()
    return

