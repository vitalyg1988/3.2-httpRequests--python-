import requests
import os


path_files = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'texts')


class MyOpen:
    def __init__(self, file_name, language, mode, encode, language_translate='ru'):
        self.path_to_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'texts', file_name)
        self.language = language
        self.language_translate = language_translate
        self.encode = encode
        self.mode = mode

    def __enter__(self):
        self.file = open(self.path_to_file, self.mode, encoding=self.encode)
        return self

    def translation_text(self):
        param = {'key': 'trnsl.1.1.20190217T044905Z.c8ff12daf020e8b6.9c55c782fed3b95e78ae886f54d81aaa277aea16',
                 'text': self.file.read(),
                 'lang': '{}-{}'.format(self.language, self.language_translate)}
        response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate', params=param)
        return response.json()['text'][0]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()


def get_files_list(path_to_files):
    return os.listdir(path_to_files)


def get_lang(iitem):
    return iitem.split('.')[0].lower()


if __name__ == '__main__':
    for item in get_files_list(path_files):
        if '{} translated.txt'.format(get_lang(item)) not in get_files_list(path_files):
            if item == '{}.txt'.format(get_lang(item).upper()):
                with MyOpen(item, get_lang(item), mode='r', encode='utf8') as f:
                    with open(os.path.join(path_files,
                              '{} translated.txt'.format(get_lang(item))), 'w', encoding='utf8') as new_f:
                        new_f.write(f.translation_text())
