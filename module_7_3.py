import os.path


class WordsFinder:
    file_names = []

    def __init__(self, *file_names):
        directory = 'text_files'
        file_names = [os.path.join(directory, file) for file in file_names]
        self.file_names = file_names

    def get_all_words_1(self) -> dict:  # через метод .translate() и str.maketrans()
        files_dict = {}

        for file in self.file_names:
            with open(file, 'r', encoding='utf-8') as f:
                all_words = []

                for line in f:
                    words_list = line.split()  # разбиваем строки по пробелу на слова

                    for word in words_list:  # проходимся по списку из слов
                        if word == '-':  # пропускаем слово - тире, которое могло появиться после разбиения строки
                            continue

                        all_words.append(word.lower().translate(str.maketrans('', '', '!?;:=.,')))  # задаем паттерн
                        # замены указанных символов на пустое значение (тире учтено ранее)

                files_dict[os.path.basename(f.name)] = all_words  # в ключ передаем базовое название файла, без пути
        return files_dict

    def get_all_words_2(self) -> dict:  # Через вспомогательную строку с исключаемыми символами. Сначала запарился и
        # Сделал не самым простым способом, пришлось чуток гугОл штрудировать, а потом сообразил, что можно сделать
        # проверочную строку. Позже ещё вспомнил, что можно было сделать через регулярки, через замену re.sub(), но
        # третий вариант уже не стал реализовывать, понятно, что там тоже довольно просто и работать будет исправно
        all_words = {}
        punctuation = ",.=!?;:"  # строка с исключаемыми символами

        for file in self.file_names:
            words = []

            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.lower()

                    for char in punctuation:
                        line = line.replace(char, '')
                        line = line.replace(' - ', '')

                    words.extend(line.split())
            all_words[os.path.basename(file)] = words
        return all_words

    def find(self, word) -> dict:
        result = {}

        iterator_words = iter(self.get_all_words_1().items())
        key, value = next(iterator_words)
        result[key] = value.index(word.lower()) + 1  # индексы с 0 элемента, позиция с 1
        return result

    def count(self, word) -> dict:
        result = {}

        iterator_words = iter(self.get_all_words_1().items())
        key, value = next(iterator_words)
        result[key] = value.count(word.lower())
        return result


if __name__ == '__main__':
    finder2 = WordsFinder('text_files/test_file.txt')
    print(finder2.get_all_words_1())  # Все слова, первый способ
    print(finder2.get_all_words_2())  # Все слова, второй способ
    print(finder2.find('TEXT'))  # 3 слово по счёту
    print(finder2.count('teXT'))  # 4 слова teXT в тексте всего
