# import pandas as pd
import pandas as pd
import sys

try:
    csvFile = sys.argv[1]
    df = pd.read_csv(csvFile)

    UniqueSrsIP = df['Src IP'].unique()
    UniqueDstIP = df['Dst IP'].unique()

    print(UniqueSrsIP)
    print("\nThere are: {} unique source IP addresses in {}\n".format(len(UniqueSrsIP), csvFile))
    print(UniqueDstIP)
    print("\nThere are: {} unique destination IP addresses in {}".format(len(UniqueDstIP), csvFile))

except FileNotFoundError:
    print("File could not be found")
except IndexError:
    print("A file path must be added")