# CLUT_gen

---
This is workspace, is the sub-Project in CellCubes.
A system for automating CLUT (color look up table).

Here is the link of PJT memo : https://docs.google.com/presentation/d/1l6uX0eqAQQYrLMDQ9fH4RFiDb84Bq0mBtqkU07wjb-w/edit?usp=sharing

# Target
- Compact Designed GUI
- Change the GUI Module (Tkinter --> Pyside6)
- Create the architecture (Like MVC)

# How to set up
 - install uv [link](https://docs.astral.sh/uv/getting-started/installation/)
 - Clone this repo
 ```
    git clone https://github.com/ianYuinCellcubes/CC_CLUT_gen.git
 ```
 - move to CC_CLUT_gen
 ```
    cd CC_CLUT_gen
 ```
 - Configure using uv
 ```
    uv sync
    uv run main.py
 ```

 # User Guide
   [User Guide](https://docs.google.com/document/d/1oxsQ9YaeLJZiKPZF5-7SX2S9k1l9feujobXLEYIP3IQ/edit?usp=sharing)


# Log
- 2025-04-17 : Start Project
- 2025-07-17 : re_Create repo
	 -  Coding - Create GUI - Simply
		- create - CLUT Tab
		- create - Display Tab
- 2025-07-19 : Fix Error
	- Coding - Create GUI & Add Func
		- Fixed -~~ func. make bin file~~
- 2025-07-20 : 
	- Coding - Fix the GUI Error
		- Add - print Dialog result label
		- Fix - data table
		- create - table interrection, save data action
- 2025-07-21 : GUI Update
	- Coding - Update Result Dialog
		- Add - ~~func.save csv file~~
		- Update - ~~result dialog~~
	- Coding - Set StyleSheet QSS
		- Create - themes.qss
		- Add - Fonts : Sansation-Regular, Sansation-Bold
		- Set - QStylesheet, icon, rcc
	- Document : [User Guide](https://docs.google.com/document/d/1oxsQ9YaeLJZiKPZF5-7SX2S9k1l9feujobXLEYIP3IQ/edit?usp=sharing)
