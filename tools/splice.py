"""Splice diagram.svg into index.html between the diagram marker comments.

Usage: python3 -I tools/splice.py diagram.svg index.html
Prints "spliced" when the page changed, "unchanged" otherwise. Exits 2 if a marker is missing.
"""
import sys

START = "<!-- diagram:start -->"
END = "<!-- diagram:end -->"


def main(svg_path: str, html_path: str) -> int:
    svg = open(svg_path).read()
    html = open(html_path).read()
    lines = html.split("\n")
    try:
        s = next(i for i, l in enumerate(lines) if l.strip() == START)
        e = next(i for i, l in enumerate(lines) if l.strip() == END)
    except StopIteration:
        missing = START if START not in html else END
        print(f"splice: marker {missing} not found in {html_path}", file=sys.stderr)
        return 2
    before = "\n".join(lines[: s + 1]) + "\n"
    after = "\n".join(lines[e:])
    new = before + svg + after
    if new == html:
        print("unchanged")
        return 0
    open(html_path, "w").write(new)
    print("spliced")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
