visited_websites = ['1000110110110011010100001011000011110100011100101000001110000101000110001010010110011100000011010001111101100011010010110110101100010101001101101000001111011011101001101000101000011010011010000101010010101011100010001011001']
fingerprint = '1000110110110011010100001011000011110000011100101000001110000101000110001010010110011100000011010001111101100011010010110110101100010101001101101000001111011011101001101000101000011010011010000101010010101011100010001011001'

threshold = 0.95
for each_website in visited_websites:
    total = 0
    xorval = bin(int(fingerprint, 2)^int(each_website, 2))[2:]
    if (len(xorval)<len(fingerprint)):
        difference = len(fingerprint)-len(xorval)
        xorval = ("0" * difference) + xorval
    for i in xorval:
        # we are forced to use xor but not xnor in this case
        # counting 0 means two digits are the same in xor
        if i == "0":
            total += 1
        
    similarity = float(total)/len(fingerprint)
    print(similarity)
    if similarity > threshold:
        print("True")

print("False")