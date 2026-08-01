#!/usr/bin/env python3
"""Import a Google Scholar CSV or BibTeX export into Jekyll publication data.

Google Scholar does not provide a supported bulk-download API. Export the
articles from your own public profile first, then run this script locally:

    python3 scripts/import_scholar.py ~/Downloads/scholar.csv --backup --force

The generated file is intended to be committed as _data/publications.yml.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "_data" / "publications.yml"
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")


def normalize_field_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("\n", " ").replace("\r", " ")
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("~", " ")
    return value.strip("{} ")


def extract_year(value: str | None) -> int | None:
    match = YEAR_RE.search(clean_text(value))
    return int(match.group(0)) if match else None


def clean_venue(value: str | None, year: int | None) -> str:
    venue = clean_text(value)
    if year:
        venue = re.sub(rf"(?:,|\s)\s*{year}\s*$", "", venue).strip(" ,")
    return venue


def split_authors(value: str | None) -> list[str]:
    authors = clean_text(value)
    if not authors:
        return []

    if re.search(r"\s+and\s+", authors, flags=re.IGNORECASE):
        parts = re.split(r"\s+and\s+", authors, flags=re.IGNORECASE)
    elif ";" in authors:
        parts = authors.split(";")
    else:
        parts = authors.split(",")

    return [part.strip() for part in parts if part.strip()]


def normalize_url(value: str | None) -> str:
    url = clean_text(value)
    if not url:
        return ""
    if url.startswith("doi:"):
        url = f"https://doi.org/{url[4:].strip()}"
    elif re.match(r"^10\.\d{4,9}/", url):
        url = f"https://doi.org/{url}"
    if not re.match(r"^https?://", url, flags=re.IGNORECASE):
        return ""
    return url


def first_value(row: dict[str, str], *names: str) -> str:
    normalized = {normalize_field_name(key): value for key, value in row.items()}
    for name in names:
        value = normalized.get(normalize_field_name(name), "")
        if isinstance(value, str) and value.strip():
            return value
    return ""


def publication_from_row(row: dict[str, str], selected: bool) -> dict:
    title = clean_text(first_value(row, "title"))
    year = extract_year(first_value(row, "year", "date", "publication date"))
    if year is None:
        year = extract_year(first_value(row, "publication", "venue", "journal", "booktitle"))

    venue = clean_venue(
        first_value(row, "venue", "publication", "journal", "booktitle", "conference"),
        year,
    )
    url = normalize_url(
        first_value(row, "paper_url", "paper url", "url", "link", "pdf_url", "doi")
    )

    publication = {
        "title": title,
        "authors": split_authors(first_value(row, "authors", "author")),
        "venue": venue,
        "year": year,
        "paper_url": url,
        "selected": selected,
    }
    return compact_publication(publication)


def parse_csv(text: str, selected: bool) -> list[dict]:
    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise ValueError("CSV input does not contain a header row")
    return [publication_from_row(row, selected) for row in reader]


def balanced_block(text: str, start: int) -> tuple[str, int]:
    opening = text[start]
    closing = "}" if opening == "{" else ")"
    depth = 0
    in_quote = False
    escaped = False

    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"' and depth > 0:
            in_quote = not in_quote
        if in_quote:
            continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
    raise ValueError("Unclosed BibTeX entry")


def split_top_level(text: str, delimiter: str = ",") -> list[str]:
    parts: list[str] = []
    start = 0
    brace_depth = 0
    in_quote = False
    escaped = False

    for index, char in enumerate(text):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            in_quote = not in_quote
        elif not in_quote and char == "{":
            brace_depth += 1
        elif not in_quote and char == "}":
            brace_depth -= 1
        elif char == delimiter and brace_depth == 0 and not in_quote:
            parts.append(text[start:index])
            start = index + 1
    parts.append(text[start:])
    return parts


def parse_bibtex_fields(body: str) -> dict[str, str]:
    chunks = split_top_level(body)
    fields: dict[str, str] = {}
    for chunk in chunks[1:]:
        if "=" not in chunk:
            continue
        name, value = chunk.split("=", 1)
        name = name.strip().lower()
        value = value.strip()
        if value.startswith("{") or value.startswith("("):
            value, _ = balanced_block(value, 0)
        elif value.startswith('"'):
            value = value[1:]
            if value.endswith('"'):
                value = value[:-1]
        fields[name] = clean_text(value)
    return fields


def parse_bibtex(text: str, selected: bool) -> list[dict]:
    publications: list[dict] = []
    cursor = 0
    entry_re = re.compile(r"@([a-zA-Z]+)\s*([\{\(])")

    while match := entry_re.search(text, cursor):
        entry_type = match.group(1).lower()
        body, cursor = balanced_block(text, match.end() - 1)
        if entry_type in {"comment", "preamble", "string"}:
            continue

        fields = parse_bibtex_fields(body)
        row = {
            "title": fields.get("title", ""),
            "author": fields.get("author", ""),
            "journal": fields.get("journal", ""),
            "booktitle": fields.get("booktitle", ""),
            "year": fields.get("year", ""),
            "url": fields.get("url", "") or fields.get("doi", ""),
        }
        publication = publication_from_row(row, selected)
        if publication:
            publications.append(publication)
    return publications


def compact_publication(publication: dict) -> dict:
    if not publication.get("title"):
        return {}
    return {
        key: value
        for key, value in publication.items()
        if value not in (None, "", [])
    }


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]", "", title.lower())


def deduplicate(publications: Iterable[dict]) -> list[dict]:
    unique: list[dict] = []
    seen: set[str] = set()
    for publication in publications:
        key = title_key(publication.get("title", ""))
        if not key or key in seen:
            continue
        seen.add(key)
        unique.append(publication)
    return unique


def yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def to_yaml(publications: list[dict], source: Path) -> str:
    lines = [
        "# Generated by scripts/import_scholar.py.",
        f"# Source export: {source.name}",
        "# Re-run the importer after exporting updated records from Google Scholar.",
    ]
    for publication in publications:
        lines.append(f"- title: {yaml_scalar(publication['title'])}")
        if publication.get("authors"):
            lines.append("  authors:")
            for author in publication["authors"]:
                lines.append(f"    - {yaml_scalar(author)}")
        if publication.get("venue"):
            lines.append(f"  venue: {yaml_scalar(publication['venue'])}")
        if publication.get("year") is not None:
            lines.append(f"  year: {publication['year']}")
        if publication.get("paper_url"):
            lines.append(f"  paper_url: {yaml_scalar(publication['paper_url'])}")
        lines.append(f"  selected: {'true' if publication.get('selected') else 'false'}")
    return "\n".join(lines) + "\n"


def detect_format(path: Path, explicit_format: str) -> str:
    if explicit_format != "auto":
        return explicit_format
    suffix = path.suffix.lower()
    if suffix in {".bib", ".bibtex"}:
        return "bibtex"
    if suffix == ".csv":
        return "csv"
    raise ValueError("Could not infer format; use --format csv or --format bibtex")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert a Google Scholar CSV or BibTeX export to Jekyll publication YAML."
    )
    parser.add_argument(
        "source",
        type=Path,
        help="Scholar export file (.csv or .bib), or - to read from stdin",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output YAML path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--format",
        choices=("auto", "csv", "bibtex"),
        default="auto",
        help="Input format, if it cannot be inferred from the file extension",
    )
    parser.add_argument(
        "--selected",
        action="store_true",
        help="Mark imported publications as selected for the homepage",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Copy an existing output file to <output>.bak before replacing it",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow replacing an existing non-empty output file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the generated YAML instead of writing the output file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output.expanduser()
    source = args.source.expanduser()

    try:
        if source == Path("-"):
            if args.format == "auto":
                raise ValueError("stdin input requires --format csv or --format bibtex")
            input_format = args.format
            source_label = Path("stdin")
            text = sys.stdin.read()
        else:
            source = source.resolve()
            if not source.is_file():
                print(f"error: source file not found: {source}", file=sys.stderr)
                return 2
            input_format = detect_format(source, args.format)
            source_label = source
            text = source.read_text(encoding="utf-8-sig")
        if input_format == "csv":
            publications = parse_csv(text, args.selected)
        else:
            publications = parse_bibtex(text, args.selected)
        publications = deduplicate(publication for publication in publications if publication)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if not publications:
        print("error: no publications were found in the export", file=sys.stderr)
        return 1

    rendered = to_yaml(publications, source_label)
    if args.dry_run:
        print(rendered, end="")
        return 0

    if output.exists() and output.read_text(encoding="utf-8").strip() not in {"", "[]"} and not args.force:
        print(
            f"error: refusing to replace non-empty output {output}; use --force or choose another --output",
            file=sys.stderr,
        )
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    if args.backup and output.exists():
        backup = output.with_name(f"{output.name}.bak")
        shutil.copy2(output, backup)
        print(f"Backed up {output} to {backup}")
    output.write_text(rendered, encoding="utf-8")
    print(f"Imported {len(publications)} publications into {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
