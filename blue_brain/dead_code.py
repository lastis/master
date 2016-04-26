
# upper_y = amps_PC_II_mean + amps_PC_II_std
# upper_x = widths_PC_I_mean + widths_PC_I_std
# lower_y = amps_PC_II_mean - amps_PC_II_std
# lower_x = widths_PC_I_mean - widths_PC_I_std
# # Fill between does not works for specials shapes like these functions.
# # Using a polygon instead. [::-1] reverses the array.
# y = np.hstack((upper_y, lower_y[::-1]))
# x = np.hstack((upper_x, lower_x[::-1]))
# points = np.zeros([len(amps_I_mean) * 2, 2])
# points[:, 0] = x
# points[:, 1] = y
# points = points.tolist()
# patch = plt.Polygon(points,
#                     color=colors[0],
#                     fill=True,
#                     edgecolor=None,
#                     alpha=0.2, )
# ax0.add_patch(patch)
