# -*- coding: utf-8 -*-
# coding: utf-8
# author: YWANG
# version: 0.2.3

import os
import pandas as pd

def load_csv(csv_filename, start_date, end_date):
    """
    read csv file and return rainfall data between given dates

    Parameters
    ----------
    csv_filename : string
        csv file path and name
    start_date : string
        start date to slice data. format YYYY-MM-DD
    end_date : string
        end date to slice data. format YYYY-MM-DD

    Returns
    -------
    pandas data frame
        rainfall data

    """
    if not os.path.exists(csv_filename):
        print(f'Cannot find csv file {csv_filename}')
        return None
    
    df = pd.read_csv(csv_filename, comment='#', header=None)
    
    df = df.set_index(0)
    df.index = pd.to_datetime(df.index)
    df.index.name = None
    df = df.loc[start_date: end_date]
    df = df.iloc[:,0].to_frame()
    
    return df

def test_load_csv():
    csv_filename = 'WISKI_BU07_2021-11-12_2021-11-19.csv'
    start_date = '2021-11-12'
    end_date = '2021-11-19'
    df = load_csv(csv_filename, start_date, end_date)
    print(df)

def main():
    print("in csv.py!")
    test_load_csv()

if __name__ == '__main__':
    main()