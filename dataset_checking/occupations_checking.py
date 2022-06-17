import sys
import pandas as pd

def main(path, output):
    df = pd.read_csv(path, header=0)
    result = df.groupby(["occupation_name","gender"]).size()
    df = pd.DataFrame(result)
    df.to_csv(output)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])