import qrcode
import parser_selenium
import rest_class
from datetime import datetime
def qr_generator(data):

       abonent_id = rest_class.abon_id(data[3])
       client = rest_class.abon_street(abonent_id)
       metadata = datetime.now()
       dt_string = metadata.strftime("%d/%m/%Y %H:%M")
       data = f"{dt_string} \n"  \
              f"{data[3]} \n"
       img = qrcode.make(data)
       img.save("test1.png")
