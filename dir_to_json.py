import argparse
import json
import os
import sys

parser = argparse.ArgumentParser(description='''Generate a JSON of all files within a directory. 
                                    Optionally limit those to one or more keywords.''')

parser.add_argument('-k', '--keywords', type=str, nargs='+', default='',
                    help='''Pass keywords into argparse to limit the output of files. 
                    The most common usage here is to identify a file extension.
                    Remember, this keyword is INCLUSIVE. If nothing is passed, everything is included.
                    If an argument is passed, ONLY files matching that argument are included.
                    Separate keywords by string and remember to enclose  with single quotes if necessary!''')

parser.add_argument('-r', '--root', type=str, nargs=1, default='',
                    help='''Pass the root folder to start from. Path may be relative or absolute.''')

parser.add_argument('-x', '--exclude', type=str, nargs='+', default='',
                    help='''Exclude keywords from the search. Words the same as -k but is exclusive.''')

parser.add_argument('-o', '--output', type=str, nargs=1, default='output.json',
                    help='''Name of the output file.''')
parser.add_argument('-v', '--verbose', type=bool, nargs=1, default=False,
                    help='''Verbose mode''')

args = parser.parse_args()


def dir_to_json(rootpath='', keywords='', exclude='', output='output.json', verbose=False) -> None:
    rootpath = rootpath[0] if len(rootpath) > 0 else rootpath
    filelist = []

    for (root, dir, files) in os.walk(rootpath, topdown=False):
        for filename in files:
            if verbose:
                print(os.path.join(root.split('/')[-1], filename).replace('\\', '/')) if any(
                    x in filename for x in keywords) and any(y not in filename for y in exclude) else None

            filelist.append(os.path.join(root.split('/')[-1], filename).replace('\\', '/')) if any(
                x in filename for x in keywords) and any(x not in filename for x in exclude) else None

    json_file = {}
    json_file['files'] = filelist

    print('Saving file to {}'.format(output))
    with open(os.path.join(rootpath, output), 'w') as f:
        json.dump(json_file, f, indent=4)


def main():
    dir_to_json(rootpath=args.root,
                keywords=args.keywords,
                exclude=args.exclude,
                output=args.output[0],
                verbose=args.verbose)


if __name__ == '__main__':
    main()
