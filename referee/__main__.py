import argparse


def arguments():
    argp = argparse.ArgumentParser()
    subparsers = argp.add_subparsers(title='subcommands')

    serve = subparsers.add_parser('')
    serve.set_defaults(command=lambda:)

    return argp.parse_args()


def main():
    args = arguments()
    args.command()

if __name__ == '__main__':
    main()
