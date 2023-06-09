# an app to rename all ebook pdfs based on isbn contained within the file

## Tasks:
---
* ~~The program should be able to process directories as well individual files~~
* ~~If directory is passed to the program:~~
    * **Able to process multiple pdfs simultaneously**
        * Multithreading required
        * I/O bound operations
    * ~~Able to process multiple pdfs simultaneously~~
* ~~All files should be in the same file tree as original~~
---

### Renamer - eBook pdf library
---
1. ~~Extract text from pdf~~
2. ~~Find ISBN in extracted text~~
    - ~~ISBN might not be on front page~~
        - ~~Iterate through pages to locate ISBN~~
        - ~~Loop until located~~
    - ~~Use PyPDF2 lib functions~~
3. ~~Query ISBN extract with an ISBN API, example:~~
https://www.googleapis.com/books/v1/volumes?q=isbn:
4. ~~Extract Title, Author from json response~~
5. ~~Rename original file name using the json response data~~