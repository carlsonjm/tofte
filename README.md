# Tofte

People first: one person, however many numbers, addresses and accounts reach
them. Tofte reads your contacts, works out which cards are the same person,
and answers a desktop search, or any program, with each person once.

It runs on your own computer, reads files only, and sends nothing anywhere.
It uses no AI: every join has a reason you can read, and every join can be
undone.

## How it decides who is who

- A **handle** is one way to reach someone: a phone number or an email
  address. A **record** is what one source says, such as one contact card. A
  **person** owns handles.
- Two records become one person only when they share a number or address, or
  when one card already lists both. A shared name alone never joins anyone. It
  is offered as a suggestion instead.
- A number or address that differently named cards share, such as a home
  landline or an office address, joins nobody.
- Joins and splits you make by hand always win. They are kept by handle, so
  the people can be rebuilt from the cards at any time.

## What it needs

- Python 3.10 or newer, and nothing else.
- Contact cards (vCard files) in a folder. By default Tofte reads
  `~/.local/share/kpeoplevcard`, where KDE Connect copies a paired phone's
  contacts when its Contacts feature is on. Set `GOOD_INPUT_PEOPLE_CARDS` to
  read another folder.

## Install

On Shuffle for Plasma it comes installed. Elsewhere:

    git clone https://github.com/carlsonjm/tofte.git
    ln -s "$PWD/tofte/bin/good-input-people" ~/.local/bin/good-input-people

## Use

`good-input-people` answers each question with one line of JSON.

| Command | Answer |
|---|---|
| `people [WORDS]` | Everyone, or those whose name, number or address fits the words |
| `person ID` | One person: every number and address, and a likely match if there is one |
| `join ID OTHER` | Those two are one person from now on |
| `not-same ID OTHER` | They are not, and Tofte won't suggest it again |
| `separate ID` | Take a joined person apart again |
| `choices` | How many cards were read, and how many joins and splits you made |
| `start-over` | Forget every join and split; people are as the cards say |

For example:

    $ good-input-people people ana
    {"count": 192, "found": 1, "people": [{"id": "12", "name": "Ana Reyes", "initials": "AR", "summary": "1 number · 1 address"}]}

Your joins and splits are kept in
`~/.local/share/good-input-people/decisions.json`. Nothing else is written.

To see who was joined and why, write a report page:

    python3 -m tofte ~/.local/share/kpeoplevcard report.html

The page holds real names, so keep it on the computer it was made on.

## Inside

- `tofte/vcard.py` reads contact cards into records.
- `tofte/model.py` is the person model and its join rules.
- `tofte/provider.py` is the command above.
- `tofte/report.py` writes the report page.

## Checks

    PYTHONPATH=. python3 -m unittest discover -s tests

The tests use made-up people only.

## Licence

GPL-2.0-or-later, as the rest of the Good Input suite. See `LICENSE`.
