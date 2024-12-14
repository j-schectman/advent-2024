from day_13.machine import build_machines


def part_2(path: str) -> int:
    machines = build_machines(path, 10000000000000)
    results = []
    for machine in machines:
        ax, ay = machine.a
        bx, by = machine.b
        px, py = machine.prize

        # ax*ap + bx*bp = px
        # ay*ap + by*bp = py
        # ap = (py - by*bp) / ay
        # ax*(py - by*bp) / ay + bx*bp = px
        # (ax*py - by*bp)/ay + bx*bp = px
        # ax*py - by*bp + ay*bx*bp = px*ay
        # ax*py - px*ay = by*bp - ay*bx*bp
        # ax*py - px*ay = bp(by - ay*bx)
        # bp = (ax*py - px*ay) / (by - ay*bx)
        bp = (py*ax - ay*px) / (by*ax - ay*bx)
        ap = (py - by*bp) / ay
        if bp % 1 == 0 and ap % 1 == 0:
            print(f'ap: {ap}, bp: {bp}')
            results.append(ap * 3 + bp)


    print(results)
    return sum(results)

