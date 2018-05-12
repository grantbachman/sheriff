import PyPDF2
import re
import geocoder


def extract_address(text):
    if 'PGH Ward'.lower() in text.lower():
        extracted = ''.join(text[11:])
    else:
        extracted = re.search('[a-zA-Z ]+([0-9]+.*)', text).groups(0)[0]
    return extracted


def geocode(address):
    geo = geocoder.google(address)
    lat = geo.lat or 0.0
    lng = geo.lng or 0.0
    return lat, lng


def process_address(raw_address, writer, identifier):
    real_address = extract_address(raw_address)
    formatted_address = re.sub(' , ', '', real_address)
    lat, lng = geocode(formatted_address)
    if lat and lng:
        writer.write('{}\t{}\t{}\t{}\n'.format(formatted_address, lat, lng, identifier))


def process_pdf(pdf, writer, identifier):
    for page_num in range(pdf.numPages):
        text = pdf.getPage(page_num).extractText()
        page_addrs = re.findall('Municipality\:\s([a-zA-Z ]+[0-9]+.*?[0-9]{5})', text)
        for raw_addr in page_addrs:
            process_address(raw_addr, writer=writer, identifier=identifier)


def main():
    files = ['bid.pdf', 'postponed.pdf']
    with open('addresses.tsv', 'w') as write:
        for filename in files:
            with open(filename, 'rb') as read:
                pdf = PyPDF2.PdfFileReader(read)
                process_pdf(pdf, writer=write, identifier=filename)


if __name__ == '__main__':
    main()
