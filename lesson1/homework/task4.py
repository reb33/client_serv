# Преобразовать слова «разработка», «администрирование», «protocol», «standard»
# из строкового представления в байтовое
# и выполнить обратное преобразование (используя методы encode и decode).


def main():
    arr = ['разработка', 'администрирование', 'protocol', 'standard']
    for i in arr:
        encoded = i.encode(encoding='utf-8')
        decoded = encoded.decode(encoding="utf-8")
        print(f'{i}   -   {encoded}   -   {decoded}')


if __name__ == '__main__':
    main()