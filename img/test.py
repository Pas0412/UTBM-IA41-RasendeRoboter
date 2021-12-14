import os
for i in os.listdir():
	os.system(f"convert -bordercolor black -border 2 {i} {i}")
	print(i)

