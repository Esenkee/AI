def solve(n, use_mrv=False, use_degree=False, use_lcv=False, limit=1_000_000):
    assignment = {}   # мөр -> багана
    nodes = 0

    def conflict(r1, c1, r2, c2):
        return c1 == c2 or abs(c1 - c2) == abs(r1 - r2)

    def legal_cols(row):
        return [c for c in range(n)
                if all(not conflict(row, c, r, assignment[r]) for r in assignment)]

    def pick_row():
        rows = [r for r in range(n) if r not in assignment]
        if not use_mrv:
            return rows[0]
        # MRV: боломжит багана хамгийн цөөн мөр
        # Degree: тэнцвэл оноогдоогүй хөрш олныг (N-Queens-д бүх мөр ижил)
        def key(r):
            degree = len(rows) - 1 if use_degree else 0
            return (len(legal_cols(r)), -degree)
        return min(rows, key=key)

    def order_cols(row):
        cols = legal_cols(row)
        if not use_lcv:
            return cols
        def removed(c):
            return sum(1 for r in range(n) if r != row and r not in assignment
                       for c2 in legal_cols(r) if conflict(row, c, r, c2))
        return sorted(cols, key=removed)

    def dfs():
        nonlocal nodes
        if len(assignment) == n:
            return True
        row = pick_row()
        for col in order_cols(row):
            nodes += 1
            if nodes > limit:
                return None          # хэт удаан
            assignment[row] = col
            result = dfs()
            if result is None or result:
                return result
            del assignment[row]
        return False

    result = dfs()
    return "хэт удаан" if result is None else nodes


configs = [
    ("A. Heuristic-гүй",      dict()),
    ("B. MRV",                dict(use_mrv=True)),
    ("C. MRV + Degree",       dict(use_mrv=True, use_degree=True)),
    ("D. MRV + Degree + LCV", dict(use_mrv=True, use_degree=True, use_lcv=True)),
]

print("| Тохиргоо | 8-Queens | 12-Queens | 16-Queens |")
print("|---|---|---|---|")
for name, kw in configs:
    row = [str(solve(n, **kw)) for n in (8, 12, 16)]
    print(f"| {name} | " + " | ".join(row) + " |")