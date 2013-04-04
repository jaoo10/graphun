import sys

def main():
    print("parametros: ", end="")
    for s in sys.argv[1:]:
        print(s, end=" ")
    print()

if __name__ == "__main__":
    main()
