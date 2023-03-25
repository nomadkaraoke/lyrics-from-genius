import musicbrainzngs
import sys
from fuzzywuzzy import fuzz

# Set up the musicbrainzngs library
musicbrainzngs.set_useragent("Karaoke Hunt", "0.1", contact="andrew@karaokehunt.com")

# Get the artist name and album name from command line arguments
artist_name = sys.argv[1]
album_name = sys.argv[2]

# Search for the artist
result = musicbrainzngs.search_artists(artist_name)

# If there are no search results, exit with an error message
if len(result['artist-list']) == 0:
    print(f"No artists found for '{artist_name}'")
    sys.exit()

# If there is more than one search result, use fuzzy matching to find the best match
artists_found = len(result['artist-list'])
if artists_found > 1:
    print(f"{str(artists_found)} artists found for search '{artist_name}', applying fuzzy logic")
    best_match = None
    best_ratio = 0
    for artist in result['artist-list']:
        ratio = fuzz.ratio(artist['name'], artist_name)
        if ratio > best_ratio:
            best_match = artist
            best_ratio = ratio
    artist_id = best_match['id']
    artist_name = best_match['name']
else:
    artist_id = result['artist-list'][0]['id']
    artist_name = result['artist-list'][0]['name']

print(f"Artist selected: '{artist_name}' with ID: {artist_id}")

# Search for the album by the artist
result = musicbrainzngs.search_releases(query=album_name, artist=artist_name, limit=10)

# If there are no search results, exit with an error message
if len(result['release-list']) == 0:
    print(f"No albums found for '{album_name}' by '{artist_name}'")
    sys.exit()

# If there is more than one search result, use fuzzy matching to find the best match
releases_found = len(result['release-list'])
if releases_found > 1:
    print(f"{str(releases_found)} releases found for search '{album_name}', applying fuzzy logic")
    best_match = None
    best_ratio = 0
    for album in result['release-list']:
        ratio = fuzz.ratio(album['title'], album_name)
        if ratio > best_ratio:
            best_match = album
            best_ratio = ratio
    album_id = best_match['id']
    album_name = best_match['title']
else:
    album_id = result['release-list'][0]['id']
    album_name = result['release-list'][0]['title']

print(f"Album selected: '{album_name}' with ID: {album_id}")

album_data = musicbrainzngs.get_release_by_id(album_id, includes=['recording-rels']);
print(album_data)

# Get the list of tracks on the album
result = musicbrainzngs.browse_recordings(release=album_id)

tracks = result['recording-list']

# Print the album and artist names
print(f"Album: {album_name} by {artist_name}")

# Print the list of tracks on the album
for idx, track in enumerate(tracks):
    print(track)
    track_data = musicbrainzngs.get_recording_by_id(track['id'], includes=['recording-rels', 'release-rels', 'release-group-rels'])
    print(track_data)
    
