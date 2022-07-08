from fpdf_table import PDFTable
from fpdf.enums import Align


def minimal_example():
    data: list[list[str]] = [
        ['Gerard', 'Martinez', '09/07/1998'],
        ['Amy ', 'Miller', 'July 30, 1969'],
        ['Ferdinand ', 'Varela ', 'November 10, 1988'],
        ['Edén ', 'Mascarenas Benavides', 'May 23, 1990'],
        ['Adrián ', 'Beltrán ', 'December 12, 1977'],
    ]
    # initialize PDFTable
    pdf = PDFTable()
    # before doing anything, fpdf needs to create a page, define a font and set colors
    pdf.init()
    # table header
    pdf.table_header(['First Name', 'Last Name', 'Date of birth'])
    # table rows
    for person in data:
        pdf.table_row(person)
    pdf.output("pdfs/minimal_example.pdf")


minimal_example()


def features_example():
    # initialize PDFTable
    pdf = PDFTable()
    # before doing anything, fpdf needs to create a page, define a font and set colors
    pdf.init()

    """
    table row
    """
    # draw a table header, pass a list with the text, by default width is the same for every column
    # and align is to left
    pdf.table_header(['First Name', 'Last Name', 'Date of birth'])
    # draw a table row, by default is only one row with height equal to pdf.default_cell_height
    pdf.table_row(['Gerard', 'Martinez', '09/07/1998'])

    """
    responsive row
    """
    # header with custom width
    pdf.table_header(['Email', 'Address'], [pdf.width_3(), 2 * pdf.width_3()])
    # responsive row with custom width
    pdf.table_row(['large_email_example-very_large_email_example-more_large_email_example@example.com',
                   '952 Rogers Ave, Okanogan, Washington(WA), 98840'],
                  [pdf.width_3(), 2 * pdf.width_3()], option='responsive')

    """
    fixed height row
    """
    # align center, expects a list of alignments but if you pass only one it spreads for every column
    pdf.table_header(['Description'], align=Align.C)
    large_text = """Lorem Ipsum is simply dummy text of the printing and typesetting industry....."""
    # fixed row needs fixed_height parameter
    pdf.table_row([large_text], option='fixed', fixed_height=6 * pdf.default_cell_height)
    # output
    pdf.output("pdfs/main_features.pdf")


features_example()
