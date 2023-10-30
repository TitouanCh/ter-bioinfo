import pandas as pd

def import_genome_data_as_df(filename = "REAL.hapt", labels = "REAL.tsv", superpopulation_code_dict = {
    'EUR': 0,
    'EAS': 1,
    'AMR': 2,
    'SAS': 3,
    'AFR': 4,
    'EUR,AFR': 5,
}):
    df = pd.read_csv('./data/' + filename, delimiter = ' ')
    if labels:
        labels_df = pd.read_csv('./data/' + labels, header = 0, sep = '\t')
        df.iloc[:, 1] = df.iloc[:, 1].astype(str).str[:-2]
        df = df.merge(labels_df[['Sample name','Superpopulation code']], left_on=df.iloc[:, 1], right_on='Sample name', how='inner')
        df['Superpopulation code'].replace(superpopulation_code_dict, inplace=True)
        df = df.drop(columns='Sample name')
    
    return df