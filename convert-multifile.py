from pathlib import Path
import re
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


def convert_document(doc) -> list[list[str]]:
    md_docs = {}

    # not necessary for website
    doc.pop("manpage_intro")
    doc.pop("manpage_epilogue")

    md_docs['_index'] = []
    frontmatter = {"title": doc.pop('headline')}
    md_docs['_index'].append(md_frontmatter(frontmatter))

    md_docs['_index'].append(doc.pop('body'))

    for section in doc.pop("sections"):
        title = section.pop('title')
        md_docs[title] = []
        md_docs[title].append(md_heading(title, depth=2))
        with suppress(KeyError):
            md_docs[title].append(section.pop("body"))

        if "entries" in section:
            for entry in section.pop("entries"):
                md_docs[title].append(md_heading(entry.pop('title'), depth=3))
                md_docs[title].append(entry.pop("body"))
                with suppress(KeyError):
                    for example in entry.pop("examples"):
                        md_docs[title].append('program:')
                        md_docs[title].append(md_code(example.pop("program"), lang="jq"))
                        md_docs[title].append('input:')
                        md_docs[title].append(md_code(example.pop("input"), lang="json"))
                        md_docs[title].append('output:')
                        md_docs[title].append(md_code(example.pop("output"), lang="json"))
                        ensure_all_keys_used(example)

                ensure_all_keys_used(entry)

        ensure_all_keys_used(section)

    ensure_all_keys_used(doc)

    return md_docs


output_dir = Path('multi')
output_dir.mkdir(exist_ok=True)

for manual in Path('manuals').glob('*.yml'):
    with open(manual, "r") as f:
        old = yaml.safe_load(f)

    new_files = convert_document(old)
    manual_dir = output_dir / manual.stem
    manual_dir.mkdir(exist_ok=True)
    for fn, lines in new_files.items():
        filename = re.sub(r'[^\w\-\.]', '', fn.lower().replace(' ', '-')).strip('.') + '.md'

        new_doc = output_dir / manual.stem / filename
        new_doc.write_text('\n'.join(lines))
        print(f'converted {manual} to {new_doc}')
