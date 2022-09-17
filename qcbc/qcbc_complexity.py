from qcbc.utils import load_bcs


def setup_complexity_args(parser):
    parser_format = parser.add_parser(
        "complexity",
        description="Compute max barcode complexity",
        help="Compute max barcode complexity",
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


def validate_complexity_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    run_complexity(fn, o)


def run_complexity(bc_fn, o):
    bcs, bcs_names = load_bcs(bc_fn)
    bc_len = min([len(i) for i in bcs])
    print(f"{qcbc_complexity(bc_len):,.0f}")
    # how many if you impose a hamming distance constrain?
    return True


def qcbc_complexity(min_bc_len):
    max_bcs = 4**min_bc_len
    return max_bcs
