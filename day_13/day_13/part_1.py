from day_13.machine import build_machines


def part_1(path: str) -> int:
    machines = build_machines(path)
    results = []
    for machine in machines:
        ax, ay = machine.a
        bx, by = machine.b
        px, py = machine.prize

        # ax*z + bx*q = px
        # ay*z + by*q = py
        # ay*z = py - by*q
        # z = (py - by*q) / ay
        # ax*(py - by*q) / ay + bx*q = px
        bp = (py*ax - ay*px) / (by*ax - ay*bx)
        ap = (py - by*bp) / ay
        if bp % 1 == 0 and ap % 1 == 0:
            print(f'ap: {ap}, bp: {bp}')
            results.append(ap * 3 + bp)


    print(results)
    return sum(results)

