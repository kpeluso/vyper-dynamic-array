#!/bin/bash

for var in "$@"
do
    # assumes $var is .vy file in contracts/
    vyper contracts/$var.vy > bytecode/$var.txt 
    vyper contracts/$var.vy -f 'abi' > abi/$var.json 
done

# Run with:     chmod u+x
#               ./getCodes.sh DynamicArray_uint DynamicArray_str

