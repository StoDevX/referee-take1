import argparse
import linter
import notifier
import specs


def arguments():
    argp = argparse.ArgumentParser()
    subparsers = argp.add_subparsers(title='subcommands')

    serve = subparsers.add_parser('lint')
    serve.set_defaults(command=linter.lint_file)

    serve = subparsers.add_parser('check-spec')
    serve.set_defaults(command=specs.check_spec)

    serve = subparsers.add_parser('send-email')
    serve.set_defaults(command=notifier.send_email)

    return argp.parse_args()


def main():
    args = arguments()
    args.command()

if __name__ == '__main__':
    main()
