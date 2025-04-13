#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <omp.h>

// Variável global para controlar quando uma solução é encontrada

bool is_valid2(int *board, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (board[i] == board[j]){
                return false;
            }
            
            // Diagonal
            int row_diff = i - j;
            int col_diff = abs(board[i] - board[j]);
        
            if (row_diff == col_diff){
                return false;
            }
        }
    }
    return true;
}

void _update(int *board, int n, int qnt, int board_pos) {
    if (board_pos < 0) return;
    int curr = board[board_pos] + qnt;
    if (curr >= n) {
        _update(board, n, 1, board_pos-1);
    }
    board[board_pos] = curr % n;
}

void update(int *board, int n, int qnt) {
    _update(board, n, qnt, n-1);
}

bool solve_n_queens_brute_force(int n, int start, int num_threads, int *found, int print_board) {

    bool solution_found = false;
    unsigned long long configurations_checked = 0;

    
    int* board = calloc(n, sizeof(int));
    update(board, n, start);

    while (!solution_found) {
        if (*found) return false;
        configurations_checked++;

        bool valid = is_valid2(board, n);

        if (valid) {
            solution_found = true;

            #pragma omp atomic write
            *found = 1;

            printf("Thread %d encontrou a solução\n", start);
            break;
        } else {
            update(board, n, num_threads);
        }
    }

    if (print_board) {
        for (int i = 0; i < n; i++) {
            int pos = board[i];
            for(int j = 0 ; j<n; j++){
                printf("%c ", j==pos ? 'Q' : '.');
            }
            printf("\n");
        }
        printf("\n");
        printf("%llu configurations checked\n", configurations_checked);
    }
    return true;
}

int main(int argc, char *argv[]) {
    // Check if board size and number of threads were provided
    if (argc < 3 || argc > 4) {
        printf("Usage: %s <board_size> <num_threads> [print_board=1]\n", argv[0]);
        printf("       print_board: 1 para imprimir o tabuleiro (padrão), 0 para não imprimir\n");
        return 1;
    }
    
    // Parse board size and number of threads
    int n = atoi(argv[1]);
    int num_threads = atoi(argv[2]);
    
    // Parse print_board flag (default is 1 - print board)
    int print_board = 1;
    if (argc == 4) {
        print_board = atoi(argv[3]);
    }
    
    // Validate board size
    omp_set_num_threads(num_threads);
    if (n <= 0) {
        printf("Board size must be a positive integer\n");
        return 1;
    }
    
    // double start_time = omp_get_wtime();

    int found = 0;

    #pragma omp parallel shared(found)
    {
        int thread_id = omp_get_thread_num();
        solve_n_queens_brute_force(n, thread_id, num_threads, &found, print_board);
    }
    
    return 0;
}
