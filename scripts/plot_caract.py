import matplotlib.pyplot as plt
import numpy as np

graph_lp = np.loadtxt('lp.txt')
plt.figure(1)
plt.plot(graph_lp[:, 0], graph_lp[:, 1], '.')
plt.grid(True)
plt.xlabel('coef 2')
plt.ylabel('coef 3')
plt.title('LP')

graph_lpcc = np.loadtxt('lpcc.txt')
plt.figure(2)
plt.plot(graph_lpcc[:, 0], graph_lpcc[:, 1], '.')
plt.grid(True)
plt.xlabel('coef 2')
plt.ylabel('coef 3')
plt.title('LPCC')

graph_mfcc = np.loadtxt('mfcc.txt')
plt.figure(3)
plt.plot(graph_mfcc[:, 0], graph_mfcc[:, 1], '.')
plt.grid(True)
plt.xlabel('coef 2')
plt.ylabel('coef 3')
plt.title('MFCC')

plt.show()