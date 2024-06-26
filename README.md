# Clean-Nmap, A Colourful Nmap Parser
A tool to enhance the efficiency of parsing through nmap scans via color coding; making it easier to identify important information.


### Basic Info
Tool used to simplify and colour code nmap output so that it is easier to read. When it is run, it will display colored nmap output in the current terminal window.

### How it works
When run it askes for the nmap command you'd like to use, after that it runs the nmap scan in the background and saves the results to a termporary .xml file (nmap_scan.xml). Host details and scan information is defined in nmap_classes.py. Together they sort through the identifiers for each data category and display that information with color & formatting applied, in the terminal.

### Setup
To set up the tool simply clone it i.e. git clone. Navigate into that directory and then enter  pip install -r requirements.txt into the command line. This will install the required python modules if not already installed on your system.

### Launching The Program
To use the program simply open up a terminal navigate to the directory and run it with "python3 'nmap_parser.py'"

### Running The Program
![alt text](screenshots/1.png "Sample Output")

^Example of Simplified Colour Coded Output^

![alt text](screenshots/2.png "Sample Output")

^Example of Original Output In Second Terminal^

### Built With

* Python 3.11.6

### Authors

*** Chance Bowers --> https://glitchingreality.github.io ; Modernized the code in 2023 for Python 3 compatability & additional features.

***Zach Fleming --> zflemingg1@gmail.com ;  created the original python2 base script in 2018 which this is based on.

### Disclaimer
This is experimental code and development is ongoing. 
