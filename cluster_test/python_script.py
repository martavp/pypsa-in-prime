# This is a simple python script
import pandas as pd

def make_csv():
    df_input = pd.read_csv(snakemake.input.csv_file_in)
    output = df_input
    output.to_csv(snakemake.output.csv_file_out)

if __name__ == "__main__":
    make_csv()
