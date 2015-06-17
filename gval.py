import os
import sys
import getopt
import json


def getkey(arg):
    if isinstance(arg, basestring):
        return repr(arg)
    try:
        return '<' + ", ".join(getkey(x) for x in arg) + '>'
    except TypeError:
        return repr(arg)

if __name__ == '__main__':
    DOC = \
        '     -e, --element\n' + \
        '          JSON element to distribute\n' + \
        '     -i, --input\n' + \
        '          Input directory\n' + \
        '     -h, --help\n' + \
        '          This message\n'

    if len(sys.argv) < 2:
        print(DOC)
        sys.exit(0)
    if '-h' in sys.argv or '--help' in sys.argv:
        print(DOC)
        sys.exit(0)
    input_dir = "."
    element = ""
    options, remainder = getopt.getopt(sys.argv[1:], 'i:e:h', ['i=', 'input=', 'element=', 'help', ])
    for opt, arg in options:
        if opt in ('-i', '--input'):
            input_dir = arg
        elif opt in ('-e', '--element'):
            element = arg
    if element is "":
        sys.exit(0)
    print 'Input directory: ' + input_dir
    print 'JSON element: ' + element
    distribution = dict()
    for subdir, dirs, files in os.walk(input_dir):
        for workfile in files:
            if workfile.endswith(".json"):
                with open(subdir + '/' + workfile, 'r') as f:
                    print "Processing: " + workfile
                    for line in f.readlines():
                        try:
                            json_data = json.loads(line)
                            value = getkey(json_data[element] if element in json_data else "")
                            if value in distribution:
                                distribution[value] += 1
                            else:
                                distribution[value] = 1
                        except Exception as details:
                            print details
                            key = workfile + ": " + str(details).encode('utf-8')
                            if key in distribution:
                                distribution[key] += 1
                            else:
                                distribution[key] = 1
                            pass
                        finally:
                            f.close()
    for k, v in sorted(distribution.iteritems(), key=lambda (k, v): (v * -1, k)):
        print u'{0}: {1}'.format(k, v)
