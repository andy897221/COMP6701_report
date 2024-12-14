import numpy as np
import math

# basic tree structure
class Node(object):
    def __init__(self, label, samplesizes=None):
        self.label = label
        self.samplesizes = samplesizes or []
        self.children = []
        self.parent = None

    def is_terminal(self):
        return len(self.children) == 0

    def add_child(self, node):
        self.children.append(node)
        self.samplesizes.append(self.children[-1].samplesizes)
        self.children[-1].parent = self

    def total_sample_size(self):
        return np.sum(self.samplesizes)

class sample_balancer():
    def __init__(self, tree):
        self.tree = tree # aka root node but with whole tree initialized with it


    ########### balancing
    # this function get the sum of the numbers in a nested list
    @staticmethod
    def sum_inhomogeneous(arr):
        total = 0
        for element in arr:
            if isinstance(element, list):  # If it's a sub-list, sum recursively
                total += sample_balancer.sum_inhomogeneous(element)
            else:
                total += element  # Otherwise, add the element directly
        return total


    @staticmethod
    def _adjust_samplesize_at_leaf(node, target_samplesize):
        if node.is_terminal():
            node.samplesizes[0] = target_samplesize
            return
        for child in node.children:
            sample_balancer._adjust_samplesize_at_leaf(child, target_samplesize / len(node.children))
        return

    @staticmethod
    def _balance_tree(node):
        if node.is_terminal(): return
        for child in node.children:
            sample_balancer._balance_tree(child)

        samplesize_sums = [sample_balancer.sum_inhomogeneous(child.samplesizes) for child in node.children]
        largest_sum, largest_idx = np.max(samplesize_sums), np.argmax(samplesize_sums)
        for i in range(len(node.children)):
            if i != largest_idx:
                sample_balancer._adjust_samplesize_at_leaf(node.children[i], largest_sum)

    def balance_tree(self):
        sample_balancer._balance_tree(self.tree)


    @staticmethod
    def _print_tree(node, level=0):
        print(" " * (level * 4) + f"Node {node.label}: {node.samplesizes}")
        for child in node.children:
            sample_balancer._print_tree(child, level + 1)

    def print_tree(self):
        sample_balancer._print_tree(self.tree)


    @staticmethod
    def _get_tree_dict(node, tree_dict, to_int):
        if node.is_terminal():
            tree_dict[node.label] = [int(i) for i in node.samplesizes] if to_int else node.samplesizes
            return 
        tree_dict[node.label] = [{} for i in node.children]
        for i, child in enumerate(node.children):
            sample_balancer._get_tree_dict(child, tree_dict[node.label][i], to_int)
        return

    def get_tree_as_dict(self, to_int=True):
        tree_dict = {}
        sample_balancer._get_tree_dict(self.tree, tree_dict, to_int)
        return tree_dict

