****************************
***** No Bullshit Disclaimer
****************************

1. No Guarantees: We make no guarantees about specific outcomes or results. Individual situations and results will vary.

2. Not Professional Advice: This content does not constitute legal, financial, or medical advice. Please consult a qualified professional for your specific needs.

3. Opinions are Our Own: Any opinions expressed belong solely to the author(s) and do not represent any third party or employer.

4. Your Responsibility: Any action you take based on the information provided here is at your own risk. We are not liable for any loss or damage you may incur.

****************************
***** Description 
****************************

1. This tool extracts AEP based on GHD 2024 IDF

2. It uses IDF curves for existing climate

3. It uses index rain from GHD report appendix

****************************
***** How to install
****************************

1. create a new enviornment in anaconda. must use python version 3.11
	
	conda create --name py311_storm python=3.11
	
2. activate the new environment

	conda activate py311_storm

3. install the tool
	
	pip install "J:\TOOLS\StormOverlay\stormoverlay-0.2-py3-none-any.whl" --trusted-host pypi.python.org
		
****************************
***** How to upgrade to newer versions
****************************

1. activate the environment

	conda activate py311_storm

2. install the tool
	
	pip install "J:\TOOLS\StormOverlay\stormoverlay-0.2-py3-none-any.whl" --trusted-host pypi.python.org --force-reinstall
	
	note that the whl file should have a newer version number
	
****************************
***** How to use
****************************

1. activate conda enviornment
	
	conda activate py311_storm
	
2. run the tool using dfs0 rain file:
	
	stormoverlay gauge_id start_date end_date --dfs0 dfs0_filepath
	
	for example, to get AEP for BU07 from 2024-10-10 to 2024-10-20 based on a dfs0 file on J drive:
	
	stormoverlay BU07 2024-10-10 2024-10-20 --dfs0 "J:\TOOLS\StormOverlay\VSA_Rainfall_Data_PDT.dfs0"
	
3. run the tool using csv rain file:
	
	stormoverlay gauge_id start_date end_date --csv csv_filepath
	
	for example, to get AEP for BU07 from 2024-10-10 to 2024-10-20 based on a csv file on J drive:
	
	stormoverlay BU07 2021-11-12 2021-11-19 --csv "J:\TOOLS\StormOverlay\WISKI_BU07_2021-11-12_2021-11-19.csv"
	
4. run the tool without providing rainfall data:
	
	stormoverlay gauge_id start_date end_date
	
	for example, to get AEP for BU07 from 2024-10-10 to 2024-10-20:
	
	stormoverlay BU07 2024-10-10 2024-10-20
	
	rainfall data will be downloaded from wiski
	
5. results are displayed in conda prompt. 
    to save a csv file, use option --savecsv at the end of the command

6. use the provided idf_template.xlsx to quickly create IDF curves
	
****************************
***** Notes
****************************

1. gauge_id must be capital letters, must be in GHD report
    if using dfs0 file, gauge id must be in column name
    if using csv file, it should not have header line. first column should be date time, second column should be depth in mm
    only selected rain gauges are available to be downloaded from WISKI directly
    
2. start_date and end_date must be in format "YYYY-MM-DD"

3. start_date must be earlier than end_date. it is suggested to keep 3 days minimum gap to make sure 72 h depth is extracted correctly

****************************
***** Version History
****************************
0.1.0 	- initial version
0.1.1 	- updated print output. consolidated data frames and series.
0.2		- added return periods to AEP, added date time columns, export to csv, created idf_template.xlsx
0.2.1   - added support to use csv file or download from wiski directly

****************************
***** Future work
****************************
1. read rainfall data from wiski directly (added in version 0.2.1)
2. also overlay with future climate IDF curves
3. double check zone idf values (updated in version 0.2.1)
4. options to switch between "forward accumulation" and "backward accumulation"
5. air quality rain gauge data (zone, index rain, rainfall time series from wiski)
6. export to spreadsheets (added in version 0.2)
7. work on multiple rain gauges with same start/end dates
8. show starting time of the max depth (added in version 0.2)
9. add return periods next to AEP (added in version 0.2)
