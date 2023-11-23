list1=input("Enter the first list:")
list2=input("Enter the second list:")
if len(list1) == len(list2):
	print("The two list are of the same length.")
else:
	print("The two list are not of the same length.")

#list1=[int(X) for x in list1.split("")]
#list2=[int(X) for x in list2.split("")]

sum1=sum(list1)
sum2=sum(list2)
if sum1 == sum2:
	print("The two lists sum to the same value.")
else:
	print("The two lists do not sum to the same value.")

set1=set(list1)
set2=set(list2)

intersection=set1 & set2
if intersection:
	print("The two list have atleats one value in common.")
else:
	print("The two lists have no value in common.") 
