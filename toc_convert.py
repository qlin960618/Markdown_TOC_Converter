import argparse







if __name__=='__main__':
    parser = argparse.ArgumentParser(description='This is a TOC processor for github')
    parser.add_argument('--input-file', metavar='path', type=str, required=True,
                help='Set the input file')
    parser.add_argument('--output-file', metavar='path', type=str, required=True,
                help='Set the output file')

    parser.add_argument('--location_identifier', metavar='string', type=str, required=False,
                default="[TOC]",
                help='Set the search string for TOC subsitution location')

    args = parser.parse_args()
    print(args)
