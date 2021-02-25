STREETS_DICT = {}

INTERSECTIONS = {}


class Intersection:

    def __init__(self) -> None:
        self.streets_in = []
        self.streets_out = []
        # probability that a short car with pr
        self.short_path_metric = []


class Street:
    def __init__(self, i_start, i_end, name, time_length):
        self.i_start = i_start
        self.i_end = i_end
        self.street_name = name
        self.time_length = time_length

        self.car_traffic = 0
        self.metric = 0

    def good_path_metric(self):
        self.metric = self.car_traffic/self.time_length


class Car:
    def __init__(self, n_streets_on_path: int, street_names: tuple):
        self.n_streets_on_path = n_streets_on_path
        self.street_names = street_names

    def path_duration(self):
        return sum((STREETS_DICT[name].time_length for name in self.street_names))

    def passes_on_street(self, street_name):
        for name in self.street_names:
            if name == street_name:
                return True
        return False


def extract_data(filename):
    global STREETS_DICT
    global INTERSECTIONS
    with open(filename, 'r') as file:
        line = file.readline()
        duration,  n_intersections, n_streets, n_cars, score_per_car = map(
            int, line.split(" ")
        )

        # collect streets
        streets = []
        for _ in range(n_streets):
            line = file.readline()
            i_start, i_end, name, time_length = line.split(" ")
            i_end = int(i_end)
            i_start = int(i_start)
            street = Street(i_start, i_end, name, int(time_length))
            streets.append(street)
            STREETS_DICT[name] = street
            #  streets in
            if INTERSECTIONS.get(int(i_end), None) is None:
                INTERSECTIONS[i_end] = Intersection()
            INTERSECTIONS[i_end].streets_in.append(name)

            # streets out
            if INTERSECTIONS.get(i_start, None) is None:
                INTERSECTIONS[i_start] = Intersection()
            INTERSECTIONS[i_start].streets_out.append(name)

        print(INTERSECTIONS)

        # collect cars
        cars = []
        for _ in range(n_cars):
            line = file.readline()
            n_streets_on_path = int(line.split(" ")[0])
            street_names = tuple(line.split(" ")[1:])
            street_names = [name.replace("\n", "") for name in street_names]
            cars.append(Car(n_streets_on_path, street_names))

    return duration, n_intersections, score_per_car, streets, cars


def submit_results(duration, n_intersections):
    submission = f"{n_intersections}\n"

    for i in range(n_intersections):
        if INTERSECTIONS.get(i, None) is None:
            continue
        submission += f"{i}\n"
        submission += f"{len(INTERSECTIONS[i].streets_in)}\n"
        for street in INTERSECTIONS[i].streets_in:
            time = 1
            submission += f"{street} {time}\n"
    return submission


def main():
    global STREETS_DICT
    global INTERSECTIONS

    duration, n_intersections, score_per_car, streets, cars = extract_data(
        'data/f.txt')

    for car in cars:
        for street_name in car.street_names:
            STREETS_DICT[street_name].car_traffic += 1
            STREETS_DICT[street_name].good_path_metric()

    for i in range(n_intersections):
        if INTERSECTIONS.get(i, None) is None:
            continue
        INTERSECTIONS[i].streets_in.sort(
            reverse=True, key=lambda name: STREETS_DICT[name].metric)

    submission = submit_results(duration, n_intersections)
    with open('results/f.txt', 'w') as file:
        file.write(submission)


if __name__ == '__main__':
    main()
