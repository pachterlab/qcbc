from qcbc.utils import load_bcs
from collections import Counter
import json
import sys


def setup_content_args(parser):
    parser_format = parser.add_parser(
        "content",
        description="Compute max barcode content",
        help="Compute max barcode content",
    )
    parser_format.add_argument("bc_file", help="Barcode file")
    parser_format.add_argument(
        "-o",
        metavar="OUT",
        help=("Path to output file"),
        type=str,
        default=None,
    )
    return parser_format


def validate_content_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    run_content(fn, o)


def run_content(bcs_fn, o):
    bcs, bcs_names = load_bcs(bcs_fn)
    r = qcbc_content(bcs, bcs_names)
    if o:
        with open(o, "w") as f:
            json.dump(r, f, indent=4)
            sys.exit()
    else:
        print(json.dumps(r, indent=4))

    return True


def qcbc_content(bcs, bcs_names):
    d = {"A": 0, "C": 0, "T": 0, "G": 0}
    r = []
    for b, n in zip(bcs, bcs_names):
        c = Counter(b)
        # ATCG
        length = len(b)
        dist = {k: c.get(k, 0) for (k, v) in d.items()}
        freq = {k: v / length for (k, v) in dist.items()}
        r.append({"name": n, "seq": b, "length": length, "count": dist, "freq": freq})
    return r
