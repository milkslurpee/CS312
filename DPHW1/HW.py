def jacks_contiguous_subseq(list_of_nums):
    current_val = 0
    solution = 0
    current_subsequence = []
    final_subsequence = []
    for number in list_of_nums:
        current_val += number
        current_subsequence.append(number)
        if solution < current_val:
            solution = current_val
            final_subsequence = current_subsequence.copy()
        if current_val < 0:
            current_val = 0
            current_subsequence.clear()
    return final_subsequence



def lukes_contiguous_subseq(list_of_nums):
    max_list = []
    max_sum = 0
    i = 0
    while i < len(list_of_nums):
        curr_list = []
        curr_sum = 0
        while curr_sum >= 0 and i < len(list_of_nums):
            curr_list.append(list_of_nums[i])
            curr_sum += list_of_nums[i]
            if curr_sum > max_sum:
                max_sum = curr_sum
                max_list = curr_list.copy()
            i += 1
    return max_list


print(jacks_contiguous_subseq([3, -2, -5, -1, 6, -3, -3, 5, -6, 7, -6, 8, -2, 3, -4]))