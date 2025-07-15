# inventory_search.py

# Potential improvements:
# - Create an inventory class to encapsulate the inventory logic. (MAJOR - other improvements are dependent on this.)
# - Allow for different objects with unique maximum stack sizes.
# - Add more detailed logging and error handling.
# - Add a command-line interface for easier interaction and solving other problems.

# Brief description of Minecraft inventories:
# In Minecraft, an inventory is a grid of slots where players can store items. Each slot can hold a certain number of items, with most items having a maximum stack size of 64.
# The inventory typically consists of 36 slots, but one may wish to simulate fewer for other constraints.
# When the inventory is open, players have an "active" cursor that can hold items and move them around.
# When the cursor is empty:
    # Right-clicking on an inventory slot takes half of the items in that slot (rounded up) and moves them to the cursor.
    # Left-clicking on an inventory slot moves all items in that slot to the cursor.
    # Drag right- and left-clicking does nothing.
# When the cursor is not empty:
    # Right-clicking on an inventory slot adds one item to that slot from the cursor, if the slot is not full.
    # Left-clicking on an inventory slot moves all items from the cursor to that slot, up to the maximum stack size.
    # Drag right-clicking on empty slots adds one item to each of those slots from the cursor.
    # Drag left-clicking on empty slots moves all items from the cursor to those slots, distributing them evenly.

# This program simulates the inventory mechanics to find the minimum number of clicks required to fill an inventory from an empty state, given a starting point where one slot is full.
# For some reason this problem has been bouncing around my head for a while, so I decided to solve it computationally rather than combinatorially, though I'm sure there is interesting combinatorics to be had.
# These comments are extremely not PEP 8, huh.

import ast
from tqdm import tqdm

INVENTORY_SIZE = 36 # Size of inventory (36 in Minecraft).
MAX_STACK = 64 # Maximum stack size for items in the inventory.
MAX_CLICKS = 20 # Purely a safety limit to prevent infinite loops.

# If false the program will not store the 'history' of the computation.
PARTIAL_COMPUTATION_STORAGE = True


def empty_space(inv, full_inds=False):
    if full_inds:
        return [i for i, v in enumerate(inv) if not v]
    return inv.count(0)


def click_right(inv, act, ind, max_stack=MAX_STACK):
    'Returns a new inventory and the size of the active slot after clicking right on inventory slot index ind.'
    inv_out = inv.copy()
    if act and inv_out[ind] < max_stack:
        inv_out[ind] += 1
        return inv_out, act - 1
    elif act:
        return inv_out, act
    else:
        act_out = (inv_out[ind] + 1) // 2
        inv_out[ind] = inv_out[ind] // 2
        return inv_out, act_out


def click_left(inv, act, ind, max_stack=MAX_STACK):
    'Returns a new inventory and the size of the active slot after clicking left on inventory slot index ind.'
    inv_out = inv.copy()
    if act:
        delta = min(max_stack - inv_out[ind], act)
        inv_out[ind] += delta
        return inv_out, act - delta
    else:
        act_out = inv_out[ind]
        inv_out[ind] = 0
        return inv_out, act_out


def drag_right(inv, act, n):
    'Returns a new inventory and the size of the active slot after dragging right click accross n empty inventory slots.'
    inv_out = inv.copy()
    act_out = act
    zero_inds = empty_space(inv_out, True)
    delta = min(len(zero_inds), n, act_out)
    for i in range(delta):
        inv_out[zero_inds[i]] += 1
        act_out -= 1
    return inv_out, act_out


def drag_left(inv, act, n):
    'Returns a new inventory and the size of the active slot after dragging left click accross n empty inventory slots.'
    inv_out = inv.copy()
    zero_inds = empty_space(inv_out, True)
    delta = min(len(zero_inds), n, act)
    if delta:
        quotient, remainder = divmod(act, delta)
        for i in range(delta):
            inv_out[zero_inds[i]] += quotient + (1 if i < remainder else 0)
        return inv_out, 0
    return inv_out, act


