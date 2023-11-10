input_word = "FORMULAQSOLUTIONS"
input_len = 16

if input_len % 2 == 0:
    input_len += 1

pyramid_1 = [j for j in range(input_len, 0, -2)][::-1]
pyramid_2 = [j for j in range(input_len, 0, -2)]

bridge_word = " "

increment = 0
j = pyramid_1[increment]

def print_diamond_pattern(word, spaces):
    print(" " * spaces + word)

for i in range(len(input_word)):
    loop_word = ""
    for k in range(i, i + j):
        try:
            loop_word = loop_word + input_word[k]
        except IndexError:
            index = (j + i - k)
            loop_word = loop_word + input_word[:index]
            break
    spaces = len(input_word) - len(loop_word) // 2
    print_diamond_pattern(loop_word, spaces)

    increment += 1
    if increment >= len(pyramid_1):
        bridge_word = loop_word
        break
    j = pyramid_1[increment]

i = 0
loop_word = bridge_word
main_count = increment
increment = 0

for k in range(i + 1, input_len - main_count + 1):
    loop_word = bridge_word[k:len(bridge_word) - k]
    spaces = len(input_word) - len(loop_word) // 2
    print_diamond_pattern(loop_word, spaces)
