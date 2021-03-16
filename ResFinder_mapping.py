import pandas as pd
import os
import glob
import sys
"""
FOR RESFINDER
This script compares location of prophage elements to location of Antibiotic resistance genes as identified by the Resfinder database (https://cge.cbs.dtu.dk/services/ResFinder/)

This script takes 3 arguments: Prophage, Dir_CARDfiles, and Output_filepath. Prophage is a CSV file containing the location (sample, contig, start, and end) of all prophage elements to check.
Dir_CARDfiles is the directory where all .txt files output by CARD for your samples. Output_file path is a blank txt file to append the results of this script to.
"""

def main(Prophage, Dir_to_files, Output_textpath):
    Prophage_df= pd.read_csv(Prophage)
    ARGdict = {}

    #get all values in a directory containing the RESFINDER text files, build a dataframe from them.
    for filepath in glob.iglob(Dir_to_files+ '*.txt'):
        name=os.path.splitext(os.path.basename(filepath))[0]
        df=pd.read_csv(filepath,sep='\t', usecols=['Resistance gene','Contig','Position in contig', 'Phenotype'])

        df['Contig']= df['Contig'].str.replace(r'Contig_','') #get only the contig number, remove the word Contig
        df['Contig'] = df['Contig'].str.replace(r'contig_', '') #get only the contig number, remove the word Contig
        startlist = []
        endlist = []
        for i in range(len(df)):

            start= df.iloc[i,[2]].str.split(".")
            startreal=int(start[0][0])
            end=int(start[0][2])
            startlist.append(startreal)
            endlist.append(end)

        startseries=pd.Series(startlist)
        endseries=pd.Series(endlist)
        df['Start']=startseries
        df['Stop']=endseries


        ARGdict[name] = df #create a dictionary where the lookup value is the sample and the key is a dataframe containing antibiotic resistance gene information.


    for i in range(len(Prophage_df)): #compare the locations of the prophage elements found in each sample to the antibiotic resistance gene locations, append findings to text file.
        value=ARGdict[str(Prophage_df.iloc[i,0])]
        for j in range(len(value)):
            x = range(Prophage_df.iloc[i, 2], Prophage_df.iloc[i, 3])
            xs = set(x)
            y = range(value.iloc[j, 4], value.iloc[j, 5])
            ys=set(y)
            if Prophage_df.iloc[i,1] == value.iloc[j, 4]:

                if xs and ys:

                    f = open(Output_textpath, "a") #arg parse 3rd value, path to text file to output to.
                    f.write( str(Prophage_df.iloc[i,0]) + ":" + str(value.iloc[j,0])+ ";" + str(value.iloc[j,3]) + "\n")

    f.close()
if __name__== '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])