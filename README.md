# Escalonador Curto

Repositório para a atividade Simulador de escalonador de curto prazo da disciplina de Sistemas Operacionais.

# O Projeto

O projeto foi realizado como uma atividade da disciplina de Sistemas Operacionais. O Simulador é um escalonador com a política de escalonamento de fila de Prioridades com cada fila utilizando o Round-Robin

# Requisitos


Preferimos que seja utilizado o Python 3.10. Última versão que o projeto foi testado foi [Python 3.10.8](https://www.python.org/downloads/release/python-3108/), recomendamos o uso.

# Maneira de Executar

```
git clone https://github.com/Pruzny/escalonador-curto
cd escalonador-curto
python main.py
```

# Argumentos adicionais


| Flag | Função                        |
|------|-------------------------------|
| -v   | Utilizando essa flag o **mesmo resultado** que é impresso em process.out, é impresso no terminal. | 
| -n   | Indica a quantidade de filas, ao utilizar -n, é esperado que você utilize um valor inteiro após essa flag, exemplo -n value |
| -q   | Indica o valor de quantum de cada fila, ao utilizar -q, é esperado que você utilize N valores inteiro após essa flag, exemplo -q values[N] |

Observações, essas flags devem vir em sequência, caso utilize -q sem utilizar -n, os valores serão padrões, vice-versa também é válida.

Exemplo de uso:
```
1. python main.py -v -n 5 -q  2 4 6 8 10
2. python main.py -v -n 6 -q  2 4 6 8 10 12
3. python main.py -n 6 -q  2 4 6 8 10 12
```
**A saída de todas estarão em process.out, o primeiro e segundo caso, irá imprimir também o que foi escrito nesse arquivo. No terceiro caso, todo o resultado se encontra apenas no arquivo process.out**

# Entrada Esperada

No arquivo **process.in** deve conter tempo de admissão, nome do programa, prioridade, listas de tempo de burst
CPU e I/O. Tempo de bust de CPU e I/O devem ser intercalados sempre terminando com tempo de burst de CPU.

Exemplo de entrada válida: 
```
0 PROG01 1 20
0 PROG02 1 10 5 10
5 PROG10 1 5 3 15 5 10
3 PROG03 2 30
10 PROG15 1 5 1 15 1 20 50
```
