import pickle

song_mood_model = 'models/moodpred'

def get_model():
    with open(song_mood_model, 'rb') as f:
        clf2 = pickle.load(f)
    return clf2

def get_users_mood(list_input):
    model = get_model()
    mood_id = model.predict(list_input)
    mood = mapping(mood_id)
    return mood

def mapping(int_value):
    if int_value <= 4:
        return 'Sad'
    elif 4 < int_value <= 6:
        return 'Calm'
    elif 6 < int_value:
        return 'Happy'
