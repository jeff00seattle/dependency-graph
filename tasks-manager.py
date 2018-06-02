#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import collections
from pprintpp import pprint

tasks = set()

# The graph tasks
class Task(object):
    def __init__(self, name, *dependencies):
        self.name = name
        self.__active = False
        self.__dependencies = set(dependencies) if dependencies else set()
        self.__tasks_requested = set()

    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, task_name):
        self.__name = task_name

    @property
    def dependencies(self):
        return self.__dependencies
    def add_dependency(self, task_name):
        self.__dependencies.add(task_name)
    def remove_dependency(self, task_name):
        self.__dependencies.remove(task_name)

    @property
    def requests(self):
        return self.__tasks_requested

    @property
    def active(self):
        return self.__active
    @active.setter
    def active(self, active):
        self.__active = active

    def check_dependencies(self, task_dependencies=None):
        if self.dependencies is None or len(self.dependencies) == 0:
            return False

        if task_dependencies is None:
            task_dependencies = set(self.name)

        for task_dependency in self.dependencies:
            if task_dependency in task_dependencies:
                return True

            task_dependencies.add(task_dependency)

        for task_dependency in self.dependencies:
            for task in tasks:
                if task_dependency == task.name:
                    if task.check_dependencies(task_dependencies):
                        return True

        return False

    def activate(self, task_requested=None):
        task_requested = task_requested if task_requested else self.name

        for task_dependency in self.dependencies:
            for task in tasks:
                if task_dependency == task.name:
                    task.activate(task_requested)

        self.__tasks_requested.add(task_requested)
        assert len(self.__tasks_requested) > 0
        self.active = True

    def deactivate(self, task_requested=None):
        task_requested = task_requested if task_requested else self.name

        for task_dependency in self.dependencies:
            for task in tasks:
                if task_dependency == task.name:
                    task.deactivate(task_requested)

        if task_requested in self.__tasks_requested:
            self.__tasks_requested.remove(task_requested)

        if len(self.__tasks_requested) == 0 or not self.__tasks_requested:
            self.active = False

    def __repr__(self):
        return self.__name
    def __eq__(self, other):
        if isinstance(other, Task):
            return (self.name == other.name)
        else:
            return False
    def __ne__(self, other):
        return (not self.__eq__(other))
    def __hash__(self):
        return hash(self.__repr__())

    def __iter__(self):
        return iter(self.dependencies)


# "Batches" are sets of tasks that can be run together
def get_task_batches():

    # Build a map of task names to task instances
    name_to_instance = dict( (t.name, t) for t in tasks)

    # Build a map of task names to dependency names
    name_to_deps = dict((t.name, set(t.dependencies)) for t in tasks)
    pprint(name_to_deps)

    # This is where we'll store the batches
    batches = []

    # While there are dependencies to solve...
    while name_to_deps:
        # Get all tasks with no dependencies
        ready = {name for name, deps in name_to_deps.items() if not deps}

        # If there aren't any, we have a loop in the graph
        if not ready:
            msg  = "Circular dependencies found!\n"
            msg += format_dependencies(name_to_deps)
            raise ValueError(msg)

        # Remove them from the dependency graph
        for name in ready:
            del name_to_deps[name]
        for deps in name_to_deps.values():
            deps.difference_update(ready)

        # Add the batch to the list
        batches.append( {name_to_instance[name] for name in ready} )

    # Return the list of batches
    return batches

# Format a dependency graph for printing
def format_dependencies(name_to_deps):
    od = collections.OrderedDict(sorted(name_to_deps.items()))
    msg = []
    for name, deps in od.items():
        if len(deps) > 0:
            for parent in sorted(deps):
                msg.append("\t%s -> %s" % (name, parent))
        else:
            parent = None
            msg.append("\t%s -> %s" % (name, parent))
    return "\n".join(msg)


# Format a statuses graph for printing
def format_statuses(name_to_requests):
    od = collections.OrderedDict(sorted(name_to_requests.items()))
    msg = []
    for name, details in od.items():
        status = "active" if details["active"] else "not active"
        if details["requests"] and len(details["requests"]) > 0:
            msg.append("\t%s: %s: %s" % (name, status, sorted(details["requests"])))
        else:
            msg.append("\t%s: %s" % (name, status))
    return "\n".join(msg)


