import PyPDF2

try:
    with open('Real_Estate_Investment_Master_Guide.pdf', 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f'PDF has {len(pdf_reader.pages)} pages')

        # Read first few pages to understand structure
        print('\n=== PDF CONTENT ANALYSIS ===')

        sections_found = []
        for page_num in range(min(20, len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()

            # Look for section headers and key content
            lines = page_text.split('\n')
            for line in lines[:10]:  # Check first 10 lines of each page
                line = line.strip()
                if len(line) > 3 and not line.startswith(' ') and any(keyword in line.lower() for keyword in
                    ['framework', 'resource', 'directory', 'contact', 'database', 'formulas', 'strategies', 'tips', 'secrets', 'county', 'state']):
                    if line not in sections_found:
                        sections_found.append(f'Page {page_num + 1}: {line}')
                        break

        print('Key sections found:')
        for section in sections_found[:10]:  # Show first 10
            print(f'  {section}')

        # Look for Excel/toolkit mentions
        excel_content = []
        for page_num in range(min(30, len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            page_text = page.extract_text()
            if 'excel' in page_text.lower() or 'spreadsheet' in page_text.lower() or 'toolkit' in page_text.lower():
                excel_content.append(f'Page {page_num + 1}: Contains Excel/toolkit references')

        if excel_content:
            print(f'\nExcel/Toolkit references found ({len(excel_content)} pages):')
            for ref in excel_content[:5]:
                print(f'  {ref}')

except Exception as e:
    print(f'Error reading PDF: {e}')