from setuptools import setup
from pathlib import Path

# Read the contents of the README file
readme_path = Path(__file__).parent / 'README.md'
with open(readme_path, 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='fetch-lyrics-from-genius',
    version='0.1.2',
    description='A package to fetch lyrics from Genius.com',
    author='Andrew Beveridge',
    author_email='andrew@beveridge.uk',
    packages=['fetch_lyrics_from_genius'],
    install_requires=[
        'lyricsgenius',
        'musicbrainzngs',
        'python-slugify'
    ],
    entry_points={
        'console_scripts': [
            'fetch-lyrics-from-genius = fetch_lyrics_from_genius.fetch_lyrics:main',
        ],
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
)
