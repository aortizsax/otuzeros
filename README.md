# otuzeros: README: Post-Qiime2 auto remove features/speices
### Adrian Ortiz-Velez


This project was created to proved a mathematical backing to eliminting sparse speices 
in an OTU table or eliminating features in a sparce data matrix. 
Input: OTU table
Output: Zero filtered table ready for downstream analysis

Download and run in commandline. Usage below.

Dependincies:
 * Pandas 1.3.3
 * Numpy 1.19.2
 * Matplotlib 3.3.4
 * SciPy 1.7.1

In this directory 
```
.
├── README.txt #
├── data
│   ├── alexdata
│   │   ├── feature-table.biom
│   │   └── table.from_biom.tsv #OTU table
│   └── nickdata
│       ├── feature-table.biom
│       └── table.from_biom.tsv #OTU table
└── scripts
    └── calccutoff.py   
	# commandline script
```


2021-11-08_calccutoff.py: This code is meant to help the user define how many zeros to keep 
		    in their OTU table 

Usage:

	python3 2021-11-08_calccutoff.py.py FILENAME 

Where:
	FILENAME: is the tab seperated OTU table file 

Example:

	cd ./scripts
	python3 2021-11-08_calccutoff.py ../data/alexdata/table.from_biom.tsv 
Output:
* Makes a new directory in the same as the input table
* Saves graphs of finding the max curvature
* Saves zero filtered table in the new directory
* Outputs code below for alexdata exaple
```
Recommended  Cutoff: Keep features with up to and including 247 zeros	
```

