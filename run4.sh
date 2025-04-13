#!/bin/bash

# Check if a parameter was provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <max_board_size>"
    echo "Example: $0 12"
    exit 1
fi

# Get the maximum board size from command line argument
max_n=$1

# Array of thread counts to test
thread_counts=(16 8 4 2 1)

# Make sure executables are compiled and up-to-date
make

# Clear the output file
> output4.txt

echo "Running n_queens_threads from size 5 up to size $max_n with different thread counts..."
echo "Results will be saved to output4.txt"

# For each thread count
for threads in "${thread_counts[@]}"; do
    echo "Testing with $threads threads..."
    
    # Run for each size from 5 to max_n
    for n in $(seq 5 $max_n); do
        # Run the n_queens_threads program with time command and append the output to a file
        {
            echo ""
            echo "======================================================="
            echo "Running n_queens_threads with board size $n and $threads threads:"
            echo "======================================================="
            # The 'time' command's output goes to stderr, so we redirect it to stdout
            { time ./n_queens_threads $n $threads 0; } 2>&1
            echo "======================================================="
            echo "Executed on: $(date)"
        } >> output4.txt
        
        echo "Completed board size $n with $threads threads"
    done
    echo ""
done

echo "All executions completed. Results saved to output4.txt"
