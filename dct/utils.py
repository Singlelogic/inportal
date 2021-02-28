import re

from django.utils import timezone


def is_ru(name: str) -> str:
    dictionary = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
                  'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k',
                  'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
                  'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c',
                  'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '', 'ы': 'y', 'ь': '',
                  'э': 'e', 'ю': 'u', 'я': 'ja',
                  }
    name = name.lower()
    if re.match(r'[а-яА-ЯёЁ]', name):
        for letter in name:
            if letter in dictionary:
                name = name.replace(letter, dictionary[letter])
    return name


def accum_lifetime(obj: 'Accumulator') -> int:
    """Returns the number of days worked by the battery."""
    sum = 0
    if obj.accumulatordate_set.all():
        for i in obj.accumulatordate_set.all():
            if i.state == 1:
                start = i.date
            else:
                stop = i.date
                delta = stop - start
                sum += delta.days
        if i.state == 1:
            delta = timezone.now() - start
            sum += delta.days
        return sum
    return 0
