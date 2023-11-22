#!/bin/bash





##### Define functions #####
#Print help menu
function print_help_menu() {
    cat <<helpChunk

    Arguments:
       -f : fasta file to extract all sequences from
       -n : names files to use for sequence extraction in the form of a file of
              file names
       -o : output directory
       -d : date threshold in the format YYYY-MM-DD
       
helpChunk
    exit 1
}




##### Body #####

REQUIRED_PAR=0 #used to determine whether all required parameters were used

#Go through input and assign input arguments to variables
while getopts ":f:n:o:d:h" opt; do
   case ${opt} in
      f )
        FASTA_FILE=$OPTARG
	(( REQUIRED_PAR++ ))
        ;;
      n )
        NAMES_FOFN=$OPTARG
	(( REQUIRED_PAR++ ))
        ;;
      o )
	OUT_DIR=$OPTARG
	;;
      d )
        DATE=$OPTARG
        (( REQUIRED_PAR++ ))
	;;
      h )
	print_help_menu
	;;
      \? )
	echo -e "\nERROR: Invalid argument: -$OPTARG" 1>&2
        print_help_menu
        ;;
    esac
done


#If required arguments are not provided throw an error and provide the help page
if (( REQUIRED_PAR != 3 )); then
    echo -e "\nERROR: The required parameters for this program are -f, -n, and -o"
    echo "You are lacking these parameters.  See our help page below"
    print_help_menu
fi


#Extract names files from FOFN
NAMES_FILES_ARRAY=()
I=1
while read -r line; do
   NAMES_FILES_ARRAY[ $I ]="$line"
   (( I++ ))
done < "$NAMES_FOFN"


I=1
for FILE in "${NAMES_FILES_ARRAY[@]}"; do
   NAMES_FILES_ARRAY[ $I ]="$FILE"
   PREFIX="${FILE%%_names.txt}"

   #Extract sequences from names files
   python ~/Scripts/1_1_2_A_gatherFastas.py "$FASTA_FILE" "$FILE" "$PREFIX.fna"

   #Filter by date using a threshold that works for most
   python ~/Scripts/1_4_filterByDateGeneral.py "$PREFIX.fna" "${PREFIX}_${DATE}.fna" "$DATE"


   (( I++ ))
done






