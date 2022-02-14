from ...attrs import LIKE_NUM


_num_words = list(set(
    """
ноль ноля нолю нолём ноле нулевой нулевого нулевому нулевым нулевом нулевая нулевую нулевое нулевые нулевых нулевыми 

один первого первому единица одного одному первой первом первый первым одним одном во-первых 

два второго второму второй втором вторым двойка двумя двум двух во-вторых двое две двоих оба обе обеим обеими 
обеих обоим обоими обоих 

полтора полторы полутора 

три третьего третьему третьем третьим третий тройка трешка трёшка трояк трёха треха тремя трем трех трое троих трёх 

четыре четвертого четвертому четвертом четвертый четвертым четверка четырьмя четырем четырех четверо четырёх четверым 
четверых 

пять пятерочка пятерка пятого пятому пятом пятый пятым пятью пяти пятеро пятерых пятерыми 

шесть шестерка шестого шестому шестой шестом шестым шестью шести шестеро шестерых 

семь семерка седьмого седьмому седьмой седьмом седьмым семью семи семеро

восемь восьмерка восьмого восьмому восемью восьмой восьмом восьмым восеми восьмером восьми восьмью 

девять девятого девятому девятка девятом девятый девятым девятью девяти девятером вдевятером девятерых 

десять десятого десятому десятка десятом десятый десятым десятью десяти десятером вдесятером 

одиннадцать одиннадцатого одиннадцатому одиннадцатом одиннадцатый одиннадцатым одиннадцатью одиннадцати 

двенадцать двенадцатого двенадцатому двенадцатом двенадцатый двенадцатым двенадцатью двенадцати 

тринадцать тринадцатого тринадцатому тринадцатом тринадцатый тринадцатым тринадцатью тринадцати 

четырнадцать четырнадцатого четырнадцатому четырнадцатом четырнадцатый четырнадцатым четырнадцатью четырнадцати 

пятнадцать пятнадцатого пятнадцатому пятнадцатом пятнадцатый пятнадцатым пятнадцатью пятнадцати 

шестнадцать шестнадцатого шестнадцатому шестнадцатом шестнадцатый шестнадцатым шестнадцатью шестнадцати 

семнадцать семнадцатого семнадцатому семнадцатом семнадцатый семнадцатым семнадцатью семнадцати 

восемнадцать восемнадцатого восемнадцатому восемнадцатом восемнадцатый восемнадцатым восемнадцатью восемнадцати 

девятнадцать девятнадцатого девятнадцатому девятнадцатом девятнадцатый девятнадцатым девятнадцатью девятнадцати 

двадцать двадцатого двадцатому двадцатом двадцатый двадцатым двадцатью двадцати 

тридцать тридцатого тридцатому тридцатом тридцатый тридцатым тридцатью тридцати 

тридевять

сорок сорокового сороковому сороковом сороковым сороковой 

пятьдесят пятьдесятого пятьдесятому пятьюдесятью пятьдесятом пятьдесятый пятьдесятым пятидесяти полтинник 

шестьдесят шестьдесятого шестьдесятому шестьюдесятью шестьдесятом шестьдесятый шестьдесятым шестидесятые шестидесяти 

семьдесят семьдесятого семьдесятому семьюдесятью семьдесятом семьдесятый семьдесятым семидесяти 

восемьдесят восемьдесятого восемьдесятому восемьюдесятью восемьдесятом восемьдесятый восемьдесятым восемидесяти 
восьмидесяти 

девяносто девяностого девяностому девяностом девяностый девяностым девяноста 

сто сотого сотому сотка сотня сотом сотен сотый сотым ста 

двести двумястами двухсотого двухсотому двухсотом двухсотый двухсотым двумстам двухстах двухсот 

триста тремястами трехсотого трехсотому трехсотом трехсотый трехсотым тремстам трехстах трехсот 

четыреста четырехсотого четырехсотому четырьмястами четырехсотом четырехсотый четырехсотым четыремстам четырехстах 
четырехсот 

пятьсот пятисотого пятисотому пятьюстами пятисотом пятисотый пятисотым пятистам пятистах пятисот 

шестьсот шестисотого шестисотому шестьюстами шестисотом шестисотый шестисотым шестистам шестистах шестисот 

семьсот семисотого семисотому семьюстами семисотом семисотый семисотым семистам семистах семисот 

восемьсот восемисотого восемисотому восемисотом восемисотый восемисотым восьмистами восьмистам восьмистах восьмисот 

девятьсот девятисотого девятисотому девятьюстами девятисотом девятисотый девятисотым девятистам девятистах девятисот 

тысяча тысячного тысячному тысячном тысячный тысячным тысячам тысячах тысячей тысяч тысячи тыс 

миллион миллионного миллионов миллионному миллионном миллионный миллионным миллионом миллиона миллионе миллиону 
миллионов лям млн 

миллиард миллиардного миллиардному миллиардном миллиардный миллиардным миллиардом миллиарда миллиарде миллиарду 
миллиардов лярд млрд 

триллион триллионного триллионному триллионном триллионный триллионным триллионом триллиона триллионе триллиону 
триллионов трлн 

квадриллион квадриллионного квадриллионному квадриллионный квадриллионным квадриллионом квадриллиона квадриллионе 
квадриллиону квадриллионов квадрлн

квинтиллион квинтиллионного квинтиллионному квинтиллионный квинтиллионным квинтиллионом квинтиллиона квинтиллионе 
квинтиллиону квинтиллионов квинтлн

i ii iii iv vi vii viii ix xi xii xiii xiv xv xvi xvii xviii xix xx xxi xxii xxiii xxiv xxv xxvi xxvii xxvii xxix
""".split()
))


def like_num(text):
    if text.startswith(("+", "-", "±", "~")):
        text = text[1:]
    text = text.replace(",", "").replace(".", "")
    if text.isdigit():
        return True
    if text.count("/") == 1:
        num, denom = text.split("/")
        if num.isdigit() and denom.isdigit():
            return True
    if text.lower() in _num_words:
        return True
    return False


LEX_ATTRS = {LIKE_NUM: like_num}
