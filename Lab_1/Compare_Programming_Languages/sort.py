import time

def insertionSort(li):
	for i in range(0, len(li)-1):
		j = i+1
		while j>=1:
			if li[j]<li[j-1]:
				temp = li[j]
				li[j] = li[j-1]
				li[j-1] = temp
			else:
				break
			j -=1
	return li

def readInput():
	return [int(x) for x in input().split(" ")]

def printOutput(res):
	print(' '.join(map(str, res)))

if __name__ == '__main__':
	li = [72, 94, 88, 62, 83, 33, 82, 92, 65, 54, 78, 49, 92, 16, 17, 70, 63, 23, 100, 16, 5, 94, 12, 23, 46, 96, 13, 14, 68, 34, 98, 90, 29, 58, 82, 68, 34, 5, 75, 76, 84, 10, 74, 68, 12, 15, 10, 30, 42, 6, 52, 44, 54, 85, 54, 27, 4]
	for _ in range(0, 10):
		li.extend(li)
	insertion_start = time.time()
	res1 = insertionSort(li)
	insertion_end = time.time()	