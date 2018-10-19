# Drug Shortages list data mining

## bc_data ##
  <b>Drug Shortages Data Miner for BC Drug Shortages.</b>

  You must have a blanket log file named bc_current_metadata.json and bc_resolved_metadata.json.

  Run the script bc_drugshortages.py to download the latest data.

  The script first checks for the file size, its ETag, and the date the file was last updated.
  If any of these values are different from the log file saved in a json format, we treat it as new data and save it under a new file with the new date timestamped onto the file name.

## national_data ##
  <b>Drug Shortages Data Miner for National Drug Shortages database from https://www.drugshortagescanada.ca</b>
  
  Accounts are required to play with their API (documentation: https://www.drugshortagescanada.ca/blog/52).  
  
  Script will continue to append to the file "drugshortagescanada.json" with daily new reports.
