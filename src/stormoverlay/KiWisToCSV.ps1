param (
[int]$TimeSeries,
	# the WISKI ts_id, e.g. 6017010 for GOlden Ears raw flow
[string]$StartDate,
	#start date in format CCYY-MM-DD, e.g. 2021-03-31
[string]$EndDate,
	#end date in format CCYY-MM-DD, e.g. 2021-04-30
[string]$AggregationType = 'None',
	#a valid KiWIS aggregation:  min, max, mean, average, total, counts, perc-#
[string]$AggregationInterval = 'None',
    #one of the valid KiWis intervals:  HHMMSS, decadal, yearly, monthly, daily, hourly
[string]$Filename = 'KIWisOut'
	#a name for the CSV output file, e.g. WestVancouverAT
)

$ErrorActionPreference="SilentlyContinue"
#Stop-Transcript | out-null
$ErrorActionPreference = "Continue"
#Start-Transcript -path "KiWisToCSV_powershell.out.txt" -append

function GetKiWisValues
{
# build a KiWis URI from the parameters passed to powershell
$base='https://mvdms.gvrd.bc.ca/KiWIS/KiWIS?service=kisters&type=queryServices&datasource=0&request=getTimeseriesValues&ts_id=' + $TimeSeries
if ($AggregationType -ne 'None') {$base = $base + ';aggregate(' + $AggregationInterval + '%7C' + $AggregationType + ')'}
$URI = $base + '&from=' + $StartDate + '&to=' + $EndDate + '&format=csv&csvdiv=,&downloadfilename=' + $Filename  + '&dateformat=yyyy-MM-dd%20HH:mm:ss&metadata=true'
#must use %7 instead of pipe symbol for KiWiS URL

write-host $URI

#this bypasses a TLS version error
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
$store = New-Object System.Security.Cryptography.X509Certificates.X509Store(“My”,”CurrentUser”)
$store.Open(“ReadOnly”)

$adisearcher = [adsisearcher]"(samaccountname=$env:USERNAME)"
$email = $adisearcher.FindOne().Properties.mail
$matchmail = 'E=' + $email + '*'
$x509cert = $store.Certificates |where-object {$_.Subject -ilike $matchmail}

Add-Type -AssemblyName System.Net.Http 
$handler = New-Object System.Net.Http.HttpClientHandler
$certOK = $handler.ClientCertificates.Add($x509cert)
$httpClient = New-Object System.Net.Http.HttpClient($handler) 

$string = $httpClient.GetStringAsync($URI)
$Filename = $Filename + '.csv'
$string.Result |Out-File $Filename  -Encoding ascii


}

GetKiWisValues 

#Stop-transcript

