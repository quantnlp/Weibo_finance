import suffix_tree
import copy
import math
import time

# Threshold for filters
MIN_COUNT = 5
MIN_ENTROPY = 2.
MIN_SCORE = 200.
MIN_CO = 2.

split_mark = "#"
word_split_mark = "/"

def load(input_file):
    return input_file.read()


def construct_tree(string):
    tree = suffix_tree.SuffixTree(string + "$")
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


def count_all_possibilities(sentence_length_count, word_length):
    """
    :return: How many combinations are there with length word_length.
    """
    count_sum = 0
    for length, count in enumerate(sentence_length_count):
        if length >= word_length:
            count_sum += count*(length - word_length + 1)
    return count_sum


def new_cursor(tree, branch):
    return suffix_tree.Cursor(tree.root, branch, 0, tree.root)


def entropy_of_list(nodes):
    """
    Calculate entropy from a list of nodes.

    :return: entropy.
    """
    node_counts = [node.counter if str(node)[0] != split_mark else 1.
                   for node in nodes]
    count_sum = sum(node_counts)
    probs = [count/count_sum for count in node_counts]

    entropy = -sum([prob*math.log(prob, 2) for prob in probs])

    for node in nodes:
        if str(node)[0] == split_mark \
              and node.counter >= 0.5 * count_sum + node.counter - 1:
            return max(entropy, MIN_ENTROPY + 0.00001)

    return entropy


def mark_words(tree, reversed_tree, count_of_length, cursor, string, output_file):
    if split_mark in string:
        return

    if cursor.current_node.counter >= MIN_COUNT:  # Filter by count
        if len(string) > 1:
            # Calculate co
            p_no_split = cursor.current_node.counter/count_of_length[len(string)]

            left_part = new_cursor(tree, string[0])
            right_part = copy.copy(cursor)
            right_part.move_front_forward(string[0])
            p_split = []
            for i in range(1, len(string)):
                p_left = left_part.current_node.counter/count_of_length[i]
                p_right = right_part.current_node.counter/count_of_length[len(string) - i]
                p_split.append(p_left*p_right)

                if i != len(string) - 1:
                    left_part.move_forward(string[i])
                    right_part.move_front_forward(string[i])
            # End of for i in range(1, len(string))

            co = p_no_split/max(p_split)

            if co >= MIN_CO:  # Filter by co
                # Calculate entropy
                reverse_lookup = reversed_tree.query_cursor(string[::-1])
                if reverse_lookup.length + 1 == len(reverse_lookup.current_node):
                    left_entropy = entropy_of_list(reverse_lookup.current_node.next.values())
                else:
                    left_entropy = 0
                right_entropy = entropy_of_list(cursor.current_node.next.values())

                # Calculate score
                score = co*(left_entropy+right_entropy)

                # Filter by score and entropy
                if score > MIN_SCORE and left_entropy > MIN_ENTROPY and right_entropy > MIN_ENTROPY:
#                    print("Write to dictionary")
                    output_file.write("%s,%d,%f,%f,%f,%f,%f\n" % (string, cursor.current_node.counter, co, left_entropy, right_entropy, left_entropy+right_entropy, score))
            # End of if co >= MIN_CO
        # End of if len(string) > 1

        # Recursively find vocabulary in child nodes
        for key, child in cursor.current_node.next.items():
            next_cursor = suffix_tree.Cursor(cursor.current_node, key, len(child), tree.root)
            mark_words(tree, reversed_tree, count_of_length, next_cursor, string + str(next_cursor.current_node), output_file)
    # End of if cursor.current_node.counter >= MIN_COUNT
# End of def mark_words


def build_dictionary(inFile):
    t0 = time.time()
#    inFile = "D:/NLP/tonghuashun-short.txt"
    input_file = open(inFile, "r", encoding='utf8')
    output_file_name = inFile.split('.')[0] + "-dict.txt"
    output_file = open(output_file_name, "w", encoding='utf8')

    string = load(input_file)
    print("Building tree")
    tree = construct_tree(string)
    print("Building tree for reversed string")
    reversed_tree = construct_tree(string[::-1])

    print("Counting sentences")
    sentence_length_count = count_sentence_length(string)
    count_of_length = [count_all_possibilities(sentence_length_count, i)
                       for i in range(len(sentence_length_count))]

    print("Finding words")
    process_update_interval = len(tree.root.next)//20
    for i, (key, child) in enumerate(tree.root.next.items()):
        if i % process_update_interval == 1:
            print("|", end="", flush=True)
        if i%10 == 0:
            print("working on " + str(i) + " of " + str(len(tree.root.next.items())))
            
        cursor = suffix_tree.Cursor(tree.root, key, len(child), tree.root)
        mark_words(tree, reversed_tree, count_of_length, cursor, str(cursor.current_node), output_file)
    print()
    
    t1 = time.time()
    print(t1-t0) 
    
    return output_file_name
