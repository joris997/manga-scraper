import os
import img2pdf
from PyPDF3 import PdfFileWriter, PdfFileReader


def convert_chapter_pdf(title, count, manga_path, folder_path):
    # change cwd to the relevant folder
    os.chdir(os.path.join(manga_path, folder_path))
    # convert all .jpg to a single .pdf
    with open(os.path.join(manga_path, title + "_" + str(count) + ".pdf"), "wb") as f:
        print(sorted(os.listdir(os.getcwd())))
        f.write(img2pdf.convert([i for i in sorted(os.listdir(os.getcwd())) if i.endswith(".jpg")]))


def combine_chapters(title, manga_path):
    os.chdir(manga_path)
    pdf_writer = PdfFileWriter()
    for path in sorted(os.listdir(manga_path)):
        if path.endswith(".pdf"):
            pdf_reader = PdfFileReader(path)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
    with open(title + "_complete.pdf", "wb") as f:
        pdf_writer.write(f)


def main():
    path = input("Specify path: ")
    title = input("Specify title: ")
    os.chdir(path)
    ch_count = 1
    for folder in sorted(os.listdir(os.getcwd())):
        convert_chapter_pdf(title, ch_count, path, folder)
        ch_count += 1
    combine_chapters(title, path)


main()
