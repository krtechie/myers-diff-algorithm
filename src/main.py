import sys


def read_lines(path):
    with open(path, "rb") as f:
        data = f.read()
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return lines


def run(path_a, path_b, with_highlight):
    a = read_lines(path_a)
    b = read_lines(path_b)


def main():
    if len(sys.argv) != 4 or sys.argv[1] not in ("lines", "highlight"):
        sys.stderr.write("usage: main.py lines|highlight A B\n")
        return 2
    try:
        run(sys.argv[2], sys.argv[3], sys.argv[1] == "highlight")
    except OSError as e:
        sys.stderr.write("cannot read file: %s\n" % e)
        return 2
    return 0


raise SystemExit(main())
