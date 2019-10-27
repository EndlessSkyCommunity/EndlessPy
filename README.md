EndlessPy
---

Known Issues:
- GitPython uses the System Git and probably fails if there is no Git installed
- If the Git version is more recent, there is no progress meter
- The Progress Meter is laggy
- There is no "finished" dialog
- The main selection window pops up again after an installation
- The main progress window is clunky
- Everything is placed in the main ES folder
- No symlinks, no menu entries, just a folder

Development Setup:
--
Prerequisites:
- Python 3
- PyCharm

Setup:
- Install the Save Actions plug-in for PyCharm, and configure it to auto-reformat on save (or remember to reformat manually, which sucks)
- Clone this Repository
- Set up a new virtualenv: `virtualenv -p python3 venv`
- Activate it: `source venv/bin/activate` (linux/mac i guess?) `.\venv\Scripts\activate` (Windows)
- Install dependencies: `pip install -r requirements.txt`
- Start hacking!
