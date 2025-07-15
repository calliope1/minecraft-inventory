# Minecraft inventory puzzles

In Minecraft, you have an inventory with 36 slots that can hold some number of an item, up to a limit. You could use that slot to hold up to 64 dirt, up to 16 snowballs, or up to 1 bed.

Furthermore, when your inventory is open you can move items around. By left-clicking on that stack of 64 dirt it becomes attached to your cursor and you can left click elsewhere in the inventory to put it back down. In fact, the behaviour is quite complicated:

**If your cursor is empty.**
Right-clicking on an inventory slot takes half of the items in that slot (rounded up) and moves them to the cursor.
Left-clicking on an inventory slot moves all items in that slot to the cursor.
Drag right- and left-clicking does nothing.

**If your cursor is not empty.**
Right-clicking on an inventory slot adds one item to that slot from the cursor, if the slot is not full
Left-clicking on an inventory slot moves all items from the cursor to that slot, up to the maximum stack size.
Drag right-clicking on empty slots adds one item to each of those slots from the cursor.
Drag left-clicking on empty slots moves all items from the cursor to those slots, distributing them evenly.

**The question.**

Suppose that you start with an empty cursor and a single stack of 64 dirt in your inventory. How many clicks does it take for you to end up with exactly 17 blocks of dirt attached to your cursor?

*Answer:* 2.
By right-clicking on the stack you take 32 blocks. By then drag right-clicking over 15 empty slots in your inventory, you put 1 dirt into each of them and leave yourself with 17 dirt on the cursor.

You leave yourself with an ungly inventory. What if I want you to clean up after yourself? So you must have 17 dirt on your cursor and the remaining 47 must be in a single stack in your inventory.

*Now* the question becomes a bit more interesting.

This code answers this question and generates a table of the number of clicks it takes to get any amount of dirt onto your cursor with a prescribed *exact* amount of 'baggage' (non-empty inventory slots left over). However, you can alter the `MAX_STACK` and `INVENTORY_SIZE` parameters to your heart's content.

*So what's the answer?* 6. In fact, here's a heatmap of all the answers for the problem described. Remember that 'baggage' (y axis) of 5 (say) means that there must be *exactly* 5 non-empty inventory slots left over at the end.

![Full solutions for `MAX_STACK=64`](https://calliope.mx/files/minecraft_inventory_solution.png)

## Potential improvements
* Create an inventory class to encapsulate the inventory logic. (MAJOR - other improvements are dependent on this.)
* Allow for different objects with unique maximum stack sizes.
* Add more detailed logging and error handling.
* Add a command-line interface for easier interaction and solving other problems.
