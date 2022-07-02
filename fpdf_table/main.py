import os
import math
from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos
from fpdf.line_break import MultiLineBreak, TextLine


class PDFTable(FPDF):
    # altura default de una celda
    default_cell_height = 8
    # tamaño de letra
    size_text = 10  # 13px
    size_title = 10  # 13px

    # override multi_cell para cambiar los valores por defectos
    # w = 0, h = 8, border = 1
    def multi_cell(
            self,
            w=0,
            h=-1,
            txt="",
            border=1,
            align=Align.J,
            fill=False,
            split_only=False,
            link="",
            ln="DEPRECATED",
            max_line_height=None,
            markdown=False,
            print_sh=False,
            new_x=XPos.RIGHT,
            new_y=YPos.TOP,
            line_break=False
    ):
        # si se llama con valor, el valor default es el atributo de clase default_cell_height
        h = self.default_cell_height if h == -1 else h
        # llamar a metodo del padre con nuevos argumentos
        super().multi_cell(w, h, txt, border, align, fill, split_only, link, ln, max_line_height, markdown,
                           print_sh, new_x, new_y)
        if line_break:
            self.ln()

    # override cell para cambiar los valores por defectos
    # w = 0, h = 8, border = 1
    def cell(
            self,
            w=0,
            h=-1,
            txt="",
            border=1,
            ln="DEPRECATED",
            align=Align.L,
            fill=False,
            link="",
            center="DEPRECATED",
            markdown=False,
            new_x=XPos.RIGHT,
            new_y=YPos.TOP,
            line_break=False
    ):
        # si se llama con valor, el valor default es el atributo de clase default_cell_height
        h = self.default_cell_height if h == -1 else h
        # llamar a metodo del padre con nuevos argumentos
        super().cell(w, h, txt, border, ln, align, fill, link, center, markdown, new_x, new_y)
        if line_break:
            self.ln()

    def set_table_header(self, text):
        """
        dibujar header para una tabla
        """
        self.set_font('Helvetica', 'B', self.size_text)
        self.cell(txt=text, align=Align.C, fill=True)
        self.set_font('Helvetica', '', self.size_text)
        self.ln()

    def logo(self):
        """
        dibujar logo
        """
        image_width = 60
        # para centrar la imagen, calcular donde es el centro para la imagen + el margen izquierdo
        pos_x = ((self.epw / 2) - (image_width / 2)) + self.l_margin
        self.image('static/assets/images/logo_pdf.png', x=pos_x, y=10, w=image_width, h=20)
        self.ln(26)

    def firma(self):
        """
        campo para firmar
        """
        self.ln()
        # self.ln()
        # self.ln()
        self.cell(w=self.width_3(), txt='Firma del Solicitante o Apoderado', border=0, align=Align.C)
        self.cell(w=self.width_3(), txt='Firma del Patrocinante', border=0, align=Align.C)
        self.cell(w=self.width_3(), txt='Firma del Funcionario Autorizado', border=0, align=Align.C)
        # final de tabla
        self.ln()
        self.ln()

    def barcode(self, id: int, tipo_solicitud: str):
        """
        codigo de barras
        """
        # cambiar fuente
        self.set_fill_color(10, 10, 10)
        self.set_font('times', '', 15)
        # codigo de barras
        codigo = ''
        if tipo_solicitud == 'OP':
            codigo = f'*{id}ROP*'
        elif tipo_solicitud == 'REN':
            codigo = f'*{id}REN*'
        # si no entra en la pagina actual, agregar otra pagina
        if self.get_y() > 265:
            self.add_page()
        self.code39(codigo, x=self.calculate_code39_center_x(codigo), y=self.get_y(), h=9)
        # texto
        self.ln()
        self.ln()
        self.text(self.calculate_center_text(codigo), self.get_y(), codigo)
        # devolver fuente
        self.default_font()
        # final de tabla
        self.ln()
        self.ln()

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        # Printing page number:
        self.cell(0, 10, f"Pagina {self.page_no()} de {{nb}}", align=Align.C, border=0)

    def default_font(self):
        # devolver fuente a su forma normal
        self.set_font('Helvetica', '', 10)
        self.set_text_color(10, 10, 10)
        self.set_draw_color(220, 220, 220)
        self.set_fill_color(220, 220, 220)

    def width_2(self) -> float:
        """
        calcula longitud para que 2 cajas tengan la misma longitud
        """
        return self.epw / 2

    def width_3(self) -> float:
        """
        calcula longitud para que 3 cajas tengan la misma longitud
        """
        return self.epw / 3

    def row_2_columns(self, txt1: str, txt2: str):
        """
        template para crear una fila de dos columnas.

        :param txt1:
        :param txt2:
        :return:
        """
        self.cell(w=self.width_2(), txt=txt1)
        self.cell(w=self.width_2(), txt=txt2)
        self.ln()

    def row_3_columns(self, txt1: str, txt2: str, txt3: str):
        """
        template para crear una fila de tres columnas.

        :param txt1:
        :param txt2:
        :param txt3:
        :return:
        """
        self.cell(w=self.width_3(), txt=txt1)
        self.cell(w=self.width_3(), txt=txt2)
        self.cell(w=self.width_3(), txt=txt3)
        self.ln()

    def calculate_center_text(self, text: str) -> int:
        """
        calcular centro para el texto + el margen izquierdo.

        :param text: texto
        :return: posicion x
        """
        return (self.l_margin + (self.epw / 2)) - (self.get_string_width(text) / 2)

    @staticmethod
    def calculate_center_object(start: float, container_width: float, element_width: float) -> float:
        """
        calcular posicion para centrar un objeto.

        :param start: posicion de inicio inicial.
        :param container_width: longitud del container del objeto.
        :param element_width: longitud del elemento.
        :return: posicion de inicio para que el elemento quede centrado
        """
        offset = (container_width - element_width) / 2
        return start + offset

    @staticmethod
    def mm_to_px(mm: float) -> int:
        """
        convertir mm to px.

        :param mm: unidad en milimetros.
        :return: unidad en pixeles.
        """
        return round(3.7795275591 * mm)

    # centrar codigo de barras, la longitud del codigo es de 43 caracteres
    @staticmethod
    def calculate_code39_width(quantity: int) -> float:
        """
        calcula la longitud del codigo de barras en mm.

        :param quantity: cantidad de caracteres.
        :return: mm
        """
        bar_width = 0.5  # mm
        # total width narrow bar + wide bar
        character_width = (6 * 0.5 + 3 * 1.5)  # 7.5 mm
        # total character + inter-character gap
        return character_width * quantity + (quantity - 1) * bar_width

    def calculate_code39_center_x(self, text: str) -> float:
        """calcula la posicion donde se debe dibujar el codigo de barras para que este centrado.

        :param text: texto del codigo de barras.
        :return: posicion de x
        """
        return (self.l_margin + (self.epw / 2)) - (self.calculate_code39_width(len(text)) / 2)

    @staticmethod
    def object_or_dash(obj):
        """
        si un objeto no tiene contenido devuelve un string -
        :param obj: objeto
        :return: objeto o string
        """
        if obj:
            return obj
        else:
            return '-'

    @staticmethod
    def object_or_empty(obj):
        """
        si un objeto no tiene contenido devuelve un string -
        :param obj: objeto
        :return: objeto o string
        """
        if obj:
            return obj
        else:
            return ''

    @staticmethod
    def identificacion(ruc: str, cedula: str):
        """
        ver cual se usa entre cedula o ruc
        :param cedula: cedula
        :param ruc: ruc
        :return: string
        """
        if ruc:
            return ruc
        elif cedula:
            return cedula
        else:
            return ''

    def calculate_text_fragments(self, w=0, txt="", column_count=1, justify=True, markdown=False) -> list[TextLine]:
        """
        dado un texto y su longitud, dividir el texto en arrays cada que debe haber un salto de linea.

        :param w: longitud del container
        :param txt: texto
        :param column_count: cantidad de columnas
        :param justify: justificar texto
        :param markdown:
        :return:
        """
        # If width is 0, set width to available width between margins
        # Si la longitud 0 , setear width al disponible restando margenes
        if w == 0:
            w = self.w - self.r_margin - self.x
        # longitud maxima disponible, self.c_margin es el margen en x
        maximum_allowed_emwidth = (w - 2 * self.c_margin) * 1000 / self.font_size
        # Calculate text length
        txt = self.normalize_text(txt)
        normalized_string = txt.replace("\r", "")
        styled_text_fragments = self._preload_font_styles(normalized_string, markdown)
        # text in lines
        text_lines = []
        multi_line_break = MultiLineBreak(
            styled_text_fragments,
            self.get_normalized_string_width_with_style,
            justify=justify,
        )
        text_line = multi_line_break.get_line_of_given_width(maximum_allowed_emwidth)
        # cortar el while al llegar a la cantidad de columnas requeridas, por lo tanto si column size es 5
        # se retornan 5 fragmentos
        column_count = 0
        while text_line is not None and column_count < column_count:
            text_lines.append(text_line)
            text_line = multi_line_break.get_line_of_given_width(
                maximum_allowed_emwidth
            )
            column_count += 1
        return text_lines

    def multi_cell_fixed_height(self, w: float, txt: str, column_height: float, container_height: float) \
            -> tuple[str, str]:
        # cantidad de columnas disponibles, redondeo hacia abajo de la division y del width
        column_count = math.floor(container_height / column_height)
        print('column_count: ', column_height)
        w = math.floor(w)
        # fragments es una lista de array de caracteres [['a','b'],['c']]
        # cada array de caracteres representa una fila y la cantidad
        # de elementos son la cantidad de columnas
        fragments = self.calculate_text_fragments(w, txt, column_count)
        # aqui se va a guardar el texto reconstruido
        join_text = ""
        for text in fragments:
            # por cada fila juntar los caracteres para tener una lista de strings [['ab'],['c']
            join_text += ''.join(text.fragments[0].characters)
            # para juntar dos filas se pone un espacio o salto de linea
            if text.trailing_nl:
                join_text += os.linesep
            else:
                join_text += ' '
        # quitar el ultimo espacio agregado, el resultado es ['ab c']
        join_text = join_text[:-1]
        # dividir texto por separador, sea txt = ['ab c de'] y join_text = ['ab c']
        # el resultado de split es ['', 'de'], esto porque el split remueve la clave separadora y separa el texto
        # antes de la clave y despues de la clave, en este caso como antes de la clave no hay nada entonces en
        # la primera parte no hay nada y en la segunda parte se encuentra el resto del texto
        split_text = txt.split(join_text, maxsplit=1)
        # agregar la clave separadora a la primera parte de la lista,
        # resultado ['ab c',' de']
        split_text[0] = join_text
        return split_text[0], split_text[1]
