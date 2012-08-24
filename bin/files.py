#!/usr/bin/env python

import argparse
import os
import re
# import subprocess


def create_snippets(functions):
    snippets = {}
    for function in functions:
        if function[0].startswith('_'):
            continue

        # function name
        snippet_args = parse_function_arguments(function[1])
        function_name = function[0]
        full_function = "%s(%s)" % (function_name, snippet_args)
        if function_name.startswith('hook_'):
            function_name = "h.%s" % (function_name.replace("hook_", ""))
            function_args = function[1]
            if not function_args:
                function_args = ""
            full_function = "/**\n * Implements %s().\n */\nfunction %s(%s) {\n\t$0\n}" % (
                function[0],
                function[0].replace("hook_", "${TM_FILENAME/(.*)\..*/$1/}_"),
                function_args.replace("$", "\$")
            )

        snippet_filename = "%s.sublime-snippet" % function[0]
        snippet = """<snippet>\n\t<tabTrigger>%(function)s</tabTrigger>\n\t<scope>source.php</scope>\n<content><![CDATA[%(full_function)s]]></content>\n</snippet>""" % (
            {"function": function_name, "args": snippet_args, "full_function": full_function, "raw_function_name": function[0]}
        )

        snippets[snippet_filename] = snippet
    return snippets


def get_functions(path, files):
    if not os.path.exists(path) or not os.path.exists(files):
        raise Exception('Directory or files path do not exist')

    if not os.path.isdir(path):
        raise Exception('Directory path is not a directory: %s' % path)

    if not os.path.isfile(files):
        raise Exception('Files path is not a file: %s' % files)

    functions = []

    # read file names
    f = open(files)
    filenames = f.readlines()
    f.close()

    function = re.compile(r'^\s*function\s*([A-Za-z0-9\-_]+)\s*\(([^\)]+)?\)\s*{')

    for filename in filenames:
        filename = filename.strip()
        filepath = "%s/%s" % (path, filename)
        print "[ ] Scanning: %s" % filepath

        try:
            this_file = open(filepath)
            this_file_lines = this_file.readlines()

            for line in this_file_lines:
                matches = function.search(line)
                if matches:
                    functions.append(matches.groups())

            this_file.close()
            print "[x] Done\n"
        except IOError:
            print "[!] Could not read: %s" % filename

    return functions


def get_optional_arguments(args, count):
    if len(args) == 0:
        return ""

    args_list = "${%d:, ${%d:%s}" % (count, count + 1, args[0])

    if len(args) > 1:
        args_list = "%s%s" % (args_list, get_optional_arguments(args[1:], count + 2))

    args_list = "%s}" % args_list
    return args_list


def parse_function_arguments(args):
    if not args:
        return ''
    args = args.split(',')
    new_args = {'args': [], 'optional': []}
    for arg in args:
        arg = arg.strip()
        if arg.find('=') < 0:
            # get the argument name
            arg_name = arg[1:]
            if arg[0:1] == '&': arg_name = arg[2:]

            # add it to the arguments list
            new_args['args'].append(arg_name)
        else:
            # optional arguments

            # get the argument name
            arg_parts = arg.split(' ')
            arg_name = arg_parts[0][1:]
            if arg_parts[0][0:1] == '&': arg_name = arg_parts[0][2:]

            # add it to the argument list
            new_args['optional'].append(arg_name)

    # build our list of arguments
    count = 1
    args_list = ""
    for required_arg in new_args['args']:
        # if this isn't empty, add a comma
        if len(args_list) != 0:
            args_list = "%s, " % args_list
        args_list = "%s${%d:%s}" % (args_list, count, required_arg)
        count += 1

    # attach our optional arguments
    args_list = "%s%s" % (args_list, get_optional_arguments(new_args['optional'], count))

    return args_list

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get functions from a directory')
    parser.add_argument('path', help="The directory path")
    parser.add_argument('files', help="The files list file path")
    parser.add_argument('destination',
        default=None,
        nargs="?",
        help="The location where the snippets will be created")
    parser.add_argument('-s', '--no-snippets',
        dest="no_snippets",
        action="store_true",
        default=False)
    args = parser.parse_args()

    functions = get_functions(args.path, args.files)

    if not args.no_snippets:
        snippets = create_snippets(functions)

        if not args.destination:
            for snippet in snippets:
                print snippet
                print "====================="
                print snippets[snippet]
                print ""
        else:
            if not os.path.exists(args.destination):
                os.mkdir(args.destination)

            for snippet in snippets:
                filename = "%s/%s" % (args.destination, snippet)
                print "[ ] Creating %s" % filename
                f = open(filename, 'w')
                f.write(snippets[snippet])
                f.close()
    else:
        functions.sort()
        for function in functions:
            print function
