"""
This script is designed to take a full sized tree file and a file with a subset
of names within the tree file representing a single clade and returns the
sample with the smallest patristic distance relative to the MRCA of the
whole clade.
Created by David E. Hufnagel on May 23, 2020
"""

from ete3 import Tree
import sys

bigTree = Tree(sys.argv[1]) #Store the tree in an ete3 object
cladeNamesFd = open(sys.argv[2])
out = open(sys.argv[3], "w")



#Go through names file and store the names in a list
cladeNames = []
for line in cladeNamesFd:
    cladeNames.append(line.strip())


#Use the ete3 tree to calculate the MRCA for the clade
ancestor = bigTree.get_common_ancestor(cladeNames)

#Iterate through all members of the clade and calculate patristic distance
#  with the MRCA.  Keep the sample with the least distance
closestSeq = ("name", 99999)  #a tuple of (name, distance)
for name in cladeNames:
    dist = bigTree.get_distance(ancestor, name)
    if dist < closestSeq[1]:
        closestSeq = (name, dist)

#Print the title line
out.write("#python %s\n" % (" ".join(sys.argv)))

#Ouptut the name of the sequence closest to the MRCA of the clade
newline = "%s\n" % (closestSeq[0])
out.write(newline)





cladeNamesFd.close()
out.close()
