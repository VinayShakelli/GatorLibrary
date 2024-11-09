#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, data):
        self.heap.append(data)
        self._heapify_up()

    def pop(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down()
        return root

    def _heapify_up(self):
        index = len(self.heap) - 1
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index][1] < self.heap[parent_index][1] or (
                self.heap[index][1] == self.heap[parent_index][1] and
                self.heap[index][2] < self.heap[parent_index][2]
            ):
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def _heapify_down(self):
        index = 0
        while True:
            left_child_index = 2 * index + 1
            right_child_index = 2 * index + 2
            smallest = index

            try:
                if (
                    left_child_index < len(self.heap) and
                    self.heap[left_child_index][1] < self.heap[smallest][1] or (
                        self.heap[left_child_index][1] == self.heap[smallest][1] and
                        self.heap[left_child_index][2] < self.heap[smallest][2]
                    )
                ):
                    smallest = left_child_index

                if (
                    right_child_index < len(self.heap) and
                    self.heap[right_child_index][1] < self.heap[smallest][1] or (
                        self.heap[right_child_index][1] == self.heap[smallest][1] and
                        self.heap[right_child_index][2] < self.heap[smallest][2]
                    )
                ):
                    smallest = right_child_index

                if smallest != index:
                    self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                    index = smallest
                else:
                    break

            except IndexError:
                break


class BookNode:
    def __init__(self, book_id, book_name, author_name, availability_status, borrowed_by=None):
        self.book_id = book_id
        self.book_name = book_name
        self.author_name = author_name
        self.availability_status = availability_status
        self.borrowed_by = borrowed_by
        self.reservation_heap = MinHeap()

    def __repr__(self):
        return f"BookID = {self.book_id}\nTitle = \"{self.book_name}\"\nAuthor = \"{self.author_name}\"\n" \
               f"Availability = \"{self.availability_status}\"\nBorrowedBy = {self.borrowed_by}\n" \
               f"Reservations = {self.reservation_heap.heap}"

