EndlessPy
---

Known Issues:
- The Progress Meter is a bit laggy
- The main progress window only shows the first letter of the current step's description
- There is no "finished" dialog
- The main selection window pops up again after an installation
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
