import PyPDF2
import re
import geocoder


def extract_address(text):
    if 'PGH Ward'.lower() in text.lower():
        extracted = ''.join(text[11:])
    else:
        extracted = re.search('[a-zA-Z ]+([0-9]+.*)', text).groups(0)[0]
    return extracted


def process_address(raw_address, writer, identifier):
    real_address = extract_address(raw_address)
    formatted_address = re.sub(' , ', '', real_address)
    writer.write('{}\t{}\n'.format(formatted_address, identifier))


def process_pdf(pdf, writer, identifier):
    print(f'  Found {pdf.numPages} pages.')
    for page_num in range(pdf.numPages):
        text = pdf.getPage(page_num).extractText()
        page_addrs = re.findall('Municipality\:\s([a-zA-Z ]+[0-9]+.*?[0-9]{5})', text)
        for idx, raw_addr in enumerate(page_addrs):
            print(f'  Processing address {idx+1} of {len(page_addrs)} on page {page_num+1}')
            process_address(raw_addr, writer=writer, identifier=identifier)


def main():
    files = ['bid.pdf', 'postponed.pdf']
    files = ['bid.pdf']
    with open('addresses.tsv', 'w') as write:
        write.write('Address\tCategory\n')
        for filename in files:
            with open(filename, 'rb') as read:
                pdf = PyPDF2.PdfFileReader(read)
                print(f'Processing {filename}')
                process_pdf(pdf, writer=write, identifier=filename)


if __name__ == '__main__':
    main()
