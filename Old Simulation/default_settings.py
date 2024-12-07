import pickle

settings = (True, True, False)
file = open("data/settings.pickle", "wb")
pickle.dump(settings, file)
file.close()
