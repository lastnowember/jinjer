from pathlib import Path
import hashlib
import constants
md_file = constants.CURRENT_PATH + '/mark.md'
path_file = Path(md_file)
md = path_file.read_bytes()
hash = hashlib.sha1(md).hexdigest()

print(hash)