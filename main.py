import json
import spotipy as SP
import polars as PL
from spotipy.oauth2  import SpotifyOAuth

with open("AppConfig.json", "r") as f:
    app_data = json.load(f)

POP_URI = "5yUDKekFsz932eonUwxNN6"

sp = SP.Spotify(auth_manager=SpotifyOAuth(client_id=app_data["client_id"],
                                               client_secret=app_data["client_secret"],
                                               redirect_uri=app_data["redirect_URI"],
                                               scope=app_data["scope"]))

def get_playlist_tracks():
    tracks = []
    track_data = []
    playlist = sp.playlist_tracks(POP_URI)
    # Get all tracks
    tracks=playlist['items']
    while playlist['next']:
        playlist = sp.next(playlist)
        tracks.extend(playlist['items'])
    # iterate through tracks
    for track in tracks:
        track_uri=track["track"]["uri"]
        track_name=track["track"]["name"]
        track_artist=track["track"]["artists"]
        result=sp.audio_features(track_uri)[0]
        result["track_uri"] = track_uri
        result["track_name"] = track_name
        result["track_artist"] = track_artist
        track_data.append(result)
    return track_data

#PL.json_normalize(get_playlist_tracks(), max_level=1)
#print(get_playlist_tracks())

tracks=get_playlist_tracks()

with open('track_data.json', 'w', encoding='utf-8') as f:
    json.dump(tracks, f, ensure_ascii=False, indent=4)


# with open('tracks.json', 'w', encoding='utf-8') as f:
#     json.dump(tracks, f, ensure_ascii=False, indent=4)

# tracks = playlist("items")

# for track in tracks:
#     print(track["name"])


# CLIENT_ID = 'ID'
# CLIENT_SECRET = "Secret"
# PLAYLIST_LINK = "https://open.spotify.com/playlist/3VJlwgnV4IaxGK8uIEZMjV?si=ca8c506dd5d04663"
# PLAYLIST_URI = "5yUDKekFsz932eonUwxNN6"

# AUTH_MANAGER = SpotifyOAuth(
#     client_id=app_data["client_id"], client_secret=app_data["client_secret"],redirect_uri=app_data["redirect_URI"],scope=app_data["scope"]
# )
# SP = spotipy.Spotify(auth_manager=AUTH_MANAGER)


# # def get_playlist_uri(playlist_link):
# #     return playlist_link.split("/")[-1].split("?")[0]


# def get_tracks():
#     tracks = []
#     for track in SP.playlist_tracks(PLAYLIST_URI)["items"]:
#         track_uri = track["track"]["uri"]
#         track_name = track["track"]["name"]
#         result = track_uri,track_name, SP.audio_features(track_uri)
#         tracks.append(result)

#     return tracks


# the_stuff = get_tracks()
# print(the_stuff)