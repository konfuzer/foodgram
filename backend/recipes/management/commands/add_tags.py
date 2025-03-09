import json
from django.core.management.base import BaseCommand
from recipes.models import TagsModel

class Command(BaseCommand):
    help = "Импортируем теги из Json файла"

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help="Путь к Json файлу")

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        exists = TagsModel.objects.exists()
        if exists:
            self.stderr.write(self.style.ERROR(f"Какие то теги уже загружены. прерываем"))
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                tags = [
                    TagsModel(name=item["name"], slug=item["slug"])
                    for item in data
                ]
                if tags:
                    TagsModel.objects.bulk_create(tags)
                    self.stdout.write(self.style.SUCCESS(f"Загружено {len(tags)} тегов"))
                else:
                    self.stdout.write(self.style.WARNING("Нет тегов к загрузке"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка импорта тегов {e}"))
