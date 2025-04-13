#!/usr/bin/env python3
import re
import matplotlib.pyplot as plt
import numpy as np

def parse_log_file(filename):
    """
    Analisa o arquivo de log e extrai os tamanhos de tabuleiro, número de threads e tempos de execução.
    """
    data = {}  # Dicionário para armazenar os dados por número de threads
    
    with open(filename, 'r') as f:
        content = f.read()
        
        # Extraindo todas as execuções
        run_pattern = r'=+\nRunning n_queens_threads with board size (\d+) and (\d+) threads:.*?Thread (\d+) encontrou a solução.*?real\s+(\d+)m(\d+\.\d+)s.*?user\s+(\d+)m(\d+\.\d+)s.*?sys\s+(\d+)m(\d+\.\d+)s.*?=+\nExecuted on:'
        runs = re.findall(run_pattern, content, re.DOTALL)
        
        for run in runs:
            board_size = int(run[0])
            num_threads = int(run[1])
            found_thread = int(run[2])
            real_time = int(run[3]) * 60 + float(run[4])  # Converte para segundos
            user_time = int(run[5]) * 60 + float(run[6])  # Converte para segundos
            sys_time = int(run[7]) * 60 + float(run[8])   # Converte para segundos
            
            if num_threads not in data:
                data[num_threads] = {
                    'board_sizes': [],
                    'real_times': [],
                    'user_times': [],
                    'sys_times': [],
                    'found_threads': []
                }
            
            data[num_threads]['board_sizes'].append(board_size)
            data[num_threads]['real_times'].append(real_time)
            data[num_threads]['user_times'].append(user_time)
            data[num_threads]['sys_times'].append(sys_time)
            data[num_threads]['found_threads'].append(found_thread)
    
    return data

# Analisa o arquivo de log
all_data = parse_log_file('output4.txt')

# Organiza os dados para plotagem
thread_counts = sorted(all_data.keys())
board_sizes = sorted(set(size for thread_data in all_data.values() for size in thread_data['board_sizes']))

# Reorganiza os dados para facilitar a plotagem
organized_data = {}
for size in board_sizes:
    organized_data[size] = {
        'threads': [],
        'real_times': [],
        'user_times': [],
        'sys_times': []
    }
    
    for threads in thread_counts:
        # Encontra o índice do tamanho do tabuleiro nos dados para esse número de threads
        if size in all_data[threads]['board_sizes']:
            idx = all_data[threads]['board_sizes'].index(size)
            organized_data[size]['threads'].append(threads)
            organized_data[size]['real_times'].append(all_data[threads]['real_times'][idx])
            organized_data[size]['user_times'].append(all_data[threads]['user_times'][idx])
            organized_data[size]['sys_times'].append(all_data[threads]['sys_times'][idx])

# Calcula speedups em relação à versão sequencial (1 thread)
speedups_by_size = {}
for size in board_sizes:
    if 1 in organized_data[size]['threads'] and organized_data[size]['real_times'][organized_data[size]['threads'].index(1)] > 0:
        sequential_time = organized_data[size]['real_times'][organized_data[size]['threads'].index(1)]
        speedups = []
        for i, threads in enumerate(organized_data[size]['threads']):
            if organized_data[size]['real_times'][i] > 0:
                speedup = sequential_time / organized_data[size]['real_times'][i]
                speedups.append((threads, speedup))
        speedups_by_size[size] = speedups

# Cria uma figura com subplots
fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Análise de Desempenho do N-Queens', fontsize=16)

# Cores para diferentes tamanhos de tabuleiro - usando um mapa de cores mais vibrante
colors = plt.cm.tab10(np.linspace(0, 1, len(board_sizes)))

# 1. Gráfico de tempo de execução real vs número de threads (para cada tamanho de tabuleiro)
for i, size in enumerate(board_sizes):
    if organized_data[size]['threads'] and organized_data[size]['real_times']:
        marker = ['o', 's', '^', 'D', '*', 'x'][i % 6]  # Diferentes marcadores para cada tamanho
        axs[0, 0].plot(
            organized_data[size]['threads'], 
            organized_data[size]['real_times'], 
            marker + '-', 
            color=colors[i], 
            linewidth=2,
            markersize=8,
            label=f'N={size}'
        )
