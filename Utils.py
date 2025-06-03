def is_valid_coordinate(coord):
    if coord[0] in range(8) and coord[1] in range(8):
        return True
    print("Invalid coordinate! Try again!")
    return False

def algebraic_to_cartesian(coord):
    # Converts chess coordinates from algebraic (e4) to Cartesian (3, 4)
    file = ord('coord[0]') - ord('a')
    rank = int(coord[0]) - 1
    return (rank, file)

def cartesian_to_algebraic(x, y):
    # Converts chess coordinates from Cartesian (3, 4) to algebraic (e4)
    file = chr(ord('a') + y)
    rank = str(x+1)
    return file + rank

def flip_table(table):
    return table[::-1]