def perform_move(inv, act, move, max_stack=MAX_STACK):
    'Performs a move on the inventory and returns the new inventory and active slot size.'
    drag, left_click, index = move
    if drag:
        return drag_left(inv, act, index) if left_click else drag_right(inv, act, index)
    return click_left(inv, act, index, max_stack) if left_click else click_right(inv, act, index, max_stack)


def possible_moves(inv, act, max_stack=MAX_STACK):
    'Returns a list of all possible moves for the given inventory and active slot size (minus some redundancies).'
    moves = []
    seen = set()
    non_zero_inds = []
    for i, val in enumerate(inv):
        if val != 0 and val != max_stack and val not in seen:
            seen.add(val)
            non_zero_inds.append(i)

    zero_space = empty_space(inv)
    for i in non_zero_inds:
        moves.extend([[0, 0, i], [0, 1, i]])

    if act and zero_space:
        first_zero = inv.index(0)
        moves.extend([[0, 0, first_zero], [0, 1, first_zero]])
        for i in range(1, min(zero_space, act) + 1):
            moves.extend([[1, 0, i], [1, 1, i]])

    if not act and max_stack in inv:
        first_max = inv.index(max_stack)
        moves.extend([[0, 0, first_max], [0, 1, first_max]])

    return moves

# Easier than remembering the baggage and active slot size, we can use a single index to represent the state.
def index_interpreter(baggage, act, max_stack=MAX_STACK):
    return act + (max_stack + 1) * baggage


def string_digits(k, n=2, pre=" "):
    return f"{str(pre) * (n - len(str(k)))}{k}"


def print_optimals(i_opts, max_stack=MAX_STACK, inv_length=INVENTORY_SIZE):
    n = max(max(len(str(x)) for x in i_opts), len(str(max_stack + 1)))
    m = len(str(inv_length))
    str_opts = [string_digits(i, n) for i in i_opts]
    print_line = " " * (m + 2)
    print_line += " ".join(string_digits(j, n) for j in range(max_stack + 1)) + "\n\n"
    for j, val in enumerate(str_opts):
        if not j % (max_stack + 1):
            print_line += f"{string_digits(j // (max_stack + 1), m)}: {val} "
        elif (j + 1) % (max_stack + 1) == 0:
            print_line += f"{val}\n"
        else:
            print_line += f"{val} "
    print(print_line)


# File writing helpers

def write_lines(filename, lines):
    with open(filename, "w") as f:
        f.write("\n".join(map(str, lines)))


def write_data(filename, data):
    with open(filename, "w") as f:
        f.write(str(data))

# Visualisation

def color_code_number(value, all_values):
    if value == ".":
        return "\033[90m .\033[0m"  # dim gray
    if value == MAX_STACK + 1:
        return "\033[90m██\033[0m"  # special color for unvisited

    # Compute max ignoring 65 (MAX_STACK + 1)
    numeric_values = [v for v in all_values if isinstance(v, int) and v != MAX_STACK + 1]
    max_value = max(numeric_values) if numeric_values else 1

    ratio = value / max_value
    if ratio < 0.2:
        color = "\033[96m"  # cyan
    elif ratio < 0.4:
        color = "\033[94m"  # blue
    elif ratio < 0.6:
        color = "\033[92m"  # green
    elif ratio < 0.8:
        color = "\033[93m"  # yellow
    else:
        color = "\033[91m"  # red
    return f"{color}{str(value).rjust(2)}\033[0m"

def print_heatmap_numbers(i_opts, max_stack=MAX_STACK, inv_length=INVENTORY_SIZE):
    print("Heatmap of optimal steps (color-coded numbers):\n")
    m = len(str(inv_length))
    print(" " * (m + 2) + " ".join(f"{i:>2}" for i in range(max_stack + 1)))
    print()

    for row in range(inv_length + 1):
        row_start = row * (max_stack + 1)
        row_vals = i_opts[row_start:row_start + max_stack + 1]
        if not row_vals:
            continue
        line = f"{str(row).rjust(m)}: "
        for val in row_vals:
            colored = color_code_number(val, i_opts)
            line += f"{colored} "
        print(line)
    print("\033[0m")  # Reset ANSI

