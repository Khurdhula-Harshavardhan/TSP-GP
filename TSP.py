import random
import matplotlib.pyplot as plt

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


class TSP():
    number_of_cities = None
    distances = None
    population_size = None
    population = None 
    population_fitness = None
    child_population = None
    generations = None
    iterations = None

    def __init__(self) -> None:
        """
        This constructor, initializes all the fields required for this solution. 
        """
        try:
            self.number_of_cities = int(input("[I/O] Enter the total number of cities: ")) #accepts the user input to total number of cities.
            self.status_update("[PROCESS] Initializing random distances to each cities!")
            self.distances = self.get_distance_matrix(self.number_of_cities) #generate random distances between cities.
            self.population_size = int(input("[I/O] Please enter population size: "))
            self.generations = list() #the output of each generation must be stored within this. e
            self.iterations = int(input("[I/O] Please enter the number of iterations you want: "))
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to intialize module params: "+str(e))
        

    def status_update(self, msg) -> None:
        """
        This method, accepts a string from other methods to give a update of current process to user.
        """
        print(msg)


    def get_distance_matrix(self, n) -> list:
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

                    row.append(round(random.uniform(1, n), 4)) #append the distance between two cities.
                matrix.append(row)


            for i in range(len(matrix)):
                for j in range(len(matrix[i])):
                    matrix[j][i] = matrix[i][j]

            self.status_update("[PROCESS] Successfully intialized distances between %d cities."%(n))
            return matrix  
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to create a distance matrix"+str(e))


    def get_population_string(self) -> list:
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
            for i in range(n):
                new_sample = self.get_population_string()
                pop.append(new_sample)
                print(f"\r[PROCESS] Total population created so far:  {round(((i/n)*100),2)}% DONE", end="")
    
            self.status_update("[PROCESS] A new population with size %d has been created successfully!"%(n))
            return pop
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to create population: "+str(e))


    def compute_distance_of_sample(self, instance:list) -> float:
        """
        This accepts a instance from population and then computes the total distance traveled.
        """
        try:
            distance = 0
            for i in range(len(instance) -1):
                j = i + 1
                distance = distance + self.distances[instance[i]][instance[j]]

            distance = distance + self.distances[instance[-1]][instance[0]]

            return round(distance,4)

        except Exception as e:
            self.status_update("[ERR] The following error occured while compute the distance for each sample: "+str(e))

    def create_population_distances(self) -> dict:
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


    def fitness(self, population) -> dict:
        """
        This method will act as a fitness function for us to select, population instances or routes with shorter distances.
        We have a simpler approach, we shall normalize the fitness level of each of the population sample and then return their fitness levels.
        Here we have to compute inverse fitness because shorter paths must have larger fitness values.
        """
        try:
            self.status_update("[PROCESS] Computing fitness values for each of the instance/routes within the population.")
            total_distance = 0
            population_fitnesss = dict()
            for route, distance in population.items():
                total_distance = total_distance + distance

            self.status_update("[PROCESS] Normalizing values for each of the population instance/routes.")

            for route, distance in population.items():
                population_fitnesss[route] = 1 - (distance/total_distance) #gives us invert fitness values!

            self.status_update("[INFO] Fitness values have been created successfully for population samples!")
            return population_fitnesss

        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to compute fitness of each function: "+str(e))

    def roulette_wheel(self) -> dict():
        """
        Roulette wheel generates a random point between 0.0, 1.0 and then selects those routes/population instances with fitness value greater than the generated value.
        """
        try:
            self.status_update("[PROCESS] Spinning roulette wheel on population instances.")
            self.status_update("[PROCESS] Determining random fitness cutoff for population.")

            cut_off = random.uniform(0.000, max(self.population_fitness.values()))
            selected_population = dict()

            for route, fitness_level in self.population_fitness.items():
                if fitness_level>=cut_off:
                    selected_population[route] = fitness_level
            self.status_update("[INFO] Population has been narrowed down to fit population.")
            return selected_population
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to spin roulette wheel over routes: "+str(e))

    def crossover(self, parent_one, parent_two) -> str:
        """
        The crossover method, accepts two parent strings from the population set,
        Then creates a new child instance(route) by combining the information from two parents.
        This resulting child is then returned as the next gen, instance of the population.
        """
        try:
            split_and_convert = lambda lst: [int(s) for s in lst.split(',')]
            parent_one = split_and_convert(parent_one)
            parent_two = split_and_convert(parent_two)
            
            if len(parent_one) != len(parent_two): #inorder to perform crossover we must have parents of same lenght
                raise Exception("Parents are of not same size!")

            random_index = random.randint(0, (len(parent_one)-1))

            child = parent_one[:random_index] + parent_two[random_index:]
            return child 
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to perform crossover for two routes/parents: "+str(e))

    def perform_crossover(self, population_fitness) -> dict:
        """
        The perform_crossover accepts a population with their fitness values defined -> route: fitness.
        The isntances are all of resulting selected instances from roulette wheel selection.
        Upon these we are to perform the crossover by randomly selecting two samples.
        """
        try:
            children = dict()
            self.status_update("[PROCESS] Applying crossover to selected fit population.")
            
            parents = list(population_fitness.keys())
            attempts = random.randint(0, (len(parents)-1))
            for i in range(attempts):
                j = random.randint(0, (len(parents)-1))
                if i == j:
                    continue
                
                child = self.crossover(parent_one= parents[i], parent_two= parents[j])
                distance = self.compute_distance_of_sample(child)
                join_and_convert = lambda lst: ','.join([str(i) for i in lst])
                children[join_and_convert(child)] = distance

            self.status_update("[PROCESS] Created a offspring population of size: "+str(attempts))
            return children
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to apply crossover over selected population: "+str(e))

    def mutate(self, child:str, mutation_rate = 2) -> list:
        """
        The mutate method, is used mutuate a particular instance of a population.
        By default the mutation rate is 2% to maintain diversity and keep the frequency in check.
        """
        try:
            percentage = random.randint(1,100)
            
            split_and_convert = lambda lst: [int(s) for s in lst.split(',')]
            child = split_and_convert(child)
            if percentage>mutation_rate:
                return None
            else:
                i = random.randint(0, (len(child)-1))
                j = random.randint(0, (len(child)-1))

                temp = child[j]
                child[j] = child[i]
                child[i] = temp

            return child
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to mutate a sample: "+str(e))

    def apply_mutation(self, population: dict) -> dict:
        """
        This method applies mutate method to the child population to randomly mutate certain routes.
        """
        try:
            mutated_samples = 0
            mutated_population = dict()
            split_and_convert = lambda lst: [int(s) for s in lst.split(',')]
            join_and_convert = lambda lst: ','.join([str(i) for i in lst])
            self.status_update("[PROCESS] Trying to apply mutation over child population!")
            self.status_update("[PROCESS] The mutation rate is 2%")
            for route, distance in population.items(): 
                result  = self.mutate(route) #try and mutate the sample.
                if result is None:  #check if there is change in route from mutation
                    continue #no mutation occured we do nothing.
                route =  split_and_convert(route)
               
                mutated_samples= mutated_samples + 1 #count mutated values
                new_distance = self.compute_distance_of_sample(result) #compute distance for new route.
                mutated_population[join_and_convert(result)] = new_distance #save the distance for new mutated route.
            self.status_update("[PROCESS] Out of %d from child population a total of %d have undergone mutation."%(len(population), mutated_samples))

            return mutated_population
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to mutate the population: "+str(e))

    def get_population_results(self, population:dict, population_fitness: dict) -> list:
        """
        This method accepts the child population and then computes the following statistics within the entire population:
        1. best route.
        2. best route fitness within it's population.
        3. average fitness of the population.
        4. average distance of the population.
        """
        try:
            self.status_update("[PROCESS] Computing statistics for latest generation please wait.")
            shortest_path = str()
            shortest_distance = max(list(population.values()))
            total_fitness = 0.0
            average_fitness = 0.0
            average_distance = 0.0
            total_distance = 0.0
            n = len(population)
            self.status_update("[PROCESS] Computing best route.")
            self.status_update("[PROCESS] Computing best distance.")
            self.status_update("[PROCESS] Computing best Fitness.")
            for route, distance in population.items():
                total_distance = total_distance + distance
                if shortest_distance>distance:
                    shortest_path = route
                    shortest_distance = distance
                
            for route, fitness in population_fitness.items():
                total_fitness = total_fitness + fitness
                
            best_fitness = population_fitness[route]
            average_distance = total_distance/n
            average_fitness = total_fitness/n

            
            stats = {
                "best_path": shortest_path,
                "best_distance": shortest_distance,
                "best_fitness": best_fitness,
                "average_distance": average_distance,
                "average_fitness": average_fitness
            }

            self.status_update("[PROCESS] Stats for the latest generation are now ready.")        
            return stats
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to compute statistics of the population: "+str(e))

    def plot_best_path_of_all_generations(self, generations):
        """
        Plots the best path across all provided generations.

        :param generations: List of dictionaries containing stats about each generation.
        """
        # Extract the path with the shortest distance from all generations
        best_gen = min(generations, key=lambda x: x["best_distance"])
        best_path = list(map(int, best_gen['best_path'].split(',')))
        
        print("Here's the best path: ", best_path)
        # Extract x and y coordinates from best path for plotting
        x_coords = [i for i, _ in enumerate(best_path)]
        y_coords = best_path

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.plot(x_coords, y_coords, '-o', label=f'Best Path: Distance = {best_gen["best_distance"]:.2f}')
        plt.scatter(x_coords, y_coords, c='red')  # Highlight each city as a point

        plt.title('Best Path Across All Generations')
        plt.xlabel('City Index')
        plt.ylabel('City Order in Path')
        plt.legend()
        plt.grid(True)
        plt.show()


    def plot_best_path_evolution(self, generations):
        """
        Plots the evolution of the best path over the provided generations.

        :param generations: List of dictionaries containing stats about each generation.
        """
        # Extract the best paths and convert them to lists of integers
        best_paths = [list(map(int, gen['best_path'].split(','))) for gen in generations]

        

        # Extract x and y coordinates from best path for plotting
        x_coords = [i for i, _ in enumerate(best_paths[0])]
        y_coords = best_paths

        # Plotting
        plt.figure(figsize=(10, 6))

        for generation, y in enumerate(y_coords):
            plt.plot(x_coords, y, label=f'Generation {generation + 1}')

        plt.title('Best Path Across Generations')
        plt.xlabel('City Index')
        plt.ylabel('City Order in Path')
        plt.legend()
        plt.show()

