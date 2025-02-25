import csv
import xml.etree.ElementTree as ET
import os
import multiprocessing
import glob

def xml_to_csv(xml_file, csv_file):
    """
    將 PubMed XML 檔案轉換為 CSV 檔案。

    Args:
        xml_file (str): XML 檔案的絕對路徑。
        csv_file (str): CSV 檔案的絕對路徑。
    """
    try:
        # Load and parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Ensure the CSV directory exists
        os.makedirs(os.path.dirname(csv_file), exist_ok=True)

        # Open the CSV file for writing
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row
            writer.writerow(['PMID', 'Title', 'Abstract', 'Authors', 'Year', 'Journal', 'Keyword'])

            # Iterate through each PubmedArticle in the XML
            for article in root.findall('PubmedArticle'):
                # Extract the PMID
                pmid = article.findtext('MedlineCitation/PMID', default='')

                # Extract the title
                title = article.findtext('MedlineCitation/Article/ArticleTitle', default='')

                # Extract the abstract
                abstract = article.findtext('MedlineCitation/Article/Abstract/AbstractText', default='')

                # Extract the authors
                authors = []
                for author in article.findall('MedlineCitation/Article/AuthorList/Author'):
                    last_name = author.findtext('LastName', default='')
                    fore_name = author.findtext('ForeName', default='')
                    authors.append(f'{fore_name} {last_name}')
                authors = ', '.join(authors)

                # Extract the year
                year = article.findtext('MedlineCitation/Article/Journal/JournalIssue/PubDate/Year', default='')

                # Extract the journal
                journal = article.findtext('MedlineCitation/Article/Journal/Title', default='')

                # Extract the keywords
                keywords = []
                for keyword in article.findall('MedlineCitation/KeywordList/Keyword'):
                    keywords.append(keyword.text)
                keywords = '&'.join([kw.replace('\n', ' ') for kw in keywords if kw is not None])

                # Write the row to the CSV file
                writer.writerow([pmid, title, abstract, authors, year, journal, keywords])

        print(f'Data has been written to {csv_file}')

    except FileNotFoundError:
        print(f'Error: File {xml_file} not found.')
    except ET.ParseError:
        print(f'Error: Unable to parse {xml_file}. Please check if the XML file is valid.')
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

def process_xml_file(xml_file, csv_dir):
    """
    處理單個 XML 檔案。

    Args:
        xml_file (str): XML 檔案的絕對路徑。
        csv_dir (str): CSV 檔案目錄的絕對路徑。
    """
    filename = os.path.splitext(os.path.basename(xml_file))[0]
    csv_file = os.path.join(csv_dir, f'{filename}.csv')
    xml_to_csv(xml_file, csv_file)

def main():
    xml_dir = 'xml'
    csv_dir = 'csv'

    # Ensure the CSV directory exists
    os.makedirs(csv_dir, exist_ok=True)

    xml_files = glob.glob(os.path.join(xml_dir, '*.xml'))

    if not xml_files:
        print(f'No XML files found in {xml_dir}.')
        return

    with multiprocessing.Pool(processes=18) as pool:
        tasks = [(xml_file, csv_dir) for xml_file in xml_files]
        pool.starmap(process_xml_file, tasks)

    print('All XML files have been processed.')

if __name__ == '__main__':
    main()