import sys, os
import pandas as pd
from datetime import datetime


def concatInsFastafiles(dirPath, date_time):
    try:
        f = open("exclude.txt", "r")
        exclude = set([line.rstrip() for line in f])
        f.close()
    except:
        exclude = 0
    f = open("exclude.txt", "a")
    # Search for all the insertions csv files in a given path
    insertionFiles = [os.path.join(root, name)
                      for root, dirs, files in os.walk(dirPath)
                      for name in files
                      if "fasta.insertions" in name]
    for x in insertionFiles:
        print(x)

    if exclude:
        insertionFiles = set(insertionFiles) - set(exclude)
    # Editing the csv files and insert them to an empty list
    li = []
    for table in insertionFiles:
        # Add Files that combined to a list
        #  for x in table.split('\\'):
        #     if "NGS" in x or "ngs" in x:
        #        f.write(x + '\n')
        f.write(table + '\n')
        df = pd.read_csv(table)
        for title in df.columns:
            if "insertion" in title:
                # Remove all the unnecessary title, write only the position of the insertion
                justPosition = title.split()[-1]
                df.rename(columns={title: justPosition}, inplace=True)
                # Change strain to 0 for sorting
            elif "strain" in title:
                df.rename(columns={title: '-1'}, inplace=True)
        li.append(df)
    if len(li) > 0:
        # combine all files in the list
        combined_csv = pd.concat(li, ignore_index=True, join='outer')
        # sorting columns by their insertion position
        combined_csv = combined_csv[sorted(combined_csv.columns, key=lambda x: tuple(map(float, x.split('_'))))]
        # changing back the strain col name
        combined_csv.rename(columns={'-1': 'strain'}, inplace=True)
        # deleting cols that all of their rows are nan
        combined_csv.dropna(axis=1, how='all', inplace=True)
        # save to csv
        code = str(hash(date_time) % 10)
        combined_csv.to_csv("CombinedCsv_" + date_time + "_" + code + ".csv", index=False, encoding='utf-8-sig')
    else:
        print("No new insertion to join")
        # combined_csv = pd.DataFrame.from_dict(map(dict, li))


def concatCsvFiles(dirPath,date_time):
    insertionFiles = [os.path.join(root, name)
                      for root, dirs, files in os.walk(dirPath)
                      for name in files
                      if ".csv" in name]
    li = []
    for table in insertionFiles:
        df = pd.read_csv(table)
        for title in df.columns:
            if "insertion" in title:
                # Remove all the unnecessary title, write only the position of the insertion
                justPosition = title.split()[-1]
                df.rename(columns={title: justPosition}, inplace=True)
                # Change strain to 0 for sorting
            elif "strain" in title:
                df.rename(columns={title: '-1'}, inplace=True)
        li.append(df)
    if len(li) > 0:
        # combine all files in the list
        combined_csv = pd.concat(li, ignore_index=True, join='outer')
        # sorting columns by their insertion position
        combined_csv = combined_csv[sorted(combined_csv.columns, key=lambda x: tuple(map(float, x.split('_'))))]
        # changing back the strain col name
        combined_csv.rename(columns={'-1': 'strain'}, inplace=True)
        # deleting cols that all of their rows are nan
        combined_csv.dropna(axis=1, how='all', inplace=True)
        # save to csv
        code = str(hash(date_time) % 10)
        combined_csv.to_csv("JoinedCSVs" + date_time + "_" + code + ".csv", index=False, encoding='utf-8-sig')
    else:
        print("No new insertion to join")



def main(argv):
    dirPath = argv
    # Taking date for the filename
    now = datetime.now()
    date_time = now.strftime("%Y%m%d")
    if len(argv) == 1:
        concatInsFastafiles(dirPath, date_time)
    else:
        concatCsvFiles(dirPath,date_time)

if __name__ == '__main__':
    main(sys.argv[1:])
