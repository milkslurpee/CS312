def align(
        seq1: str,
        seq2: str,
        match_award=-3,
        indel_penalty=5,
        sub_penalty=1,
        banded_width=-1,
        gap_open_penalty=0,
        gap='-',
) -> tuple[float, str | None, str | None]:
    """
        Align seq1 against seq2 using Needleman-Wunsch
        Put seq1 on left (j) and seq2 on top (i)
        => matrix[i][j]
        :param seq1: the first sequence to align; should be on the "left" of the matrix
        :param seq2: the second sequence to align; should be on the "top" of the matrix
        :param match_award: how many points to award a match
        :param indel_penalty: how many points to award a gap in either sequence
        :param sub_penalty: how many points to award a substitution
        :param banded_width: banded_width * 2 + 1 is the width of the banded alignment; -1 indicates full alignment
        :param gap_open_penalty: how much it costs to open a gap. If 0, there is no gap_open penalty
        :param gap: the character to use to represent gaps in the alignment strings
    """
    len1 = len(seq1)
    len2 = len(seq2)
    starting_array_val, starting_array_dir = compute_starting_arrays(seq1, seq2, len1, len2, gap, indel_penalty)
    print(f"Starting array values for seq1='{seq1}', seq2='{seq2}':")
    for row in starting_array_val:
        # Format each cell to fixed width
        formatted_cells = [f"{str(cell):>4}" for cell in row]
        print(formatted_cells)
    print()

    finished_array_val, finished_array_dir = compute_path(starting_array_val, starting_array_dir, len1, len2, match_award, indel_penalty, sub_penalty)

    print(f"finished array vals for seq1='{seq1}', seq2='{seq2}':")
    for row in finished_array_val:
        # Format each cell to fixed width
        formatted_cells = [f"{str(cell):>4}" for cell in row]
        print(formatted_cells)
    print()

    string1, string2 = traceback(finished_array_dir, len1, len2, gap)
    string1_str = ''.join(string1) if string1 is not None else None
    string2_str = ''.join(string2) if string2 is not None else None

    final_cost = finished_array_val[-1][-1]


    print(final_cost, '\n')
    print(string1_str, '\n')
    print(string2_str, '\n')
    return final_cost, string1_str, string2_str


def compute_starting_arrays(seq1, seq2, len1, len2, gap, indel_penalty):
    matrix_val = [[''] * (len1 + 2) for _ in range(len2 + 2)]
    matrix_dir = [[''] * (len1 + 2) for _ in range(len2 + 2)]
    matrix_val[0][0], matrix_dir[0][0] = gap, gap
    matrix_val[0][1], matrix_dir[0][1] = gap, gap
    matrix_val[1][0], matrix_dir[1][0] = gap, gap
    matrix_val[1][1], matrix_dir[1][1] = 0, 'NA'
    insert_val_j = 0
    insert_val_i = 0
    for j in range(len1):
        insert_val_j += indel_penalty
        matrix_val[0][j+2], matrix_dir[0][j+2] = seq1[j], seq1[j]
        matrix_val[1][j+2], matrix_dir[1][j+2] = insert_val_j, 'L'
    for i in range(len2):
        insert_val_i += indel_penalty
        matrix_val[i+2][0], matrix_dir[i+2][0] = seq2[i], seq2[i]
        matrix_val[i+2][1], matrix_dir[i+2][1] = insert_val_i, 'U'
    return matrix_val, matrix_dir

def compute_path(matrix_val, matrix_dir, len1, len2, match_award, indel_penalty, sub_penalty):
    for i in range(len2):
        for j in range(len1):
            choices = []
            if matrix_val[0][j+2] == matrix_val[i+2][0]:
                Diagonal = matrix_val[i+1][j+1] + match_award
            else:
                Diagonal = matrix_val[i+1][j+1] + sub_penalty
            choices.append(Diagonal)
            Above = matrix_val[i+1][j+2] + indel_penalty
            choices.append(Above)
            Left = matrix_val[i+2][j+1] + indel_penalty
            choices.append(Left)
            min_score = min(choices)
            if min_score == Diagonal:
                matrix_val[i+2][j+2] = Diagonal
                matrix_dir[i+2][j+2] = 'D'
            elif min_score == Above:
                matrix_val[i+2][j+2] = Above
                matrix_dir[i+2][j+2] = 'U'
            elif min_score == Left:
                matrix_val[i+2][j+2] = Left
                matrix_dir[i+2][j+2] = 'L'
    return matrix_val, matrix_dir


def traceback(matrix_dir, len1, len2, gap):
    string1 = []
    string2 = []

    i, j = len2 + 1, len1 + 1
    while i > 1 or j > 1:
        if matrix_dir[i][j] == 'D':
            string1.append(matrix_dir[0][j])
            string2.append(matrix_dir[i][0])
            i -= 1
            j -= 1
        elif matrix_dir[i][j] == 'U':
            string1.append(gap)
            string2.append(matrix_dir[i][0])
            i -= 1
        elif matrix_dir[i][j] == 'L':
            string1.append(matrix_dir[0][j])
            string2.append(gap)
            j -= 1
        else:
            string1.append(gap)
            string2.append(gap)
            i -= 1
            j -= 1
    string1.reverse()
    string2.reverse()
    return string1, string2



# Test with longer sequences
align("ACGTACGT", "ACGTTG")