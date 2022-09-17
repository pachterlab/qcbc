from collections import defaultdict


def load_bcs(bcs_fn):
    bcs = []
    bcs_names = []
    with open(bcs_fn, "r") as f:
        for line in f.readlines():
            l_strip = line.strip()
            bc, n = l_strip.split("\t")
            bcs.append(bc)
            bcs_names.append(n)
    return (bcs, bcs_names)


def kmerize(s, k):
    L = len(s)
    return [s[i : i + k] for i in range(L - k + 1)]


complement = {"A": "T", "C": "G", "G": "C", "T": "A"}


def rev_c(seq):
    bases = list(seq)
    bases = reversed([complement.get(base, base) for base in bases])
    bases = "".join(bases)
    return bases


def make_ec(bcs, bcs_names, k=None, rc=False):
    length = min([len(i) for i in bcs])
    if not k:
        k = length
    d = defaultdict(list)
    for bc, bc_name in zip(bcs, bcs_names):
        # forward strand
        if rc:
            bc = rev_c(bc)
            bc_name = f"{bc_name}_rc"
        kmers = kmerize(bc, k)
        for kmer in kmers:
            d["".join(kmer)].append(bc_name)
    return d
