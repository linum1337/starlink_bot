import qrcode
import parser_selenium
import rest_class
from datetime import datetime
def qr_generator(data):
       abonent_id = rest_class.abon_id(data[3])
       client = rest_class.abon_street(abonent_id)
       metadata = datetime.now().date()
       print(metadata)
       data = f"Дата создания: {metadata} \n"  \
              f"Договор: {data[3]} \n" \
              f"Абонент: \n {client}"

       img = qrcode.make(data)
       img.save("test1.png")

