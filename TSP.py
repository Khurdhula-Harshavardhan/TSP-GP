import random

class TSP():
    number_of_cities = None
    distances = None
    population_size = None
    population = None 

    def __init__(self) -> None:
        """
        This constructor, initializes all the fields required for this solution. 
        """
        try:
            self.number_of_cities = int(input("[I/O] Enter the total number of cities: ")) #accepts the user input to total number of cities.
            self.status_update("[PROCESS] Initializing random distances to each cities!")
            self.distances = self.get_distance_matrix(self.number_of_cities) #generate random distances between cities.
            self.population_size = int(input("[I/O] Please enter population size: "))
            for row in self.distances:
                print(row)
            self.population = self.create_population(self.population_size) #create population
            print(self.population)
            print(self.create_population_distances())

            
            
            
            


        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to intialize module params: "+str(e))
        

    def status_update(self, msg) -> None:
        """
        This method, accepts a string from other methods to give a update of current process to user.
        """
        print(msg)


    def get_distance_matrix(self, n) -> [[]]:
        """
        This method generates a distance matrix for n cities.
        """
        try:
            matrix = list()
            self.status_update("[PROCESS] Initializing distances between %d cities"%(n))
            for i in range(n):
                row = list()
                for j in range(n):
                    if i == j :
                        row.append(0) #distance from a city to itself is zero!
                        continue

                    row.append(round(random.uniform(1, n), 2)) #append the distance between two cities.
                matrix.append(row)


            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    matrix[j][i] = matrix[i][j]

            self.status_update("[PROCESS] Successfully intialized distances between %d cities."%(n))
            return matrix  
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to create a distance matrix"+str(e))


    def get_population_string(self) -> list():
        """
        This method creates a instance for the population and returns it to the calling method.
        """
        try:
            string = list()

            while len(string) != self.number_of_cities:
                value = random.randint(0, (self.number_of_cities - 1))
                if value not in string:
                    string.append(value)
                else:
                    continue

            return string
        except Exception as e:
            pass

    def create_population(self, n) -> [[]]:
        """
        This method, accepts size of total population to be created,
        then creates each instance of population using "get_population_string" and returns the entire population created.
        """
        try:
            pop = list()
            self.status_update("[PROCESS] Creating population with size %d"%(n))
            for _ in range(n):
                new_sample = self.get_population_string()
                pop.append(new_sample)

            self.status_update("[PROCESS] A new population with size %d has been created successfully!"%(n))
            return pop
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to create population: "+str(e))


    def compute_distance_of_sample(self, instance) -> int():
        """
        This accepts a instance from population and then computes the total distance traveled.
        """
        try:
            distance = 0
            for i in range(len(instance) -1):
                j = i + 1
                distance = distance + self.distances[instance[i]][instance[j]]

            distance = distance + self.distances[instance[-1]][instance[0]]

            return round(distance,2)

        except Exception as e:
            self.status_update("[ERR] The following error occured while compute the distance for each sample: "+str(e))

    def create_population_distances(self) -> dict():
        """
        Computes distances for each sample within entire population:
        """
        try:
            self.status_update("[PROCESS] Trying to compute distances using population samples!")
            sample_distance = dict()
            join_and_convert = lambda lst: ','.join([str(i) for i in lst])
            for sample in self.population:
                distance = self.compute_distance_of_sample(sample)
                sample_distance[join_and_convert(sample)] = distance
            
            return sample_distance
        
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to compute distances for population samples: "+str(e))

    


obj = TSP()