# Sample usage
# generations = [ { ... }, { ... }, ... ]  # your list of dictionaries
# plot_best_path_evolution(generations)
    def verify_stats(self, stats) -> bool:
        """
        This method varifies if the results of the current generation are valid or not.
        """
        try:
            if stats is None:
                return False
            else:
                if stats["best_path"] == "":
                    return False
                elif stats["best_distance"] == 0:
                    return False
                elif stats["best_fitness"] == 0:
                    return False
                elif stats["average_fitness"] == 0.0:
                    return False
                elif stats["average_distance"] == 0.0:
                    return False
            return True
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to verify results for a generation: "+str(e))

    import matplotlib.pyplot as plt

    def plot_results(self, generations):
        # Extracting values
        gen_numbers = list(range(1, len(generations) + 1))
        best_distances = [gen['best_distance'] for gen in generations]
        average_distances = [gen['average_distance'] for gen in generations]
        
        plt.figure(figsize=(14, 6))
        
        # 1. Best distances over generations
        plt.subplot(2, 2, 1)
        plt.plot(gen_numbers, best_distances, marker='o', linestyle='-', color='b')
        plt.title('Best Distance over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Best Distance')
        plt.grid(True)

        # 2. Average distances over generations
        plt.subplot(2, 2, 2)
        plt.plot(gen_numbers, average_distances, marker='o', linestyle='-', color='r')
        plt.title('Average Distance over Generations')
        plt.xlabel('Generation')
        plt.ylabel('Average Distance')
        plt.grid(True)

        # 3. Histogram of average distances
        plt.subplot(2, 2, 3)
        plt.hist(average_distances, bins=10, color='g', edgecolor='black')
        plt.title('Histogram of Average Distances')
        plt.xlabel('Distance')
        plt.ylabel('Count')

        # 4. Histogram of best distances
        plt.subplot(2, 2, 4)
        plt.hist(best_distances, bins=10, color='c', edgecolor='black')
        plt.title('Histogram of Best Distances')
        plt.xlabel('Distance')
        plt.ylabel('Count')

        plt.tight_layout()
        plt.show()



    def run(self) -> None:
        """
        The run method acts like the driver method for this module/class, kinda like a main function within C.
        """
        try:
            i = 0
            self.population = self.create_population(self.population_size) #create population
            
            while i<self.iterations:
                
                print("-"*100)
                print("\t\t\t\t\t\t Generation %d"%(len(self.generations)+1))
                print("-"*100)
                self.population_distance = self.create_population_distances()  #detemine total distance travelled for a route.
                self.population_fitness = self.fitness(self.population_distance) #call the fitness function on population, by normalizing the fitness for each of the population instance.           
                self.population_fitness = self.roulette_wheel() #performs selection from fitness generated, and then selects fit instances from samples.
                if len(self.population_fitness) == 0:
                    self.status_update("[BREAK] Terminating abruptly because population size is too small!")
                    break
                self.child_population = self.perform_crossover(self.population_fitness) #performs crossover for fit parents in an attempt to create new children that are better.
                if len(self.child_population) == 0:
                    self.status_update("[BREAK] Terminating abruptly because population size is too small!")
                    break
                self.child_population.update(self.apply_mutation(self.child_population)) #apply mutation over this new population.
                self.child_fitness = self.fitness(self.child_population)
                stats = self.get_population_results(self.child_population, self.child_fitness)
                
                
                
                if self.verify_stats(stats=stats):
                    self.generations.append(stats)
                    i = i + 1
                else:
                    i=i-1 #recompute the results again.
                self.population_distance = self.child_population
                self.status_update("[INFO] Current child population shall become ordinary population for next generation.\n\n")
                clear_screen()
            
            self.plot_best_path_evolution(self.generations)
            self.plot_results(self.generations)
            self.plot_best_path_of_all_generations(self.generations)
        except Exception as e:
            self.status_update("[ERR] The following error occured while trying to run the module: "+str(e))


obj = TSP()
obj.run()

