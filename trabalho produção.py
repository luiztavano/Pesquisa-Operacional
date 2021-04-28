from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable, LpMinimize
import pandas as pd

# Declarando os conjuntos
# fornecedores
s = 4
# matérias_primas
f = 14
# níveis de desconto
d = 5
# períodos
theta = 4
# tarefas
t = 29
# unidades de produção
m = 3
# subperíodos
fi = 8
# Produtos
j = 10
# unidades de embalagem
n = 1
# todos os tanques de armazenamento
k = 11

# Declarando os parâmetros
# Níveis de desconto por fornecedor, 5 níveis para cada um dos 4 fornecedores - DIS
niveis_desconto = {0: [0, 0.03, 0.10, 0.22, 0.25],
                    1: [0, 0.07, 0.13, 0.20, 0.26],
                    2: [0, 0.05, 0.18, 0.22, 0.30],
                    3: [0, 0.06, 0.17, 0.23, 0.31]}

#custo da compra de matéria prima de acordo com fornecedor, para cada uma das 14 matérias primas tem o custo dos 4 fornecedores
custo_comprar_materia_prima_fornecedores = {0: [2, 2, 3, 2], 1: [3, 4, 5, 3], 2: [5, 5, 3, 4], 3: [3, 2, 2, 2], 4: [2, 5, 3, 1],
                                            5: [6, 3, 5, 4], 6: [4, 4, 6, 4], 7: [6, 8, 2, 2], 8: [4, 3, 2, 4], 9: [6, 2, 3, 3],
                                            10: [3, 4, 2, 2], 11: [4, 6, 3, 3], 12: [2, 3, 4, 1], 13: [1, 3, 3, 5]}

# Número Suficientemente Grande (α)
numero_suficientemente_grande = 1_000_000_000

# Custos com fornecedor
custos_fornecedor = {0: 51, 1: 54, 2: 46, 3: 40}

# Custo de armazenamento das matérias primas
custo_armazenamento_materias_primas = {0: 529, 1: 881, 2: 999, 3: 529, 4: 646, 5: 1058, 6: 1058, 7: 1058, 8: 764, 9: 823, 10: 646, 11: 940, 12: 588, 13: 705}

# Inventário máximo das matérias primas
inventario_maximo_materias_primas = {0: 4000, 1: 0, 2: 400, 3: 100, 4: 300, 5: 600, 6: 0, 7: 200, 8: 500, 9: 100, 10: 1000, 11: 600, 12: 2500, 13: 300}

# tarefas, cada uma com seu número e as horas para produzir unidades 1, 2, 3, respectivamente
tarefas = {0: [1, 3, 2], 1: [2, 1, 3], 2: [3, 2, 2], 3: [2, 5, 3], 4: [4, 3, 4],
            5: [3, 4, 4], 6: [4, 6, 6], 7: [2, 3, 5], 8: [5, 2, 6], 9: [2, 6, 7],
            10: [5, 5, 5], 11: [2, 7, 4], 12: [6, 2, 3], 13: [3, 1, 3], 14: [2, 5, 5],
            15: [5, 3, 2], 16: [6, 3, 3], 17: [3, 4, 2], 18: [2, 2, 5], 19: [5, 3, 7],
            20: [3, 5, 3], 21: [6, 2, 2], 22: [3, 3, 1], 23: [1, 3, 6], 24: [3, 3, 5],
            25: [3, 5, 3], 26: [6, 4, 4], 27: [2, 2, 3], 28: [6, 5, 5]}

