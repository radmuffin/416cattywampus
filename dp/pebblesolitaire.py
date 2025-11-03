import functools

@functools.cache
def rMinPieces(board: str):
    left = 0
    mSoFar = len(board)
    for i, x in enumerate(board):
        if x == '-':
            if board[i+1:i+3] == 'oo':
                move = board[:i]+ 'o--' + board[i+3:]
                mSoFar = min(mSoFar, rMinPieces(move))
            if i > 1 and board[i-2:i] == 'oo':
                move = board[:i-2] + '--o' + board[i+1:]
                mSoFar = min(mSoFar, rMinPieces(move))
        else:
            left += 1
    return min(mSoFar, left)

n = int(input())
for _ in range(n):
    start = input()
    print(rMinPieces(start))
