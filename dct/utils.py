import re


def is_ru(name: str) -> str:
    """Translation of the Cyrillic alphabet into the Latin alphabet."""
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


def add_order_filter_context(request):
    """Adding sorting and filtering data."""
    context = {}
    filtering = request.GET.get('filtering', '')
    context['filtering'] = filtering
    order = request.GET.get('order', '')
    context['order'] = order
    return context
