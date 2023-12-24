import random
import time
import matplotlib.pyplot as plt
from k_shortest_path import shortest_k_path
from memory_profiler import memory_usage
from makeD import makeD



def test_shortest_k_path():
    if __name__ == '__main__':

        # Initialize lists to collect data
        input_sizes = []
        execution_times = []
        memory_usages = []    
        def_times = []
        def_usages = []

        # Test the code with different input sizes and values of k
        for n in range(10 , 100, 10):  # Test with different input sizes from 10 to 100
            k = 3 #random.randint(2, n)
            points = generate_synthetic_example(n)  
            D = makeD(points)  

            # Measure execution time
            start_time = time.time()
            minDist, shortestPath = shortest_k_path(D, k) 
            end_time = time.time()
            execution_time = end_time - start_time    

            # Measure defult time and mem usage
            def_start_time = time.time()
            defult_time_execution(n, k) 
            def_end_time = time.time()
            def_execution_time = def_end_time - def_start_time  
            def_times.append(def_execution_time)
            def_mem_usage = memory_usage((defult_mem_usage, (n,k), {}), max_usage=True)
            def_usages.append(def_mem_usage)


            # Collect memory usage data from memory-profiler output
            mem_usage = memory_usage((shortest_k_path, (D,k), {}), max_usage=True)


            # Append data to the lists
            input_sizes.append(n)
            execution_times.append(execution_time)
            memory_usages.append(mem_usage)    



        # Plot execution time
        plt.figure('Execution Time')
        plt.plot(input_sizes, execution_times, label='Execution Time')
        plt.plot(input_sizes, def_times, label='kn^2 Time')
        plt.xlabel('Input Size')
        plt.ylabel('Time (s)')
        plt.legend()
        plt.title('Execution Time vs. Input Size')

        # Plot memory usage
        plt.figure('Memory Usage')
        plt.plot(input_sizes, memory_usages, label='Memory Usage')  
        plt.plot(input_sizes, def_usages, label='kn Memory Usage')  
        plt.xlabel('Input Size')
        plt.ylabel('Memory (MB)')
        plt.legend()
        plt.title('Memory Usage vs. Input Size')
        plt.show()    


# unction to generate synthetic examples of vectors represent nodes
def generate_synthetic_example(n):
    points = [(i,random.randint(-999, 999)) for i in range(n)]
    return points

def defult_time_execution(n, k):
    x = 0
    for i in range(n*n*k*3):
        x += 1
def defult_mem_usage(n, k):
    x = [[i for i in range(n*k)]]
    x[0] = 1


test_shortest_k_path()

