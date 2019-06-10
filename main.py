from pyeasyga import pyeasyga


def calculate(usb_size, memes):
    """

    :param usb_size: int - capacity of usb stick in GiB
    :param memes: List[Tuple[str, int, int]] - list of 3-element tuples, each with the name, size in MiB , and price
    :return: - Tuple[int, set] a tuple with the first element being the value of the most expensive set of memes
    and the second being the set of names of the memes that should be copied
    onto the USB stick to maximize its value.
    """
    usb_size *= 1024

    def fitness(individual, data):
        """

        :param individual: list - a candidate solution
        :param data: dict of 3-element dict, each with the name, size in MiB, and price
        :return: tuple - first element being int value of the most expensive set of memes and
        the second being the list with used element
        """
        values, weights = 0, 0
        for selected, box in zip(individual, data):
            if selected:
                values += box.get('price')
                weights += box.get('size')
        if weights > usb_size:
            values = 0
        return values

    x = [{'name': memes[i][0], 'price': memes[i][2], 'size': memes[i][1]} for i in range(len(memes))]
    ga = pyeasyga.GeneticAlgorithm(x)
    ga.fitness_function = fitness
    ga.run()
    return ga.best_individual()[0], set([memes[x][0] for x, v in enumerate(ga.best_individual()[1]) if v == 1])
