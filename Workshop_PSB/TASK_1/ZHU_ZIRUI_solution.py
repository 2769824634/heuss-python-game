# This is the content of ZHU_ZIRUI_solution.py file

def ZZR_cal_average(num_list):
    if not num_list: 
        raise ValueError("The list cannot be empty.")
    if not all(isinstance(x, int) for x in num_list): 
        raise ValueError("The list must contain only integers.")
    return round(sum(num_list) / len(num_list), 2)

# Below is an optional testing code block, 
# it's better to move it to a separate file like main.py for testing.

# if __name__ == "__main__":
#     try:
#         average = ZZR_cal_average([2, 6, 8, 3, 4, 6])
#         print(average)  # Should print 4.83
#     except ValueError as e:
#         print(e)