# tempo para fazer o setup da produção, para cada tarefa tem os tempos de cada uma das 3 unidades de produção
tempo_setup_producao = {0: [13, 14, 12], 1: [13, 14, 12], 2: [13, 14, 12], 3: [13, 14, 12], 4: [13, 14, 12],
                        5: [13, 14, 12], 6: [13, 14, 12], 7: [13, 14, 12], 8: [13, 14, 12], 9: [13, 14, 15],
                        10: [13, 14, 15], 11: [19, 17, 15], 12: [19, 17, 15], 13: [19, 17, 15], 14: [19, 17, 15],
                        15: [19, 17, 15], 16: [19, 17, 15], 17: [19, 17, 15], 18: [11, 12, 10], 19: [11, 12, 10],
                        20: [11, 12, 10], 21: [11, 12, 10], 22: [11, 12, 10], 23: [11, 12, 10], 24: [11, 12, 10],
                        25: [11, 12, 10], 26: [11, 12, 10], 27: [11, 12, 10], 28: [11, 12, 10]}

# Tamanho máximo do lote da tarefa t produzida na unidade de produção m
tamanho_maximo_lote_tarefa_produzida_na_unidade_produção = {0: [6, 6, 6], 1: [4, 4, 4], 2: [5, 5, 5], 3: [6, 6, 6], 4: [4, 4, 4],
                                                            5: [5, 5, 5], 6: [6, 6, 6], 7: [4, 4, 4], 8: [5, 5, 5], 9: [6, 6, 6],
                                                            10: [4, 4, 4], 11: [5, 5, 5], 12: [6, 6, 6], 13: [4, 4, 4], 14: [5, 5, 5],
                                                            15: [6, 6, 6], 16: [4, 4, 4], 17: [5, 5, 5], 18: [6, 6, 6], 19: [4, 4, 4],
                                                            20: [5, 5, 5], 21: [6, 6, 6], 22: [4, 4, 4], 23: [5, 5, 5], 24: [6, 6, 6],
                                                            25: [4, 4, 4], 26: [5, 5, 5], 27: [6, 6, 6], 28: [4, 4, 4]}

# consumo de matéria-prima f para produzir um lote da tarefa t na unidade de produção m, para cada tarefa tem os valores das
# 3 unidades de produção, respectivamente
consumo_materia_prima_produzir_lote_cada_tarefa_unidade_producao = {0: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},
                                                                    
                                                                    1: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},

                                                                    2: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},
                                                                    
                                                                    3: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},

                                                                    4: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},
                                                                    
                                                                    5: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},
                                                                    
                                                                    6: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},                                                                   

                                                                    7: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},
                                                                    
                                                                    8: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},                                                                    

                                                                    9: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},

                                                                    10: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},

                                                                    11: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},

                                                                    12: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]},

                                                                    13: {0: [3, 4, 3], 1: [5, 4, 3], 2: [2, 3, 4], 3: [2, 3, 2], 4: [1, 2, 3],
                                                                    5: [2, 6, 2], 6: [1, 2, 4], 7: [2, 3, 4], 8: [3, 4, 3], 9: [5, 4, 3],
                                                                    10: [2, 3, 4], 11: [2, 3, 2], 12: [1, 2, 3], 13: [2, 6, 2], 14: [1, 2, 4],
                                                                    15: [2, 3, 4], 16: [3, 4, 3], 17: [5, 4, 3], 18: [2, 3, 4], 19: [2, 3, 2],
                                                                    20: [1, 2, 3], 21: [2, 6, 2], 22: [1, 2, 4], 23: [2, 3, 4], 24: [3, 4, 3],
                                                                    25: [5, 4, 3], 26: [2, 3, 4], 27: [2, 3, 2], 28: [1, 2, 3]}}


# Tamanho mínimo do lote da tarefa t produzida na unidade de produção m, para cada tarefa tem o tamanho de cada unidade de produção, respectivamente
tamanho_minimo_lote_tarefa_produzida_na_unidade_producao = {0: [2, 2, 2], 1: [1, 1, 1], 2: [2, 2, 2], 3: [3, 3, 3], 4: [1, 1, 1],
                                                            5: [1, 1, 1], 6: [2, 2, 2], 7: [1, 1, 1], 8: [2, 2, 2], 9: [2, 2, 2],
                                                            10: [1, 1, 1], 11: [2, 2, 2], 12: [2, 2, 2], 13: [1, 1, 1], 14: [2, 2, 2],
                                                            15: [2, 2, 2], 16: [1, 1, 1], 17: [2, 2, 2], 18: [2, 2, 2], 19: [1, 1, 1],
                                                            20: [2, 2, 2], 21: [2, 2, 2], 22: [1, 1, 1], 23: [2, 2, 2], 24: [2, 2, 2],
                                                            25: [1, 1, 1], 26: [2, 2, 2], 27: [2, 2, 2], 28: [1, 1, 1]}

