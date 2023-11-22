"""
This script is designed to take a full sized tree file and a file with a subset
of names within the tree file representing a single clade and returns the
sample with the smallest patristic distance relative to the MRCA of the
whole clade.
Created by David E. Hufnagel on May 23, 2020
"""

from ete3 import Tree
import sys

bigTree = Tree(sys.argv[1])
cladeNamesFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through names file and store the names in a list
cladeNames = []
for line in cladeNamesFd:
    cladeNames.append(line.strip())


#Use the ete3 tree to calculate the MRCA for the clade
mrca = bigTree.get_common_ancestor(cladeNames)

#Iterate through all members of the clade and calculate patristic distance
#  with the MRCA
distList = [] #a list of tuples with the format [(distA, nameA), (distB, nameB)...]
for name in cladeNames:
    dist = bigTree.get_distance(mrca, name)
    distList.append((dist, name))
distList.sort()


#Output the results
newline = "%s\n" % (distList[0][1])
out.write(newline)




cladeNamesFd.close()
out.close()
