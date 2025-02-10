## HammerTime: computing Hamming distances between groups in an alignment

The script requires Python 3 and BioPython. The basic usage of the script is as follows (the groups below represent different swine influenza A virus clades). Generally, g1 and g2 can be any regex patterns specifying some (non-overlapping) groups of interest in the alignment.
```
python hammertime.py -s alignment.fasta -g1 "1A.3.3.3" -g2 "1A.1.1.3" -i
```

Then the script will perform pairwise comparisons and output something like the following
```
Min distance: 0.032 (54)
Median distance: 0.041 (70)
Max distance: 0.053 (90)
```
The first number indicates the fractional distance and the number in the paranthesis indicates the Hamming distance. See `python hammertime.py -h` for more details.

**Fun fact:** I tried to code the script while listening exclusively to "U Can't Touch This". Unfortunately, on 10th repeat I got too tired of it and had to finish the script in silence.