# Porcentagem do produto j produzido na tarefa t na unidade m
porcentagem_produto_j_tarefa_t_producao_m = {0: [0.25, 0.35, 0.40], 1: [0.20, 0.30, 0.50], 2: [0.45, 0.20, 0.35], 3: [0.26, 0.50, 0.24], 4: [0.35, 0.35, 0.30],
                                             5: [0.33, 0.33, 0.34], 6: [0.25, 0.35, 0.40], 7: [0.25, 0.25, 0.50], 8: [0.42, 0.28, 0.30], 9: [0.10, 0.23, 0.67],
                                            10: [0.30, 0.30, 0.40], 11: [0.20, 0.55, 0.25], 12: [0.48, 0.22, 0.30], 13: [0.45, 0.25, 0.30], 14: [0.27, 0.43, 0.30],
                                            15: [0.35, 0.45, 0.20], 16: [0.50, 0.20, 0.30], 17: [0.35, 0.40, 0.25], 18: [0.25, 0.20, 0.55], 19: [0.30, 0.25, 0.45],
                                            20: [0.33, 0.35, 0.32], 21: [0.45, 0.35, 0.20], 22: [0.40, 0.40, 0.20], 23: [0.20, 0.30, 0.50], 24: [0.35, 0.25, 0.40],
                                            25: [0.25, 0.45, 0.30], 26: [0.40, 0.25, 0.35], 27: [0.30, 0.30, 0.40], 28: [0.35, 0.30, 0.35]}

# demanda do produto embalado j no período θ
demanda_produto_embalado_j_periodo_theta = {0: [1, 3, 5, 3, 2, 1, 5, 6, 7, 3], 1: [4, 5, 2, 3, 4, 1, 3, 5, 4, 3], 2: [5, 6, 4, 3, 4, 5, 6, 7, 3, 4],
                                    3: [4, 3, 2, 1, 5, 7, 5, 4, 3, 2]}

# demanda no subperíodo φ para cada produto a granel j
demanda_produtos_granel_j_subperiodos_fi = {0: [5, 4, 3, 4, 3, 2, 2, 3, 1, 3], 1: [5, 6, 4, 3, 4, 5, 6, 7, 3, 4], 2: [4, 3, 2, 1, 5, 7, 5, 4, 3, 2],
                                        3: [1, 3, 5, 3, 2, 1, 5, 6, 7, 3], 4: [4, 5, 2, 3, 4, 1, 3, 5, 4, 3], 5: [4, 3, 2, 6, 4, 2, 5, 6, 2, 2],
                                        6: [2, 5, 6, 3, 2, 6, 4, 2, 3, 3], 7: [5, 5, 6, 3, 1, 2, 3, 4, 5, 6]}

#realizando a transposição da tabela para j fi
demanda_produtos_granel_j_subperiodos_fi = pd.DataFrame(demanda_produtos_granel_j_subperiodos_fi)
demanda_produtos_granel_j_subperiodos_fi = demanda_produtos_granel_j_subperiodos_fi.T

# Tempo de processamento disponível para a unidade de embalagem m no subperíodo φ
tempo_processamento_unidade_embalagem_m_superiodo_fi = 345600
tempo_processamento_unidade_embalagem_n_superiodo_fi = 345600

# tempo para fazer as embalagens de cada produto, o tempo é em segundos
tempo_fazer_embalagens = {0:{0: 12, 1: 13, 2: 14, 3: 15, 4: 14, 5: 12, 6: 16, 7: 19, 8: 13, 9: 15}}

