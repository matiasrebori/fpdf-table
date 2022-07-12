from fpdf_table import PDFTable


def minimal_example():
    data: list[list[str]] = [
        ['Gerard', 'Martinez', '09/07/1998'],
        ['Amy ', 'Miller', 'July 30, 1969'],
        ['Ferdinand ', 'Varela ', 'November 10, 1988'],
        ['Edén ', 'Mascarenas Benavides', 'May 23, 1990'],
        ['Adrián ', 'Beltrán ', 'December 12, 1977'],
    ]
    # initialize PDFTable, before doing anything, __init__ adds a page, sets font, size and colors
    pdf = PDFTable()
    # table header
    pdf.table_header(['First Name', 'Last Name', 'Date of birth'])
    # table rows
    for person in data:
        pdf.table_row(person)
    # file path where to save the pdf
    pdf.output("../pdfs/minimal_example.pdf")


minimal_example()
