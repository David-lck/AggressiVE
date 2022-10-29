import pandas as pd

def main(file=r'C:\AggressiVE_GITHUB\AggressiVE\input_parameters.xlsx'):
    df = pd.read_excel(file,'aggressive')
    auto_attr = df['auto_attr'].values.tolist()[0]
    is_targsim = df['is_targsim'].values.tolist()[0]
    if auto_attr == 'None':
        print('Expected')
    if not is_targsim:
        print('Expected')
