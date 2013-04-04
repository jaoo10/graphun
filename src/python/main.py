import sys

def main():
    print "parametros:",
    for s in sys.argv[1:]:
        print s,
    print

if __name__ == "__main__":
    main()
