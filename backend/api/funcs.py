import base64
import binascii


def convert_base64_int(pk):
    if isinstance(pk, str) and not pk.isdigit():
        try:
            pk = base64.urlsafe_b64decode(pk).decode()
        except (binascii.Error, binascii.Error):
            return pk
    return pk


def create_output_shopping_cart(ingredients):
    file_content = ""
    for item in ingredients:
        file_content += (
            f"{item['ingredient__name']} "
            f"{item['total_amount']}"
            f" {item['ingredient__measurement_unit']}\n"
        )

    return file_content
