import argparse
import server

def arguments():
    argp = argparse.ArgumentParser()
    subparsers = argp.add_subparsers(title='subcommands')

    serve = subparsers.add_parser('serve')
    serve.add_argument('-a', help='a flag')
    serve.set_defaults(__command=server.run)

    return argp.parse_args()


def main():
    args = arguments()
    args.__command()

if __name__ == '__main__':
    main()
