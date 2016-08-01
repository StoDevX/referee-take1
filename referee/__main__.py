from argparse import ArgumentParser

def args():
    argp = ArgumentParser()
    subparsers = argp.add_subparsers()

    serve = subparsers.add_parser('serve')
    serve.add_argument('-a', help='a flag')

    return argp.parse_args()


def main():
    print(args())

if __name__ == '__main__':
    main()
