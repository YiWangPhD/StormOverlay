# -*- coding: utf-8 -*-
# coding: utf-8
# author: YWANG
# version: 0.2.3
# this module includes functions to calculate statistics for data frames

import pandas as pd

def max_block(s, window):
    """
    returns the maximums of a rolling block. eg. maximum 24 h average flow
    it assumes equal intervals along time axis

    Parameters
    ----------
    s : pd.Series
        Time series.
    window : int, timedelta, str, offset, optional
        Pandas time window. The default is '1H'. 
        e.g. 1 hour is '1H', 5 min is '5T' or '5min'

    Returns
    -------
    Float
        Maximums of series, rolling averaged.

    """
    s = s.rolling(window).sum()
    s = s[(s.index[0] + pd.Timedelta(window)):]
    return {'MaxDepth': s.max().round(3).item(), 'MaxTimeStart': f'{s.idxmax() - pd.Timedelta(window)}', 'MaxTimeEnd':f'{s.idxmax()}'}

def get_duration_max(s, durations):
    """
    calculate duration maximums 

    Parameters
    ----------
    s : pd.series
        rainfall time series at one gauge
    durations: list
        duration windows
        
    Returns
    -------
    pd.DataFrame
        duration maximums

    """
    du_max = {du: max_block(s, du) for du in durations}
    
    return pd.DataFrame(data = du_max).T