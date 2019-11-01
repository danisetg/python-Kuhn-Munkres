from Khun import Khun

g = list()
while True:
    print("Introduzca la cantidad de X")
    n = input()
    try:
        n = int(n)
        for x in range(n):
            g.append(list())
            g[x] = [int(number) for number in input().split(' ')]
        kuhn = Khun(n, g)
        m = kuhn.solve()
        c = 0
        print("El apareamiento resultante es:")
        for x in range(n):
            print(x, m[x] - n)
            c += g[x][m[x] - n]
        print("El costo resultante es ", c)
            
    except:
        if n == 'exit':
            break
        else:
            print("Debe introducir un valor numérico")