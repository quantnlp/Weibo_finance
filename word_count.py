word_split_mark = "/"
split_mark = "，"

counter = dict()

def word_count(fileIn):
    print("\nCounting words")
    input_file = open(fileIn, "r", encoding='utf8')
    output_file_name = fileIn.split('.')[0] + "-count.txt"
    output_file = open(output_file_name, "w", encoding='utf8')
    
    # Split words
    string = input_file.read()
    string = ''.join(string.split("\n"))

    string = word_split_mark.join(string.split(split_mark))
    words = string.split(word_split_mark)

    # Count words
    for word in words:
        if word in counter:
            counter[word] += 1
        else:
            counter[word] = 1

    # Sort words
    table = list(counter.items())
    table.sort(key=lambda x: x[1], reverse=True)

    # Save result
    for row in table:
        if len(row[0]) > 1:
            output_file.write("%s,%d\n" % (row[0], row[1]))
            
    print("\n Finished word counting")