/*
	CSC D84 - Unit 2 - MiniMax and adversarial games

	This file contains the API function headers for your assignment.
	Please pay close attention to the function prototypes, and
	understand what the arguments are.

	Stubs for implementing each function are to be found in MiniMax_search.c,
	along with clear ** TO DO markers to let you know where to add code.

	You are free to add helper functions within reason. But you must
	provide a prototype *in this file* as well as the implementation
	in the .c program file.

	Script by: F.J.E., Sep. 2015
*/

#ifndef __MiniMax_search_header

#define __MiniMax_search_header

// Generally needed includes
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<malloc.h>
#include<string.h>

#include "board_layout.h"

// Function prototypes for D84 - Unit 2 - MiniMax assignment solution
double MiniMax(double gr[graph_size][4], int path[1][2], double minmax_cost[size_X][size_Y], int cat_loc[10][2], int cats, int cheese_loc[10][2], int cheeses, int mouse_loc[1][2], int mode, double (*utility)(int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, int depth, double gr[graph_size][4]), int agentId, int depth, int maxDepth, double alpha, double beta);

double utility(int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, int depth, double gr[graph_size][4]);

int checkForTerminal(int mouse_loc[1][2],int cat_loc[10][2],int cheese_loc[10][2],int cats,int cheeses);
// If you need to add any function prototypes yourself, you can do so *below* this line.

#define queue_size graph_size
#define set_size graph_size

#define TO_INDEX(x, y) (x + ((y)*size_X))
#define Y_VALUE(index) ((index) / size_Y)
#define X_VALUE(index) ((index) % size_X)

int connected_index(int index, int direction);
void init_seen(int seen[graph_size]);
void add_to_path(int path[graph_size][2], int index);
int get_next(int q[][2]);
void update_queue(int q[][2], int value, int priority);
void init_queue(int q[][2]);
int queue_is_empty(int q[][2]);
void add_to_set(int s[set_size], int value);
int set_contains(int s[set_size], int value);
void set_distances(double graph[graph_size][4]);

#endif


