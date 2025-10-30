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
    if banded_width == -1:  #baseline
        starting_array_val, starting_array_dir = compute_starting_arrays(seq1, seq2, len1, len2, gap, indel_penalty)
        finished_array_val, finished_array_dir = compute_path(starting_array_val, starting_array_dir, len1, len2, match_award, indel_penalty, sub_penalty)
    else:                   #core
        finished_array_val, finished_array_dir = compute_banded_path(seq1, seq2, len1, len2, match_award, indel_penalty, sub_penalty, banded_width)

    print(f"finished array vals for seq1='{seq1}', seq2='{seq2}':")
    for row in finished_array_val:
        # Format each cell to fixed width
        formatted_cells = [f"{str(cell):>4}" for cell in row]
        print(formatted_cells)
    print()

    final_cost = finished_array_val[-1][-1]
    if final_cost == float('inf'):
        return final_cost, None, None

    string1, string2 = traceback(finished_array_dir, len1, len2, gap)
    string1_str = ''.join(string1) if string1 is not None else None
    string2_str = ''.join(string2) if string2 is not None else None

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


def compute_banded_path(seq1, seq2, len1, len2, match_award, indel_penalty, sub_penalty, banded_width):

    if abs(len1 - len2) > banded_width:
        matrix_val = [[float('inf')] * (len1 + 2) for _ in range(len2 + 2)]
        matrix_dir = [[''] * (len1 + 2) for _ in range(len2 + 2)]
        return matrix_val, matrix_dir

    matrix_val = [[float('inf')] * (len1 + 2) for _ in range(len2 + 2)]
    matrix_dir = [[''] * (len1 + 2) for _ in range(len2 + 2)]

    # Header setup
    matrix_val[0][0] = matrix_dir[0][0] = '-'
    matrix_val[0][1] = matrix_dir[0][1] = '-'
    matrix_val[1][0] = matrix_dir[1][0] = '-'
    matrix_val[1][1], matrix_dir[1][1] = 0, 'NA'

    # Initialize sequence headers
    for j in range(len1):
        matrix_val[0][j + 2] = seq1[j]
        matrix_dir[0][j + 2] = seq1[j]
    for i in range(len2):
        matrix_val[i + 2][0] = seq2[i]
        matrix_dir[i + 2][0] = seq2[i]

    # Initialize top-left cells within band
    for j in range(1, min(len1, banded_width) + 1):
        matrix_val[1][j + 1] = j * indel_penalty
        matrix_dir[1][j + 1] = 'L'
    for i in range(1, min(len2, banded_width) + 1):
        matrix_val[i + 1][1] = i * indel_penalty
        matrix_dir[i + 1][1] = 'U'

    # DP within band
    for i in range(1, len2 + 1):
        start_j = max(1, i - banded_width)
        end_j = min(len1, i + banded_width)
        for j in range(start_j, end_j + 1):
            matrix_i = i + 1
            matrix_j = j + 1

            choices = []
            directions = []

            # Diagonal
            if abs(i - j) <= banded_width and matrix_val[matrix_i - 1][matrix_j - 1] != float('inf'):
                score = match_award if seq1[j - 1] == seq2[i - 1] else sub_penalty
                diag = matrix_val[matrix_i - 1][matrix_j - 1] + score
                choices.append(diag)
                directions.append('D')

            # Up
            if abs((i - 1) - j) <= banded_width and matrix_val[matrix_i - 1][matrix_j] != float('inf'):
                up = matrix_val[matrix_i - 1][matrix_j] + indel_penalty
                choices.append(up)
                directions.append('U')

            # Left
            if abs(i - (j - 1)) <= banded_width and matrix_val[matrix_i][matrix_j - 1] != float('inf'):
                left = matrix_val[matrix_i][matrix_j - 1] + indel_penalty
                choices.append(left)
                directions.append('L')

            if not choices:
                continue  # outside band or no valid moves

            min_score = min(choices)
            min_index = choices.index(min_score)
            matrix_val[matrix_i][matrix_j] = min_score
            matrix_dir[matrix_i][matrix_j] = directions[min_index]

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