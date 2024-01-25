# File Search Tool

File Search Tool is a Python application built with Tkinter that allows users to search for text within documents. The application supports searching within `.docx`, `.txt`, `.html`, and `.rtf` files and offers options such as regular expression matching, inclusion of subdirectories, and case sensitivity.

## Features

- **Directory Selection**: Choose the starting directory for your search.
- **Search Text**: Input the text you are searching for in the selected directory.
- **Regular Expression**: Toggle the option to use regular expressions for more advanced searches.
- **Include Subdirectories**: Choose whether to include subdirectories in the search.
- **Case Sensitive**: Toggle case sensitivity for the search.

## Prerequisites

Before running this script, you need to have Python installed on your system. If you do not have Python installed, download and install it from the official [Python website](https://www.python.org/). Additionally, you need the following packages:

- `tkinter`
- `python-docx`

To install `python-docx`, run the following command:

```bash
pip install python-docx
```

## Running the Application

To run the File Search Tool, you can either execute the script directly using Python or integrate it into your own application.

To run it directly, navigate to the directory containing the script and execute:

```bash
python file_search_tool.py
```

## Usage

1. Start the application.
2. Click "Browse..." to select the directory where you want to search for files.
3. Enter the text you want to search for in the "Search Text" field.
4. Check the desired options (Use Regular Expression, Include Subdirectories, Case Sensitive).
5. Click "Search" to begin the search process.
6. The results will be displayed in the scrolled text box at the bottom.
7. Click "Cancel" if you wish to stop the search before it completes.
