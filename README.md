# otuzeros: README: Qiime2 auto remove features 
### Adrian Ortiz-Velez


This project was created to proved a mathematical backing to eliminting sparse speices 
in an OTU table or eliminating features in a sparce data matrix.

DOWNLOAD TO YOUR HARDRIVE and run in commandline. Usage below.

In this directory 
```
.
├── README.txt #
├── data
│   ├── PTforcoda.txt
│   ├── SHTforcoda.txt
│   ├── alexdata
│   │   ├── feature-table.biom
│   │   └── table.from_biom.tsv
│   ├── alexdataforcoda.txt
│   ├── cloroxforcoda.txt
│   ├── nickdata
│   │   ├── feature-table.biom
│   │   └── table.from_biom.tsv 
│   │       # For calc_hist to make a 'forcoda.txt' table 
│   ├── nickdataforcoda.txt     
│   │   # Ready for zero filtering
│   │
│   │	# Test data
│   ├── testdata.1.txt
│   ├── testdata.2.txt
│   ├── testdata.3.txt
│   ├── testdata.4.txt
│   ├── testdata.5.txt
│   ├── testdata.6.txt		 
│   └── testdata.txt		 
└── scripts
    ├── 2020-05-18_autoCutoff.py
    │   # Run in spyder to get plots 
    ├── 2021-01-10_autoCutoff.py 
    │   # Reads data and identfies where to filter the zeros
    └── 2021-07-26_calc_hist.py  
        # Reads OTU table 
```


DATE_autoCutoff.py: This code is meant to help the user define how many zeros to keep 
		    in their OTU table 

Usage:

	python3 DATE_autoCutoff.py FILENAME flag

Where:
	FILENAME: is the OTU table file
	flag: 0 or 1; use one as default unless the error statment from below 
	
	  File "calccutoff.py", line 62, in MakeFileForZeroFilteringCutoff
    		for ii in i[itterwhere]:
	TypeError: 'int' object is not iterable

Example:

	cd ./scripts
	python3 calccutoff.py ../data/alexdata/table.from_biom.tsv 0
 	table.from_biom.tsv:
	0/1: for file reading. if data is float == 1
				if data is string == 0
Output:
	Recommended  Cutoff: Keep features with up to and including 247 zeros

In R:
	
	#alex data
	OTUtableA <- read.csv('../data/alexdata/table.from_biom.tsv',
			     sep = '\t',header = T,row.names = 1,
			     check.names = F)

	tftabA<-OTUtableA==0
	tftabA[tftabA] <- 1

	#from python code
	CUTOFF <- 246.65
	sum(rowSums(tftabA)>CUTOFF)

	#Zerofiltered OTU table
	zerofiltOTUa <- OTUtableA[rowSums(tftabA)<CUTOFF,]
	dim(zerofiltOTUa)