# Initialization
inventory = [0] * INVENTORY_SIZE
inventory[0] = MAX_STACK
active = 0
exact_baggage = True
clear_palette = True
then_quit = False

if clear_palette:
    inventory = inventory[:active + sum(inventory)]

    move_history = [[[inventory, active, []]]]
    optimals = [MAX_STACK + 1] * ((MAX_STACK + 1) * (len(inventory) + 1))
    optimal_witnesses = [[] for _ in range(len(optimals))]
    used_states = set()

    state_key = (tuple(sorted(inventory)), active)
    used_states.add(state_key)

    co_baggage = empty_space(inventory)
    baggage = len(inventory) - co_baggage
    interpreted_index = index_interpreter(baggage, active)
    optimals[interpreted_index] = 0

    write_data("round_data.txt", 0)
    write_lines("optimals_data.txt", optimals)
    write_lines("optimals_witness_data.txt", optimal_witnesses)
    write_data("trees_data.txt", move_history)
    write_data("used_states_data.txt", list(used_states))
    print("Palette cleared.")
    if then_quit:
        print("Quitting.")
        exit()

# Read files

with open("round_data.txt") as f:
    round_number = int(f.read())

with open("optimals_data.txt") as f:
    optimals = [int(line.strip()) for line in f]

with open("optimals_witness_data.txt") as f:
    optimal_witnesses = [ast.literal_eval(line.strip()) for line in f]

with open("trees_data.txt") as f:
    move_history = ast.literal_eval(f.read())

with open("used_states_data.txt") as f:
    used_states = set(tuple(i) for i in ast.literal_eval(f.read()))

# Layout analysis

total_blocks = active + sum(inventory)
impossible_layouts = set(range(total_blocks))

if exact_baggage:
    for a in range(MAX_STACK + 1):
        for b in range(len(inventory) + 1):
            if a + b > total_blocks:
                impossible_layouts.add(index_interpreter(b, a))

possible_layouts = {
    i for i in range(len(optimals)) if i not in impossible_layouts and optimals[i] == MAX_STACK + 1
}

# Main search loop

for j in range(MAX_CLICKS):
    if j >= round_number:
        new_round = []
        for state in tqdm(move_history[-1]):
            if not possible_layouts:
                break
            for move in possible_moves(state[0], state[1]):
                new_inv, new_act = perform_move(state[0], state[1], move)
                state_key = (tuple(sorted(new_inv)), new_act)
                if state_key not in used_states:
                    used_states.add(state_key)
                    new_path = state[2] + [move]
                    new_round.append([new_inv, new_act, new_path])

                    co_baggage = empty_space(new_inv)
                    baggage = len(new_inv) - co_baggage

                    indices_to_check = (
                        [index_interpreter(baggage, new_act)]
                        if exact_baggage
                        else [index_interpreter(baggage + i, new_act) for i in range(co_baggage + 1)]
                    )

                    for idx in indices_to_check:
                        if idx in possible_layouts:
                            optimals[idx] = len(new_path)
                            optimal_witnesses[idx] = new_path
                            possible_layouts.remove(idx)

        move_history.append(new_round)
        print(f"Search after {j + 1} clicks. {len(new_round)} states to check next click.")
        print_heatmap_numbers(optimals)
#        print_optimals(optimals, MAX_STACK, len(inventory))

        round_number += 1
        if PARTIAL_COMPUTATION_STORAGE:
            write_data("round_data.txt", round_number)
            write_data("trees_data.txt", move_history)
            write_data("used_states_data.txt", list(used_states))

        write_lines("optimals_data.txt", optimals)
        write_lines("optimals_witness_data.txt", optimal_witnesses)

        if not new_round:
            print(f"Finished in {j + 1} clicks after searching {sum(len(r) for r in move_history)} inventories.")
            formatted = ["." if v == MAX_STACK + 1 else v for v in optimals]
            print_heatmap_numbers(optimals)
#            print_optimals(formatted, MAX_STACK, len(inventory))
            break