class RedBlackTreeNode:
    def __init__(self, key, color, book_node):
        self.key = key
        self.color = color
        self.book_node = book_node
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RedBlackTreeNode(key=None, color="BLACK", book_node=None)
        self.root = self.NIL
        self.color_flip_count = 0
    
    def _find_node(self, node, key):
        while node != self.NIL:
            if key == node.key:
                return node
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        return None

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _right_rotate(self, y):
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent == None:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def _insert_fixup(self, z):
        if z.parent == None:
            return
        while z.parent.color == "RED":
            if z.parent.parent == None :
                break
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self._left_rotate(z.parent.parent)
            if z.parent == None:
                break

        self.root.color = "BLACK"

    def insert(self, book_node):
        z = RedBlackTreeNode(key=book_node.book_id, color="RED", book_node=book_node)
        y = None
        x = self.root
        #while x != None:
        while x != self.NIL:
            if x == None:
                break
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right

        z.parent = y
        if y == None:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        self._insert_fixup(z)

    def _color_flip_count(self, old_color, new_color):
        if old_color != new_color:
            self.color_flip_count += 1

    def _delete_fixup(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                w = x.parent.right
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._left_rotate(x.parent)
                    w = x.parent.right

                if w.left.color == "BLACK" and w.right.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.right.color == "BLACK":
                        w.left.color = "BLACK"
                        w.color = "RED"
                        self._right_rotate(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.right.color = "BLACK"
                    self._left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == "RED":
                    w.color = "BLACK"
                    x.parent.color = "RED"
                    self._right_rotate(x.parent)
                    w = x.parent.left

                if w.right.color == "BLACK" and w.left.color == "BLACK":
                    w.color = "RED"
                    x = x.parent
                else:
                    if w.left.color == "BLACK":
                        w.right.color = "BLACK"
                        w.color = "RED"
                        self._left_rotate(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = "BLACK"
                    w.left.color = "BLACK"
                    self._right_rotate(x.parent)
                    x = self.root

        x.color = "BLACK"

    def delete(self, z):
        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            if y == None:
                return
            y_original_color = y.color
            x = y.right

            if y.parent != z:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        self._color_flip_count(y_original_color, x.color)
        if y_original_color == "BLACK":
            self._delete_fixup(x)

    def _minimum(self, x):
        while x.left != self.NIL:
            x = x.left
            if x == None:
                break
        return x


    def _transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent


    def find_closest(self, target_id):
        current_node = self.root
        closest_node = None
        while current_node != self.NIL:
            if current_node == None:
                break
            if current_node.key == target_id:
                return current_node.book_node
            elif current_node.key < target_id:
                closest_node = current_node
                current_node = current_node.right
            else:
                closest_node = current_node
                current_node = current_node.left

        return closest_node.book_node

    def inorder_traversal(self, node, result):
        if node != self.NIL:
            self.inorder_traversal(node.left, result)
            result.append(node.book_node)
            self.inorder_traversal(node.right, result)



def parse_arguments(arguments):
    return [arg.strip().strip(')').split(',') for arg in arguments]

def parse_input_line(line):
    parts = line.strip().split('(')
    if len(parts) == 1:
        return parts[0], []
    else:
        return parts[0], parts[1].strip(')').split(',')

def main():
    library = RedBlackTree()

    with open('test3.txt', 'r') as file:
        lines = file.readlines()

    output_file = open('test3_output_file.txt', 'w')

    for line in lines:
        operation, args = parse_input_line(line)
        arguments = parse_arguments(args)
        if operation == 'InsertBook':
            book_id, title, author, availability = map(str, arguments)
            book_node = BookNode(int(book_id[2:-2]), title, author, availability)
            library.insert(book_node)

        elif operation == 'PrintBook':
            book_id = int(arguments[0][0])
            book_node = library.find_closest(book_id)
            if book_node.book_id == book_id:
                output_file.write(repr(book_node) + '\n')
            else:
                output_file.write(f'Book {book_id} not found in the Library\n')

        elif operation == 'PrintBooks':
            book_id1 = int(arguments[0][0]) 
            book_id2 = int(arguments[1][0])
            books_result = []
            for i in range(book_id1, book_id2 + 1):
                book_node = library.find_closest(i)
                if book_node.book_id == i:
                    books_result.append(book_node)
            for book_node in books_result:
                output_file.write(repr(book_node) + '\n')

        elif operation == 'BorrowBook':
            patron_id = int(arguments[0][0])
            book_id = int(arguments[1][0])
            priority = int( arguments[2][0])
            book_node = library.find_closest(book_id)
            if book_node.availability_status == 'Yes':
                book_node.availability_status = 'No'
                book_node.borrowed_by = patron_id
                output_file.write(f'Book {book_id} Borrowed by Patron {patron_id}\n')
            else:
                book_node.reservation_heap.push((patron_id, priority, time.time()))
                output_file.write(f'Book {book_id} Reserved by Patron {patron_id}\n')

        elif operation == 'ReturnBook':
            patron_id = int(arguments[0][0])
            book_id = int(arguments[1][0])
            book_node = library.find_closest(book_id)
            book_node.availability_status = 'Yes'
            output_file.write(f'Book {book_id} Returned by Patron {patron_id}\n')
            reservation = book_node.reservation_heap.pop()
            if reservation:
                output_file.write(f'Book {book_id} Allotted to Patron {reservation[0]}\n')

        elif operation == 'DeleteBook':
            book_id = int(arguments[0][0])
            book_node = library.find_closest(book_id)
            reservations = book_node.reservation_heap.heap
            if len(reservations) > 0:
                output_file.write(f'Book {book_id} is no longer available. Reservations made by Patrons {", ".join(str(res[0]) for res in reservations)} have been cancelled!\n')
            else:
                output_file.write(f'Book {book_id} is no longer available\n')
            library.delete(library._find_node(library.root, book_id))

        elif operation == 'FindClosestBook':
            target_id = int(arguments[0][0])
            book_node = library.find_closest(target_id)
            output_file.write(repr(book_node) + '\n')

        elif operation == 'ColorFlipCount':
            output_file.write(f'Colour Flip Count: {library.color_flip_count}\n')

        elif operation == 'Quit':
            output_file.write('Program Terminated!!\n')
            break

    output_file.close()

if __name__ == '__main__':
    main()