def grab_data() -> dict:
    """
    Сгенерировать случайные числа в качестве результата
    """

    from random import random
    return {
        'v1': random() * 100,
        'v2': random() * 100
    }
