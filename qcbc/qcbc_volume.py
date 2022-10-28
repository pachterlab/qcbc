from qcbc.utils import load_bcs


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
    return parser_format


def validate_volume_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    run_volume(fn, o)


def run_volume(bc_fn, o):
    bcs, bcs_names = load_bcs(bc_fn)
    bc_len = min([len(i) for i in bcs])

    n = qcbc_volume(bc_len)
    nbcs = len(bcs)
    if o:
        with open(o, "w") as f:
            f.write(
                f"{nbcs} out of {n:,.0f} possible unique barcodes representing {nbcs/n*100:,.4f}%\n"
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
