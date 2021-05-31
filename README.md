# concatInsertions


This program concat all the CSV files in a given path

1) python main.py (PATH)

i.e: python main.py /data2/NGS_runs/datasets/

This program iterate over all files and folders in a given path, find files with the - "fasta.insertions" pattern in their names and join them to one big table.

if we want to join some output CSV files, we can add a flag

1) python main.py (PATH) (another argument)

i.e: python main.py /data2/NGS_runs/datasets/ 1

if the program get more than 1 argument it's searching for ".csv" files and join them.

Useful if you want gather some CombinedCSV.csv files




