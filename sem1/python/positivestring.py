words=input("Enter a string:")
word_list=list(map(str,words.split()))
positive_words=['good','great','nice','happy']
negative_words=['bad','worst','sad']
if words in positive_words:
	print("Positive words")
elif words in negative_words:
	print("Negative words") 