# tempo para fazer o setup para as embalagens de cada produto
tempo_setup_embalagem = {0:{0: 15, 1: 13, 2: 16, 3: 19, 4: 15, 5: 14, 6: 12, 7: 11, 8: 17, 9: 15}}


# Inventário máximo das matérias primas
inventario_maximo_materias_primas = {0: 4000, 1: 0, 2: 400, 3: 100, 4: 300, 5: 600, 6: 0, 7: 200, 8: 500, 9: 100, 10: 1000, 11: 600, 12: 2500, 13: 300}

# Capacidade de armazenamento
capacidade_armazenamento = {0: 170, 1: 210, 2: 250, 3: 280, 4: 660, 5: 660, 6: 770, 7: 1240, 8: 1260, 9: 1310, 10:	1350}

# Inventário máximo dos produtos a granel
inventario_maximo_produtos_granel = {0: 44, 1:38, 2:29, 3:20, 4:19, 5:24, 6:27, 7:31, 8:24, 9:21}

# Custo de armazenamento dos produtos
custo_armazenamento_produtos = {0: 250.20, 1: 271.05, 2: 291.90, 3: 312.75, 4: 291.90, 5: 250.20, 6: 333.60, 7: 396.15, 8: 271.05, 9: 312.75}

# Custo de setup ##adicionado custo por tarefa por máquina, antes só estava por máquina
custo_setup = {0: [0.78,0.78,0.78], 1: [0.78,0.78,0.78], 2: [0.78,0.78,0.78], 3: [0.78,0.78,0.78], 4: [0.78,0.78,0.78], 5: [0.78,0.78,0.78], 6: [0.78,0.78,0.78], 7: [0.78,0.78,0.78], 8: [0.78,0.78,0.78], 9: [0.84,0.84,0.84], 10: [0.84,0.84,0.84],
                11: [1.02,1.02,1.02], 12: [1.02,1.02,1.02], 13: [1.02,1.02,1.02], 14: [1.02,1.02,1.02], 15: [1.02,1.02,1.02], 16: [1.02,1.02,1.02], 17: [1.02,1.02,1.02], 18: [0.66,0.66,0.66], 19: [0.66,0.66,0.66], 20: [0.66,0.66,0.66],
                21: [0.66,0.66,0.66], 22: [0.66,0.66,0.66], 23: [0.66,0.66,0.66], 24: [0.66,0.66,0.66], 25: [0.66,0.66,0.66], 26: [0.66,0.66,0.66], 27: [0.66,0.66,0.66], 28: [0.66,0.66,0.66]}

# Custo de produção por tarefa, por máquina  ##adicionado custo por tarefa por máquina, antes só estava por máquina
custos_producao_tarefa = {0: [1,1,1], 1: [1,1,1], 2: [1,1,1], 3: [1,1,1], 4: [1,1,1], 5: [2,2,2], 6: [2,2,2], 7: [2,2,2], 8: [2,2,2], 9: [2,2,2], 10: [2,2,2], 11: [2,2,2], 12: [2,2,2], 13: [2,2,2], 14: [2,2,2],
                          15: [3,3,3], 16: [3,3,3], 17: [3,3,3], 18: [3,3,3], 19: [2,2,2], 20: [2,2,2], 21: [2,2,2], 22: [2,2,2], 23: [2,2,2], 24: [2,2,2], 25: [1,1,1], 26: [1,1,1], 27: [1,1,1], 28: [1,1,1]}


#-----PROGRAMAÇÃO LINEAR-----

#----Definição do Modelo----

model = LpProblem(name="Problema_da_Produção", sense=LpMinimize)

#----Definição das variáveis----

#---Variáveis contínuas---

quantidade_materia_prima_f_comprada_fornecedor_s_nivel_desconto_d_periodo_theta = LpVariable.dicts("quantidade_materia_prima_f_comprada_fornecedor_s_nivel_desconto_d_periodo_theta",(range(f),range(s), range(d),range(theta)), lowBound=(0),cat="Continuous")

