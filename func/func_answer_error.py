#!/usr/bin/python
# -*- coding: utf-8 -*-

import random


def answer_error() -> str:
    """
    Описание

    Параметры:
    ----------
    
    Возвращает:
    -------
    """
    answer_error_list = [
        'Такое случается. Не расстраивайтесь, мы всё поправим.',
        'Ничего страшного, попейте кофе, гдядишь потом и получится.',
        'Видимо, пришло время взглянуть в окно и отдохнуть.',
        'Надеемся сегодня не понедельник, а то будет вдвойне обидно.',
        (
            'Возможно, Вы что-то сделали не так. Впрочем, какая' +
            ' разница. За окном солнце, жизнь продолжается.'
        ),
        'Срочно позовите разработчика, чтобы Вы не страдали в одиночестве',
        'Ошибки наши учителя. Надеемся и это нас чему-то научит.',
        'Как только поймёте как это исправить, сообщите нам.',
        'Мы что-то не доглядели. Сообщите и мы исправимся.',
        'Хм, нужно подумать...',
        'Поздравляем, Вы нашли место, которое не работает. Сообщите Нам!',
        (
            'Поздравляем, Вы один из немногих, кто увидел это. Но не' +
            ' отчаивайтесь, это не тупик, нужно действовать дальше.'
        ),
        'Сегодня можно уйти немного пораньше. Всё равно ничего не работает.',
    ]
    len_list = len(answer_error_list)
    rand = random.randint(0, len_list-1)
    return answer_error_list[rand]
