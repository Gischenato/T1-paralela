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

void print_board(int *board, int n) {
    for (int i = 0; i < n; i++) {
        int pos = board[i];
        for(int j = 0 ; j<n; j++){
            printf("%c ", j==pos ? 'Q' : '.');
        }
        printf("\n");
    }
    printf("\n");
}

bool solve_n_queens_brute_force(int n, int start, int num_threads, int *found, int should_print_board, int total_solutions_to_find) {

    bool all_solutions_found = false;
    unsigned long long configurations_checked = 0;

    
    int* board = calloc(n, sizeof(int));
    update(board, n, start);

    while (!all_solutions_found) {
        if (*found >= total_solutions_to_find) return false;
        configurations_checked++;

        bool valid = is_valid2(board, n);

        if (valid) {
            all_solutions_found = *found >= total_solutions_to_find;

            #pragma omp atomic write
            *found = *found + 1;

            printf("Thread %d encontrou uma solução\n", start);
            // break;
            // print_board(board, n);
        } 

        update(board, n, num_threads);
    }

    if (should_print_board) {
        print_board(board, n);

        printf("\n");
        printf("%llu configurations checked\n", configurations_checked);
    }
    return true;
}

int main(int argc, char *argv[]) {
    // Check if board size and number of threads were provided
    if (argc < 3 || argc > 5) {
        printf("Usage: %s <board_size> <num_threads> <total_solutions_to_find> [should_print_board=1]\n", argv[0]);
        printf("       print_board: 1 para imprimir o tabuleiro (padrão), 0 para não imprimir\n");
        return 1;
    }

    // Quantidade de soluções que devem ser encontradas
    
    // Parse board size and number of threads
    int n = atoi(argv[1]);
    int num_threads = atoi(argv[2]);
    int qnt = atoi(argv[3]);
    if (qnt == 0) qnt = 1;
    
    // Parse print_board flag (default is 1 - print board)
    int should_print_board = 1;
    if (argc == 4) {
        should_print_board = atoi(argv[4]);
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
        solve_n_queens_brute_force(n, thread_id, num_threads, &found, should_print_board, qnt);
    }
    
    return 0;
}
