<h1> mdtodocu - Markdown to Docusaurus Converter </h1>

<h2>Table of Contents</h2>

- [Introduction](#introduction)
- [Features](#features)
- [Limitations](#limitations)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Convert mdbook to Docusaurus](#1-convert-mdbook-to-docusaurus)
  - [2. Command-Line Arguments](#2-command-line-arguments)
    - [Example:](#example)
- [How It Works](#how-it-works)
- [Notes](#notes)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

**mdtodocu** is a Python script designed to convert markdown files structured for **mdbook** into a format compatible with **Docusaurus**. It automates the process of reorganizing files, adding frontmatter, and creating directory structures required by Docusaurus. This tool is ideal for developers migrating documentation from mdbook to Docusaurus.


## Features

- Converts mdbook `SUMMARY.md` hierarchy into Docusaurus-compatible directory structures.
- Automatically generates `_category_.json` files for Docusaurus sidebar categories.
- Adds frontmatter (title and sidebar position) to markdown files.
- Recursively searches for and organizes markdown files.
- Preserves the original content while adapting it for Docusaurus.

## Limitations

- It does not copy the images
- It does not include the hero mdbook include sections

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mik-tf/mdtodocu.git
   cd mdtodocu
   ```

2. Ensure Python 3.x is installed on your system.

## Usage

### 1. Convert mdbook to Docusaurus

Run the script with the following command:
```bash
python mdtodocu.py <userinput>
```

Replace `<userinput>` with the name of the mdbook directory you want to convert. The script will look for a `SUMMARY.md` file in `../books/<userinput>/SUMMARY.md` and process the markdown files accordingly.

### 2. Command-Line Arguments

- `<userinput>`: The name of the mdbook directory to convert. This is a required argument.

#### Example:
```bash
python mdtodocu.py my-mdbook
```

This will:
1. Parse the `SUMMARY.md` file in `../books/my-mdbook/SUMMARY.md`.
2. Create a Docusaurus-compatible directory structure in `docu_books/my-mdbook`.
3. Add frontmatter to markdown files and generate `_category_.json` files.

## How It Works

1. **Parsing `SUMMARY.md`**: The script reads the `SUMMARY.md` file to extract the hierarchy of markdown files, including titles and indentation levels.
2. **Directory Structure**: It creates a directory structure in the output folder (`docu_books/<userinput>`) based on the hierarchy.
3. **Frontmatter**: Adds Docusaurus-compatible frontmatter (title and sidebar position) to each markdown file.
4. **Category Files**: Generates `_category_.json` files for directories to define sidebar categories in Docusaurus.
5. **File Copying**: Copies and updates markdown files while preserving their content.

## Notes

- Ensure the `SUMMARY.md` file follows the standard mdbook format.
- The script assumes markdown files are located in the current directory or its subdirectories.
- Binary files and non-markdown files are ignored.
- If a file is not found in the source directory, a warning is displayed, and the file is skipped.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/mik-tf/mdtodocu/issues) or submit a pull request.

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.