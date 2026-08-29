s= 'woihfiwe'

freq = {}

strs = ["a"]

for word in strs:
    word  = "".join(sorted(word))
    freq[word] = freq.get(word,0) + 1


print(freq)