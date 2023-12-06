![EGA_logo](https://github.com/iamgeorgp/EGA_consult/assets/128215564/c9c8750d-7d13-4e0c-96c6-8968a708eb8b)

# EGA System Tool: A graphical information system for working with the database of a consulting company

## Project Documents
[RU README version](https://github.com/iamgeorgp/EGA_consult/blob/main/README_RU.md)

[Terms of Reference](https://github.com/iamgeorgp/EGA_consult/blob/main/TermsofReference.md)

[User Manual](https://github.com/iamgeorgp/EGA_consult/blob/main/UserManual.md)

## Description

The repository contains a graphical user interface (GUI) information system designed specifically for efficient database management in a consulting company. The system provides parsing, data generation functions and provides a GUI for easy interaction with the database.

## Features of EGA System Tool

EGA System Tool is a graphical application (GUI) designed for use in a consulting agency. Access to the main database window requires authentication with a user login and password.

The main functionality of the interface allows you to create SQL scripts for database queries and provides a convenient table form for viewing query results. It is also possible to export these results in .csv format.

A schema displayed in the interface is provided for easy navigation of the database. In addition, the user can download a scan of the contract by specifying its number.

The window interface is divided into blocks using separators, allowing the user to resize or close them at will.

### Project Structure

### Parsing
The `parsing` folder contains files responsible for parsing information about people's first and last names. This parsed data is used in the data generation process.

### Generator
The `generator` folder contains the `gen_funcs2.py` file that generates information about companies, clients, service types, agency services, managers, contracts, etc. It also contains functions for creating contract scans and creating a working SQL database.

### GUI_app.
The `GUI_app` folder contains scripts for creating a GUI application and the specifications needed to implement it.

### Distribution Package
The `dist/ega_system` directory contains a sample working application packaged for distribution.

### License

This project is licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode).

## Contact Information

For questions and discussions, please contact [author](https://github.com/iamgeorgp) via the contacts listed in his profile.
