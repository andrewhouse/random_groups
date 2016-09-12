import random
import os
import copy
import json
from sys import argv

class RandomGroups:
    def __init__(self, number_per_group=2):
        self.number_per_group = number_per_group
        self.adjectives = []
        self.nouns = []
        self.groups = []
        self.students = []
        self.run_setup_functions()

    def run_setup_functions(self):
        """ Functions to be run during initilization """
        self.set_adjectives()
        self.set_nouns()
        self.set_students()
        random.shuffle(self.students)
        self.student_list_copy = copy.deepcopy(self.students)
        self.set_group()

    def set_adjectives(self):
        with open('adjectives.txt') as inputAdjectives:
            self.adjectives = inputAdjectives
            """ Strip Off Newlines"""
            self.adjectives = [line.rstrip('\n').split(',') for line in self.adjectives]
            """ Flatten List """
            self.adjectives = [item for sublist in self.adjectives for item in sublist ]

    def set_nouns(self):
        with open('nouns.txt') as inputNouns:
            self.nouns = inputNouns
            """ Strip Off Newlines"""
            self.nouns = [line.rstrip('\n').split(',') for line in self.nouns]
            """ Flatten List """
            self.nouns = [item for sublist in self.nouns for item in sublist ]

    def set_students(self):
        with open('students.json', 'r') as f:
            self.students = json.load(f)

    def set_group(self):
        """ Main function to gather the groups """
        while len(self.student_list_copy) > 0:
            if len(self.student_list_copy) >= self.number_per_group:
                choices = self.random_add_to_group()
            elif len(self.student_list_copy) is 1:
                choices = self.add_one_to_group()
            else:
                choices = self.add_remaining_to_groups()
            self.remove(choices)
        self.add_teams_to_groups()

    def add_remaining_to_groups(self):
        """ Add leftover students to groups if there are
        more than one remaining students but not enough
        for a full group """
        choices = copy.deepcopy(self.student_list_copy)
        self.groups.append(choices)
        return choices

    def random_add_to_group(self):
        """ Randomly add students to group based on the 
        passed in number per group"""
        choices = random.sample(self.student_list_copy, self.number_per_group)
        self.groups.append(choices)
        return choices

    def add_one_to_group(self):
        """ Add leftover student to an existing group at random"""
        choices = [self.student_list_copy[0]]
        smallest_group_index = self.groups.index(min(self.groups, key=len))
        self.groups[smallest_group_index].append(self.student_list_copy[0])
        return choices

    def remove(self, choices):
        """ Remove selected students from the selection list """
        for choice in choices:
            self.student_list_copy.remove(choice)
            
    def add_teams_to_groups(self):
        self.teamed_groups = []
        for group in self.groups:
            adj = random.choice(self.adjectives).capitalize()
            noun = random.choice(self.nouns).capitalize()
            str_group = ", ".join(group)
            teams = "Team {0} {1}: {2}".format(adj, noun, str_group)
            self.teamed_groups.append(teams)


    def print_groups(self):
        """ Print the groups to the terminal """
        os.system('clear')
        print("\n" * 8)
        for group in self.teamed_groups:
            print(group)
            print(len(group) * '-' + "\n")


def run():
    """ Fuction that instantiates the class and calls print groups"""
    try:
        number_per_group = int(argv[1])
        groups = RandomGroups(number_per_group)
    except:
        groups = RandomGroups()
    groups.print_groups()

if __name__ == "__main__":
    run()
