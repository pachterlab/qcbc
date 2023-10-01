from qcbc.utils import load_bcs
import scipy.special


def setup_volume_args(parser):
    parser_format = parser.add_parser(
        "volume",
        description="compute size of barcode space",
        help="compute size of barcode space",
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
        "-d",
        metavar="MIN_HAMMING_DISTANCE",
        help=("Minimum hamming distance between barcodes"),
        type=int,
        default=None,
        required=False,
    )
    return parser_format


def validate_volume_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    d = args.d
    return run_volume(fn, o, d)


def run_volume(bc_fn, o, d=None):
    bcs, bcs_names = load_bcs(bc_fn)
    bc_len = min([len(i) for i in bcs])
    if d:
        n = qcbc_hamming_bound(bc_len, d)
    else:
        n = qcbc_volume(bc_len)
    nbcs = len(bcs)
    if o:
        with open(o, "w") as f:
            if d:
                f.write(
                    f"{nbcs} out of {n:,.0f} barcodes (with minimum pairwise Hamming distance {d:,}) representing {nbcs/n*100:,.4f}%\n"
                )
            else:
                f.write(
                    f"{nbcs} out of {n:,.0f} possible unique barcodes representing {nbcs/n*100:,.4f}%\n"
                )
    else:
        if d:
            print(
                f"{nbcs} out of {n:,.0f} possible barcodes (with minimum pairwise Hamming distance {d:,}) representing {nbcs/n*100:,.4f}%"
            )
        else:
            print(
                f"{nbcs} out of {n:,.0f} possible unique barcodes representing {nbcs/n*100:,.4f}%"
            )
    # how many if you impose a hamming distance constrain?
    return True


def qcbc_volume(min_bc_len):
    max_bcs = 4**min_bc_len
    return max_bcs


def qcbc_hamming_bound(N, D, q=4):
    # N = length of codeword
    # D is min ham
    # q is alphabet size    

    t = (D - 1) // 2
    denominator = sum(scipy.special.comb(N, i) * (q - 1)**i for i in range(t + 1))
    if denominator == 0:
        return 0  # Avoid division by zero
    return q**N / denominator