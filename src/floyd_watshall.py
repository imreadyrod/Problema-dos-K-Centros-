
n = int(input())

D_ant = [[]*n for i in range(n)]
for i in range(n):
    linha = input().split(' ')
    linha = list(map(int,linha))
    D_ant[i] = (linha)


P_ant = [[-1]*n for i in range(n)]
#nenhum custo será maior que o maior custo vezes o numero de vertices do grafo
#aqui foi estipulado como 100
infty = 100
for i in range(n):
    for j in range(n):
        if(0 < D_ant[i][j] < infty):
            P_ant[i][j] = i


D = [[0]*n for i in range(n)]
P = [[0]*n for i in range(n)]


for k in range(n):
    for i in range(n):
        for j in range(n):
            if D_ant[i][j] <= D_ant[i][k] + D_ant[k][j]:
                D[i][j] = D_ant[i][j]
                P[i][j] = P_ant[i][j]
            else:
                D[i][j] = D_ant[i][k] +  D_ant[k][j]
                P[i][j] = P_ant[k][j]
    for i in range(n):
        for j in range(n):
            D_ant[i][j] = D[i][j]
            P_ant[i][j] = P[i][j]

print(D)
print(P)

for i in range(n):
    for j in range(n):
        print("Caminho ótimo de", i+1, "para",j+1)
        print("Custo: ", D[i][j])
        print("Trajeto: ", end='')
        C = [j+1]
        k = P[i][j]
        while k != -1:
            C.append(k+1)
            k = P[i][k]
        print(list(reversed(C)))
        print()


'''
Entrada de exemplo

5
0 1 3 100 6
100 0 1 3 100
1 2 0 1 100
3 100 100 0 2
100 100 100 1 0
'''
