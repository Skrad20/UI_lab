
def profiler(launch_location: str):
    def decorator(func):
        import time

        def wrapper(*args, **kwargs):
            start = time.time()
            res = func(*args, **kwargs)
            end = time.time()
            duration = round(end-start, 3)
            print(
                f"[*] {launch_location} : Время выполнения {func.__name__}:" +
                f" {duration} секунд."
                )
            return res
        return wrapper
    return decorator


@profiler("Test")
def test(data):
    count = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            count += data[i][j]
    return count


@profiler("Test")
def test_1(data):
    count = 0
    for j in range(len(data[0])):
        for i in range(len(data)):
            count += data[i][j]
    return count


data = [
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
    [*range(500000)],
]


if __name__ == "__main__":
    test_1(data)
    test(data)
