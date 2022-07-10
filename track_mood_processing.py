import pickle
import random
import ast

import sklearn

import numpy as np

song_mood_model = 'model/Keras-Classification'

def get_model():
    with open(song_mood_model, 'rb') as f:
        clf2 = pickle.load(f)
    return clf2


def get_songs_features(track_id, sp):

    meta = sp.track(track_id)
    features = sp.audio_features(track_id)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    track_id = meta['id']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, track_id, release_date, popularity, length, danceability, acousticness,
             energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name','album','artist','id','release_date','popularity','length','danceability','acousticness','energy','instrumentalness',
               'liveness','valence','loudness','speechiness','tempo','key','time_signature']
    return track, columns


def get_tracks_mood(tracks_ids, sp):
    tracks_dict = {'Happy': [],
                   'Sad': [],
                   'Calm': []}
    for track_id in tracks_ids:
        preds = get_songs_features(track_id, sp)
        preds_features = np.array(preds[0][6:-2]).reshape(-1, 1).T
        model = get_model()
        s_mood = model.predict(preds_features)[0]
        tracks_dict[s_mood].append(track_id)

    return tracks_dict


def get_user_tracks(sp):

    liked_tracks = sp.current_user_saved_tracks(limit=50)
    liked_tracks_ids = [liked_tracks['items'][n]['track']['uri'] for n in range(len(liked_tracks['items']))]

    print(liked_tracks_ids)
    return liked_tracks_ids


def get_proper_track(mood, sp):

    tracks = get_user_tracks(sp)
    mood_tracks_dict = get_tracks_mood(tracks, sp)
    track_selection = mood_tracks_dict[mood].pop(random.randint(0, len(mood_tracks_dict[mood])-1))

    return track_selection


def get_track_info(track_id, sp):
    meta = sp.track(track_id)

    track_name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    cover_url = meta['album']['images'][0]['url']
    return track_name, album, artist, cover_url