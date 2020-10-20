# coding: utf-8
from __future__ import unicode_literals

import pytest


ABBREV_TESTS = [
        ("Dr. Murat Bey ile görüştüm.", ["Dr.", "Murat", "Bey", "ile", "görüştüm", "."]),
        ("Dr.la görüştüm.", ["Dr.la", "görüştüm", "."]),
        ("Dr.'la görüştüm.", ["Dr.'la", "görüştüm", "."]),
        ("TBMM'de çalışıyormuş.", ["TBMM'de", "çalışıyormuş", "."]),
        ("Hem İst. hem Ank. bu konuda gayet iyi durumda.", ["Hem", "İst.", "hem", "Ank.", "bu", "konuda", "gayet", "iyi", "durumda", "."]),
        ("Hem İst. hem Ank.'da yağış var.", ["Hem", "İst.", "hem", "Ank.'da", "yağış", "var", "."]),
        ("Dr.", ["Dr."]),
        ("Yrd.Doç.", ["Yrd.Doç."]),
        ("Prof.'un", ["Prof.'un"]),
        ("Böl.'nde", ["Böl.'nde"]),
]



NUMBER_TESTS = [
        ("Rakamla 6 yazılıydı.", ["Rakamla", "6", "yazılıydı", "."]),
        ("Hava -4 dereceydi.", ["Hava", "-4", "dereceydi", "."]),
        ("Hava sıcaklığı -4ten +6ya yükseldi.", ["Hava", "sıcaklığı", "-4ten", "+6ya", "yükseldi", "."]),
        ("Hava sıcaklığı -4'ten +6'ya yükseldi.", ["Hava", "sıcaklığı", "-4'ten", "+6'ya", "yükseldi", "."]),
        ("Yarışta 6. oldum.", ["Yarışta", "6.", "oldum", "."]),
        ("Yarışta 438547745. oldum.", ["Yarışta", "438547745.", "oldum", "."]),
        ("Kitap IV. Murat hakkında.",["Kitap", "IV.", "Murat", "hakkında", "."]),
        ("Bana söylediği sayı 6.", ["Bana", "söylediği", "sayı", "6", "."]),
        ("Saat 6'da buluşalım.", ["Saat", "6'da", "buluşalım", "."]),
        ("Saat 6dan sonra buluşalım.", ["Saat", "6dan", "sonra", "buluşalım", "."]),
        ("6.dan sonra saymadım.", ["6.dan", "sonra", "saymadım", "."]),
        ("6.'dan sonra saymadım.", ["6.'dan", "sonra", "saymadım", "."]),
        ("Saat 6'ydı.", ["Saat", "6'ydı", "."]),
        ("5'te", ["5'te"]),
        ("6'da", ["6'da"]),
        ("9dan", ["9dan"]),
        ("19'da", ["19'da"]),
        ("VI'da", ["VI'da"]),
        ("5.", ["5", "."]),
        ("72.", ["72", "."]),
        ("VI.", ["VI", "."]),
        ("6.'dan", ["6.'dan"]),
        ("19.'dan", ["19.'dan"]),
        ("6.dan", ["6.dan"]),
        ("16.dan", ["16.dan"]),
        ("VI.'dan", ["VI.'dan"]),
        ("VI.dan", ["VI.dan"]),
        ("Hepsi 1994 yılında oldu.", ["Hepsi", "1994", "yılında", "oldu", "."]),
        ("Hepsi 1994'te oldu.", ["Hepsi", "1994'te", "oldu", "."]),
        ("2/3 tarihli faturayı bulamadım.", ["2/3", "tarihli", "faturayı", "bulamadım", "."]),
        ("2.3 tarihli faturayı bulamadım.", ["2.3", "tarihli", "faturayı", "bulamadım", "."]),
        ("2.3. tarihli faturayı bulamadım.", ["2.3.", "tarihli", "faturayı", "bulamadım", "."]),
        ("2/3/2020 tarihli faturayı bulamadm.", ["2/3/2020", "tarihli", "faturayı", "bulamadm", "."]),
        ("2/3/1987 tarihinden beri burda yaşıyorum.", ["2/3/1987", "tarihinden", "beri", "burda", "yaşıyorum", "."]),
        ("2-3-1987 tarihinden beri burdayım.", ["2-3-1987", "tarihinden", "beri", "burdayım", "."]),
        ("2.3.1987 tarihinden beri burdayım.", ["2.3.1987", "tarihinden", "beri", "burdayım", "."]),
        ("Bu olay 2005-2006 tarihleri arasında oldu.", ["Bu", "olay", "2005", "-", "2006", "tarihleri", "arasında", "oldu", "."]),
        ("Bu olay 4/12/2005-21/3/2006 tarihleri arasında oldu.", ["Bu", "olay", "4/12/2005", "-", "21/3/2006", "tarihleri", "arasında", "oldu", ".",]),
        ("Ek fıkra: 5/11/2003-4999/3 maddesine göre uygundur.", ["Ek", "fıkra", ":", "5/11/2003-4999/3", "maddesine", "göre", "uygundur", "."]),
        ("2/A alanları: 6831 sayılı Kanunun 2 nci maddesinin birinci fıkrasının (A) bendine göre", []),
        ("2-3-2025", ["2-3-2025",]),
        ("2/3/2025", ["2/3/2025"]),
        ("Yıllardır 0.5 uç kullanıyorum.", ["Yıllardır", "0.5", "uç", "kullanıyorum", "."]),
        ("Kan değerlerim 0.5-0.7 arasıydı.", ["Kan", "değerlerim", "0.5", "-", "0.7", "arasıydı", "."]),
        ("0.5", ["0.5"]),
        ("%1", ["%", "1"]),
        ("%1.5", ["%", "1.5"]),
        ("%1-%2 arası büyüme bekleniyor.", ["%", "1", "-", "%", "2", "arası", "büyüme", "bekleniyor", "."]),
        ("%1-2 arası büyüme bekliyoruz.", ["%", "1", "-", "2", "arası", "büyüme", "bekleniyor", "."]),
        ("%1.5luk büyüme bekliyoruz.", ["%", "1.5luk", "büyüme", "bekleniyor", "."]),
        ("Saat 1-2 arası gelin lütfen.", ["Saat", "1", "-", "2", "arası", "gelin", "lütfen", "."]),
        ("Saat 15:30 gibi buluşalım.", ["Saat", "15:30", "gibi", "buluşalım", "."]),
        ("Saat 15:30'da buluşalım.", ["Saat", "15:30'da", "buluşalım", "."]),
        ("Saat 15.30'da buluşalım.", ["Saat", "15.30'da", "buluşalım", "."]),
        ("Saat 15.30da buluşalım.", ["Saat", "15.30da", "buluşalım", "."]),
        ("Saat 15 civarı buluşalım.", ["Saat", "15", "civarı", "buluşalım", "."]),
        ("9’daki otobüse binsek mi?", ["9’daki", "otobüse", "binsek", "mi", "?"]),
        ("Okulumuz 3-B şubesi", ["Okulumuz", "3-B", "şubesi"]),
        ("Okulumuz 3/B şubesi", ["Okulumuz", "3/B", "şubesi"]),
        ("Okulumuz 3B şubesi", ["Okulumuz", "3B", "şubesi"]),
        ("Okulumuz 3b şubesi", ["Okulumuz", "3b", "şubesi"]),
        ("Antonio Gaudí 20. yüzyılda, 1904-1914 yılları arasında on yıl süren bir reform süreci getirmiştir.", ["Antonio", "Gaudí", "20.", "yüzyılda", ",", "1904", "-", "1914", "yılları", "arasında", "on", "yıl", "süren", "bir", "reform", "süreci", "getirmiştir", "."]),
        ("Dizel yakıtın avro bölgesi ortalaması olan 1,165 avroya kıyasla litre başına 1,335 avroya mal olduğunu gösteriyor.", ["Dizel", "yakıtın", "avro", "bölgesi", "ortalaması", "olan", "1,165", "avroya", "kıyasla", "litre", "başına", "1,335", "avroya", "mal", "olduğunu", "gösteriyor", "."]),
        ("Marcus Antonius M.Ö. 1 Ocak 49'da, Sezar'dan Vali'nin kendisini barış dostu ilan ettiği bir bildiri yayınlamıştır.", ["Marcus", "Antonius", "M.Ö.", "1", "Ocak", "49'da", ",", "Sezar'dan", "Vali'nin", "kendisini", "barış", "dostu", "ilan", "ettiği", "bir", "bildiri", "yayınlamıştır", "."])
]


