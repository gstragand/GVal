import os
import sys
import getopt
import json

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
    options, remainder = getopt.getopt(sys.argv[1:], 'i:e:h' , ['i=', 'input=', 'element=', 'help', ])
    for opt, arg in options:
        if opt in ('-i', '--input'):
            input_dir = arg
        elif opt in ('-e', '--element'):
            element = args
    if element is "":
        sys.exit(0)
    print 'Input directory: ' + input_dir
    print 'JSON element: ' + element
    distribution = dict()
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                with open(subdir + '/' + file, 'r') as f:
                    print "Processing: " + file
                    for line in f.readlines():
                        json_data = json.loads(line)
                        value = json_data[element] if element in json_data else ""
                        if value in distribution:
                            distribution[value] = distribution[value] + 1
                        else:
                            distribution[value] = 0
                f.close()
    for k, v in sorted(distribution.iteritems(), key=lambda (k,v): (v * -1,k)):
        print u'{0}: {1}'.format(k, v)
