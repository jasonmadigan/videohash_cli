#!/usr/bin/env python3

import argparse
import sys
import os
import logging
from videohash import VideoHash
from tqdm import tqdm

def list_video_files(directory, recursive=False):
    video_files = []
    extensions = ('.mp4', '.avi', '.mkv', '.mov', '.flv', '.wmv')

    for root, dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(extensions):
                video_files.append(os.path.join(root, f))
        
        if not recursive:
            break
    return video_files

def main(args):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if args.subparser_name == "compute":
        hash = VideoHash(args.file)
        logging.info(f"VideoHash: {hash}")
    elif args.subparser_name == "compare":
        hash1 = VideoHash(args.file1)
        hash2 = VideoHash(args.file2)
        difference = hash1 - hash2
        similarity = 100 - difference
        logging.info(f"Comparing {args.file1} and {args.file2}")
        logging.info(f"Similarity: {similarity:.2f} %")
    elif args.subparser_name == "find_duplicates":
        video_files = list_video_files(args.directory, args.recursive)
        
        logging.info("Computing video hashes...")
        hashes = []
        for f in video_files:
            logging.info(f"Computing hash for {f}")
            hashes.append(VideoHash(f))

        duplicates = []

        logging.info("Comparing video files...")
        
        with tqdm(total=(len(video_files) * (len(video_files) - 1)) // 2) as progress_bar:
            for i, hash1 in enumerate(hashes):
                for j, hash2 in enumerate(hashes[i + 1:]):
                    logging.debug(f"Comparing {video_files[i]} and {video_files[i + j + 1]}")
                    difference = hash1 - hash2
                    similarity = 100 - difference
                    if similarity >= args.threshold:
                        duplicates.append((video_files[i], video_files[i + j + 1], similarity))
                    progress_bar.update(1)

        if duplicates:
            logging.info("Duplicates found:")
            for file1, file2, similarity in duplicates:
                logging.info(f"{file1} and {file2} have a similarity of {similarity:.2f} %")
        else:
            logging.info("No duplicates found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute and compare video hashes using the videohash library.")
    subparsers = parser.add_subparsers(dest="subparser_name")

    # Subparser for computing a video hash
    parser_compute = subparsers.add_parser("compute", help="Compute the video hash of a given video.")
    parser_compute.add_argument("file", type=str, help="Path to the video file.")

    # Subparser for comparing two video hashes
    parser_compare = subparsers.add_parser("compare", help="Compare two video files and show their similarity.")
    parser_compare.add_argument("file1", type=str, help="Path to the first video file.")
    parser_compare.add_argument("file2", type=str, help="Path to the second video file.")

    # Subparser for finding duplicate videos in a directory
    parser_find_duplicates = subparsers.add_parser("find_duplicates", help="Find duplicate videos in a given directory.")
    parser_find_duplicates.add_argument("directory", type=str, help="Path to the directory containing video files.")
    parser_find_duplicates.add_argument("--threshold", type=float, default=95.0, help="Similarity threshold for considering videos as duplicates (default: 95.0).")
    parser_find_duplicates.add_argument("--recursive", action="store_true", help="Search for video files recursively in sub-directories.")

    args = parser.parse_args()
    main(args)