import os

import docx
from bs4 import BeautifulSoup
import codecs
import aspose.words as aw
from htmldocx import HtmlToDocx


class DocView:
    def __init__(self, document):
        self.document = document
        self.convert_doc = ''  # название файла для отображения на сайте
        self.interim_code = ''  # код промежуточного шаблона
        self.html = ''  # для поиска чекпоинтов

    def word2html(self):
        """ Сохранение в HTML """
        doc = aw.Document(self.document)

        # Включить двустороннюю информацию
        saveOptions = aw.saving.HtmlSaveOptions()
        saveOptions.export_roundtrip_information = True

        htmldoc_name = self.document[0:-5] + ".html"
        self.convert_doc = htmldoc_name
        doc.save(htmldoc_name, saveOptions)

        f = codecs.open(htmldoc_name, 'r', 'utf-8')
        html = f.read()

        # убираем ватермарки
        html = html.replace(
            '<span style="font-weight:bold; color:#ff0000">Evaluation Only. Created with Aspose.Words. Copyright '
            '2003-2023 Aspose Pty Ltd.</span>', "")

        html = html.replace(
            '<span style="font-weight:bold; color:#ff0000">Created with an evaluation copy of Aspose.Words. To '
            'discover the full versions of our APIs please visit: https://products.aspose.com/words/</span>',
            '')

        html = html.replace('<div><div style="-aw-different-first-page:true; -aw-headerfooter-type:header-primary; '
                            'clear:both"><p style="margin-top:0pt; margin-bottom:0pt"><span style="height:0pt; display:block; '
                            'position:absolute; z-index:-65537"><img src="Document.001.png" width="643" height="350" alt="" '
                            'style="margin-top:243.35pt; -aw-left-pos:0pt; -aw-rel-hpos:margin; -aw-rel-vpos:margin; '
                            '-aw-top-pos:0pt; -aw-wrap-type:none; position:absolute" /></span><span '
                            'style="-aw-import:ignore">&#xa0;</span></p></div>', '')
        self.html = html
        return html

    def get_checkpoints(self):
        """ Получение и установка чекпоинтов """
        soap = BeautifulSoup(self.html, 'lxml')
        tags = soap.find_all('span')
        checkpoints = {}  # словарь чекпоинтов вида чекпоинт_номер: фраза
        num_of_point = 0
        for i in tags:
            try:
                # TODO поменять определение по цвету текста, в редакторе делать фон выделения
                if 'background-color:#00ff00' in i['style']:  # #00ff00 - зеленый фон выделения
                    checkpoints["checkpoint_" + str(num_of_point)] = i.text
                    i.string = "{{checkpoint_" + str(num_of_point) + "}}"  # переписываем чекпоинты в рабочем шаблоне

                    num_of_point += 1
            except KeyError:
                continue

        self.interim_code = soap
        return checkpoints

    def save_interim_template_html(self):
        """ Сохранение рабочего шаблона в HTML """

        interim_template_name = self.document[0:-5]
        interim_template_code = self.interim_code

        # сохраняем рабочий шаблон в html
        with open(interim_template_name + ".html", "w", encoding="utf-8") as file:
            file.write(str(interim_template_code))

    def save_interim_template_docx(self):
        """ Сохранение рабочего шаблона в DOCX """

        # TODO удалить вотермарки

        interim_template_name = self.document[0:-5]
        # interim_template_code = self.interim_code

        interim_template_doc = aw.Document(interim_template_name + ".html")
        interim_template_doc.save(interim_template_name + ".docx")

