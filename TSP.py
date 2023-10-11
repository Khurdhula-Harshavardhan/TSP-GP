

class TSP():
    number_of_cities = None

    def __init__(self) -> None:
        """
        This constructor, initializes all the fields required for this solution. 
        """
        try:
            self.number_of_cities = int(input("[I/O] Enter the total number of cities: "))

        except Exception as e:
            pass