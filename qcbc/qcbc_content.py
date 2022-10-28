from qcbc.utils import load_bcs
from collections import Counter
import json
import sys
from scipy.stats import entropy
import numpy as np
import itertools


def setup_content_args(parser):
    parser_format = parser.add_parser(
        "content",
        description="compute base distribution (A,T,C,G counts/frequencies)",
        help="compute base distribution (A,T,C,G counts/frequencies)",
    )
    parser_format.add_argument("bc_file", help="Barcode file")
    parser_format.add_argument(
        "-o",
        metavar="OUT",
        help=("Path to output file"),
        type=str,
        default=None,
    )
    parser_format.add_argument(
        "-f", "--frequency", action="store_true", help=("Nucleotide frequencies")
    )
    parser_format.add_argument(
        "-e", "--entropy", action="store_true", help=("Fraction of max entropy")
    )
    parser_format.add_argument(
        "-T", "--transpose", action="store_true", help=("Content per position")
    )
    return parser_format


def validate_content_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    frequency = args.frequency
    ent = args.entropy
    transpose = args.transpose
    run_content(fn, o, frequency, ent, transpose)


# add -frequency, -entropy
def run_content(bcs_fn, o, frequency, ent, transpose):
    bcs, bcs_names = load_bcs(bcs_fn)

    if transpose:
        r = qcbc_content_T(bcs, bcs_names)
        if o:
            with open(o, "w") as f:
                f.write(f"pos\t")
                if ent:
                    f.write("ent\n")
                else:
                    f.write("A,T,C,G\n")
                for idx, b in enumerate(r):
                    if ent:
                        e = entropy(list(b["freq"].values()))
                        f.write(f"{idx}\t{e/np.log2(4):,.2f}\n")
                    elif frequency:
                        f.write(f"{idx}\t{','.join(map(str, b['freq'].values()))}\n")
                    else:
                        f.write(f"{idx}\t{','.join(map(str, b['count'].values()))}\n")
        else:
            print(f"pos\t", end="")
            if ent:
                print("ent\n", end="")
            else:
                print("A,T,C,G\n", end="")
            for idx, b in enumerate(r):
                if ent:
                    e = entropy(list(b["freq"].values()))
                    print(f"{idx}\t{e/np.log2(4):,.2f}")
                elif frequency:
                    print(f"{idx}\t{','.join(map(str, b['freq'].values()))}")
                else:
                    print(f"{idx}\t{','.join(map(str, b['count'].values()))}")

    else:
        r = qcbc_content(bcs, bcs_names)
        if o:
            with open(o, "w") as f:
                f.write("name\tseq\t")
                if ent:
                    f.write("ent\n")
                else:
                    f.write("A,T,C,G\n")
                for b in r:
                    if ent:
                        e = entropy(list(b["freq"].values()))
                        f.write(f"{b['name']}\t{b['seq']}\t{e/np.log2(4):,.2f}\n")
                    elif frequency:
                        f.write(
                            f"{b['name']}\t{b['seq']}\t{','.join(map(str, b['freq'].values()))}\n"
                        )
                    else:
                        f.write(
                            f"{b['name']}\t{b['seq']}\t{','.join(map(str, b['count'].values()))}\n"
                        )

        else:
            print("name\tseq\t", end="")
            if ent:
                print("ent\n", end="")
            else:
                print("A,T,C,G\n", end="")
            for b in r:
                if ent:
                    e = entropy(list(b["freq"].values()))
                    print(f"{b['name']}\t{b['seq']}\t{e/np.log2(4):,.2f}")
                elif frequency:
                    print(
                        f"{b['name']}\t{b['seq']}\t{','.join(map(str, b['freq'].values()))}"
                    )
                else:
                    print(
                        f"{b['name']}\t{b['seq']}\t{','.join(map(str, b['count'].values()))}"
                    )

    return True


def qcbc_content(bcs, bcs_names):
    d = {"A": 0, "T": 0, "C": 0, "G": 0}
    r = []
    for b, n in zip(bcs, bcs_names):
        c = Counter(b)
        # ATCG
        length = len(b)
        dist = {k: c.get(k, 0) for (k, v) in d.items()}
        freq = {k: v / length for (k, v) in dist.items()}
        r.append({"name": n, "seq": b, "length": length, "count": dist, "freq": freq})
    return r


# todo, entropy
def qcbc_content_T(bcs, bcs_names):
    d = {"A": 0, "T": 0, "C": 0, "G": 0}
    r = []
    bcs_T = list(map(list, itertools.zip_longest(*bcs, fillvalue=None)))
    for b in bcs_T:
        c = Counter(b)
        # ATCG
        length = len(b)
        dist = {k: c.get(k, 0) for (k, v) in d.items()}
        freq = {k: v / length for (k, v) in dist.items()}
        r.append({"count": dist, "freq": freq})
    return r
