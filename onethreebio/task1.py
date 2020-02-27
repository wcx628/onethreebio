from lib import *
import pprint
import argparse

# Initialize API argument parser
parser = argparse.ArgumentParser()
parser.add_argument("drug_id", nargs='?', default="", help="individual drugbank id string to look up in drug bank website")
parser.add_argument("-f","--file", help="file with list of drugbank id in the current folder, one id each line")
parser.add_argument("-v","--verbose", action="store_true", help="turn on verbose")
args = parser.parse_args()

if args.verbose:
    print("Verbose is turned on.")

def load_id_list(args, test=True):
    
    drugbank_id_list = set()
    
    # Test mode
    if test:
        initial_drug_list = [
            'DB00619',
            'DB01048',
            'DB14093',
            'DB00173',
            'DB00734',
            'DB00218',
            'DB05196',
            'DB09095',
            'DB01053',
            'DB00274',
        ]

        drugbank_id_list |= set(initial_drug_list)
        
        return drugbank_id_list

    # Normal mode
    with open(args.file) as f:
        try:
            while True:
                drugbank_id_list.add(f.readline().strip())
        except EOFError as e:
            pass

    return drugbank_id_list


def main():
    
    # Loading request (can input a file)
    drugbank_id_list = load_id_list(args, test=True)

    # Get result
    gene_result = {}
    for drug_id in drugbank_id_list:

        # Get url for the drug
        drugurl = create_drugurl(drug_id)

        # Process the drug page
        res, _ = process_drugurl(drugurl)

        # Store into the master result
        if res is not None:
            gene_result[drug_id] = res.copy()
            print("retrieving gene info " + drug_id + " successful")

    pprint.pprint(gene_result)
            
    return gene_result

if __name__ == "__main__":
     main()
