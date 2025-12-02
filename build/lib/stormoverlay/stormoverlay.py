# -*- coding: utf-8 -*-
# coding: utf-8
# author: YWANG
# version: 0.2.1

import sys
import pandas as pd
import stormoverlay.data as data
import stormoverlay.idf as idf
import stormoverlay.load_dfs0 as ld
import stormoverlay.load_csv as lc
import stormoverlay.wiski as wiski
import stormoverlay.statistics_calculator as sc
import re
import os
import argparse
import time
from datetime import datetime

def check_date(date_str):
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    return not re.search(pattern, date_str)

def load_idf_curves(gauge_id):
    """
    load IDF values from GHD spreadsheets

    Parameters
    ----------
    gauge_id : string
        gauge ID

    Returns
    -------
    idf_curves : data frame of pandas data frames

    """
    zone = f'Zone {data.ZONES[gauge_id]}'
    idf_curves = idf.IDF(zone, 'Ex', data.INDEX_RAINS[gauge_id], data.IDF[zone])
    return idf_curves

def load_ts_dfs0(dfs0_filename, start_date, end_date):
    """
    create time series from dfs0 file
    dfs0 file should have gauge id as column names

    Parameters
    ----------
    dfs0_filename : file path to dfs0
        
    start_date : date
        formate: YYYY-MM-DD
    end_date : date
        formate: YYYY-MM-DD

    Returns
    -------
    rainfall_df : pandas data frame

    """
    rainfall_df = ld.load_dfs0(dfs0_filename, start_date, end_date)
    
    return rainfall_df

def load_ts_csv(csv_filename, start_date, end_date):
    """
    create time series from csv file
    csv file should have no column names

    Parameters
    ----------
    csv_filename : file path to csv
        
    start_date : date
        formate: YYYY-MM-DD
    end_date : date
        formate: YYYY-MM-DD

    Returns
    -------
    rainfall_df : pandas data frame

    """
    rainfall_df = lc.load_csv(csv_filename, start_date, end_date)
    
    return rainfall_df

def extract_duration_max(rainfall_ds, durations = data.DURATIONS_TEXT):
    """
    Calculate maximum rainfall depth by durations

    Parameters
    ----------
    rainfall_ds : pandas series
        rainfall time series
    durations: list of string
        duration time deltas

    Returns
    -------
    rainfall_max : pandas data frame
        key value pairs of max rainfall depth and time by durations

    """
    rainfall_max = sc.get_duration_max(rainfall_ds, durations)
    #rainfall_max.column[0] = rainfall_ds.name
    return rainfall_max

def prepare_results(idf_curves, rainfall_AEP, rainfall_max):
    """
    generate dataframe for display and output

    Parameters
    ----------
    idf_curves : idf.IDF
        idf instant
    rainfall_AEP : pd.Series
        rainfall AEP
    rainfall_max : pd.DataFrame
        rainfall max depth and times

    Returns
    -------
    idf_df : pd.DataFrame
        one dataframe of all outputs

    """
    idf_df = idf_curves.get_idf().round(2)
    idf_df.insert(0, 'AEP', rainfall_AEP)
    idf_df = pd.concat([rainfall_max, idf_df], axis=1)
    return idf_df

def display_results(idf_df, gauge_id, start_date, end_date):
    """
    display results to screen

    Parameters
    ----------
    idf_df : pd.DataFrame
        one dataframe of all outputs
    gauge_id : str
        Gauge ID
    start_date : str
        start date
    end_date : str
        end date

    Returns
    -------
    None.

    """
    print('')
    print(f'Gauge ID: {gauge_id}, from {start_date} to {end_date}')
    print(idf_df)
    
def export_results(idf_df, gauge_id, start_date, end_date):
    """
    export results to csv file

    Parameters
    ----------
    idf_df : pd.DataFrame
        one dataframe of all outputs
    gauge_id : str
        Gauge ID
    start_date : str
        start date
    end_date : str
        end date

    Returns
    -------
    None.

    """
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    filepath = f'{gauge_id}_{start_date.replace("", "")}_{end_date.replace("", "")}_{time_now}.csv'
    filepath = os.path.join(os.getcwd(), filepath)
    idf_df.to_csv(filepath)
    print(f'Results exported to CSV file saved at: {filepath}')