tamanho_lote_tarefa_t_producao_m_subperíodo_fi = LpVariable.dicts("tamanho_lote_tarefa_t_producao_m_subperíodo_fi",(range(t),range(m), range(fi)),lowBound=(0), cat="Continuous")

quantidade_embalada_produto_j_embalagem_n_subperíodo_fi = LpVariable.dicts("quantidade_embalada_produto_j_embalagem_n_subperíodo_fi",(range(j),range(n), range(fi)),lowBound=(0), cat="Continuous")

estoque_materia_prima_f_período_theta = LpVariable.dicts("estoque_materia_prima_f_período_theta",(range(f),range(theta)),lowBound=(0), cat="Continuous")

estoque_produto_granel_j_subperíodo_fi = LpVariable.dicts("estoque_produto_granel_j_subperíodo_fi",(range(j),range(fi)),lowBound=(0), cat="Continuous")

estoque_produto_embalado_j_período_theta = LpVariable.dicts("estoque_produto_embalado_j_período_theta",(range(j),range(theta)),lowBound=(0), cat="Continuous")

#---Variáveis binárias---

fornecedor_s_período_theta = LpVariable.dicts("fornecedor_s_período_theta",(range(s),range(theta)), cat="Binary")

tarefa_t_producao_m_subperíodo_fi = LpVariable.dicts("tarefa_t_producao_m_subperíodo_fi",(range(t),range(m),range(fi)), cat="Binary")

produto_de_embalagem_j_unidade_de_embalagem_n_subperíodo_fi = LpVariable.dicts("produto_de_embalagem_j_unidade_de_embalagem_n_subperíodo_fi",(range(j),range(n),range(fi)), cat="Binary")

fornecedores_nível_desconto_d_período_theta = LpVariable.dicts("fornecedores_nível_desconto_d_período_theta",(range(s),range(d),range(theta)), cat="Binary")

tanque_k_armazena_matéria_prima_f_período_theta = LpVariable.dicts("tanque_k_armazena_matéria_prima_f_período_theta",(range(k),range(f),range(theta)), cat="Binary")

tanque_k_armazena_produto_granel_j_subperodo_fi = LpVariable.dicts("tanque_k_armazena_produto_granel_j_subperodo_fi",(range(k),range(j),range(fi)), cat="Binary")

#---Variáveis Inteiras---

int_tarefa_t_producao_m_subperiodo_fi = LpVariable.dicts("int_tarefa_t_producao_m_subperiodo_fi",(range(t),range(m),range(fi)),lowBound=(0), cat="Integer")


# # #----Definição da Função objetivo----

# obj_func1 = lpSum((1-niveis_desconto[j][k]) * 
#                   lpSum(custo_comprar_materia_prima_fornecedores[i][j] 
#                         * quantidade_materia_prima_f_comprada_fornecedor_s_nivel_desconto_d_periodo_theta[i][j][k][l] 
#                         for i in range(f)) 
#                   for j in range(s) for k in range(d) for l in range(theta))
# model += obj_func1

# #função ok
# obj_func2 = lpSum(custos_fornecedor[j] * fornecedor_s_período_theta[j][k] 
#                   for j in range(s) for k in range(theta))
# model += obj_func2

# obj_func3 = lpSum(custo_armazenamento_materias_primas[i] * estoque_materia_prima_f_período_theta[i][k]
#                   for i in range(f) for k in range(theta))
# model += obj_func3

# #####Não entendi essa função objetivo, removi o somatório de theta
# obj_func4 = lpSum(custo_armazenamento_produtos[a] / fi * estoque_produto_granel_j_subperíodo_fi[a][c]
#                   for a in range(j) for c in range(fi))
# model += obj_func4

# obj_func5 = lpSum(custo_armazenamento_produtos[a] * estoque_produto_embalado_j_período_theta[a][b]
#                   for a in range(j) for b in range(theta))
# model += obj_func5

