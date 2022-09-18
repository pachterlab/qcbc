from collections import defaultdict
import numpy as np


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


def ham(k1, k2):
    if len(k1) != len(k2):
        raise "kmers not the same length"
    first = np.array(list(k1))
    second = np.array(list(k2))
    dist = (first != second).sum()
    return dist


# currently not used but may be useful?
def merge_ecs(ecs1, ecs2):
    m = defaultdict(set)

    uniq = set(list(ecs1.keys()) + list(ecs2.keys()))
    print(f"{len(uniq):,.0f} unique kmers")
    for k in uniq:
        m[k].update(ecs2[k])
        m[k].update(ecs1[k])
    return m


# used to count ambiguous barcodes after running qcbc_ambiguous
def list_ambiguous(ambig_bcs):
    a = set()
    abcs = []
    for i in ambig_bcs:
        for k, v in i.items():
            a.update(v)
        abcs.append(a)
        a = set()
    return abcs


# currently not used but may be useful
def make_rev_ec(ec):
    rev_ec = {}
    for k, v in ec.items():
        for n in v:
            rev_ec[n] = k

    return rev_ec
