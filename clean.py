import pandas as pd

data = pd.read_csv('signatories.csv')
names = data['sign_link'].apply(lambda link: str(link).split('.')[-2].split('/')[-1].replace('_', ' ').replace('-', ' ').upper())
data['signatory_names'] = names
data.to_excel('clean_signatories_final.xlsx')