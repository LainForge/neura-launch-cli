import argparse
from utils import init_nl, add_token


def main():
    parser = argparse.ArgumentParser(
        prog="neura-launch-cli",
        description="neura-launch cli tool helps you upload your ml models to cloud",
    )

    sub_parser = parser.add_subparsers()

    # init project subparser
    init_parser = sub_parser.add_parser("init", help="Initialize neura-launch")
    init_parser.set_defaults(func=init_nl)

    # manage token subparser
    token_parser = sub_parser.add_parser(
        "add_token", help="Add the token for the current project"
    )
    token_parser.set_defaults(func=add_token)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
