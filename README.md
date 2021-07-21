# otuzeros: README: Qiime2 auto remove features 
### Adrian Ortiz-Velez


Mathematical basis to remove taxa from an OTU table that are in few samples. 

This script was created to proved a mathematical backing to eliminting features with many 
zeros.

In this directory 
.

├── ./scripts/$DATE_autoCutoff.py      # Reads data and identfies where to cut off the data

├── ./data/testdata.txt            # Test data

└── README.txt


DATE_autoCutoff.py: This code is meant to help the user define how many zeros to keep in their OTU table 

Usage:
	python 2020-12-09_autoCutoff.py FILENAME

Where:
  FILENAME: is the file with the histogram data
			               
testdata.txt: File Format: one row of number of zeros 
			   one row of number of features with the coorisponding 
			       of zeros from the first row
                                    (spaces are added for ease of view) 
	                1,3,4,5,6,7,8,10,11,12,13,14,15,16,17, 18,  19,  20
	                1,1,5,8,4,3,2,3, 4, 2, 11,18,34,55,74,171,1272,8697

Note: 8697 features have 0s in 20 samples
