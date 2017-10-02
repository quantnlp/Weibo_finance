import dict_creat
import suffix_tree

split_mark = "#"

friendly_split_mark = "，"
word_split_mark = "/"

long_word_punishment = 1000


def load(input_file):
    return input_file.read()


def construct_tree(string):
    tree = suffix_tree.SuffixTree(string)
    tree.update_counter()
    return tree

def count_sentence_length(string):
    """
    Count number of sentences for each sentence length.

    :return: count. There are count[i] sentences with length i.
    """
    split_mark = "#"
    sentences = string.split(split_mark)
    length = [len(string) for string in sentences]
    max_length = max(length)

    count = [0]*(max_length+1)
    for l in length:
        count[l] += 1

    return count

def load_dict(dict_file):
    dictionary = dict()
    lines = dict_file.read().split("\n") # load dictionary lines
    count_sum = 0
    for line in lines: # each line in the dict
        if line:
            print(line)
            cols = line.split(",")
            if ((cols[1] == '') | (cols[0] == '')):
                continue
            dictionary[cols[0]] = int(cols[1])*float(cols[-1])
            count_sum += int(cols[1])
    return {key: value/count_sum for key, value in dictionary.items()}

def count_all_possibilities(sentence_length_count, word_length):
        """
        :return: How many combinations are there with length word_length.
        """
        count_sum = 0
        for length, count in enumerate(sentence_length_count):
            if length >= word_length:
                count_sum += count*(length - word_length + 1)
        return count_sum
    
def get_prob(tree, dictionary, sentence_length_count, string):
    """
    Get the probability that string is a word.
    :return: probability
    """
    try:
        current_word_prob = dictionary[string]
    except KeyError:
        current_word_count = tree.query(string).counter
        current_word_prob = current_word_count / count_all_possibilities(sentence_length_count, len(string))

        if current_word_count == 1:
            for i in range(len(string)-1):
                current_word_prob /= long_word_punishment

    return current_word_prob


def split(tree, dictionary, sentence_length_count, string):
    """
    Split string to words.

    :return: words
    """
    prob = [1]  # Probability for the best split
    last_word_index = [0]  # Position for best split of last word

    # Calculate probability
    for i in range(1, len(string)+1):
        max_prob = -1
        max_prob_candidate = None
        for candidate in range(max(0, i-4), i):
            current_word = string[candidate: i]
            current_prob = prob[candidate]*get_prob(tree, dictionary, sentence_length_count, current_word)

            if current_prob > max_prob:
                max_prob = current_prob
                max_prob_candidate = candidate

            # print("[%d:%d]%s/%s:%.10f" % (candidate, i, last_word, current_word, current_prob))

        prob.append(max_prob)
        last_word_index.append(max_prob_candidate)

    # Get result
    result = []
    cursor = len(string)
    while cursor != 0:
        prev = last_word_index[cursor]
        result.append(string[prev: cursor])
        cursor = prev
    return list(reversed(result))


def split_all(tree, dictionary, sentence_length_count, string, out_file, show_progress=True):
    all_list = string.split(split_mark)
    progress_update_interval = len(all_list)//20
    for i, s in enumerate(all_list):
        out_file.write(word_split_mark.join(split(tree, dictionary, sentence_length_count, s)))
        out_file.write(friendly_split_mark)

        if i % progress_update_interval == 1 and show_progress:
            print("|", end="", flush=True)
    if show_progress:
        print()

    out_file.write("\n\n")


def word_split(inFile, dictFile):
    input_file = open(inFile, "r", encoding='utf8')
    dict_file = open(dictFile, "r", encoding='utf8')
    print("Loading dictionary")
    dictionary = load_dict(dict_file)

    print("Building tree")
    string = load(input_file)
    tree = construct_tree(string)
    sentence_length_count = count_sentence_length(string)

    print("Processing")
    output_file_name = inFile.split('.')[0] + "-splitted.txt"
    output_file = open(output_file_name, "w", encoding='utf8')
    split_all(tree, dictionary, sentence_length_count, string, output_file)
    
    return output_file_name

# def test_cursor():
#     tree = construct_tree("banana$")
#     tree.root.visualize()
#     cursor = tree.query_cursor("an")
#     cursor.node.visualize()
#     cursor.current_node.visualize()
#     cursor.move_front_forward()
#     cursor.node.visualize()
#     cursor.current_node.visualize()

