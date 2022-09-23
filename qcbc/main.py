from . import __version__
import argparse
import logging
import sys

from .qcbc_ambiguous import setup_ambiguous_args, validate_ambiguous_args
from .qcbc_volume import setup_volume_args, validate_volume_args
from .qcbc_pdist import setup_pdist_args, validate_pdist_args
from .qcbc_content import setup_content_args, validate_content_args
from .qcbc_homopolymer import setup_homopolymer_args, validate_homopolymer_args

# Steps to add new subcommands
# Create qcbc_subcommand.py (create setup_subcmd_args, validate_subcmd_args, run_subcmd in that file)
# (in this file) from qcbc_subcmd import setup_subcmd_args, validate_subcmd_args
# Add setup_subcmd_args to command_to_parser along with its key==str(subcmd)
# Add validate_subcmd_args to COMMAND_TO_FUNCTION along with its key==str(subcmd)

logger = logging.getLogger(__name__)


def main():
    # setup parsers
    parser = argparse.ArgumentParser(
        description=f"qcbc {__version__}: Format sequence specification files"
    )
    parser.add_argument(
        "--verbose", help="Print debugging information", action="store_true"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        metavar="<CMD>",
    )

    # Setup the arguments for all subcommands
    command_to_parser = {
        "ambiguous": setup_ambiguous_args(subparsers),
        "content": setup_content_args(subparsers),
        "homopolymer": setup_homopolymer_args(subparsers),
        "pdist": setup_pdist_args(subparsers),
        "volume": setup_volume_args(subparsers),
    }

    # Show help when no arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 2:
        if sys.argv[1] in command_to_parser:
            command_to_parser[sys.argv[1]].print_help(sys.stderr)
        else:
            parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] %(levelname)7s %(message)s",
        level=logging.DEBUG if args.verbose else logging.INFO,
    )

    # Setup validator and runner for all subcommands (validate and run if valid)
    COMMAND_TO_FUNCTION = {
        "ambiguous": validate_ambiguous_args,
        "content": validate_content_args,
        "homopolymer": validate_homopolymer_args,
        "pdist": validate_pdist_args,
        "volume": validate_volume_args,
    }
    COMMAND_TO_FUNCTION[sys.argv[1]](parser, args)


if __name__ == "__main__":
    main()
