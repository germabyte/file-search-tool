# File Search Tool

## Description
The File Search Tool is a Python application built using the Tkinter library. It provides a user-friendly graphical interface to search for text within files across various formats, including `.docx`, `.txt`, `.html`, and `.rtf`. The tool supports regular expression searches, inclusion of subdirectories, and case-sensitive searches. Additionally, it displays snippets of context around the found text.

## Features
- **Directory Selection**: Choose a specific directory to search in.
- **Text Search**: Input the text or pattern to search for within the files.
- **Regular Expression Support**: Option to use regular expressions for advanced search capabilities.
- **Include Subdirectories**: Ability to include subdirectories in the search.
- **Case Sensitive Search**: Option to perform case-sensitive searches.
- **Context Display**: Shows snippets of text surrounding the found patterns.
- **File Type Support**: Searches within `.docx`, `.txt`, `.html`, and `.rtf` files.

## Installation

To run this application, ensure you have Python installed on your system. You will also need to install the following dependencies:

```bash
pip install tkinter docx
```

## Usage

1. **Start the Application**: Run the script to start the application.
2. **Select Directory**: Click on 'Browse...' to choose the directory you want to search.
3. **Enter Search Text**: Type the text or regular expression pattern you are searching for in the 'Search Text' field.
4. **Set Search Options**: Select the options for regular expression, subdirectory inclusion, and case sensitivity as needed.
5. **Start Search**: Click on 'Search' to begin the search.
6. **View Results**: Results are displayed in the list box. Selecting a result will display a context snippet.
7. **Cancel Search**: Click on 'Cancel' to stop the ongoing search.
8. **Reset**: Resets the application for a new search.
