# -*- coding: utf-8 -*-
# coding: utf-8
# author: YWANG
# version: 0.2.3

from importlib.resources import files
import subprocess
import argparse

def get_wiski_csv(ts_id, start_date, end_date, file_name, aggregation_type = 'None', aggregation_interval = '00:05:00'):
    # adapt to python package
    script_file_path = files('stormoverlay').joinpath('KiWisToCSV.ps1')
    
    # Construct the command with parameters
    mycom = f'powershell -ExecutionPolicy Bypass -f {script_file_path} {ts_id} {start_date} {end_date} {aggregation_type} {aggregation_interval} {file_name}'
    # Execute the command
    return subprocess.run(mycom, capture_output=True, text=True, shell=True)

def main():
    description_text = """
        Download data from WISKI
    """
    
    example_text = """Example:
        
        To download rainfall data for VA63 from 2024-10-10 to 2024-10-20 in 5 minutes interval:
            
        wiski 18375010 2024-10-10 2024-10-20 VA63_rainfall --type total --interval 00:05:00
        
    """
    
    aggregation_type_text = """
        a valid KiWIS aggregation:  min, max, mean, average, total, counts, perc-
    """
    
    aggregation_interval_text = """
        valid KiWis intervals:  HHMMSS, decadal, yearly, monthly, daily, hourly
    """
    
    # parse arguments
    parser = argparse.ArgumentParser(description=description_text, 
                                     prog='wiski',
                                     epilog=example_text)
    parser.add_argument('ts_id', help='WISKI data id')
    parser.add_argument('start_date', help='Start date of the storm event')
    parser.add_argument('end_date', help='End date of the storm event')
    parser.add_argument('file_name', help='csv file name, excluding extension')
    parser.add_argument('--type', default='None', help=aggregation_type_text)
    parser.add_argument('--interval', default='None', help=aggregation_interval_text)
    
    args = parser.parse_args()
    
    result = get_wiski_csv(args.ts_id, args.start_date, args.end_date, args.file_name, args.type, args.interval)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

if __name__ == '__main__':
    main()

