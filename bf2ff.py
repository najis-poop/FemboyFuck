import sys

argv = sys.argv[1:]

if argv:
    try:
        i = open(argv[0])
        o = open(f'{argv[0]}.ff', 'w')
        for c in i.read():
            match c:
                case '+':
                    o.write('femboy ')
                case '-':
                    o.write('fuck ')
                case '>':
                    o.write('gay ')
                case '<':
                    o.write('bi ')
                case '.':
                    o.write('uwu ')
                case ',':
                    o.write('owo ')
                case '[':
                    o.write('twink ')
                case ']':
                    o.write('twink ')
        i.close()
        o.close()
    except FileNotFoundError:
        sys.stderr.write('File not found\n')
    except PermissionError:
        sys.stderr.write('No permission\n')