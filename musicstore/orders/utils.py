import qrcode
from io import BytesIO

def generate_qr_code(data):
    """
    Генерирует QR-код на основе входных данных.
    Возвращает изображение в виде байтов.
    """
    # Создаем объект QR-кода
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Генерация изображения
    img = qr.make_image(fill_color="black", back_color="white")

    # Сохраняем изображение в буфер
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)  # Перемещаем указатель в начало файла

    return buffer.getvalue()  # Возвращаем данные изображения в байтовом формате
