# -*- coding: utf-8 -*-
# coding: utf-8
# author: YWANG
# version: 0.2.3

import pandas as pd

class IDF():

    AEP_LOW_TEXT = '> 50 % / < 2 y'
    
    def __init__(self, zone_id, climate_id, index_rains, idf):
        self._zone_id = zone_id
        self._climate_id = climate_id
        self._index_rains = index_rains
        self._idf = idf
        self._gauge_id = ''
        
    def __str__(self):
        if self._gauge_id == '':
            return f'climate: {self._climate_id}, gauge: {self._gauge_id}'
        else:
            return f'climate: {self._climate_id}, zone: {self._zone_id}'
    
    def get_zone_id(self):
        return self._zone_id
    
    def get_climate_id(self):
        return self._climate_id
    
    def get_gauge_id(self):
        return self._gauge_id
    
    def set_gauge_id(self, gauge_id):
        self._gauge_id = gauge_id.strip()
        
    def set_index_rains(self, index_rains):
        self._index_rains = index_rains
        
    def get_idf(self):
        return self._idf.transpose().mul(self._index_rains).transpose().round(4)
    
    def get_aep(self, rainfall_max):
        rainfall_aep = {}
        idf_df = self.get_idf()
        durations = idf_df.index
        for du in durations:
            ds = idf_df.loc[du,]
            depth = rainfall_max.loc[du].item()
            ds = ds[ds < depth]
            if ds.size == 0:
                rainfall_aep[du] = self.AEP_LOW_TEXT
            else:
                rainfall_aep[du] = ds.index[-1]
        rainfall_aep = pd.DataFrame(data = {self._gauge_id: rainfall_aep})
        return rainfall_aep
        
def test_IDF():
    import data
    gauge_id = 'BU07'
    zone = f'Zone {data.ZONES[gauge_id]}'
    idf = IDF(zone, 'Ex', data.INDEX_RAINS[gauge_id], data.IDF[zone])
    print(idf.get_idf())

def main():
    print("in IDF.py!")
    test_IDF()

if __name__ == '__main__':
    main()