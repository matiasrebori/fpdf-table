from fpdf_table import PDFTable, Align


def features_example():
    # initialize PDFTable, before doing anything, __init__ adds a page, sets font, size and colors
    pdf = PDFTable()
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
    pdf.table_header(['Email', 'Address'], [pdf.calculate_width_3(), 2 * pdf.calculate_width_3()])
    # responsive row with custom width
    pdf.table_row(['large_email_example-very_large_email_example-more_large_email_example@example.com',
                   '952 Rogers Ave, Okanogan, Washington(WA), 98840'],
                  pdf.table_cols(4, 8), option='responsive')

    """
    fixed height row
    """
    # align center, expects a list of alignments but if you pass only one it spreads for every column
    pdf.table_header(['Description'], align=Align.C)
    large_text = """Lorem Ipsum is simply dummy text of the printing and typesetting industry....."""
    # fixed row needs fixed_height parameter
    pdf.table_row([large_text], option='fixed', fixed_height=6 * pdf.row_height_cell)
    # output
    pdf.output("../pdfs/main_features.pdf")


features_example()
