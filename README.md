# Compliance Horizon Scanning
Compliance Horizon Scanning is a library for automating collection of regulatory compliance data.
Compliance Horizon Scanning enables continuous subscriptions and data ingestion from prime regulatory agencies across operating geographies.

## What is it?
Compliance Horizon Scanning is NLP powered automated toolkit for continues ingestion, analysis and categorisation of new and fast changing publications from hundreads of agencies across the globe to keep companies and various business units within them up-to-date. 

## Why is it important?
- Regulatory space is not static, they evolve over time.
- Compliance teams need to keep up with a regulatory tsunami. Approximately 2500 COVID related regulatory updates published to date.
- Regulatory and compliance teams spend a significant amount of time keeping up with regulatory changes and acting upon them.

These challanges are not only common across investment and asset management firms but they're also critically important. Compliance Horizon Scanning toolkit allows firms to automate the collection of pre-configured data and enrich it using custom NLP processes, so that your data is ready to be consumed at different level.  

## How does it work?

## What are the benefits?
- One stop solution for every requirements related to regulatory compliance data. 
- Automated, easy and efficient way of collecting super dynamic data. 
- NLP layer sanitize incoming data, so that it's consumable at different levels. 
- Reduction in time/effort spent for rules creation
- Compliance SMEs focus on more value-adding activities
- Faster fulfilment for portfolio managers and clients alike
- Accelerated compliance rule remediation identification.


## Development setup
1. The code has been built and tested on Python version 3.7
2. Clone the repository
3. Create Python enviornment with version 3.7
4. Install required libraries using requirement.text file

## Usage Example
1. Validate you've cloned latest version of the code and run following commands with appropriate arguments
2. All arguments are optional
3. python main.py --agency --output --month
    3.1 --agency argument accepts name of the agency for which you need data or you can also use value "all" for obtaining data from all supported agencies. You can check Roadmap section to valdiate names of agencies supported. 
    3.2 --output argument accepts name of the file in which resultant data will be stored. The file format HAS to be JSON
    3.3 --months accepts number of months for which you need data. 
4. Examples :- 
    4.1 python main.py --agency esma --output result.json
    This command will extract data from ESMA agency for 1 month and store it in result.json file.
    4.2 python main.py --agency finra --month 12
    This command will extract data from FINRA agency for 12 months and store it in agency.json file. 
    4.3 python main.py
    This command will extract data from ALL supported agency for 1 month and store it in agency.json file. 
    

## Support
TBD

## Roadmap
In it's current version, Compliance Horizon Scanning tool supports below mentioned agencies and its corrosponding topics. The roadmap will be constantly updated based on initial planning & requests from the community. 

| Version | Agencies | Topics | Status |
| ------ | ------ | ------ | ------ | 
| 1.0 | FINRA | Notices, Rules & News Feeds| Active |
| 1.0 | ESMA  | News, Consultation & Press Release | Active |
| 1.0 | PRA | News, Publications & Prudential Regulations| Active |
| 1.1 | SEC | Press Release, Proposed Rules & Administrative Proceedings | Next-Release |
| 1.1 | CSSF | Publications | Next-Release |

## Contributing
1. Fork it (https://github.com/yourname/yourproject/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Read our contribution guidelines and Community Code of Conduct
4. Commit your changes (git commit -am 'Add some fooBar')
5. Push to the branch (git push origin feature/fooBar)
6. Create a new Pull Request

NOTE: Commits and pull requests to FINOS repositories will only be accepted from those contributors with an active, executed Individual Contributor License Agreement (ICLA) with FINOS OR who are covered under an existing and active Corporate Contribution License Agreement (CCLA) executed with FINOS. Commits from individuals not covered under an ICLA or CCLA will be flagged and blocked by the FINOS Clabot tool. Please note that some CCLAs require individuals/employees to be explicitly named on the CCLA.

## Authors and acknowledgment
TBD

## Project status
Currently the project is running on version 1.0