def main():
    
    description_text = """
        Calculate AEP / Return Period based on GHD 2024 IDF curves
    """
    
    example_text = """Example:
        
        To get AEP for BU07 from 2024-10-10 to 2024-10-20 based on a dfs0 file on J drive:
            
        stormoverlay BU07 2024-10-10 2024-10-20 --dfs0 "J:\TOOLS\StormOverlay\VSA_Rainfall_Data_PDT.dfs0"

        To get AEP for BU07 from 2024-10-10 to 2024-10-20 based on a csv file on J drive:

        stormoverlay BU07 2021-11-12 2021-11-19 --csv "J:\TOOLS\StormOverlay\WISKI_BU07_2021-11-12_2021-11-19.csv"
        
        To save results to csv file, add '--savecsv' to the end of the command
    """
    
    # parse arguments
    parser = argparse.ArgumentParser(description=description_text, 
                                     prog='StormOverlay',
                                     epilog=example_text)
    parser.add_argument('gauge_id', help='Name of the rain gauge')
    parser.add_argument('start_date', help='Start date of the storm event')
    parser.add_argument('end_date', help='End date of the storm event')
    parser.add_argument('--dfs0', default=None, help='File path to the dfs0 file')
    parser.add_argument('--csv', default=None, help='File path to the csv file')
    parser.add_argument('--savecsv', action='store_true', 
                        help='export result to csv file')
    args = parser.parse_args()
    
    # check user inputs
    gauge_id = args.gauge_id
    start_date = args.start_date
    end_date = args.end_date
    dfs0_filename = args.dfs0
    csv_filename = args.csv
    savecsv = args.savecsv
    
    if check_date(start_date) or check_date(end_date):
        print('start date and end date should be in the format of "YYYY-MM-DD"')
        exit()
    if not (start_date < end_date):
        print('start date must be earlier than end date')
        exit()

    # load rainfall data
    if dfs0_filename is not None:
        print(f'Working on gauge {gauge_id} from {start_date} to {end_date} based on dfs0 file {dfs0_filename}')
        rainfall_df = load_ts_dfs0(dfs0_filename, start_date, end_date)
        if gauge_id not in rainfall_df.columns:
            print(f'Rain gauge {gauge_id} is not in dfs0 file. Make sure to use gauge IDs as column names')
            exit()
    elif csv_filename is not None:
        print(f'Working on gauge {gauge_id} from {start_date} to {end_date} based on csv file {csv_filename}')
        rainfall_df = load_ts_csv(csv_filename, start_date, end_date)
        rainfall_df.columns = [gauge_id]
    else:
        csv_filename = f'WISKI_{gauge_id}_{start_date.replace("", "")}_{end_date.replace("", "")}'
        
        print('Downloading data from WISKI ...')
        ts_id = data.WISKI_ID[gauge_id]
        wiski.get_wiski_csv(ts_id, start_date, end_date, csv_filename, 'total', '00:10:00')
        
        csv_filename = csv_filename + '.csv'
        print(f'Working on gauge {gauge_id} from {start_date} to {end_date} based on csv file {csv_filename} downloaded from WISKI')
        if os.path.exists(csv_filename):
            rainfall_df = load_ts_csv(csv_filename, start_date, end_date)
            rainfall_df.columns = [gauge_id]
        else:
            print('Failed to download data from WISKI')
            exit()
            
    # processing
    rainfall_ds = rainfall_df[gauge_id]
    rainfall_max = extract_duration_max(rainfall_ds)
    idf_curves = load_idf_curves(gauge_id)
    rainfall_AEP = idf_curves.get_aep(rainfall_max[['MaxDepth']])
    
    # cleanup
    idf_df = prepare_results(idf_curves, rainfall_AEP, rainfall_max)
    
    # print to screen
    display_results(idf_df, gauge_id, start_date, end_date)
    
    # export to csv
    if savecsv:
        export_results(idf_df, gauge_id, start_date, end_date)

if __name__ == '__main__':
    main()