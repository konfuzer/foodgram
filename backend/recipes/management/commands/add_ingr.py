import json

from django.core.management.base import BaseCommand

from recipes.models import IngredientsModel


class Command(BaseCommand):
    help = "Импортируем ингредиенты из Json файла"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к Json файлу")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        exists = IngredientsModel.objects.exists()
        if exists:
            self.stderr.write(
                self.style.ERROR(
                    "Какие то ингредиенты уже загружены. прерываем"
                )
            )
            return
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                ingredients = [
                    IngredientsModel(
                        name=item["name"],
                        measurement_unit=item["measurement_unit"],
                    )
                    for item in data
                ]
                if ingredients:
                    IngredientsModel.objects.bulk_create(ingredients)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Загружено {len(ingredients)} ингредиентов"
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING("Нет ингредиентов к загрузке")
                    )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Ошибка импорта ингредиентов {e}")
            )
