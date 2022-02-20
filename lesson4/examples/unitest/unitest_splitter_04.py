import unittest


def super_split(line, types=None, delimiter=' '):
    """ Разбивает текстовую строку и при необходимости
        выполняет преобразование типов.
        Например:
        >>> super_split('GOOG 100 490.50')
        ['GOOG', '100', '490.50']
        >>> super_split('GOOG 100 490.50', [str, int, float])
        ['GOOG', 100, 490.5]
        >>>
        По умолчанию разбиение производится по пробельным символам,
        но имеется возможность указать другой символ-разделитель, в виде именованного аргумента:

        >>> super_split('GOOG,100,490.50', delimiter=',')
        ['GOOG', '100', '490.50']
        >>>
    """
    fields = line.split(delimiter)
    if types:
        fields = [ty(val) for ty, val in zip(types, fields)]
    return fields


# Модульные тесты
# (удобно выносить тесты в отдельный модуль, в примерах этого не делается для упрощения)
class TestSplitFunction(unittest.TestCase):
    def setUp(self):
        # Выполнить настройку тестов (если необходимо)
        pass

    def tearDown(self):
        # Выполнить завершающие действия (если необходимо)
        pass

    def test_simple_string(self):
        r = super_split('GOOG 100 490.50')
        self.assertEqual(r, ['GOOG', '100', '490.50'])

    def test_type_convert(self):
        r = super_split('GOOG 100 490.50', [str, int, float])
        self.assertEqual(r, ['GOOG', 100, 490.5])

    def test_delimiter(self):
        r = super_split('GOOG,100,490.50', delimiter=',')
        self.assertEqual(r, ['GOOG', '100', '490.50'])


# Запустить тестирование
if __name__ == '__main__':
    unittest.main()
