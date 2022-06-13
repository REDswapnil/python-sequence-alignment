## INTRODUCTION

This is a Python implementation of the Sequence Alignment problem using the Dynamic Programming method.

Two different implementations are included, one being the basic algorithm and the second being the memory efficient equivalent of the basic algorthm.

Both implementations are written in pure Python.

## USAGE

Only Python - 3.10.0 is supported due to the usage of type-hinting syntax introduced in this version.

Running the script:
```
python basic_3.sh SampleTestCases/input1.txt output.txt
```
```
python efficient_3.sh SampleTestCases/input1.txt output.txt
```
Both the scripts will require 2 arguments:
1. The sample input from the mentioned directory
2. The output file to which the results will be written to

## EXAMPLES

Sample output when running the basic_3.py script with input1.txt:

```
Waking up...
Generating input strings
Starting Sequence Alignment DP Basic Algorithm...
Performing Sequence Alignment DP Basic Run
String 01: ACACACTGACTACTGACTGGTGACTACTGACTGGACTGACTACTGACTGGTGACTACTGACTGG (length - 64
String 02: TATTATTATACGCTATTATACGCGACGCGGACGCGTATACGCTATTATACGCGACGCGGACGCG (length - 64)
Initializing memo array...
Building memo array ...
Alignment Score :: 1296
Getting alignment of the 2 strings from the memo array
Str1 Alignment :: _______ACACACTG__ACTAC_TGACTG_GTGA__C_TACTGACTGGACTGACTACTGACTGGTGACTAC_TGACTG_G
Str2 Alignment :: TATTATTATACGCTATTA_TACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GCG_GAC_GCG
Time taken :: 4.719018936157227
Process Memory :: 13956
Writing output file to output.txt
Completed !
```

Sample output when running the efficient_3.py script with input1.txt:

```
Waking up...
Generating input strings
Starting Sequence Alignment DP Efficient Algorithm...
Time taken :: 3.4799575805664062
Process Memory :: 13344
Writing output file to output.txt
String 1 Alignment: _AC_AC_ACT__G__ACTA__C_TGACTG_GTGAC___TACTGACTGGACTGACTACTGACTGGTGACTACTG_ACTG_G
String 2 Alignment: TATTATTA_TACGCTATTATACGCGAC_GCG_GACGCGTA_T_AC__G_CT_ATTA_T_AC__GCGAC_GC_GGAC_GCG
Completed !
```