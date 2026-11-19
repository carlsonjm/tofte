# Tofte

People first: one person, however many numbers, addresses and accounts reach
them. This repository holds the first piece, the model that turns what
sources say into people, and a small command a desktop search can ask.

## What is here

- `tofte/vcard.py` reads contact cards into source records.
- `tofte/model.py` is the person model. A handle is one way to reach someone,
  a record is what one source says, and a person owns handles. Records join
  only on the same number or address, never on a name. A number or address
  that differently named cards share joins nobody. Joins and splits made by
  hand always win and are kept by handle, so the people can be rebuilt from
  the sources at any time.
- `tofte/provider.py` answers `people`, `person`, `join`, `not-same`,
  `separate`, `choices` and `start-over` as JSON. `bin/good-input-people` runs it.
- `tofte/report.py` writes a page of who was joined and why:
  `python3 -m tofte CONTACTS_FOLDER REPORT.html`. The page holds real names
  and stays on the computer it was made on.

It needs Python 3.10 or newer and nothing else. The contact cards are the ones
KDE Connect copies from a paired phone to `~/.local/share/kpeoplevcard`.

## Checks

    PYTHONPATH=. python3 tests/test_model.py
    PYTHONPATH=. python3 tests/test_provider.py

The tests use made-up people only.

## Licence

GPL-2.0-or-later, as the rest of the Good Input suite. See `LICENSE`.
