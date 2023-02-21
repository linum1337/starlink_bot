import qrcode
import parser_selenium
from datetime import datetime
def qr_generator(data):
       parsed = parser_selenium.request_parser(parser_selenium.login_form(data[3], data[4]))
       lic = parser_selenium.lic_parse(parsed[1])[1]
       lic = str(str(str(lic).split('<td>')[1]).split('</td>')[0])
       dogovor = parser_selenium.lic_parse(parsed[1])[5]
       dogovor = str(str(str(dogovor).split('<td>')[1]).split('</td>')[0])
       client = parser_selenium.client_parse(parsed[0])[0]
       client = " ".join(str(str(str(client).split('<p class="no-margin">')[1]).split('</p>')[0]).split())
       metadata = datetime.now().date()
       print(metadata)
       data = f"Дата создания: {metadata} \n" \
              f"Номер лицевого счёта: {lic} \n" \
              f"Договор: {dogovor} \n" \
              f"Абонент: \n {client}"

       img = qrcode.make(data)
       img.save("test1.png")
