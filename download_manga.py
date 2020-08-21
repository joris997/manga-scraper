import requests
import shutil
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
import sys
from PyPDF3 import PdfFileWriter, PdfFileReader
import img2pdf


#def get_url():
#    title = "ajin"
#    url = "https://mangahub.io/manga/ajin_101"
#    return title, url


def list_chapters(url, title):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    chapter_links = []
    for text in soup.find_all("a", href=True):
        if "manga" and "chapter" and title in text["href"]:
            chapter_links.append(text["href"])
    chapter_links = chapter_links[::-1]
    print("I will be downloading " + str(len(chapter_links)) + " chapters!")
    return chapter_links


def download_chapter_jpg(url, new_pth):
    """Download all images from the manga chapter"""
    if not os.path.exists(new_pth):
        os.makedirs(new_pth)
    # start selenium webdriver for accessing manga image files
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    # find all images in the HTML
    images = driver.find_elements_by_tag_name("img")
    count = 1
    for image in images:
        # if image link contains file/imghub it is an image of a manga page
        if "file/imghub" in image.get_attribute("src"):
            # make an image request using the image link
            r = requests.get(image.get_attribute("src"), stream=True)
            if r.status_code == 200:
                with open(new_pth + "{0:04}".format(count) + ".jpg", "wb") as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
            count += 1
    driver.quit()
    print("Chapter done")


def convert_chapter_pdf(title, ch_cnt, new_path):
    # change cwd to the relevant folder
    os.chdir(new_path)
    # convert all .jpg to a single .pdf
    with open(title + "_" + str(ch_cnt) + ".pdf", "wb") as f:
        print(sorted(os.listdir(os.getcwd())))
        f.write(img2pdf.convert([i for i in sorted(os.listdir(os.getcwd())) if i.endswith(".jpg") and title not in i]))


def remove_chapter_jpg(new_path):
    # change cwd to the relevant folder
    os.chdir(new_path)
    # remove all .jpg images in the current directory
    for item in os.listdir(os.getcwd()):
        if item.endswith(".jpg"):
            os.remove(os.path.join(new_path, item))


def combine_chapters(title, new_path):
    os.chdir(new_path)
    pdf_writer = PdfFileWriter()
    for path in new_path:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
    with open(title + "_complete.pdf", "wb") as f:
        pdf_writer.write(f)


#def main():
if __name__ == "__main__":
    # manga_title, manga_url = get_url()
    try:
        manga_title = sys.argv[1]
        manga_url = sys.argv[2]
    except IndexError:
        print("expected 2 input arguments ('title' 'mangahub url')")

    manga_ch_urls = list_chapters(manga_url, manga_title)
    new_path = './' + "_" + manga_title + "_/"
    chapter_count = 1
    for manga_ch_url in manga_ch_urls:
        download_chapter_jpg(manga_ch_url, new_path)
        convert_chapter_pdf(manga_title, chapter_count, new_path)
        remove_chapter_jpg(new_path)
        chapter_count += 1
    combine_chapters(manga_title, new_path)

