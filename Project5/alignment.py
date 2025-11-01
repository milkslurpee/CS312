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
    if banded_width == -1:  # baseline
        starting_array_val, starting_array_dir = compute_starting_arrays(seq1, seq2, len1, len2, gap, indel_penalty)
        finished_array_val, finished_array_dir = compute_path(starting_array_val, starting_array_dir, len1, len2,
                                                              match_award, indel_penalty, sub_penalty)
        final_cost = finished_array_val[-1][-1]

        if final_cost == float('inf'):
            return final_cost, None, None

        string1, string2 = traceback(
            seq1, seq2, finished_array_dir, len1, len2, gap
        )

    else:  # core - MODIFIED to use compact banded matrix
        # compute_banded_path now returns the compact matrix and the col_index function
        finished_array_val, finished_array_dir, col_index = compute_banded_path(seq1, seq2, len1, len2, match_award, indel_penalty,
                                                                sub_penalty, banded_width)

        band = banded_width

        # Calculate final cost
        if abs(len1 - len2) <= band:
            col = col_index(len2, len1)
            # The bottom-right cell is matrix_val[len2][col]
            final_cost = finished_array_val[len2][col]
        else:
            # This path is hit if the early exit in compute_banded_path didn't catch it
            final_cost = float('inf')

        if final_cost == float('inf'):
            return final_cost, None, None

        # Call the banded traceback function
        band = banded_width
        string1, string2 = traceback(
            seq1, seq2, finished_array_dir, len1, len2, gap,
            banded=True,
            col_index=(lambda i, j: j - (i - band)),
            band=band
        )

    string1_str = ''.join(string1) if string1 is not None else None
    string2_str = ''.join(string2) if string2 is not None else None

    # print(final_cost, '\n')
    # print(string1_str, '\n')
    # print(string2_str, '\n')
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
        matrix_val[0][j + 2], matrix_dir[0][j + 2] = seq1[j], seq1[j]
        matrix_val[1][j + 2], matrix_dir[1][j + 2] = insert_val_j, 'L'
    for i in range(len2):
        insert_val_i += indel_penalty
        matrix_val[i + 2][0], matrix_dir[i + 2][0] = seq2[i], seq2[i]
        matrix_val[i + 2][1], matrix_dir[i + 2][1] = insert_val_i, 'U'
    return matrix_val, matrix_dir


def compute_path(matrix_val, matrix_dir, len1, len2, match_award, indel_penalty, sub_penalty):
    for i in range(len2):
        for j in range(len1):
            choices = []
            if matrix_val[0][j + 2] == matrix_val[i + 2][0]:
                Diagonal = matrix_val[i + 1][j + 1] + match_award
            else:
                Diagonal = matrix_val[i + 1][j + 1] + sub_penalty
            choices.append(Diagonal)
            Above = matrix_val[i + 1][j + 2] + indel_penalty
            choices.append(Above)
            Left = matrix_val[i + 2][j + 1] + indel_penalty
            choices.append(Left)
            min_score = min(choices)
            if min_score == Diagonal:
                matrix_val[i + 2][j + 2] = Diagonal
                matrix_dir[i + 2][j + 2] = 'D'
            elif min_score == Above:
                matrix_val[i + 2][j + 2] = Above
                matrix_dir[i + 2][j + 2] = 'U'
            elif min_score == Left:
                matrix_val[i + 2][j + 2] = Left
                matrix_dir[i + 2][j + 2] = 'L'
    return matrix_val, matrix_dir


