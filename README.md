# SearchACT

This is a quick tool to search contacts in ACT genomics.

## quick use

```
python SearchACT.py # enter the interactive window

>>> benlin  # serch "benlin" in contact

>林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>>> AI & ben  # multiple condtion to search

>林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>>> (AI & ben) | bruce  # multiple condtion can using bracket to seperate

>林邦齊        Ben Lin 人工智慧部      ******@*******.***  1624    ****-***-***

>陳柏劭        Bruce Chen      次世代定序部    ******@*******.***  1520    ****-***-***

>>> *cal    # entering calculator mode
Calculator >>> 1+1*2
answer:  3.0
Calculator >>> exit

>>> ex  # type "ex" to leave
```

## install procedure

### install requirements by pip

```
pip install -r requirements.txt
```

### copy latest contact file to directory of *SearchACT*

```
\\tp-fs01\Public\公司通訊錄及座位表
```

### update dictionary

```
python UpdataContact.py
```

### run

```
python SearchACT.py
```

### or using GUI version

```
python SearchACT-GUI.py
```

### compile as .exe on windows (recommend)

```
pyinstaller -F SearchACT.py -i icon.ico
pyinstaller -F SearchACT-GUI.py -i icon.ico
pyinstaller -F UpdataContact.py
```

## Ready-to-use *.exe file. Can obtatin from folder \\tp-fs01\PUBLIC. Directly copy whole folder to your local

```
\\tp-fs01\Public\SearchACT
```

# GUI for SearchACT

## Start

```
python SearchACT-GUI.py # enter the interactive window
```

## Functions

- Input text field: input some text
- Search button: serch the input text in contact
- Calculate button: calculate the input expression
- File menu
  - Load: input pickle files (one for contact data, the other one for searching)
- Info menu: show version information

## Keyboard shortcuts

- Text + `Enter`: saerch the input text in contact
- Text + `Ctrl` + `Enter`: calculate the input expression
- `Ctrl` + `A`/`a`: select all text in the input text field
- `Ctrl` + `L`/`l`: input pickle files
- `Ctrl` + `I`/`i`: show version information
- Subwindow + `Esc`: close the subwindow
- Main window + Double `Esc`: exit GUI
