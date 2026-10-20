# Experiment 10: average time and throughput from three runs
import sys

size_bytes = int(sys.argv[1])
times = [float(t) for t in sys.argv[2:]]

average = sum(times) / len(times)
throughput = (size_bytes / 1024) / average
print("Runs         :", ", ".join("{:.4f} s".format(t) for t in times))
print("Average time : {:.4f} s".format(average))
print("Throughput   : {:.2f} KB/s".format(throughput))
