#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

bool is_valid2(int *board, int n) {

    // Para cada rainha (linha)
    for (int i = 0; i < n; i++) {
        // Verificar colisões com todas as rainhas anteriores
        for (int j = 0; j < i; j++) {
            // Mesma coluna
            if (board[i] == board[j]){
                return false;
            }
            
            // Diagonal
            int row_diff = i - j;
            int col_diff = abs(board[i] - board[j]);
            
            // Se a diferença entre linhas for igual à diferença entre colunas,
            // então as rainhas estão na mesma diagonal
            if (row_diff == col_diff){
                return false;
            }
        }
    }
    return true;
}

void update(int *board, int n, int qnt) {
    int board_pos = n-1;
    
    while (board_pos >= 0 && qnt > 0) {
        board[board_pos] += qnt;
        if (board[board_pos] >= n) {
            qnt = board[board_pos] / n;
            board[board_pos] %= n;
            board_pos--;
        } else {
            qnt = 0;
        }
    }
}

void solve_n_queens_brute_force(int n) {
    // Board is represented as an array where the index is the row
    // and the value is the column where the queen is placed

    bool solution_found = false;
    unsigned long long configurations_checked = 0;
    
    int* board = calloc(n, sizeof(int));

    // Iterate through all possible configurations
    while (!solution_found) {
        configurations_checked++;

        bool valid = is_valid2(board, n);

        solution_found = valid;
        if (!valid) update(board, n, 1);
    }

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

int main(int argc, char *argv[]) {
    // Check if board size was provided
    if (argc != 2) {
        printf("Usage: %s <board_size>\n", argv[0]);
        return 1;
    }
    
    // Parse board size
    int n = atoi(argv[1]);
    
    // Validate board size
    if (n <= 0) {
        printf("Board size must be a positive integer\n");
        return 1;
    }
    
    solve_n_queens_brute_force(n);
    
    return 0;
}
