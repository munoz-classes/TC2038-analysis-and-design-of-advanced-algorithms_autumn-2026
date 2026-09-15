import argparse
import sys


def suma(a: int, b: int):
    return a + b


if __name__ == "__main__":
    if len(sys.argv) > 1:
        a = int(sys.argv[1])
        b = int(sys.argv[2])
        print(suma(a, b))
    else:
        print("Llamada sin parametros")
