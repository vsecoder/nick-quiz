"""
https://twinery.org - Twine - инструмент для удобного создания интерактивных историй.
"""
import json


class TweeReader:
    """
    TweeReader is a class that reads a .twee file and returns the formatted data.
    """

    def __init__(self, path):
        self.path = path
        self.content = self.read()

        self.stop_words = ['StoryTitle', 'StoryData', 'StoryAuthor']

    def read(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            return f.read()

    def to_html(self, data):
        """
        // ... // - курсив
        '' ... '' - жирный
        """
        while '//' in data or "''" in data:
            data = data.replace('//', '<i>', 1).replace('//', '</i>', 1)
            data = data.replace("''", '<b>', 1).replace("''", '</b>', 1)

        return data

    def get_links(self, text):
        """
        [[Название|Ссылка на другую сцену]]
        """
        for link in text.split('[[')[1:]:
            link = link.split(']]')[0]
            title = link.split('|')[0]
            link = link.split('|')[1]

            yield title, link

    def format(self):
        data = {
            'data': {},
            'scenes': {},
            'all_links': []
        }

        for line in self.content.split('::'):
            if not line:
                continue

            title = line.split('\n')[0].strip()
            text = line.split('\n', 1)[1:][0].strip()
            if title in self.stop_words:
                data['data'][title] = text \
                    if title != 'StoryData' else (
                    json.loads(text.replace('\n', ''))
                )
            else:
                image = text.split('\n')[0].strip()
                text = text.replace(image, '')
                title = title.split('{')[0].strip()
                data['scenes'][title] = {
                    'image': image,
                    'title': title.split('{')[0].strip(),
                    'text': self.to_html(text.split('[[')[0].strip()),
                    'links': list(self.get_links(text))
                }

        return data
