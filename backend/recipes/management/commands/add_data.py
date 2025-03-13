import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = "Импортируем данные (ингредиенты и теги) из JSON файлов"

    DATA_FILES = {
        "ingredients": {
            "model": Ingredient,
            "file_path": "../data/ingredients.json",
            "fields": ["name", "measurement_unit"],
        },
        "tags": {
            "model": Tag,
            "file_path": "../data/tags.json",
            "fields": ["name", "slug"],
        },
    }

    def handle(self, *args, **kwargs):
        for key, config in self.DATA_FILES.items():
            model = config["model"]
            file_path = config["file_path"]
            fields = config["fields"]

            if model.objects.exists():
                self.stderr.write(
                    self.style.ERROR(
                        f"Какие-то {key} уже загружены. Прерываем"
                    )
                )
            else:
                self.load_data(model, file_path, fields, key)

    def load_data(self, model, file_path, fields, data_type):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            objects = [
                model(**{field: item[field] for field in fields})
                for item in data
            ]

            if objects:
                model.objects.bulk_create(objects)
                self.stdout.write(
                    self.style.SUCCESS(f"Загружено {len(objects)} {data_type}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Нет {data_type} к загрузке")
                )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Ошибка импорта {data_type}: {e}")
            )
