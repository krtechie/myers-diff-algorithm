import sys
from array import array


def myers(a, b):
    """Minimal diff of two sequences.

    Returns (dels, adds): sorted lists of indices. dels are positions in a that
    are deleted, adds are positions in b that are inserted. Everything else is
    kept, in order.
    """
    n, m = len(a), len(b)

    # 1. Trim the common prefix and suffix. On real files most lines match,
    #    so this removes almost all of the work before Myers even starts.
    lo = 0
    while lo < n and lo < m and a[lo] == b[lo]:
        lo += 1
    hi_a, hi_b = n, m
    while hi_a > lo and hi_b > lo and a[hi_a - 1] == b[hi_b - 1]:
        hi_a -= 1
        hi_b -= 1

    core_a = list(a[lo:hi_a])
    core_b = list(b[lo:hi_b])

    if not core_a:
        return [], list(range(lo, hi_b))
    if not core_b:
        return list(range(lo, hi_a)), []

    dels, adds = _myers_core(core_a, core_b)
    return [x + lo for x in dels], [y + lo for y in adds]


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
