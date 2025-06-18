#!/usr/bin/python3
# -*- coding: utf-8 -*-
import argparse
import re
import random as rnd
from statistics import median_low

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

parser = argparse.ArgumentParser(description='HammerTime: compute the pairwise Hamming distances between two groups '
                                             'of sequences in an alignment',
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
parser._optionals.title = "Arguments"
parser.add_argument('-s', type=str, action='store', dest='alignment',
                    help='Path to the FASTA sequence alignment to extract groups from', required=True)
parser.add_argument('-g1', type=str, action='store', dest='group1',
                    help='REGEX to specify the FIRST group of sequences', required=True)
parser.add_argument('-g2', type=str, action='store', dest='group2',
                    help='REGEX to specify the SECOND group of sequences', required=True)
parser.add_argument('-i', '--ignore-gaps', action='store_true', dest='ignore_gaps',
                    help="Doesn't count the mismatches between two sequences when one is a gap")
parser.add_argument('-p', action='store', dest='pairwise_mat',
                    help='Specify a path to output a pairwise comparison log file.')
parser.add_argument('--max-comp', action='store', dest='max_comp', type=int,
                    help="The maximum number of pairwise comparisons to make (Default: 1000)", default=1000)


def compute_distance(r1: SeqRecord, r2: SeqRecord, ignore_gaps: bool):
    dist = 0
    for i, l1 in enumerate(r1.seq):
        l2 = r2.seq[i]
        if (l1 == '-' or l2 == '-') and ignore_gaps:
            continue
        if l1 != l2:
            dist += 1
    return dist


def parse_args():
    args = parser.parse_args()
    aln = list(SeqIO.parse(args.alignment, 'fasta'))

    g1 = [record for record in aln if re.search(args.group1, record.id)]
    g2 = [record for record in aln if re.search(args.group2, record.id)]
    g1_ids = {record.id for record in g1}
    g2_ids = {record.id for record in g2}

    if len(g1_ids) == 0:
        parser.error(f'Could not find any sequences matching g1 REGEX "{args.group1}"')
    if len(g2_ids) == 0:
        parser.error(f'Could not find any sequences matching g2 REGEX "{args.group2}"')
    if g1_ids.intersection(g2_ids):
        intersection = g1_ids.intersection(g2_ids)
        parser.error(f'The specified groups need to be disjoint! They intersect on {len(intersection)} sequences. '
                     f'E.g., "{next(intersection.__iter__())}"')

    if args.max_comp < 1:
        parser.error('max_comp has to be a positive integer')

    output_log = None
    if args.pairwise_mat:
        output_log = open(args.pairwise_mat, 'w')
        output_log.write('sequence1, sequence2, hamming_distance, %_dist\n')

    ignore_gaps = args.ignore_gaps
    aln_len = len(g1[0].seq)

    distances = []
    if len(g1) * len(g2) > args.max_comp:
        print(f'Will randomly sample sequences from the groups to perform at most {args.max_comp} comparisons')
        for i in range(args.max_comp):
            r1 = rnd.choice(g1)
            r2 = rnd.choice(g2)
            dist = compute_distance(r1, r2, ignore_gaps)
            distances.append(dist)
            if output_log:
                output_log.write(f'{r1.id}, {r2.id}, {dist}, {round(dist / aln_len, 3)}\n')
    else:
        for r1 in g1:
            for r2 in g2:
                dist = compute_distance(r1, r2, ignore_gaps)
                distances.append(dist)
                if output_log:
                    output_log.write(f'{r1.id}, {r2.id}, {dist}, {round(dist / aln_len, 3)}\n')
    min_dist, med_dist, max_dist = min(distances), median_low(distances), max(distances)
    min_frac, med_frac, max_frac = min_dist / aln_len, med_dist / aln_len, max_dist / aln_len
    print(f'Min distance: {round(min_frac, 3)} ({min_dist})')
    print(f'Median distance: {round(med_frac, 3)} ({round(med_dist, 1)})')
    print(f'Max distance: {round(max_frac, 3)} ({max_dist})')

    if output_log:
        output_log.close()


if __name__ == '__main__':
    parse_args()
