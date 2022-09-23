from qcbc.utils import load_bcs
import json
import sys


def setup_homopolymer_args(parser):
    parser_format = parser.add_parser(
        "homopolymer",
        description="compute homopolymer distribution",
        help="compute homopolymer distribution",
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


def validate_homopolymer_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    run_homopolymer(fn, o)


def run_homopolymer(bc_fn, o):
    bcs, bcs_names = load_bcs(bc_fn)
    bc_len = min([len(i) for i in bcs])

    r = qcbc_homopolymer(bcs, bcs_names)
    if o:
        with open(o, "w") as f:
            json.dump(r, f, indent=4)
            sys.exit()
    else:
        for b in r:
            print(
                f"{b['name']}\t{b['seq']}\t{','.join(map(str, b['homopolymers'].values()))}"
            )

    return True


def qcbc_homopolymer(bcs, bcs_names):
    l = 1
    lst = []
    for barcode, name in zip(bcs, bcs_names):
        start = end = 0
        base = -1
        d = {i: 0 for i in range(2, len(barcode) + 1)}
        for b in barcode:
            if b != base:
                if end - start > l:
                    d[end - start] += 1
                start = end
                base = b
            end += 1
        if end - start > l:
            d[end - start] += 1
        lst.append({"name": name, "seq": barcode, "homopolymers": d})
    return lst
