import glob, os, re, sys

inputfile = sys.argv[1]
header = "Your antigenic motif for amino acid position \n"


def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name:
                yield (name, "".join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name:
        yield (name, "".join(seq))


def write_file(data):
    output = filename + "-AB-AntigenicSites.txt"
    with open(output, "a") as out_file:
        # print(len(protein))
        out_file.write(
            str(name + " Sa ")
            + str(protein[128])
            + " "
            + str(protein[129])
            + " "
            + str(protein[158])
            + " "
            + str(protein[160])
            + " "
            + str(protein[162])
            + " "
            + str(protein[163])
            + " "
            + str(protein[165])
            + " "
            + str(protein[167] + "\n")
            + str(name + " Sb ")
            + str(protein[156])
            + " "
            + str(protein[159])
            + " "
            + str(protein[192])
            + " "
            + str(protein[193])
            + " "
            + str(protein[196])
            + " "
            + str(protein[198] + "\n")
            + str(name + " Ca-1 ")
            + str(protein[169])
            + " "
            + str(protein[173])
            + " "
            + str(protein[207] + "\n")
            + str(name + " Ca-2 ")
            + str(protein[140])
            + " "
            + str(protein[143])
            + " "
            + str(protein[145])
            + " "
            + str(protein[224])
            + " "
            + str(protein[225] + "\n")
            + str(name + " Cb ")
            + " "
            + str(protein[78])
            + " "
            + str(protein[79])
            + " "
            + str(protein[80])
            + " "
            + str(protein[81])
            + " "
            + str(protein[82])
            + " "
            + str(protein[83])
            + " "
            + str(protein[122] + "\n")
        )


def write_header(header):
    output = filename + "-AB-AntigenicSites.txt"
    with open(output, "w") as out_file:
        out_file.write(header)


table = {
    "ATA": "I",
    "ATC": "I",
    "ATT": "I",
    "ATG": "M",
    "ACA": "T",
    "ACC": "T",
    "ACG": "T",
    "ACT": "T",
    "AAC": "N",
    "AAT": "N",
    "AAA": "K",
    "AAG": "K",
    "AGC": "S",
    "AGT": "S",
    "AGA": "R",
    "AGG": "R",
    "CTA": "L",
    "CTC": "L",
    "CTG": "L",
    "CTT": "L",
    "CCA": "P",
    "CCC": "P",
    "CCG": "P",
    "CCT": "P",
    "CAC": "H",
    "CAT": "H",
    "CAA": "Q",
    "CAG": "Q",
    "CGA": "R",
    "CGC": "R",
    "CGG": "R",
    "CGT": "R",
    "GTA": "V",
    "GTC": "V",
    "GTG": "V",
    "GTT": "V",
    "GCA": "A",
    "GCC": "A",
    "GCG": "A",
    "GCT": "A",
    "GAC": "D",
    "GAT": "D",
    "GAA": "E",
    "GAG": "E",
    "GGA": "G",
    "GGC": "G",
    "GGG": "G",
    "GGT": "G",
    "TCA": "S",
    "TCC": "S",
    "TCG": "S",
    "TCT": "S",
    "TTC": "F",
    "TTT": "F",
    "TTA": "L",
    "TTG": "L",
    "TAC": "Y",
    "TAT": "Y",
    "TAA": "*",
    "TAG": "*",
    "TGC": "C",
    "TGT": "C",
    "TGA": "*",
    "TGG": "W",
}

print("Output written to " + inputfile + "-AB-AntigenicSites.txt")

for filename in glob.glob(inputfile):
    with open(os.path.join(os.getcwd(), filename), "r") as fp:
        write_header(header)
        for name, seq in read_fasta(fp):
            # seq = seq.replace("\n", "")
            # seq = seq.replace("\r", "")
            seq = seq[seq.find("gac") :]
            seq = seq[:678]
            seq = seq.upper()

            protein = ""

            if len(seq) % 3 == 0:

                for i in range(0, len(seq), 3):
                    codon = seq[i : i + 3]
                    if codon not in table:
                        protein = protein + "X"
                    else:
                        protein += table[codon]
                print(len(protein))
                write_file(protein)
                # output=open(filename+"-antigenic_moif.txt", "w")
                # output.write(str(name + ":") + str(protein[144])+ " " + str(protein[154]) + " " + str(protein[155]) + " " + str(protein[157]) + " " + str(protein[158]) + " " + str(protein[188]))

                # print(str(name + ":") + str(protein[144])+ " " + str(protein[154]) + " " + str(protein[155]) + " " + str(protein[157]) + " " + str(protein[158]) + " " + str(protein[188]))
        # output.close()C