# #função ok
# obj_func6 = lpSum(custo_setup[a][b] * tarefa_t_producao_m_subperíodo_fi[a][b][c]
#                   for a in range(t) for b in range(m) for c in range(fi))
# model += obj_func6

# #função ok
# obj_func7 = lpSum(custos_producao_tarefa[a][b] * int_tarefa_t_producao_m_subperiodo_fi[a][b][c]
#                   for a in range(t) for b in range(m) for c in range(fi))
# model += obj_func7


# #----Definição da Função objetivo----

obj_func = ((lpSum((1-niveis_desconto[j][k]) *lpSum(custo_comprar_materia_prima_fornecedores[i][j] * quantidade_materia_prima_f_comprada_fornecedor_s_nivel_desconto_d_periodo_theta[i][j][k][l] for i in range(f)) 
                  for j in range(s) for k in range(d) for l in range(theta)))

             + (lpSum(custos_fornecedor[j] * fornecedor_s_período_theta[j][k] 
                  for j in range(s) for k in range(theta)))

             + (lpSum(custo_armazenamento_materias_primas[i] * estoque_materia_prima_f_período_theta[i][k]
                  for i in range(f) for k in range(theta)))

             + (lpSum(custo_armazenamento_produtos[a] / fi * estoque_produto_granel_j_subperíodo_fi[a][c]
                  for a in range(j) for c in range(fi)))

             + (lpSum(custo_armazenamento_produtos[a] * estoque_produto_embalado_j_período_theta[a][b]
                  for a in range(j) for b in range(theta)))

             + (lpSum(custo_setup[a][b] * tarefa_t_producao_m_subperíodo_fi[a][b][c]
                  for a in range(t) for b in range(m) for c in range(fi)))

             + (lpSum(custos_producao_tarefa[a][b] * int_tarefa_t_producao_m_subperiodo_fi[a][b][c]
                  for a in range(t) for b in range(m) for c in range(fi))))


model += obj_func

#----Restrições----

#Purchasing constraints
#(2)
# for i in range(compy):
#     model += (lpSum(x[i][j] for j in range(compx)) == 1)

(3)
for i in range(s):
    for k in range(theta):        
        model += (lpSum(fornecedores_nível_desconto_d_período_theta[i][j][k] for j in range(d))
                  <= fornecedor_s_período_theta[i][k])

#(4)
for i in range(s):
    for k in range(theta):
        model += (lpSum(quantidade_materia_prima_f_comprada_fornecedor_s_nivel_desconto_d_periodo_theta[j][i][l][k] for j in range(f) for l in range(d))
                  <= numero_suficientemente_grande * fornecedor_s_período_theta[i][k])


#Production tasks constraints #restrições ok
#(5)
for j in range(m):
    for k in range(fi):
        model += (lpSum((tarefas[i][j] * int_tarefa_t_producao_m_subperiodo_fi[i][j][k]) + (tempo_setup_producao[i][j] * tarefa_t_producao_m_subperíodo_fi[i][j][k])for i in range(t))
                  <= tempo_processamento_unidade_embalagem_m_superiodo_fi)
 
     
#(6)
for i in range(t):
    for j in range(m):
        for k in range(fi):
            model += (int_tarefa_t_producao_m_subperiodo_fi[i][j][k]
                      <=numero_suficientemente_grande * tarefa_t_producao_m_subperíodo_fi[i][j][k])

#(7)
for i in range(t):
    for j in range(m):
        for k in range(fi):
            model += (tamanho_maximo_lote_tarefa_produzida_na_unidade_produção[i][j] * int_tarefa_t_producao_m_subperiodo_fi[i][j][k]
                      <= tamanho_lote_tarefa_t_producao_m_subperíodo_fi[i][j][k] <= tamanho_minimo_lote_tarefa_produzida_na_unidade_producao[i][j] * int_tarefa_t_producao_m_subperiodo_fi[i][j][k])

   
