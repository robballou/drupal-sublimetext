#!/usr/bin/env python

import argparse
import os
import sys

def create_snippets(functions):
    snippets = {}
    for function in functions:

        snippet_function = function
        snippet_function_name = function
        if function.startswith('theme_'):
            snippet_function_name = snippet_function_name.replace('theme_', 'theme_preprocess_')
            snippet_function = snippet_function_name.replace("theme_", "${TM_FILENAME/(.*)\..*/$1/}_")
        elif function.startswith('hook_'):
            snippet_function = snippet_function.replace('hook_', "${TM_FILENAME/(.*)\..*/$1/}_")

        full_function = "/**\n * Implements %s().\n */\nfunction %s(%s) {\n\t$0\n}" % (
            snippet_function_name,
            snippet_function,
            "&\$vars"
        )
        snippet_filename = "%s.sublime-snippet" % function
        snippet = """<snippet>\n\t<tabTrigger>pre_%(function)s</tabTrigger>\n\t<scope>source.php</scope>\n<content><![CDATA[%(full_function)s]]></content>\n</snippet>""" % (
            {"function": function.replace('theme_', ''), "full_function": full_function, "raw_function_name": function}
        )
        snippets[snippet_filename] = snippet
    return snippets

def get_functions(lines):
    return [line.strip() for line in lines]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create snippets from function names in a file')
    parser.add_argument('-s', '--no-snippets',
        dest="no_snippets",
        action="store_true",
        default=False)
    parser.add_argument('file', help="The file that lists function names")
    parser.add_argument('destination',
        default=None,
        nargs="?",
        help="The location where the snippets will be created")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print "ERROR: could not find file: %s" % args.file
        sys.exit(1)

    lines = file(args.file)
    functions = get_functions(lines)
    snippets = create_snippets(functions)

    if args.no_snippets:
        for snippet in snippets:
            print "=" * 72
            print snippet
            print "=" * 72
            print snippets[snippet]
            print "=" * 72
    else:
        # create them
        if not os.path.exists(args.destination):
            os.mkdir(args.destination)
        for snippet in snippets:
            filename = "%s/%s" % (args.destination, snippet)
            if not os.path.exists(filename):
                print "[ ] Creating %s" % filename
                f = open(filename, 'w')
                f.write(snippets[snippet])
                f.close()
            else:
                print "[ ] Skipping %s" % filename
