import requests
from bs4 import BeautifulSoup
from pyrogram import Client, Filters

from pyrobot import COMMAND_HAND_LER


@Client.on_message(Filters.command("coronatr", COMMAND_HAND_LER)  & Filters.me)
async def cor_tr(client: Client, message):
    x = await message.edit("`Corona Virüs Bilgileri https://covid19.saglik.gov.tr/ adresinden alınıyor..`")
    try:
        r = requests.get("https://covid19.saglik.gov.tr/")
        if r.status_code == 200:
            sayfa_linki = requests.get('https://covid19.saglik.gov.tr/')
            soup =  BeautifulSoup(sayfa_linki.content, 'html.parser')
            vakalar = soup.find_all(class_="list-group list-group-genislik")
            vaka = vakalar[0].text.split()
            toplam_test = vaka[3]
            toplam_vaka = vaka[7]
            toplam_olum = vaka[11]
            toplam_yog_bakım = vaka[17]
            entube = vaka[22]
            iyilesen = vaka[27]


            bugun_test = soup.find(class_="buyuk-bilgi-l-sayi").text
            bugun_= soup.find_all("span",class_="")
            bugun_vaka = bugun_[13].text
            bugun_vefat = bugun_[15].text
            bugun_iyilesen = bugun_[17].text

            tarih = soup.find(class_="takvim text-center")
            tarih = tarih.text.split()
            tarih_ = tarih[0] + " " + tarih[1] + " " + tarih[2]
            msg = """
Sağlık Bakanlığı Corona Virus Bilgileri
Kaynak: `https://covid19.saglik.gov.tr/`

Toplam Test: **{}**
Toplam Vaka: **{}**
Toplam Vefat: **{}**
Toplam Yoğun Bakımdaki Hasta: **{}**
Toplam Entübe: **{}**
Toplam İyileşen: **{}**

Bugünün Verileri

Bugünkü Test: **{}**
Bugünkü Vaka: **{}**
Bugünkü Vefat: **{}**
Bugünkü İyileşen: **{}**

Tarih: **{}**
""".format(
    toplam_test,
    toplam_vaka,
    toplam_olum,
    toplam_yog_bakım,
    entube,iyilesen,
    bugun_test,
    bugun_vaka,
    bugun_vefat,
    bugun_iyilesen,
    tarih_
)
            await x.edit(msg)
        else:
            await x.edit("`Bakanlık sitesine bağlanırken sorun oluştu`")
    except :
        await x.edit("`Hata oluştu. Hata kodu: {}`".format(str(err)))
