# -*- coding: utf-8 -*-
# coding: utf-8
# author: YWANG
# version: 0.2.1

import os
import mikeio
import pandas as pd


def load_dfs0(dfs0_filename, start_date, end_date):
    """
    read dfs0 file and return rainfall data between given dates

    Parameters
    ----------
    dfs0_filename : string
        dfs0 file path and name
    start_date : string
        start date to slice data. format YYYY-MM-DD
    end_date : string
        end date to slice data. format YYYY-MM-DD

    Returns
    -------
    pandas data frame
        rainfall data

    """
    if not os.path.exists(dfs0_filename):
        print(f'Cannot find Dfs0 file {dfs0_filename}')
        return None
    
    ds = mikeio.read(dfs0_filename)

    df = ds.to_dataframe()
    
    df = df.loc[start_date: end_date]
    
    return df

def test_load_dfs0():
    dfs0_filename = 'VSA_Rainfall_Data_PDT.dfs0'
    start_date = '2024-10-17'
    end_date = '2024-10-22'
    df = load_dfs0(dfs0_filename, start_date, end_date)
    print(df)

def main():
    print("in dfs0.py!")
    test_load_dfs0()

if __name__ == '__main__':
    main()