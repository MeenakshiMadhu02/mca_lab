num_rows=9
for i in range(1, num_rows + 1):
	num_stars=min(i, num_rows - i + 1):
	for j in range(num_stars):
		print("*",end=" ")
	print()
