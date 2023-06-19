"""
преобразовать текстовый файл книги в словарь, 
где ключами будут номера страниц, а значениями - тексты этих страниц.
"""
import os


PAGE_SIZE = 1050
book: dict[int, str] = {}

book: dict[int, str] = {}

# Функция, возвращающая строку с текстом страницы и ее размер
def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    # символы на которые должна заканчиваться страничка
    ending_symbols = '.,!?:;'
    # устанавливаем верхнюю границу для среза. Если максимальный размер фрагмента+смещение от точки старта больше размер входящего текста,
    # то верхняя граница = длине входящего текста.  
    if size + start < len(text)-1:
        size += start - 1
    else:
        size = len(text)-1
    
    # проверка на случай если срез на середине троеточия
    # в таком случае идем назад пока не натыкаемся на букву
    if size+1 < len(text):
        while text[size+1] in ending_symbols:
            size -= 1
        size += 1
            
    # здесь продолжаем идти назад проверяя, чтобы завершающий символ был знаком препинания
    # отсекая с конца все иные символы
    while text[size] not in ending_symbols and text[size+1]:
        size -= 1
   
    result = text[start:size+1]
    return result, len(result)



# Функция, формирующая словарь книги
def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    start = 0
    page_num = 1
    page, length = _get_part_text(text, start, PAGE_SIZE)
    book[page_num] = page.lstrip()
    while start + length < len(text):
        # print(start)
        page_num += 1
        start += length
        page, length = _get_part_text(text, start, PAGE_SIZE)
        book[page_num] = page.lstrip()
    
