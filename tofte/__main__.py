"""python3 -m tofte CONTACTS_FOLDER REPORT.html: prints counts only."""
import json
import sys
from pathlib import Path

from .model import resolve
from .report import counts, page
from .vcard import read_folder

folder, out = Path(sys.argv[1]), Path(sys.argv[2])
res = resolve(read_folder(folder))
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(page(res), "utf-8")
print(json.dumps(counts(res), indent=1))
