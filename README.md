# BoatsScraper
## Simple script for retrieving from free service and saving the information about vessels (via names and IMO numbers)

After launching the parsing process from main.py vessels list will be loaded from source file (boatslist.txt), then bot will check if scrapping results file (boatsdatabase.txt) exist (and will continue after last record) in other case will start from the begining. 

Parametres could be set in the "scrap_params.py" file. It includes:
1. Credentials for fleetmon.com service (visit https://www.fleetmon.com/ for free registration, it's required for receiving full data)
2. A full pathname and filename for list of boats. Data should be in next format: "CertificateNumber ShipName IMONumber ExpirationDate", space-separated.
3. A full pathname and filename for parsing results. Data will be saved in JSON format, separate line for every vessel. Every JSON consist of: 
  - "Generic": available vessel data such as Name, Category, Vessel type and so on
  - "Link": link for particular vessel page at the fleetmon.com service
  - "Photo": link for vessel photo at the fleetmon.com service
