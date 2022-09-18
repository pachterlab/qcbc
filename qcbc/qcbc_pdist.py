# pdist on the sequences, or pdist on the kmers
from qcbc.utils import rev_c, load_bcs
import numpy as np


def setup_pdist_args(parser):
    parser_format = parser.add_parser(
        "pdist",
        description="Compute max barcode pdist",
        help="Compute pairwise distance between barcodes",
    )
    parser_format.add_argument("bc_file", help="Barcode file")
    parser_format.add_argument(
        "-o",
        metavar="OUT",
        help=("Path to output file"),
        type=str,
        default=None,
    )
    parser_format.add_argument("-rc", "--reverse-complement", action="store_true")
    return parser_format


def validate_pdist_args(parser, args):
    # if everything is valid the run_format
    fn = args.bc_file
    o = args.o
    rc = args.reverse_complement
    run_pdist(fn, o, rc)


def run_pdist(bc_fn, o, rc):
    bcs, bcs_names = load_bcs(bc_fn)
    # bc_len = min([len(i) for i in bcs])
    # print(f"{qcbc_pdist(bc_len):,.0f}")
    dists = qcbc_pdist(bcs)
    ridx, cidx = np.triu_indices(len(bcs), k=1)
    for i, j, d in zip(ridx, cidx, dists):
        bc1 = bcs[i]
        bc2 = bcs[j] if not rc else rev_c(bcs[j])
        bc1_name = bcs_names[i]
        bc2_name = bcs_names[j] if not rc else bcs_names[j] + "_rc"

        print(bc1, bc1_name, bc2, bc2_name, d, sep="\t")
    # how many if you impose a hamming distance constrain?
    return True


def qcbc_pdist(bcs, rc=False):
    n_bcs = len(bcs)
    mat = np.zeros((n_bcs, n_bcs))
    mat_rc = np.zeros((n_bcs, n_bcs))
    for i in range(len(bcs)):
        for j in range(i, len(bcs)):
            first = np.array(list(bcs[i]))
            second = np.array(list(bcs[j]))
            second_rc = np.array(list(rev_c(bcs[j])))
            mat[i, j] = (first != second).sum()
            mat_rc[i, j] = (first != second_rc).sum()
    if rc:
        return mat_rc[np.triu_indices(mat_rc.shape[0], k=1)]
    return mat[np.triu_indices(mat.shape[0], k=1)]
