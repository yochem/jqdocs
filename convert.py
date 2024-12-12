from pathlib import Path
import yaml
from contextlib import suppress


def str_presenter(dumper, data):
    if len(data.splitlines()) > 1:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


yaml.add_representer(str, str_presenter)


def ensure_all_keys_used(dictionary):
    if len(dictionary) > 0:
        raise RuntimeWarning(
            f"dictionary still contains fields {list(dictionary.keys())}"
        )

def md_code(code, lang=""):
    if isinstance(code, str):
        code = [code]
    return "\n".join([f"```{lang}", *code, f"```"])

def md_frontmatter(fm):
    return "\n".join(["---", yaml.dump(fm),"---"])

def md_heading(title, depth):
    return f"{'#'*depth} {title}"


def convert_document(doc):
    md_doc = []
    frontmatter = {}
    for key in ("headline", "manpage_intro", "manpage_epilogue"):
        frontmatter[key] = doc.pop(key)
    md_doc.append(md_frontmatter(frontmatter))

    md_doc.append(doc.pop('body'))

    for section in doc.pop("sections"):
        md_doc.append(md_heading(section.pop('title'), depth=2))
        with suppress(KeyError):
            md_doc.append(section.pop("body"))

        if "entries" in section:
            for entry in section.pop("entries"):
                md_doc.append(md_heading(entry.pop('title'), depth=3))
                md_doc.append(entry.pop("body"))
                with suppress(KeyError):
                    for example in entry.pop("examples"):
                        md_doc.append('program:')
                        md_doc.append(md_code(example.pop("program"), lang="jq"))
                        md_doc.append('input:')
                        md_doc.append(md_code(example.pop("input"), lang="json"))
                        md_doc.append('output:')
                        md_doc.append(md_code(example.pop("output"), lang="json"))
                        ensure_all_keys_used(example)

                ensure_all_keys_used(entry)

        ensure_all_keys_used(section)

    ensure_all_keys_used(doc)

    return '\n'.join(md_doc)


output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

for manual in Path('manuals').glob('*.yml'):
    with open(manual, "r") as f:
        old = yaml.safe_load(f)

    new = convert_document(old)
    new_doc = output_dir / manual.with_suffix('.md').name
    print(f'converted {manual} to {new_doc}')
    new_doc.write_text(new)
