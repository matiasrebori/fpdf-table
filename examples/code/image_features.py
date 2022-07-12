from fpdf_table import PDFTable, add_image_local


def image_example():
    # initialize PDFTable, before doing anything, __init__ adds a page, sets font, size and colors
    pdf = PDFTable()
    # load image from file
    img, img_width, img_height = add_image_local('../pdfs/logo1.png')
    # set custom width and height
    img_width, img_height = pdf.use_px_to_mm(150), pdf.use_px_to_mm(150)
    # draw image, center on page
    pdf.draw_image_center(img=img, img_width=img_width, img_height=img_height, container_width=pdf.get_width_effective())
    # line breaks
    pdf.ln(img_height)
    pdf.ln(10)
    # get cursor position
    x, y = pdf.get_x(), pdf.get_y()
    # draw a fixed table without content
    table_height = pdf.use_px_to_mm(200)
    # change color of table border
    pdf.set_draw_color(10, 10, 10)
    pdf.table_row(['', '', ''], option='fixed', fixed_height=table_height)
    # draw image no align
    pdf.draw_image_center(img=img, x=x, y=y, img_width=img_width, img_height=img_height)
    # draw image center horizontally
    x = x + pdf.calculate_width_3()
    pdf.draw_image_center(img=img, x=x, y=y, img_width=pdf.use_px_to_mm(150), img_height=pdf.use_px_to_mm(150),
                          container_width=pdf.calculate_width_3())
    # draw image center horizontally and vertically
    x = x + pdf.calculate_width_3()
    pdf.draw_image_center(img=img, x=x, y=y, img_width=pdf.use_px_to_mm(150), img_height=pdf.use_px_to_mm(150),
                          container_width=pdf.calculate_width_3(), container_height=table_height)

    # file path where to save the pdf
    pdf.output("../pdfs/image_example.pdf")


image_example()
