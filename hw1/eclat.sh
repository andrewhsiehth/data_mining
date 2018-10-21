#!/bin/bash
inputFile=$1 
minimumSupport=$2 
outputFile=$3 

python src/hw1.py -i $inputFile -o $outputFile -s $minimumSupport -e 