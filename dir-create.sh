#!/bin/bash

# Create directories Ch1 through Ch26
for i in {1..26}
do
    mkdir -p "Ch$i"
    echo "Created directory Ch$i"
done

echo "All directories have been created."
