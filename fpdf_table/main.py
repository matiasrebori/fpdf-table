import functools
import math

from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos
from fpdf.line_break import MultiLineBreak, TextLine
from PIL import Image
import base64
import io


# clase padre
class PDFTable(FPDF):
    # text and header text sizes
    size_text = 7.5  # 7.5 pt ~ 10px
    size_title = 9  # 9 pt ~ 12px
    # default height if every row
    default_cell_height = 5
    # height of every row in multi cell
    multi_cell_row_height: float = 5  # mm
    # text size used for text inside multi cell
    multi_cell_text_size: float = 7.5  # mm
    # font
    font: str = 'Helvetica'

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
        if line_break:
            new_x = XPos.LMARGIN
            new_y = YPos.NEXT
        # llamar a metodo del padre con nuevos argumentos
        super().multi_cell(w, h, txt, border, align, fill, split_only, link, ln, max_line_height, markdown,
                           print_sh, new_x, new_y)
        # if line_break:
        #     self.ln()

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

    def default_font(self):
        """
        return font to default values.

        :return:
        """
        # devolver fuente a su forma normal
        self.set_font(self.font, '', self.size_text)
        self.set_text_color(10, 10, 10)
        self.set_draw_color(220, 220, 220)
        self.set_fill_color(220, 220, 220)

    def width_2(self) -> float:
        """
        get width for 2 columns of same width.

        :return: width of one column
        """
        return self.epw / 2

    def width_3(self) -> float:
        """
        get width for 2 columns of same width.

        :return: width of one column
        """
        return self.epw / 3

    def width_n(self, n: int) -> float:
        """
        get width for n columns of same width.

        :return: width of one column
        """
        return self.epw / n

    def row_2_columns(self, txt1: str, txt2: str):
        """
        draw a row with two straightforward columns.

        :param txt1: text 1
        :param txt2: text 2
        :return:
        """
        self.cell(w=self.width_2(), txt=txt1)
        self.cell(w=self.width_2(), txt=txt2)
        self.ln()

    def row_3_columns(self, txt1: str, txt2: str, txt3: str):
        """
        draw a row with three straightforward columns.

        :param txt1: text 1
        :param txt2: text 2
        :param txt3: text 3
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
    def calculate_center_object(start: float, container_length: float, element_length: float) -> float:
        """
        calcular posicion para centrar un objeto.

        :param start: posicion de inicio inicial.
        :param container_length: longitud del container del objeto.
        :param element_length: longitud del elemento.
        :return: posicion de inicio para que el elemento quede centrado
        """
        # if container_length equals element_length it's already in the center, and prevents division by zero
        offset = 0 if container_length == element_length else (container_length - element_length) / 2
        return start + offset

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
    def mm_to_px(mm: float) -> int:
        """
        convertir mm to px.

        :param mm: unidad en milimetros.
        :return: unidad en pixeles.
        """
        return round(3.7795275591 * mm)

    @staticmethod
    def px_to_mm(px: int) -> float:
        """
        convertir px to mm.

        :param px: unidad en pixeles.
        :return: unidad en milimetros.
        """
        return round(px * 0.2645833333, 3)

    @staticmethod
    def px_to_pt(px: int) -> float:
        """
        convertir px to pt.

        :param px: unidad en pixeles.
        :return: unidad en points.
        """
        return round(px * 0.75, 3)

    @staticmethod
    def object_or_dash(obj):
        """
        si un objeto no tiene contenido devuelve un dash -.

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
        si un objeto no tiene contenido devuelve un string vacio.

        :param obj: objeto
        :return: objeto o string
        """
        if obj:
            return obj
        else:
            return ''

    @staticmethod
    def object_or_text(obj, text: str):
        """
        si un objeto no tiene contenido devuelve un texto.

        :param obj: objeto
        :param text: texto
        :return: objeto o string
        """
        # if obj is string
        if isinstance(obj, str):
            # if string is only whitespaces
            if obj.isspace():
                # set string as empty (None)
                obj = ''

        if obj:
            return obj
        else:
            return text

    def calculate_text_fragments(self, w=0, txt="", row_quantity=1, justify=True, markdown=False) \
            -> tuple[list[TextLine], bool]:
        """
        dado un texto y su longitud, dividir el texto en arrays cada que debe haber un salto de linea.
        devuelve también si el texto se dividió

        :param w: longitud del container.
        :param txt: texto.
        :param row_quantity: cantidad de filas.
        :param justify: justificar texto.
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
        row_count = 0
        while text_line is not None and row_count < row_quantity:
            text_lines.append(text_line)
            text_line = multi_line_break.get_line_of_given_width(
                maximum_allowed_emwidth
            )
            row_count += 1
        # if text is larger than container and has to divide, if text_line has more content
        # it means that the text is larger
        text_is_larger = True if text_line is not None else False
        return text_lines, text_is_larger

    def calculate_text_rows(self, w: float = 0, txt="", justify=True, markdown=False):
        """
        calculate how many rows will take the given text in the given width.

        :param w: longitud del container.
        :param txt: texto
        :param justify: justify
        :param markdown: markdown
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
        # calcular cantidad de filas
        row_count = 0
        while text_line is not None:
            text_lines.append(text_line)
            text_line = multi_line_break.get_line_of_given_width(
                maximum_allowed_emwidth
            )
            row_count += 1
        return row_count

    def fit_text_fixed_height(self, txt: str, row_height: float, container_width: float, container_height: float,
                              linesep: str = '\n', ellipsis: bool = False) -> tuple[str, str]:
        """
        divide the text in two string, the first string contains the piece of text that fits in the container,
        the second string contains the remaining text that doesn't it.

        :param container_width: width of the container
        :param txt: text
        :param row_height: height of every row
        :param container_height: total height of the container
        :param linesep: os new line representation
        :return: list with two strings
        :param ellipsis: truncate text and add ellipsis
        """
        # cantidad de filas disponibles, redondeo hacia abajo de la division y del width
        row_count: int = math.floor(container_height / row_height)
        container_width: int = math.floor(container_width)
        # if text is empty, return two empty strings
        if not txt:
            return '', ''
        # en fragments se encuentra la porcion de texto que entra en el container, pero el texto esta deconstruido
        # fragments es una lista de array de caracteres [['a','b'],['c']]
        # cada array de caracteres representa una fila y la cantidad de arrays son la cantidad de filas
        # ver objeto TextLine y Fragment
        fragments, text_is_larger = self.calculate_text_fragments(container_width, txt, row_count)
        # si la cantidad de fragmentos (filas) es menor o igual a la cantidad de filas disponibles,
        # entonces no se necesita calcular nada, ya que el texto entero entra en el container
        if not text_is_larger:
            return txt, ''
        # reconstruir los fragmentos en el texto que entra en el container
        join_text = ''
        for text in fragments:
            #  if the fragment object is empty means the row is a new line, doesn't have text
            if text.fragments:
                # por cada fila juntar los caracteres para tener una lista de strings [['ab'],['c']
                join_text += ''.join(text.fragments[0].characters)
            # para juntar dos filas se pone un espacio o salto de linea
            if text.trailing_nl:
                # join_text += os.linesep
                join_text += linesep
            else:
                join_text += ' '
        # quitar el ultimo espacio agregado, el resultado es ['ab c']
        # remove trailing new line
        join_text = join_text.rstrip()
        # dividir el texto por un separador que es join_text, sea txt = ['ab c de'] y join_text = ['ab c']
        # el resultado de split es ['', 'de'], esto porque el split remueve la clave separadora y separa el texto
        # antes de la clave y despues de la clave, en este caso como antes de la clave no hay nada entonces en
        # la primera parte no hay nada y en la segunda parte se encuentra el resto del texto
        split_text = txt.split(join_text, maxsplit=1)
        try:
            # agregar la clave separadora a la primera parte de la lista,
            split_text[0] = join_text
            # remove whitespace, new line or tab present at start of the string
            split_text[1] = split_text[1].lstrip()
            # calculate ellipsis
            if ellipsis and text_is_larger:
                # split the whole first string by whitespaces, then remove last part ( last word),
                # finally join again the parts with whitespaces and concatenate ellipsis
                split = split_text[0].split(' ')
                last_word = split[-1]
                # if last word have less than 3 characters
                if len(last_word) >= 3:
                    split_text[0] = ' '.join(split[:-1]) + ' ' + '...'
                else:
                    # add backlash instead of dots
                    backslash_quantity = '\\' * len(last_word)
                    split_text[0] = ' '.join(split[:-1]) + ' ' + backslash_quantity
                # add removed word to the second string
                split_text[1] = last_word + ' ' + split_text[1]
            # resultado ['ab c',' de']
            return split_text[0], split_text[1]
        except IndexError:
            # if error is find here means that probably split_text doesn't have 2 elements.
            # i.e. split_text[1] doesn't exist
            # probably is caused by os specific new line, i.e. windows = \r\n, unix = \n
            # throw custom error
            raise SplitTextError

    def cell_fixed(self, container_width: float, container_height: float, txt: str = '',
                   line_break: bool = False, inline: bool = False):
        """
        draw a fixed size table border.

        :param container_width: container_width
        :param container_height: container_height
        :param txt: text
        :param line_break: perform a new line
        :param inline: next Y with be in the same line
        :return:
        """

        # self.ln() defaults to last cell height, so a new self.ln() here, will draw a new line
        # with height equals to container height, to fix it, instead of draw a new line with self.ln()
        # use a cell with height equal to default cell height, and the next Ypos will be under de
        # border of the cell that draws the border
        if inline:
            # draw border, if inline next position is right top
            self.cell(w=container_width, h=container_height, txt=txt, new_x=XPos.LEFT, new_y=YPos.TOP)
            # self.ln()
            self.cell(w=container_width, h=self.default_cell_height, border=0, new_x=XPos.RIGHT, new_y=YPos.TOP)
        else:
            # if not inline next position is left margin under the border
            self.cell(w=container_width, h=container_height, txt=txt, new_x=XPos.LEFT, new_y=YPos.NEXT)
            # self.ln()
            self.cell(w=container_width, h=self.default_cell_height, border=0, new_x=XPos.LMARGIN, new_y=YPos.TOP)

        if line_break:
            self.ln()

    def multi_cell_fixed(self, w: float, txt: str, row_height: float, container_height: float,
                         align: str | Align = Align.J,
                         line_break: bool = False, ellipsis: bool = False, inline: bool = False):
        """
        draw a fixed size cell, if the text is larger than the cell ( container ), it will draw the text until it fits
        and will return the text that doesn't fit for later use.

        :param w: container width
        :param txt: text
        :param row_height: height of every row
        :param container_height: total height of the container
        :param align: alignment
        :param line_break: add a trailing new line
        :param ellipsis: truncate text and add ellipsis
        :param inline: next Y with be in the same line
        :return:
        """
        # calculate text truncation ( division)
        try:
            text_that_fits, text_overflow = self.fit_text_fixed_height(txt, row_height, w, container_height,
                                                                       ellipsis=ellipsis)
        except SplitTextError:
            # if there's a custom error call again with different line separator
            text_that_fits, text_overflow = self.fit_text_fixed_height(txt, row_height, w, container_height, '\r\n',
                                                                       ellipsis)
        # draw text without border
        self.multi_cell(w=w, h=row_height, txt=text_that_fits, border=0, new_x=XPos.LEFT, new_y=YPos.TOP, align=align)
        # draw border and fix self.ln()
        self.cell_fixed(w, container_height, line_break=line_break, inline=inline)
        return text_overflow

    def check_available_width(self, total_width: float):
        """
        check if some calculated width fits in the available page width.

        :param total_width: calculated width.
        :return:
        :raise WidthOverflowError: calculated width doesn't fit in available page space
        """
        # available_width = total page width - right margin - actual x position
        available_width = self.w - self.r_margin - self.get_x()
        # if total width is larger than page width
        if total_width > available_width:
            raise WidthOverflowError
        return

    def make_width_list(self, width_list: list[float], columns_count: int) -> list[float]:
        """
        if width_list is not empty check the total width ,if width_list is empty make list of equals width´s.

        :param width_list: list of width for every column
        :param columns_count: columns count
        :return:
        :raise NumberColumnsTextDoesntMatchError: columns count doesn't match text count
        """
        # if the list is not empty, check width´s
        if width_list:
            # if elements count in width_list and text_list doesn't match
            if len(width_list) != columns_count:
                raise NumberElementsListMismatchError
            # calculate total width
            total_width = functools.reduce(lambda a, b: a + b, width_list)
            # check width
            self.check_available_width(total_width)
        else:
            # if the list is empty, make list of equals width´s. i.e. [10,10,10]
            width_list = [self.width_n(columns_count)] * columns_count
        return width_list

    def make_align_list(self, align: Align | list[Align], columns_count: int, default_value: Align = Align.J) \
            -> list[Align]:
        """
        make list of alignments.

        :param align: list of alignment or one alignment value
        :param columns_count: columns count
        :return:
        """
        # if align is only one value
        if isinstance(align, Align):
            align_list = [align] * columns_count
            return align_list
        # if align is a list
        elif isinstance(align, list):
            # if is a list of align values
            if align:
                # if elements count doesn't match
                if len(align) != columns_count:
                    raise NumberElementsListMismatchError
                align_list = align
            else:
                # if is an empty list
                align_list = [default_value] * columns_count
            return align_list

    def row_line(self, text_list: list[str], width_list: list[float], align: Align | list[Align],
                 line_break: bool = False):
        """
        draw n columns in the same row, columns height are 1 column.

        :param text_list: list of the texts to write
        :param width_list: list of width for every column
        :param line_break: perform a line break
        :param align: alignment
        :return:
        """
        columns_count: int = len(text_list)
        # check width_list
        width_list = self.make_width_list(width_list, columns_count)
        align_list = self.make_align_list(align, columns_count, Align.L)
        # draw n-1 cells inline
        for i in range(columns_count - 1):
            # draw cell
            self.cell(w=width_list[i], txt=text_list[i], align=align_list[i])
        # perform an extra line break if desired
        self.cell(w=width_list[-1], txt=text_list[-1], align=align_list[-1], line_break=line_break)
        self.ln()

    def row_fixed(self, text_list: list[str], width_list: list[float], align: Align | list[Align],
                  fixed_height: float = None, line_break: bool = False):
        """
        draw n columns in the same row, columns height is fixed.

        :param text_list: list of the texts to write
        :param width_list: list of width for every column
        :param fixed_height: height of every column
        :param line_break: perform a line break
        :param align: alignment
        :return:
        """
        columns_count: int = len(text_list)
        # check width_list
        width_list = self.make_width_list(width_list, columns_count)
        align_list = self.make_align_list(align, columns_count)
        print('align_list: ', align_list)
        # draw n-1 fixed multi_cells inline
        for i in range(columns_count - 1):
            # container height for every cell is fixed
            self.multi_cell_fixed(w=width_list[i], txt=text_list[i], row_height=self.multi_cell_row_height,
                                  container_height=fixed_height, align=align_list[i], inline=True)
        # last cell doesn't have to be inline ir order to leave the cursor under the cells, line break is optional
        self.multi_cell_fixed(w=width_list[-1], txt=text_list[-1], row_height=self.multi_cell_row_height,
                              container_height=fixed_height, align=align_list[-1], line_break=line_break)

    def row_responsive(self, text_list: list[str], width_list: list[float], align: Align | list[Align],
                       line_break: bool = False):
        """
        draw n columns in the same row, every column has height equals to the column with maximum height.

        :param text_list: list of the texts to write
        :param width_list: list of width for every column
        :param line_break: perform a line break
        :param align: alignment
        :return:
        """
        columns_count: int = len(text_list)
        # check width_list
        width_list = self.make_width_list(width_list, columns_count)
        align_list = self.make_align_list(align, columns_count)
        # calculate maximum number of rows, so every cell will have the same amount of rows
        max_rows: int = 0
        for i in range(columns_count):
            # calculate row count for cell i
            justify = True if align_list[i] == Align.J else False
            row_count = self.calculate_text_rows(w=width_list[i], txt=text_list[i], justify=justify)
            # save max
            if row_count > max_rows:
                max_rows = row_count
        # draw n-1 cells inline
        for i in range(columns_count - 1):
            # container height for every cell will be the maximum height, that is,
            # maximum number of rows * height of every row
            self.multi_cell_fixed(w=width_list[i], txt=text_list[i], row_height=self.multi_cell_row_height,
                                  container_height=max_rows * self.multi_cell_row_height, align=align_list[i],
                                  inline=True)
        # last cell doesn't have to be inline ir order to leave the cursor under the cells, line break is optional
        self.multi_cell_fixed(w=width_list[-1], txt=text_list[-1], row_height=self.multi_cell_row_height,
                              container_height=max_rows * self.multi_cell_row_height, align=align_list[-1],
                              line_break=line_break)

    def table_row(self, text_list: list[str], width_list: list[float] | str, align: Align | list[Align],
                  option: str = 'line', fixed_height: float = None):
        """
        draw a row for a table.

        :param text_list: list of the texts to write
        :param width_list: list of width´s for every column
        :param option: define what type of row to draw
        :param fixed_height: height if option is fixed
        :param align: alignment
        :return:
        :raise MissingValueError: a value was expected and wasn't found
        :raise HeightError: height cannot be smaller than default cell height
        :raise MismatchValueError: undefined option
        """
        if len(text_list) == 1 and len(width_list) == 1:
            if option == 'line':
                self.cell()

        # if width_list is string, convert to empty list
        if isinstance(width_list, str):
            width_list = []
        if option == 'line':
            self.row_line(text_list, width_list, align, False)
        elif option == 'fixed':
            if not fixed_height:
                raise MissingValueError
            if fixed_height < self.default_cell_height:
                raise HeightError
            self.row_fixed(text_list, width_list, align, fixed_height, False)
        elif option == 'responsive':
            self.row_responsive(text_list, width_list, align, False)
        else:
            raise MismatchValueError

    def table_header(self, text_list: list[str], width_list: list[float] | str, align: Align | list[Align]):
        """
        draw a table header for a table.

        :param text_list: list of the texts to write
        :param width_list: list of width´s for every column
        :param align: alignment
        :return:
        """
        columns_count: int = len(text_list)
        # if width_list is string, convert to empty list
        if isinstance(width_list, str):
            width_list = []
        width_list = self.make_width_list(width_list, columns_count)
        align_list = self.make_align_list(align, columns_count, Align.C)
        # set font
        self.set_font(self.font, 'B', self.size_title)
        # draw n-1 cells inline
        for i in range(columns_count - 1):
            # draw cell
            self.cell(w=width_list[i], txt=text_list[i], align=align_list[i], fill=True)
        # draw last column with a line break
        self.cell(w=width_list[-1], txt=text_list[-1], align=align_list[-1], fill=True, line_break=True)
        # default font
        self.set_font(self.font, '', self.size_text)

    def image_center(self, img: any, x: float = None, y: float = None, img_width: float = 0, img_height: float = 0,
                     container_width: float = None, container_height: float = None):
        """
        draw an image and center its position in a given container.

        :param img: either a string representing a file path to an image, a URL to an image, an io.BytesIO,
                or an instance of `PIL.Image.Image`.
        :param x: optional horizontal position where to put the image on the page.
                If not specified or equal to None, the current abscissa is used.
        :param y: optional vertical position where to put the image on the page.
                If not specified or equal to None, the current ordinate is used.
                After the call, the current ordinate is moved to the bottom of the image
        :param img_width: optional width of the image. If not specified or equal to zero,
                it is automatically calculated from the image size.
                Pass `pdf.epw` to scale horizontally to the full page width.
        :param img_height: optional height of the image. If not specified or equal to zero,
                it is automatically calculated from the image size.
                Pass `pdf.eph` to scale horizontally to the full page height.
        :param container_width: with of the rectangle that contains the image.
                If not specified or equal to None, the current image width is used.
        :param container_height: height of the rectangle that contains the image
                If not specified or equal to None, the current image height is used.
        :return:
        """
        if x is None:
            x = self.get_x()
        if y is None:
            y = self.get_y()
        if container_width is None:
            container_width = img_width
        if container_height is None:
            container_height = img_height
        if img:
            self.image(img,
                       x=self.calculate_center_object(x, container_length=container_width,
                                                     element_length=img_width),
                       y=self.calculate_center_object(y, container_length=container_height,
                                                     element_length=img_height),
                       w=img_width, h=img_height)


class SplitTextError(Exception):
    """
    Error to raise error when string.split() fails to split
    """
    pass


class HeightError(Exception):
    """
    Error to raise when there is an error on the value of the height
    """
    pass


class WidthOverflowError(Exception):
    """
    Custom error to raise when a calculated width is larger than the maximum width of the page
    """
    pass


class NumberElementsListMismatchError(Exception):
    """
    Custom error to raise when a columns count doesn't match text count
    """
    pass


class MissingValueError(Exception):
    """
    A value was expected and wasn't found
    """
    pass


class MismatchValueError(Exception):
    """
    Value has an unexpected value
    """
    pass


def base64_to_image(image_base64: str):
    """
    convertir string base64 a objeto Imagen.

    :param image_base64: string base64
    :return: Image
    """
    imagen_data = base64.b64decode(image_base64)
    try:
        # convertir y guardar imagen
        return Image.open(io.BytesIO(imagen_data))
    except OSError:
        return False


def resize_image(img: Image, width: int, height: int) -> Image:
    """
     cambiar tamaño manteniendo el ratio.

    :param img: imagen
    :param width: longitud de nueva imagen.
    :param height: altura de nueva imagen.
    :return:
    """
    # si no hay imagen
    if not img:
        return False
    # thumbnail image
    img.thumbnail((width, height))
    return img
