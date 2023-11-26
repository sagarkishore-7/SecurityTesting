'''
TODO:
Write the faulty line numbers and explanations in line1-4 and explanation_line1-4.
line1-4 must be ints. explanation_line1-4 must be strings.
'''

line1 = 17
line2 = 12
line3 = 20
line4 = 23

explanation_line1 = "The bug occurred due to an incorrect initialization error: Instead of 'memory[ptr-1] = 0', the line should be 'memory[ptr] = 0' for proper memory cell initialization."
explanation_line2 = "The bug occurred due to an incorrect initialization error: Instead of 'memory[ptr+1] = 0', the line should be 'memory[ptr] = 0' for proper memory cell initialization."
explanation_line3 = "The bug occurred due to an overflow error: Instead of 'memory[ptr] = (memory[ptr]+1)', the line should be 'memory[ptr] = (memory[ptr]+1) % 256' to make sure that the value stays within the valid range."
explanation_line4 = "The bug occurred due to an underflow error: Instead of 'memory[ptr] = (memory[ptr]-1)', the line should be 'memory[ptr] = (memory[ptr]-1) % 256' to make sure that the value stays within the valid range."
