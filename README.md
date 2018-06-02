# tasks-manager

## Introduction
The following code is a task management tools.

1. Add tasks with dependencies, and checks for circular dependencies as they are applied.
1. Remove tasks provided they are not currently active.
1. Start tasks
1. Stop tasks provided they are not a currently active dependency.


## Usage
```bash
$ python3 tasks-manager.py

	**********************************************
	***  Tasks Manager                         ***
	**********************************************

[1] List tasks dependencies.
[2] List tasks active.
[3] List tasks batches.
[5] Add or Update task.
[6] Remove task.
[7] Start task.
[8] Stop task.
[q] Quit.

What would you like to do?
```

## Add Task
```bash
What would you like to do? 5
Add task by name: a
Add Dependency: b
Add Dependency: c
Add Dependency:
	**********************************************
	***  Tasks Dependencies                    ***
	**********************************************
	a -> b
	a -> c
	b -> None
	c -> None
	**********************************************
```

## Activate Task
```bash
What would you like to do? 7
Activate task by name: c
	**********************************************
	***  Tasks Statuses                        ***
	**********************************************
	a: not active
	b: not active
	c: active: ['c']
	**********************************************
```

## Activate Task
```bash
What would you like to do? 7
Activate task by name: a
	**********************************************
	***  Tasks Statuses                        ***
	**********************************************
	a: active: ['a']
	b: active: ['a']
	c: active: ['a', 'c']
	**********************************************
```