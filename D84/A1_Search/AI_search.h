/*
	CSC D84 - Unit 1 - Search

	This file contains the API function headers for your assignment.
	Please pay close attention to the function prototypes, and
	understand what the arguments are.

	Stubs for implementing each function are to be found in AI_search.c,
	along with clear ** TO DO markers to let you know where to add code.

	You are free to add helper functions within reason. But you must
	provide a prototype *in this file* as well as the implementation
	in the .c program file.

	Starter by: F.J.E., Jul. 2015
	Updated by: F.J.E., Jan. 2018
*/

#ifndef __AI_search_header

#define __AI_search_header

// Generally needed includes
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<malloc.h>
#include<climits>

#include "board_layout.h"

// Function prototypes for D84 - Unit 1 - Search assignment solution

void search(double gr[graph_size][4], int path[graph_size][2], int visit_order[size_X][size_Y], int cat_loc[10][2], int cats, int cheese_loc[10][2], int cheeses, int mouse_loc[1][2], int mode, int (*heuristic)(int x, int y, int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, double gr[graph_size][4]));
int H_cost(int x, int y, int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, double gr[graph_size][4]);
int H_cost_nokitty(int x, int y, int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, double gr[graph_size][4]);

// If you need to add any function prototypes yourself, you can do so *below* this line.
#define queue_size graph_size
#define set_size graph_size

#define TO_INDEX(x, y) (x + ((y)*size_X))
#define Y_VALUE(index) ((index) / size_Y)
#define X_VALUE(index) ((index) % size_X)

int euclidian_distance(int x1, int y1, int x2, int y2);
int cat_position(int index, int cat_loc[10][2], int cats);
int closest(int x, int y, int thing_loc[10][2], int things);
void update_visited(int index_visited, int visit_order[size_X][size_Y], int num_visited);
void init_seen(int seen[graph_size]);
int connected_index(int index, int direction);
int get_next(int q[][2]);
void update_queue(int q[][2], int value, int priority);
void init_queue(int q[][2]);
int queue_is_empty(int q[][2]);
void add_to_set(int s[graph_size], int value);
int set_contains(int s[graph_size], int value);
void BFS(double graph[graph_size][4], int start, int goal, int path[graph_size][2], int visit_order[size_X][size_Y], int cat_loc[10][2], int cats);
int DFS(double graph[graph_size][4], int start, int goal, int seen[graph_size], int path[graph_size][2], int depth, int visit_order[size_X][size_Y], int cat_loc[10][2], int cats);
void A_STAR(double graph[graph_size][4], int start, int goal, int path[graph_size][2], int visit_order[size_X][size_Y], int cat_loc[10][2], int cats, int cheese_loc[10][2], int mouse_loc[1][2], int cheeses,
     int (*heuristic)(int x, int y, int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, double gr[graph_size][4]));
void set_distances(double graph[graph_size][4], int distance[graph_size], int index);


#endif

