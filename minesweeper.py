import random

# Ukuran grid dan jumlah ranjau
GRID_SIZE = 6  # Ubah ukuran untuk tingkat kesulitan yang berbeda
NUM_MINES = 4  # Jumlah ranjau

def create_board():
    return [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def place_mines(board):
    mines = random.sample(range(GRID_SIZE * GRID_SIZE), NUM_MINES)
    for mine in mines:
        row, col = divmod(mine, GRID_SIZE)
        board[row][col] = 'X'

def print_board(board):
    print("  " + " ".join(map(str, range(GRID_SIZE))))
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(row))

def count_adjacent_mines(board, row, col):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    mine_count = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == 'X':
            mine_count += 1
    return mine_count

def open_cell(board, display_board, row, col):
    # Jika sel sudah dibuka, hentikan proses
    if display_board[row][col] != ' ':
        return True

    # Jika terkena ranjau, permainan berakhir
    if board[row][col] == 'X':
        return False

    # Gunakan stack untuk proses iteratif
    stack = [(row, col)]

    while stack:
        r, c = stack.pop()

        # Jika sel sudah dibuka, lewati
        if display_board[r][c] != ' ':
            continue

        # Hitung jumlah ranjau di sekitar
        adjacent_mines = count_adjacent_mines(board, r, c)
        display_board[r][c] = str(adjacent_mines) if adjacent_mines > 0 else ' '

        # Jika tidak ada ranjau di sekitar, tambahkan tetangga ke stack
        if adjacent_mines == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and display_board[nr][nc] == ' ':
                    stack.append((nr, nc))

    return True


def check_win(display_board):
    for row in display_board:
        if ' ' in row:
            return False
    return True

def main():
    board = create_board()
    display_board = create_board()
    place_mines(board)

    game_over = False
    while not game_over:
        print_board(display_board)
        try:
            row, col = map(int, input("Masukkan baris dan kolom (contoh: 3 4): ").split())
            if not (0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE):
                print("Koordinat di luar jangkauan. Coba lagi.")
                continue
            if display_board[row][col] != ' ':
                print("Sel sudah dibuka. Coba lagi.")
                continue

            game_over = not open_cell(board, display_board, row, col)
            if check_win(display_board):
                print_board(display_board)
                print("Selamat! Anda menang!")
                return

        except ValueError:
            print("Input tidak valid. Masukkan dua angka, contoh: 3 4.")

    print_board(board)
    print("Permainan berakhir. Anda terkena ranjau!")

if __name__ == "__main__":
    main()
