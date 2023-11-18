# Artificial Intelligence Project

## Project Structure
```bash
├── data/                       # Database file
├── logs/                       # system logs
├── res/                        # PNGs, JPEGs, GIFs etc
├── src/                        
    ├── prolog/                 # prolog files
    ├── scripts/                # python source files
        ├── database/           # database functions
        ├── gui/                # UI components
        ├── main.py             # app entry point
        └── prolog_interface.py # bridge between prolog and python
├── Project Outline.pdf         # project outline
├── requirements.txt            # pip dependencies
└── README.md
```

## Getting Started

### Tech Stack
- Python
- Prolog
- SQLite

### Prerequisites
- Python 3.12+
- Prolog SWI Compiler

### PIP Dependencies
- pyswip `pip install git+https://github.com/yuce/pyswip@master`
- tkinter `pip install tkinter`
- PIL `pip install pillow`
- sqlite3 `pip install sqlite3`
- easygui `pip install easygui`
- reportlab `pip install reportlab`

> Tested in IntelliJ IDEA (Ultimate Edition) with Python and Prolog plugin.
