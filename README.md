# VideoHash CLI

A simple command-line interface (CLI) to compute and compare video hashes using the [videohash](https://github.com/akamhy/videohash) library.

## Requirements

- Python 3.6 or higher
- videohash
- tqdm

Install the required libraries using the `requirements.txt` file:

`pip install -r requirements.txt`

## Usage

1. Compute the video hash of a given video:

`python videohash_cli.py compute <video_file>`

2. Compare two video files and show their similarity:

`python videohash_cli.py compare <video_file1> <video_file2>`

3. Find duplicate videos in a given directory:

`python videohash_cli.py find_duplicates <directory> [--threshold <threshold>] [--recursive]`

- `threshold`: (optional) similarity threshold for considering videos as duplicates (default: 95.0)
- `recursive`: (optional) search for video files recursively in sub-directories

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
