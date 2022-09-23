


# qcbc
`qcbc` is a python package to quality control synthetic barcode sequences for orthogonal sequencing-based assays such as:
- [Perturb-Seq](https://doi.org/10.1016/j.cell.2022.05.013)
- [TAPSeq](https://doi.org/10.1038/s41592-020-0837-5)
- [10x CRISPR](https://www.10xgenomics.com/products/single-cell-crispr-screening)
- [CiteSeq](https://doi.org/10.1038/nmeth.4380)
- [Clicktag](https://doi.org/10.1038/s41587-019-0372-z)
- [Multiseq](https://doi.org/10.1038/s41592-019-0433-8)
- [10x Feature Barcoding](https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/feature-bc)

## Installation

The development version can be installed with
```bash
pip install git+https://github.com/sbooeshaghi/qcbc
```

## Usage
`qcbc` consists of four subcommands:

```
$ qcbc
usage: qcbc [-h] [--verbose] <CMD> ...

qcbc 0.0.0: Format sequence specification files

positional arguments:
  <CMD>
    volume     Compute max barcode volume
    ambiguous  Find ambiguous barcodes by ec
    pdist      Compute pairwise distance between barcodes
    content    Compute max barcode content
    homopolymer
               Compute homopolymer distribution
```

Barcode files are expected to contain both the barcode sequence and a name associated with the barcode, separated by a tab. For example

```
$ cat barcodes.txt
AGCAGTTACAG tag1
CTTGTACCCAG tag2

$ cat -t barcodes.txt 
CATGGAGGCG^Itag1
AGCAGTTACAG^Itag2
```
Note that `cat -t file.txt` converts `<tabs>` into `^I` and can be used to verify that the file is properly setup.

### `qcbc ambiguous`: find barcodes with shared subsequence

Find barcodes that share subsequences of a given length.
```
qcbc ambiguous -l <length> <bc_file>
```
- optionally, `-rc` can be used to check the reverse complement of the subsequences.
- `<length>` corresponds to the subsequence length used to evaluate ambiguity between barcodes.
- `<bc_file>` corresponds to the barcode file.

#### Examples
```bash
# check ambiguous barcodes by subsequences of length 6
$ qcbc ambiguous -l 3 barcodes.txt
CAG	tag1,tag1,tag2
TAC	tag1,tag2
```

### `qcbc content`: compute base distribution
Compute the base distribution within each barcode.
```
qcbc content <bc_file>
```
- optionally, specify `-- frequency` to return the base distribution fraction
- optionally, specify `--entropy` to return the entropy of the base distribution fraction relative to the max entropy.
- `<bc_file>` corresponds to the barcode file.

#### Examples
```
$ qcbc content -e barcodes.txt
tag1	AGCAGTTACAG	0.67
tag2	CTTGTACCCAG	0.67
```

### `qcbc homopolymer`: compute homopolymer distribution
Find the number of homopolymers of length two or greater.
```
qcbc homopolymer <bc_file>
```
- `<bc_file>` corresponds to the barcode file.

#### Examples
```
$ qcbc homopolymer barcodes.txt
tag1	AGCAGTTACAG	1,0,0,0,0,0,0,0,0,0
tag2	CTTGTACCCAG	1,1,0,0,0,0,0,0,0,0
```

### `qcbc pdist`: compute pairwise distance 
Compute the pairwise hamming distance between barcodes.
```
qcbc pdist <bc_file>
```
-   optionally,  `-rc`  can be used to check the reverse complement of the subsequences.
- `<bc_file>` corresponds to the barcode file.

#### Examples
```
$ qcbc pdist barcodes.txt
AGCAGTTACAG	tag1	CTTGTACCCAG	tag2	8.0
```

### `qcbc volume`:  compute size of barcode space
Compute the fraction of barcode space occupied by the given barcodes.
```
qcbc volume <bc_file>
```
- `<bc_file>` corresponds to the barcode file.

#### Examples

```
$  qcbc volume barcodes.txt
2 out of 4,194,304 possible unique barcodes representing 0.0000%
```

## Contributing

Thank you for wanting to improve `qcbc`. If you have a bug that is related to `qcbc` please create an issue. The issue should contain

- the `qcbc` command ran,
- the error message, and
- the `qcbc` and python version.

If you'd like to add assays sequence specifications or make modifications to the `qcbc` tool please do the following:

1. Fork the project.
```
# Press "Fork" at the top right of the GitHub page
```

2. Clone the fork and create a branch for your feature
```bash
git clone https://github.com/<USERNAME>/qcbc.git
cd qcbc
git checkout -b cool-new-feature
```

3. Make changes, add files, and commit
```bash
# make changes, add files, and commit them
git add path/to/file1.py path/to/file2.py
git commit -m "I made these changes"
```

4. Push changes to GitHub
```bash
git push origin cool-new-feature
```

5. Submit a pull request

If you are unfamilar with pull requests, you find more information on the [GitHub help page.](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)
