from hashlib import sha224

def simhash(word_frequency_dict):
    '''takes in the word frequency dict and output a binary vector for the ID of the website'''
    bin_length = 256
    total_vector = [0] * bin_length
    for word, frequency in word_frequency_dict.items():
        one_vector = list()
        hash_val = bin(int(sha224(word.encode("utf-8")).hexdigest(), 16))[2:(bin_length+2)]
        hash_len = len(hash_val)
        
        if (hash_len<bin_length):
            difference = bin_length - hash_len
            hash_val = ("0" * difference) + hash_val

        for binary in hash_val:
            if binary == "0":
                one_vector.append(-1*word_frequency_dict[word])
            else:
                one_vector.append(word_frequency_dict[word])
        
        for indx in range(len(total_vector)):
            total_vector[indx] += one_vector[indx]
    binary_vector = []
    for i in total_vector:
        if i>0:
            binary_vector.append(1)
        else:
            binary_vector.append(0)       
            
    return binary_vector
  
tokens = {
    "d": 2,
    "asdf": 2,
    "hi": 1,
    "found": 1,
    "pie": 1,
    "ll": 4,
    "a" : 1,
    "bn" : 1
}
print(simhash(tokens))