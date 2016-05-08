# coding: utf-8

import argparse
import os

import starwar

SUPPORTED_BACKEND = ('json', 'mongodb', 'mysql', 'sqlite')


def expand_path(path):
    """Return the absolute path for a given path.

    Expand `~` and `.` characters, transform relative path to absolute one.
    """
    if path is None:
        path = 'data'

    path = os.path.abspath(os.path.expanduser(path))
    try:
        if not os.path.isdir(path):
            os.mkdir(path)
    except OSError as err:
        print("Can not create directory: %s" % err.message)
        return None
    return path


def main():
    parser = argparse.ArgumentParser(description="Mystarwar Cli: Own your own starwar dataset in secs.")
    parser.add_argument('-b', '--backend', dest='backend', default='json',
                        help='Backend to store the dataset, current support: json, mysql, mongo, sqlite.')
    parser.add_argument('-l', '--location', dest='location',
                        help='The backend location: directory for json backend, '
                             'connection url for mysql or mongo backend, filename for sqlite backend')

    args = parser.parse_args()
    args.backend = args.backend.lower()

    if args.backend not in SUPPORTED_BACKEND:
        raise ValueError(
                "Support %s to save data, but get %s" % (SUPPORTED_BACKEND,
                                                         args.backend))

    if args.backend == 'json':
        args.location = expand_path(args.location)

    if not args.backend:
        return

    c = starwar.StarwarCrawler(['http://swapi.co/api/'],
                                backend=args.backend,
                                location=args.location)
    c.run()


if __name__ == '__main__':
    main()