PUNCT_TESTS = [
        ("Gitmedim dedim ya!", ["Gitmedim", "dedim", "!"]),
        ("Gitmedim dedim ya!!", ["Gitmedim", "dedim", "!", "!"]),
        ("Gitsek mi?", ["Gitsek", "mi", "?"]),
        ("Gitsek mi??", ["Gitsek", "mi", "?", "?"]),
        ("Gitsek mi?!?", ["Gitsek", "mi", "?", "!", "?"]),
        ("Ankara - Antalya arası otobüs işliyor.", ["Ankara", "-",  "Antalya", "arası", "otobüs", "işliyor", "."]),
        ("Ankara-Antalya arası otobüs işliyor.", ["Ankara", "-", "Antalya", "arası", "otobüs", "işliyor", "."]),
        ("Sen--ben, ya da onlar.", ["Sen", "--", "ben", ",", "ya", "da", "onlar", "."]),
        ("Senden, benden, bizden şarkısını biliyor musun?", ["Senden", ",", "benden", ",", "bizden", "şarkısını", "biliyor", "musun", "?"]),
        ("Akif'le geldik, sonra da o ayrıldı.", ["Akif'le", "geldik", ",", "sonra", "da", "o", "ayrıldı", "."]),
        ("Bu adam ne dedi şimdi???", ["Bu", "adam", "ne", "dedi", "şimdi", "?", "?", "?"]),
        ("Yok hasta olmuş, yok annesi hastaymış, bahaneler işte...", ["Yok", "hasta", "olmuş", ",", "yok", "annesi", "hastaymış", ",", "bahaneler", "işte", ".", ".", "."]),
        ("Ankara'dan İstanbul'a ... bir aşk hikayesi.", ["Ankara'dan", "İstanbul'a", "...", "bir", "aşk", "hikayesi", "."]),
        ("Ahmet'te", ["Ahmet'te"]),
        ("İstanbul'da", ["İstanbul'da"]),
]

