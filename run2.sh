#!/bin/bash

# Check if a parameter was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <max_board_size>"
    echo "Example: $0 12"
    exit 1
fi

# Get the maximum board size from command line argument
max_n=$1

# Make sure executables are compiled and up-to-date
make

# Clear the output file
> output2.txt

echo "Running n_queens from size 5 up to size $max_n..."
echo "Results will be saved to output2.txt"

# Run for each size from 5 to max_n
for n in $(seq 5 $max_n); do
    # Run the n_queens program with time command and append the output to a file
    {
        echo ""
        echo "======================================================="
        echo "Running n_queens with board size $n:"
        echo "======================================================="
        # The 'time' command's output goes to stderr, so we redirect it to stdout
        { time ./n_queens $n; } 2>&1
        echo "======================================================="
        echo "Executed on: $(date)"
    } >> output2.txt
    
    echo "Completed board size $n"
done

echo "All executions completed. Results saved to output2.txt"
