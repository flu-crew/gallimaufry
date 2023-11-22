#!/usr/bin/env python3
"""
This script is designed to take an alignment fasta file with gaps at the
beginning and end of sequences and removes them.  This assumes that all
sequences have been trimmed to the same size and that this trimming will not
shift the alignment.
Created on Jun 10, 2020 by David E. Hufnagel
"""

import sys

inp = open(sys.argv[1])
out = open(sys.argv[2], "w")


for line in inp:
    if not line.startswith(">"):
        seq = line.strip().strip("-")
        newline = "%s\n" % (seq)
        out.write(newline)
    else:
        out.write(line)



inp.close()
out.close()


