import pickle

# open a file, where you stored the pickled data
file = open(fr"C:\Users\Liat\Documents\tof_flight_scan_12.p", "rb")

# dump information to that file
data = pickle.load(file)

# close the file
#file.close()

print(f'Showing the pickled data: {data}')