# Create and format a tasks dependency graph for printing
def list_tasks_dependencies():
    print()
    print("\t**********************************************")
    print("\t***  Tasks Dependencies                    ***")
    print("\t**********************************************")

    if not len(tasks):
        print("Tasks empty")
        return

    print(format_dependencies(dict((t.name, t.dependencies) for t in tasks)))
    print("\t**********************************************")


# Create and format a tasks active for printing
def list_tasks_statuses():
    print()
    print("\t**********************************************")
    print("\t***  Tasks Statuses                        ***")
    print("\t**********************************************")

    if not len(tasks):
        print("Tasks empty")
        return

    print(format_statuses(dict((t.name, {"requests": t.requests, "active": t.active}) for t in tasks)))
    print("\t**********************************************")

def list_tasks_batches():
    print()
    print("\t**********************************************")
    print("\t***  Tasks Batches                         ***")
    print("\t**********************************************")

    if not len(tasks):
        print("Tasks empty")
        return

    for bundle in get_task_batches():
        print("\t{0}".format(", ".join(task.name for task in bundle)))

    print()
    print("\t**********************************************")

def add_task():
    task_name = input("Add task by name: ")

    task_element = None
    for task in tasks:
        if task_name == task.name:
            task_element = task

    if task_element is not None:
        print("Task '{0}' does exists".format(task_name))
    else:
        task_element = Task(task_name)
        tasks.add(task_element)

    while True:
        task_depend_name = input("Add Dependency: ")
        if task_name == task_depend_name:
            print("\tX: %s -> %s, Avoiding circular dependency and ignoring" % (task_name, task_depend_name))
            continue

        if not task_depend_name:
            break

        task_element.add_dependency(task_depend_name)

        if not validate_tasks_dependencies():
            print("\tX: %s -> %s, Avoiding circular dependency and ignoring" % (task_name, task_depend_name))
            task_element.remove_dependency(task_depend_name)
        else:
            found_task_depend = False
            for task in tasks:
                if task_depend_name == task.name:
                    found_task_depend = True
                    break

            if not found_task_depend:
                task_depend_element = Task(task_depend_name)
                tasks.add(task_depend_element)

            if task_element.active:
                for task_requested in task_element.requests:
                    task_depend_element.activate(task_requested)

    list_tasks_dependencies()

def remove_task():
    task_name = input("Remove task by name: ")

    task_element = None
    for task in tasks:
        if task_name == task.name:
            task_element = task

    if task_element is None:
        print("Task '{0}' does not exists.".format(task_name))
        return

    if task_element.active:
        print("Task '{0}' is currently active and can not remove.".format(task_name))
        return

    tasks.remove(task_element)

    # Remove dependencies
    for task in tasks:
        if task_name in task.dependencies:
            task.dependencies.remove(task_name)

    list_tasks_dependencies()


def validate_tasks_dependencies():
    check_tasks = {}
    for task in sorted(tasks, key=lambda task: task.name):
        check_tasks[task.name] = task.check_dependencies()

    return all(value == False for value in check_tasks.values())


def activate_task():
    task_name = input("Activate task by name: ")

    for task in tasks:
        if task_name == task.name:
            task.activate()

    list_tasks_statuses()


def deactivate_task():
    task_name = input("Deactivate task by name: ")

    for task in tasks:
        if task_name == task.name:
            task.deactivate()

    list_tasks_statuses()


def display_title_bar():
    # Clears the terminal screen, and displays a title bar.
    os.system('clear')

    print()
    print("\t**********************************************")
    print("\t***  Tasks Manager                         ***")
    print("\t**********************************************")

def get_user_choice():

    print()
    print("[1] List tasks dependencies.")
    print("[2] List tasks active.")
    print("[3] List tasks batches.")

    print("[5] Add or Update task.")
    print("[6] Remove task.")
    print("[7] Start task.")
    print("[8] Stop task.")
    print("[q] Quit.")
    print()

    return input("What would you like to do? ")


# The test code
if __name__ == "__main__":

    display_title_bar()

    choice = ''

    while choice != 'q':

        choice = get_user_choice()

        if choice == '1':
            list_tasks_dependencies()

        elif choice == '2':
            list_tasks_statuses()

        elif choice == '3':
            list_tasks_batches()

        elif choice == '5':
            add_task()

        elif choice == '6':
            remove_task()

        elif choice == '7':
            activate_task()

        elif choice == '8':
            deactivate_task()