def compute_banded_path(seq1, seq2, len1, len2, match_award, indel_penalty, sub_penalty, banded_width):
    """
    Compute the banded Needleman-Wunsch dynamic programming matrix.

    Only cells where |i - j| <= banded_width are computed to save time and space.
    Returns:
        matrix_val: 2D list of DP costs (shape = [len2+1][2*band+1])
        matrix_dir: 2D list of directions ('D', 'U', 'L', 'NA')
        col_index:  dummy lambda (for compatibility with caller)
    """

    INF = float('inf')
    band = banded_width
    band_width = 2 * band + 1  # number of columns per row

    # ---------------------------
    # 0. Early Exit: impossible alignment
    # ---------------------------
    if abs(len1 - len2) > band:
        dummy_val = [[INF] * band_width for _ in range(len2 + 1)]
        dummy_dir = [[''] * band_width for _ in range(len2 + 1)]
        dummy_col_index = lambda i, j: 0  # compatibility
        return dummy_val, dummy_dir, dummy_col_index

    # ---------------------------
    # 1. Initialize DP Matrices
    # ---------------------------
    matrix_val = [[INF] * band_width for _ in range(len2 + 1)]
    matrix_dir = [[''] * band_width for _ in range(len2 + 1)]

    # ---------------------------
    # 2. Initialize Top-left Corner
    # ---------------------------
    center_col = band  # main diagonal (i == j)
    matrix_val[0][center_col] = 0
    matrix_dir[0][center_col] = 'NA'

    # ---------------------------
    # 3. Initialize First Row (i = 0)
    # ---------------------------
    for j in range(1, min(len1, band) + 1):
        col = j - (0 - band)  # inline col_index(0, j)
        matrix_val[0][col] = j * indel_penalty
        matrix_dir[0][col] = 'L'

    # ---------------------------
    # 4. Initialize First Column (j = 0)
    # ---------------------------
    for i in range(1, min(len2, band) + 1):
        col = 0 - (i - band)  # inline col_index(i, 0)
        matrix_val[i][col] = i * indel_penalty
        matrix_dir[i][col] = 'U'

    # ---------------------------
    # 5. Main DP Loop
    # ---------------------------
    for i in range(1, len2 + 1):
        j_start = max(1, i - band)
        j_end = min(len1, i + band)

        for j in range(j_start, j_end + 1):
            col = j - (i - band)  # inline col_index(i, j)

            if not (0 <= col < band_width):
                continue  # skip if outside the band

            best_cost = INF
            best_dir = ''

            # --- Diagonal (Match/Mismatch) ---
            if j > 0 and abs((j - 1) - (i - 1)) <= band:
                diag_col = (j - 1) - ((i - 1) - band)
                if 0 <= diag_col < band_width:
                    diag_score = match_award if seq1[j - 1] == seq2[i - 1] else sub_penalty
                    cost_diag = matrix_val[i - 1][diag_col] + diag_score
                    if cost_diag < best_cost:
                        best_cost = cost_diag
                        best_dir = 'D'

            # --- Up (Gap in seq1) ---
            if abs(j - (i - 1)) <= band:
                up_col = j - ((i - 1) - band)
                if 0 <= up_col < band_width:
                    cost_up = matrix_val[i - 1][up_col] + indel_penalty
                    if cost_up < best_cost:
                        best_cost = cost_up
                        best_dir = 'U'

            # --- Left (Gap in seq2) ---
            if j > 0 and abs((j - 1) - i) <= band:
                left_col = (j - 1) - (i - band)
                if 0 <= left_col < band_width:
                    cost_left = matrix_val[i][left_col] + indel_penalty
                    if cost_left < best_cost:
                        best_cost = cost_left
                        best_dir = 'L'

            # Store result
            matrix_val[i][col] = best_cost
            matrix_dir[i][col] = best_dir

    # ---------------------------
    # 6. Return Results
    # ---------------------------
    # Return dummy lambda to preserve original function signature compatibility
    return matrix_val, matrix_dir, (lambda i, j: j - (i - band))



def traceback(seq1, seq2, matrix_dir, len1, len2, gap, banded=False, col_index=None, band=None):
    string1, string2 = [], []

    # Start from bottom-right corner
    i, j = len2, len1

    while i > 0 or j > 0:
        # Determine direction cell
        if banded:
            if col_index is None or band is None:
                raise ValueError("banded=True requires col_index and band arguments")
            col = col_index(i, j)
            if col < 0 or col >= 2 * band + 1:
                break
            direction = matrix_dir[i][col]
        else:
            direction = matrix_dir[i + 1][j + 1]

        # Follow traceback path
        if direction == 'D':
            string1.append(seq1[j - 1])
            string2.append(seq2[i - 1])
            i -= 1
            j -= 1
        elif direction == 'U':
            string1.append(gap)
            string2.append(seq2[i - 1])
            i -= 1
        elif direction == 'L':
            string1.append(seq1[j - 1])
            string2.append(gap)
            j -= 1
        elif direction == 'NA':
            break
        else:
            break  # should not happen in a valid matrix

    string1.reverse()
    string2.reverse()
    return string1, string2