axs[0, 0].set_xlabel('Número de Threads')
axs[0, 0].set_ylabel('Tempo Real (segundos)')
axs[0, 0].set_title('Tempo de Execução Real vs Número de Threads')
axs[0, 0].set_xscale('log', base=2)  # Escala logarítmica para o número de threads
axs[0, 0].set_yscale('log')  # Escala logarítmica para o tempo também
axs[0, 0].set_xticks(sorted(thread_counts))
axs[0, 0].set_xticklabels(sorted(thread_counts))
axs[0, 0].legend(loc='upper right')
axs[0, 0].grid(True, which="both")  # Grade para linhas principais e secundárias

# 2. Gráfico de speedup vs número de threads (para cada tamanho de tabuleiro)
for i, size in enumerate(speedups_by_size.keys()):
    threads = [s[0] for s in speedups_by_size[size]]
    speedup_values = [s[1] for s in speedups_by_size[size]]
    marker = ['o', 's', '^', 'D', '*', 'x'][i % 6]  # Diferentes marcadores para cada tamanho
    axs[0, 1].plot(
        threads, 
        speedup_values, 
        marker + '-', 
        color=colors[i], 
        linewidth=2,
        markersize=8,
        label=f'N={size}'
    )

axs[0, 1].set_xlabel('Número de Threads')
axs[0, 1].set_ylabel('Speedup (T1/Tn)')
axs[0, 1].set_title('Speedup vs Número de Threads')
axs[0, 1].set_xscale('log', base=2)  # Escala logarítmica para o número de threads
axs[0, 1].set_xticks(sorted(thread_counts))
axs[0, 1].set_xticklabels(sorted(thread_counts))
# Adiciona linha diagonal para speedup ideal
max_threads = max(thread_counts)
axs[0, 1].plot([1, max_threads], [1, max_threads], 'k--', label='Speedup Ideal')
axs[0, 1].legend(loc='upper left')
axs[0, 1].grid(True)

# 3. Gráfico de tempo de CPU do usuário vs número de threads
for i, size in enumerate(board_sizes):
    if organized_data[size]['threads'] and organized_data[size]['user_times']:
        marker = ['o', 's', '^', 'D', '*', 'x'][i % 6]  # Diferentes marcadores para cada tamanho
        axs[1, 0].plot(
            organized_data[size]['threads'], 
            organized_data[size]['user_times'], 
            marker + '-', 
            color=colors[i], 
            linewidth=2,
            markersize=8,
            label=f'N={size}'
        )
axs[1, 0].set_xlabel('Número de Threads')
axs[1, 0].set_ylabel('Tempo CPU do Usuário (segundos)')
axs[1, 0].set_title('Tempo CPU do Usuário vs Número de Threads')
axs[1, 0].set_xscale('log', base=2)  # Escala logarítmica para o número de threads
axs[1, 0].set_xticks(sorted(thread_counts))
axs[1, 0].set_xticklabels(sorted(thread_counts))
axs[1, 0].legend(loc='upper right')
axs[1, 0].grid(True)

# 4. Gráfico de eficiência (speedup/número de threads) vs número de threads
for i, size in enumerate(speedups_by_size.keys()):
    threads = [s[0] for s in speedups_by_size[size]]
    speedup_values = [s[1] for s in speedups_by_size[size]]
    efficiency_values = [s/t for s, t in zip(speedup_values, threads)]
    marker = ['o', 's', '^', 'D', '*', 'x'][i % 6]  # Diferentes marcadores para cada tamanho
    axs[1, 1].plot(
        threads, 
        efficiency_values, 
        marker + '-', 
        color=colors[i], 
        linewidth=2,
        markersize=8,
        label=f'N={size}'
    )

axs[1, 1].set_xlabel('Número de Threads')
axs[1, 1].set_ylabel('Eficiência (Speedup/Threads)')
axs[1, 1].set_title('Eficiência vs Número de Threads')
axs[1, 1].set_xscale('log', base=2)  # Escala logarítmica para o número de threads
axs[1, 1].set_xticks(sorted(thread_counts))
axs[1, 1].set_xticklabels(sorted(thread_counts))
axs[1, 1].axhline(y=1.0, color='k', linestyle='--', label='Eficiência Ideal')
axs[1, 1].legend(loc='upper right')
axs[1, 1].grid(True)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('n_queens_performance.png', dpi=300)

# Verifica se o ambiente é interativo antes de tentar mostrar a figura
import matplotlib
if matplotlib.get_backend().lower() in ['tk', 'gtk', 'wx', 'qt4', 'qt5', 'qt', 'macosx']:
    plt.show()
else:
    print("Gráfico salvo em 'n_queens_performance.png'")
    # Não chama plt.show() em ambientes não-interativos