GENERAL_TESTS = [
        ("1914'teki Endurance seferinde, Sir Ernest Shackleton'ın kaptanlığını yaptığı İngiliz Endurance gemisi yirmi sekiz kişi ile Antarktika'yı geçmek üzere yelken açtı.", ["1914'teki", "Endurance", "seferinde", ",", "Sir", "Ernest", "Shackleton'ın", "kaptanlığını", "yaptığı", "İngiliz", "Endurance", "gemisi", "yirmi", "sekiz", "kişi", "ile", "Antarktika'yı", "geçmek", "üzere", "yelken", "açtı", "."]),
        ("Danışılan \"%100 Cospedal\" olduğunu belirtti.", ["Danışılan", '"', "%", "100", "Cospedal", '"', "olduğunu", "belirtti", "."]),
        ("1976'da parkur artık kullanılmıyordu; 1990'da ise bir yangın, daha sonraları ahırlarla birlikte yıkılacak olan tahta tribünlerden geri kalanları da yok etmişti.", ["1976'da", "parkur", "artık", "kullanılmıyordu", ";", "1990'da", "ise", "bir", "yangın", ",", "daha", "sonraları", "ahırlarla", "birlikte", "yıkılacak", "olan", "tahta", "tribünlerden", "geri", "kalanları", "da", "yok", "etmişti", "."]),
        ("Dahiyane bir ameliyat ve zorlu bir rehabilitasyon sürecinden sonra, tamamen iyileştim.", ["Dahiyane", "bir", "ameliyat", "ve", "zorlu", "bir", "rehabilitasyon", "sürecinden", "sonra", ",", "tamamen", "iyileştim", "."]),
        ("Yaklaşık iki hafta süren bireysel erken oy kullanma döneminin ardından 5,7 milyondan fazla Floridalı sandık başına gitti.", ["Yaklaşık", "iki", "hafta", "süren", "bireysel", "erken", "oy", "kullanma", "döneminin", "ardından", "5,7", "milyondan", "fazla", "Floridalı", "sandık", "başına", "gitti", "."]),
        ("Ancak, bu ABD Çevre Koruma Ajansı'nın dünyayı bu konularda uyarmasının ardından ortaya çıktı.", ["Ancak", ",", "bu", "ABD", "Çevre", "Koruma", "Ajansı'nın", "dünyayı", "bu", "konularda", "uyarmasının", "ardından", "ortaya", "çıktı", "."]),
        ("Ortalama şansa ve 10.000 Sterlin değerinde tahvillere sahip bir yatırımcı yılda 125 Sterlin ikramiye kazanabilir.", ["Ortalama", "şansa", "ve", "10.000", "Sterlin", "değerinde", "tahvillere", "sahip", "bir", "yatırımcı", "yılda", "125", "Sterlin", "ikramiye", "kazanabilir", "."]),
        ("Granit adaları; Seyşeller ve Tioman ile Saint Helena gibi volkanik adaları kapsar." , ["Granit", "adaları", ";", "Seyşeller", "ve", "Tioman", "ile", "Saint", "Helena", "gibi", "volkanik", "adaları", "kapsar", "."]),
        ("Barış antlaşmasıyla İspanya, Amerika'ya Porto Riko, Guam ve Filipinler kolonilerini devretti.", ["Barış", "antlaşmasıyla", "İspanya", "Amerika'ya", "Porto", "Riko", "Guam", "ve", "Filipinler", "kolonilerini", "devretti", "."]),
        ("Makedonya\'nın sınır bölgelerini güvence altına alan Philip, büyük bir Makedon ordusu kurdu ve uzun bir fetih seferi için Trakya\'ya doğru yürüdü.", ["Makedonya\'nın", "sınır", "bölgelerini", "güvence", "altına", "alan", "Philip", ",", "büyük", "bir", "Makedon", "ordusu", "kurdu", "ve", "uzun", "bir", "fetih", "seferi", "için", "Trakya\'ya", "doğru", "yürüdü", "."]),
        ("Fransız gazetesi Le Figaro'ya göre bu hükumet planı sayesinde 42 milyon Euro kazanç sağlanabilir ve elde edilen paranın 15.5 milyonu ulusal güvenlik için kullanılabilir.", ["Fransız", "gazetesi", "Le", "Figaro'ya", "göre", "bu", "hükumet", "planı", "sayesinde", "42", "milyon", "Euro", "kazanç", "sağlanabilir", "ve", "elde", "edilen", "paranın", "15.5", "milyonu", "ulusal", "güvenlik", "için", "kullanılabilir", "."]),
        ("Ortalama şansa ve 10.000 Sterlin değerinde tahvillere sahip bir yatırımcı yılda 125 Sterlin ikramiye kazanabilir.", ["Ortalama", "şansa", "ve", "10.000", "Sterlin", "değerinde", "tahvillere", "sahip", "bir", "yatırımcı", "yılda", "125", "Sterlin", "ikramiye", "kazanabilir", "."]),
        ("3 Kasım Salı günü, Saint-Gaudens Belediye Başkanı 2014'te hükümetle birlikte oluşturulan kentsel gelişim anlaşmasını askıya alma kararı verdi.", ["3", "Kasım", "Salı", "günü", ",", "Saint-Gaudens", "Belediye", "Başkanı", "2014'te", "hükümetle", "birlikte", "oluşturulan", "kentsel", "gelişim", "anlaşmasını", "askıya", "alma", "kararı", "verdi", "."]),
        ("Stalin, Abakumov'u Beria'nın enerji bakanlıkları üzerindeki baskınlığına karşı MGB içinde kendi ağını kurmaya teşvik etmeye başlamıştı.", ["Stalin", ",", "Abakumov'u", "Beria'nın", "enerji", "bakanlıkları", "üzerindeki", "baskınlığına", "karşı", "MGB", "içinde", "kendi", "ağını", "kurmaya", "teşvik", "etmeye", "başlamıştı", "."]),
        ("Güney Avrupa'daki kazı alanlarının çoğunluğu gibi, bu bulgu M.Ö. 5. yüzyılın başlar", ["Güney", "Avrupa'daki", "kazı", "alanlarının", "çoğunluğu", "gibi", ",", "bu", "bulgu", "M.Ö.", "5.", "yüzyılın", "başlar"]),
        ("Sağlığın bozulması Hitchcock hayatının son yirmi yılında üretimini azalttı.", ["Sağlığın", "bozulması", "Hitchcock", "hayatının", "son", "yirmi", "yılında", "üretimini", "azalttı", "."]),
]


TESTS = (ABBREV_TESTS + NUMBER_TESTS + PUNCT_TESTS + GENERAL_TESTS)



def test_tr_tokenizer_exc_lemma_in_text(tr_tokenizer):
    text = "Dr. Murat Bey ile görüştüm."
    tokens = tr_tokenizer(text)
    assert len(tokens) == 6
    assert tokens[0].text == "Dr."
    assert tokens[0].lemma_ == "doktor"



@pytest.mark.parametrize("text,expected_tokens", TESTS)
def test_tr_tokenizer_handles_allcases(tr_tokenizer, text, expected_tokens):
    tokens = tr_tokenizer(text)
    token_list = [token.text for token in tokens if not token.is_space]
    assert expected_tokens == token_list