#Packing tasks constraints #restrições ok
#(8)
for l in range(n):
    for k in range(fi):
        model += (lpSum((tempo_fazer_embalagens[l][i] * quantidade_embalada_produto_j_embalagem_n_subperíodo_fi[i][l][k]) + (tempo_setup_embalagem[l][i] * produto_de_embalagem_j_unidade_de_embalagem_n_subperíodo_fi[i][l][k]) for i in range(j))
                  <= tempo_processamento_unidade_embalagem_n_superiodo_fi)

#(9)
for i in range(j):
    for j in range(n):
        for k in range(fi):
            model += (quantidade_embalada_produto_j_embalagem_n_subperíodo_fi[i][j][k]
                      <= numero_suficientemente_grande * produto_de_embalagem_j_unidade_de_embalagem_n_subperíodo_fi[i][j][k])


#Inventory control constraints
#(10)
#verificar sinais de menos na restrição, na variável consumo de matéria prima, só possui o consumo de uma matéria
for i in range(f):
    for j in range(theta-1):
        model +=(estoque_materia_prima_f_período_theta[i][j] + lpSum(quantidade_materia_prima_f_comprada_fornecedor_s_nivel_desconto_d_periodo_theta[i][a][b][j] for a in range(s) for b in range(d))
                  == lpSum(consumo_materia_prima_produzir_lote_cada_tarefa_unidade_producao[i][o][p] * tamanho_lote_tarefa_t_producao_m_subperíodo_fi[o][p][q] for o in range(t) for p in range(m) for q in range(fi)) + estoque_materia_prima_f_período_theta[i][j+1])

#(11)
#na variável porcentagem de consumo de matéria prima, só possui o consumo de uma matéria
for c in range(j):
    for e in range(fi-1):          
        model +=(estoque_produto_granel_j_subperíodo_fi[c][e] + lpSum(porcentagem_produto_j_tarefa_t_producao_m[a][b]*tamanho_lote_tarefa_t_producao_m_subperíodo_fi[a][b][e+1] for a in range(t) for b in range(m))
                  == demanda_produtos_granel_j_subperiodos_fi[c][e+1] +  lpSum(quantidade_embalada_produto_j_embalagem_n_subperíodo_fi[c][g][e+1] for g in range(n)) + estoque_produto_granel_j_subperíodo_fi[c][e+1])
#(12)
for c in range(j):
    for d in range(theta-1):
        model +=(estoque_produto_embalado_j_período_theta[c][d] + lpSum(quantidade_embalada_produto_j_embalagem_n_subperíodo_fi[c][a][b] for a in range(n) for b in range(fi))
                  == demanda_produto_embalado_j_periodo_theta[d+1][c] + estoque_produto_embalado_j_período_theta[c][d+1])


#Multipurpose storage tank control constraints
#(13)
for i in range(f):
    for j in range(theta):
        model += (estoque_materia_prima_f_período_theta[i][j]
                  <= inventario_maximo_materias_primas[i] + (lpSum(capacidade_armazenamento[l] * tanque_k_armazena_matéria_prima_f_período_theta[l][i][j] for l in range(k))))

#(14)
for i in range(j):
    for l in range(fi):
        model += (estoque_produto_granel_j_subperíodo_fi[i][l]
                  <= inventario_maximo_produtos_granel[i] + (lpSum(capacidade_armazenamento[g] * tanque_k_armazena_produto_granel_j_subperodo_fi[g][i][l] for g in range(k))))

#(15)
for b in range(k):
    e= -1 
    for c in range(fi):
        resto = c%2
        if resto == 0:
            e = e + 1     
        model +=(lpSum(tanque_k_armazena_produto_granel_j_subperodo_fi[b][l][c] for l in range(j)) + lpSum(tanque_k_armazena_matéria_prima_f_período_theta[b][a][e] for a in range(f)) <= 1)


#----Executar modelo----
status = model.solve()

print(LpStatus[status])

#Ótimo da função
otimo = model.objective.value()

print("Valor da funçao objetivo:", otimo)

# print(model.objective)

#Exibir valores das variáveis
for var in model.variables():
    if var.value() != 0:
        print (var.name, var.value())


