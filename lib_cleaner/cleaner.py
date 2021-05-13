def sub_html_symb(sentences): # Функция для очистки html спец. символов
    new_sentences = []
    for s in sentences:
        s = html.unescape(s.replace("&nbsp;", " ")).replace("\n", " ").replace("\r", "").replace("\xa0", " ").replace("\u202f", " ")
        new_sentences.append(s)

    return new_sentences

def interfaxdecode(sentences): # Кодировка интерафкса
    new_sentences = []
    if "È" in " ".join(sentences):
        for s in sentences:
            s = s.encode("windows-1252").decode("windows-1251")
            new_sentences.append(s)
    else:
        return sentences
    return new_sentences


def teleformat(sentences): # Форматирование в телеге
    sentences[0] = "<b>" + sentences[0] + "</b>\n"
    return sentences

def metalinkscleaner(sentences): # Очистка всякого говнища
    if "Allhockey" in " ".join(sentences):
        return ["", ""]
    if ":: РБК" in sentences[0]:
        print(">>>>>>>>", sentences[0])
        sentences[0] = sentences[0].replace(sentences[0][sentences[0].find("::")-1:sentences[0].find(".", sentences[0].find("::"), len(sentences[0]))+1], "")
        print(">>>>>>>>", sentences[0])
    elif ": Lenta.ru" in sentences[0]:
        sentences[0] = sentences[0].replace(sentences[0][sentences[0].find(":"):sentences[0].find(".", sentences[0].find(":"), len(sentences[0])) + 3], "")
    elif "Читайте подробнее" in sentences[0]:
        sentences[0] = sentences[0].replace(sentences[0][sentences[0].find(" -"):sentences[0].find(".", sentences[0].find(" -"), len(sentences[0]))], "")
    elif " - МК" in sentences[0]:
        sentences[0] = sentences[0].replace(" - МК", "")
    elif " - 7Дней.ру" in sentences[0]:
        sentences[0] = sentences[0].replace(" - 7Дней.ру", "")
    
    elif "|" in sentences[0]:
        tempsplit = sentences[0].split()
        print(">>>>", tempsplit)
        for i in range(len(tempsplit)-1):
            if tempsplit[i] == "|":
                del(tempsplit[i+1])
                del(tempsplit[i])
                break
        sentences[0] = " ".join(tempsplit) + "."
    elif "РИА Новости," in " ".join(sentences):
        for i in range(len(sentences)):
            if "РИА Новости," in sentences[i]:
                    sentences[i] = sentences[i].replace(sentences[i][sentences[i].find("РИА Новости,"):len(sentences[i])+1], "")
            if "Новости в России и мире," in sentences[i]:
                    sentences[i] = sentences[i].replace(sentences[i][sentences[i].find("Новости в России и мире,"):len(sentences[i])+1], "")
    elif "znak Новости," in sentences[-1]:
        sentences[-1] = sentences[-1].replace(sentences[-1][sentences[-1].find("znak Новости,"):len(sentences[-1])], "")
    elif "/ Znak.com" in " ".join(sentences):
        for i in range(len(sentences)):
            if "/ Znak.com" in sentences[i]:
                tempsent = sentences[i][::-1]
                print(tempsent)
                tempsent = tempsent.replace(tempsent[tempsent.find("moc.kanZ"):tempsent.find(".", tempsent.find("moc.kanZ")+6, len(tempsent))], "")
                sentences[i] = tempsent[::-1][1:]
    elif "/ТАСС/" in " ".join(sentences):
        for i in range(len(sentences)):
            if "/ТАСС/" in sentences[i]:
                sentences[i] = sentences[i].replace("/ТАСС/.", "").replace("/ТАСС/", "")
        if len(sentences[0]) <= 2:
            del(sentences[0])
    elif "©" in sentences[-1] or "Все права защищены" in sentences[-1] or "(c)" in sentences[-1] or "Copyright" in sentences[-1] or "Зарегистрировано Федеральной службой" in sentences[-1] :
        del(sentences[-1])
    elif "Интерфакс: " in sentences[0]:
        sentences[0] = sentences[0].replace("Интерфакс: ", "")
    return sentences

def bayancleaner(sentences): # [...]
    if "[…]" in sentences[-1]:
        return sentences[:-1]
    else:
        return sentences

def links(sentences): # Ссылки в тексте
    tempjoin = " ".join(sentences)
    if "http" in tempjoin:
        for i in range(len(sentences)):
            if "http" in sentences[i]:
                sentences[i] = sentences[i].replace(sentences[i][sentences[i].find("http") : sentences[i].find(" ", sentences[i].find("http"), len(sentences[i])) + 1], "")

    return sentences

def russianlang(text): # Проверка, что новость содержит больше половины русских символов, а не странных кодировок, чтобы не проходило говно
    alph = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    punc = set('''!()-[]{};?@#$%:'"\,./^&;*_ ''')
    numb = set("0123456789")
    rus = 0
    t = 0
    for k in text.lower():
        if k not in punc and k not in numb:
            if k in alph:
                rus += 1
                t += 1
            else:
                t += 1
    if rus / t < 0.5:
        return None
    else:
        return text
    
def checkspaces(sentences):
    for i in range(len(sentences)):
        if len(sentences[i]) >= 1:
            if sentences[i][-2] == " ":
                sentences[i] = sentences[i][:-2] + sentences[i][-1]
        else:
            pass
    return sentences
    
def fresh_text(text):
    try:       
        #1 - make array of sentences
        sentences = make_sentences(text)
        

        #2 - in each sentence clean not words from start and end
        sentences = clean_tech(sentences)

        #3 - check that each next setnence it is not duplicate to previous ones
        sentences = clean_duplicates(sentences)

        #4 - add dots to end of sentences
        sentences = add_dots(sentences)
        
        #5 - subs html special symbols like &mdash and others
        sentences = sub_html_symb(sentences)

        #6 - decoding intefax
        sentences = interfaxdecode(sentences)
        
        #7 - cleaning some sh*t
        sentences = metalinkscleaner(sentences)
        
        #8 - "[...]"
        sentences = bayancleaner(sentences)
        
        #9 - cleaning intext links
        sentences = links(sentences)
        
        #10 - cheking spaces bedore dots
        sentences = checkspaces(sentences)
        
        #11 - formatting telegram message
        sentences = teleformat(sentences)
    
        #12 - generate fresh_text
        temptext = "".join(sentences[0:2])
        fresh_text = temptext + " " + ' '.join(sentences[2:])
        
        #13 - final check for bad symbols and other languages
        fresh_text = russianlang(fresh_text)
