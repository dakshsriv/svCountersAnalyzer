from matplotlib import pyplot as plt
names = ['group_a', 'group_b', 'group_c']
values = [1, 10, 100]

plt.figure(figsize=(9, 3))

"""plt.subplot(131)
plt.bar(names, values)"""
"""plt.subplot(132)
plt.scatter(names, values)"""
# Above four lines are for bar and scatter plots
# Next two lines are for line graph
plt.subplot(133)
plt.plot(names, values)
plt.suptitle('Categorical Plotting')
plt.show()

