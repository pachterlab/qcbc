qcbc/qcbc_homopolymer.pyfrom collections import defaultdict
import logging
from qcbc.utils import load_bcs, make_ec

logger = logging.getLogger(__name__)

# TODO want to be able to get ambigouos seqs for multiple lengths


def setup_ambiguous_args(parser):
    parser_format = parser.add_parser(
        "ambiguous",
        description="find barcodes with shared subsequence",
        help="find barcodes with shared subsequence",
    )
    parser_format.add_argument("bc_file", help="Barcode file")
    parser_format.add_argument(
        "-l",
        metavar="LENGTH",
        help=("Length of subsequence (default: shortest barcode)"),
        type=int,
        default=-1,
    )
    parser_format.add_argument(
        "-o",
        metavar="OUT",
        help=("Path to output file"),
        type=str,
        default=None,
    )
    # default value is false
    parser_format.add_argument("-rc", "--reverse-complement", action="store_true")
    return parser_format


def validate_ambiguous_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    rc = args.reverse_complement
    subseq_l = args.l
    run_ambiguous(fn, o, subseq_l, rc)


# setup variables
def run_ambiguous(bc_fn, o, subseq_l, rc):
    bcs, bcs_names = load_bcs(bc_fn)
    bc_len = min([len(i) for i in bcs])
    optimal_l = bc_len if bc_len % 2 else bc_len - 1
    if subseq_l == -1:
        subseq_l = optimal_l
    if subseq_l < 2 or subseq_l > optimal_l:
        logger.warning(
            f"Length of {subseq_l} specified with barcode length {bc_len}. Using {optimal_l} instead."
        )
        subseq_l = optimal_l
    ecs = make_ec(bcs, bcs_names, k=subseq_l, rc=rc)
    # how many if you impose a hamming distance constrain?

    for ec in qcbc_ambiguous(ecs):
        if o:
            with open(o, "w") as f:
                for k, v in ec.items():
                    f.write(f"{k}\t")
                    for i in v[:-1]:
                        f.write(f"{i},")
                    f.write(f"{v[-1]}\n")
        else:
            for k, v in ec.items():
                print(f"{k}\t", end="")
                for i in v[:-1]:
                    print(f"{i},", end="")
                print(f"{v[-1]}")
    return True


# run qcbc
def qcbc_ambiguous(*list_ecs):  # why 9?
    ambig_bcs = []
    for ecs in list_ecs:
        # find the ambiguous barcodes
        ambig = ambig_ecs(ecs)

        # append the ambig barcodes to abmig_bcs
        ambig_bcs.append(ambig)
    return ambig_bcs


def ambig_ecs(ecs):
    ambig = defaultdict(list)
    for k, v in ecs.items():
        if len(v) > 1:
            ambig[k] = v
    return ambig
