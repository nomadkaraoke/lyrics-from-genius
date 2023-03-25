import argparse
import os
import re
import lyricsgenius

def clean_lyrics(lyrics):
    lyrics = lyrics.replace('\\n', '\n')
    lyrics = re.sub(r'You might also like', '', lyrics)
    lyrics = re.sub(r'.*?Lyrics([A-Z])', r'\1', lyrics)  # Remove the song name and word "Lyrics" if this has a non-newline char at the start
    lyrics = re.sub(r'[0-9]+Embed$', '', lyrics)  # Remove the word "Embed" at end of line with preceding numbers if found
    lyrics = re.sub(r'(\S)Embed$', r'\1', lyrics)  # Remove the word "Embed" if it has been tacked onto a word at the end of a line
    lyrics = re.sub(r'.*?\[.*?\].*?', '', lyrics)  # Remove lines containing square brackets
    # add any additional cleaning rules here
    return lyrics

def write_lyrics_file(song_title, artist_name, lyrics):
    directory = f'lyrics/{artist_name}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f'{directory}/{song_title}.txt'
    with open(filename, 'w') as f:
        f.write(lyrics)

def main():
    parser = argparse.ArgumentParser(description='Fetch lyrics from Genius.com and write them to text files')
    parser.add_argument('artist_name', type=str, help='the name of the artist to fetch lyrics for')
    parser.add_argument('--song_title', type=str, help='(optional) the title of a specific song to fetch lyrics for')
    parser.add_argument('--max_songs', type=int, default=3, help='(optional) the maximum number of songs to fetch lyrics for (default=100)')
    parser.add_argument('--api_token', type=str, help='(optional) the API token for Genius.com')
    args = parser.parse_args()

    if args.api_token:
        genius = lyricsgenius.Genius(args.api_token)
    elif 'GENIUS_API_TOKEN' in os.environ:
        genius = lyricsgenius.Genius(os.environ['GENIUS_API_TOKEN'])
    else:
        print('Please provide an API token either as a command line argument or as the GENIUS_API_TOKEN environment variable')
        return

    if args.song_title:
        # fetch lyrics for a specific song
        song = genius.search_song(args.song_title, args.artist_name)
        if song is None:
            print(f'Could not find lyrics for "{args.song_title}" by {args.artist_name}')
            return
        lyrics = clean_lyrics(song.lyrics)
        write_lyrics_file(song.title, song.artist, lyrics)
        print(f'Successfully fetched lyrics for "{song.title}" by {song.artist}')
    else:
        # fetch lyrics for all songs by the artist
        artist = genius.search_artist(args.artist_name, max_songs=args.max_songs)
        if artist is None:
            print(f'Could not find lyrics for {args.artist_name}')
            return
        for song in artist.songs:
            lyrics = clean_lyrics(song.lyrics)
            write_lyrics_file(song.title, song.artist, lyrics)
            print(f'Successfully fetched lyrics for "{song.title}" by {song.artist}')

if __name__ == '__main__':
    main()
