

import sys
seek_index = dict()


def create_seek_index():
    global seek_index
    curr_offset = 0
    with open("Index.txt", "r") as index:
        for line in index:
            token = line.split(',')[0].split(':')[0]
            seek_index[token] = curr_offset
            curr_offset += (len(line)+1)


def main():
    create_seek_index()  # hyperlink: 34704489
