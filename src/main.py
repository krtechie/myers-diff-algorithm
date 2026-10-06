import sys
from array import array


def _myers_core(a, b):
    n, m = len(a), len(b)

    max_d = n + m
    offset = max_d + 1            # v[offset + k] is the furthest x on diagonal k
    v = [0] * (2 * max_d + 3)

    # snaps[d] holds v after round d, only for the diagonals that round could
    # touch (k = -d, -d+2, ..., d). Index of diagonal k is (k + d) // 2.
    snaps = []
    final_d = 0

    for d in range(max_d + 1):
        done = False
        for k in range(-d, d + 1, 2):
            idx = offset + k
            if k == -d or (k != d and v[idx - 1] < v[idx + 1]):
                x = v[idx + 1]          # move down: an insertion
            else:
                x = v[idx - 1] + 1      # move right: a deletion
            y = x - k
            while x < n and y < m and a[x] == b[y]:   # follow the snake
                x += 1
                y += 1
            v[idx] = x
            if x >= n and y >= m:
                done = True
                break
        if done:
            final_d = d
            break
        snaps.append(array('i', v[offset - d: offset + d + 1: 2]))

    # Walk back from (n, m) to (0, 0) and record the edits.
    dels, adds = [], []
    x, y = n, m
    for d in range(final_d, 0, -1):
        vs = snaps[d - 1]       # v after round d-1; diagonal kk is at (kk + d - 1) // 2
        k = x - y
        if k == -d or (k != d and vs[(k - 1 + d - 1) >> 1] < vs[(k + 1 + d - 1) >> 1]):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = vs[(prev_k + d - 1) >> 1]
        prev_y = prev_x - prev_k
        if prev_k == k + 1:
            adds.append(prev_y)         # went down: b[prev_y] was inserted
        else:
            dels.append(prev_x)         # went right: a[prev_x] was deleted
        x, y = prev_x, prev_y

    dels.reverse()
    adds.reverse()
    return dels, adds


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
