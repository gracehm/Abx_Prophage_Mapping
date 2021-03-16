import pandas as pd
import os
import glob
import sys

"""
FOR CARD files
This script compares location of prophage elements to location of Antibiotic resistance genes as identified by the CARD database (https://card.mcmaster.ca/analyze/rgi)

This script takes 3 arguments: Prophage, Dir_CARDfiles, and Output_filepath. Prophage is a CSV file containing the location (sample, contig, start, and end) of all prophage elements to check.
Dir_CARDfiles is the directory where all .txt files output by CARD for your samples. Output_file path is a blank txt file to append the results of this script to.
"""
def main (Prophage, Dir_CARDfiles, Output_filepath):
    Prophage_df= pd.read_csv(Prophage) #
    Prophage_df=Prophage_df.dropna()
    Prophage_df=Prophage_df.astype(int)
    ARGdict = {}


    for filepath in glob.iglob(Dir_CARDfiles + '*.txt'):
        name=os.path.splitext(os.path.basename(filepath))[0]
        df=pd.read_csv(filepath,sep='\t', usecols=[ 'Contig','Start','Stop', 'Drug class', 'Resistance Mechanism', 'AMR Gene Family' ])
        df['Contig']= df['Contig'].str.replace(r'Contig_','')
        df['Contig'] = df['Contig'].str.replace(r'contig_', '')
        df['Contig']= df['Contig'].str.replace('_\d+','')
        ARGdict[name] = df


    for i in range(len(Prophage_df)):
        value=ARGdict[str(Prophage_df.iloc[i,0])]
        for j in range(len(value)):
            x = range(Prophage_df.iloc[i, 2], Prophage_df.iloc[i, 3])
            xs = set(x)
            y = range(value.iloc[j,1], value.iloc[2])
            ys=set(y)

            if Prophage_df.iloc[i,1] == value.iloc[j, 1]:
    #
                if xs and ys:
                    print('overlap found')
                    file = open(Output_filepath, "a")
                    file.write( str(Prophage_df.iloc[i,0]) + ":" + str(value.iloc[j,3])+ ";" + str(value.iloc[j,4]) + str(value.iloc[j,5]) +  "\n")
                    file.close()
            else:
                print(Prophage_df.iloc[i,0])
                print('no overlap')
if __name__== '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
