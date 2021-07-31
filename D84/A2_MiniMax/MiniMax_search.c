/*
	CSC D84 - Unit 2 - MiniMax search and adversarial games

	This file contains stubs for implementing a MiniMax search
        procedure with alpha-beta pruning. Please read the assignment
	handout carefully - it describes the game, the data you will
	have to handle, and the search functions you must provide.

	Once you have read the handout carefully, implement your search
	code in the sections below marked with

	**************
	*** TO DO:
	**************

	Make sure to add it to your report.txt file - it will be marked!

	Have fun!

	DO NOT FORGET TO 'valgrind' YOUR CODE - We will check for pointer
	management being done properly, and for memory leaks.

	Starter code: F.J.E. Sep. 15
*/

#include "MiniMax_search.h"

/*
   This function is the interface between your solution for the assignment and the driver code. The driver code
   in MiniMax_search_core_GL will call this function once per frame, and provide the following data
   
   Board and game layout:

	Exactly the same as for Assignment 1 - have a look at your code if you need a reminder of how the adjacency
	list and agent positions are stored.	

	Note that in this case, the path will contain a single move - at the top level, this function will provide
	an agent with the 'optimal' mini-max move given the game state.


   IMPORTANT NOTE: Mini-max is a recursive procedure. This function will need to fill-in the mini-max values for 
	 	   all game states down to the maximum search depth specified by the user. In order to do that,
		   the function needs to be called with the correct state at each specific node in the mini-max
		   search tree.

		   The game state is composed of:

			* Mouse, cat, and cheese positions (and number of cats and cheeses)
			
		   At the top level (when this function is called by the mini-max driver code), the game state
		   correspond to the current situation of the game. But once you start recursively calling
		   this function for lower levels of the search tree the positions of agents will have changed.
		   
		   Therefore, you will need to define local variables to keep the game state at each node of the
		   mini-max search tree, and you will need to update this state when calling recursively so that
		   the search does the right thing.

		   This function *must check* whether:
			* A candidate move results in a terminal configuration (cat eats mouse, mouse eats cheese)
			  at which point it calls the utility function to get a value
	 		* Maximum search depth has been reached (depth==maxDepth), at which point it will also call
			  the utility function to get a value
			* Otherwise, call recursively using the candidate configuration to find out what happens
			  deeper into the mini-max tree.

   Arguments:
		gr[graph_size][4]   		- This is an adjacency list for the maze
		path[1][2] 			- Your function will return the optimal mini-max move in this array.
		minmax_cost[size_X][size_Y]	- An array in which your code will store the
						  minimax value for maze locations expanded by
						  the search *when called for the mouse, not
						  for the cats!*

						  This array will be used to provide a visual 
						  display of minimax values during the game.

		cat_loc[10][2], cats   - Location of cats and number of cats (we can have at most 10,
					 but there can be fewer). Only valid cat locations are 0 to (cats-1)
		cheese_loc[10][2], cheeses - Location and number of cheese chunks (again at most 10,
					     but possibly fewer). Valid locations are 0 to (cheeses-1)
		mouse_loc[1][2] - Mouse location - there can be only one!
		mode - Search mode selection:
					mode = 0 	- No alpha-beta pruning
					mode = 1	- Alpha-beta pruning

		(*utility)(int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, int depth, double gr[graph_size][4]);
				- This is a pointer to the utility function which returns a value for a specific game configuration

				   NOTE: Unlike the search assignment, this utility function also gets access to the graph so you can do any processing 					 that requires knowledge of the maze for computing the utility values.

				  * How to call the utility function from within this function : *
					- Like any other function:
						u = utility(cat_loc, cheese_loc, mouse_loc, cats, cheeses, depth, gr);
						
		agentId: Identifies which agent we are doing MiniMax for. agentId=0 for the mouse, agentId in [1, cats] for cats. Notice that recursive calls
                         to this function should increase the agentId to reflect the fact that the next level down corresponds to the next agent! For a game
                         with two cats and a mouse, the agentIds for the recursion should look like 0, 1, 2, 0, 1, 2, ...
	
		depth: Current search depth - whether this is a MIN or a MAX node depends both on depth and agentId.
		
		maxDepth: maximum desired search depth - once reached, your code should somehow return
			  a minimax utility value for this location.

		alpha. beta: alpha and beta values passed from the parent node to constrain search at this
			     level.

   Return values:
		Your search code will directly update data passed-in as arguments:
		
		- Mini-Max value	: Notice this function returns a double precision number. This is
					  the minimax value at this level of the tree. It will be used 
					  as the recursion backtracks filling-in the mini-max values back
					  from the leaves to the root of the search tree. 

		- path[1][2]		: Your MiniMax function will return the location for the agent's 
					  next location (i.e. the optimal move for the agent). 
		- minmax_cost[size_X][size_Y] 	:  Your search code will update this array to contain the
						   minimax value for locations that were expanded during
						   the search. This must be done *only* for the mouse.

						   Values in this array will be in the range returned by
						   your utility function.

		* Your code MUST NOT modify the locations or numbers of cats and/or cheeses, the graph,
	     	  or the location of the mouse - if you try, the driver code will know it *
			
		That's that, now, implement your solution!
 */

 /********************************************************************************************************
 * 
 * TO DO:	Implement code to perform a MiniMax search. This will involve a limited-depth BFS-like
 *              expansion. Once nodes below return values, your function will propagate minimax utilities
 *		as per the minimax algorithm.
 *	
 *		Note that if alpha-beta pruning is specified, you must keep track of alphas and betas
 *		along the path.
 *
 *		You can use helper functions if it seems reasonable. Add them to the MiniMax_search.h
 *		file and explain in your code why they are needed and how they are used.
 *
 *		Recursion should appear somewhere.
 *
 *		MiniMax cost: If the agentId=0 (Mouse), then once you have a MiniMax value for a location
 *		in the maze, you must update minmax_cost[][] for that location.
 *
 *		How you design your solution is up to you. But:
 *
 *		- Document your implementation by adding concise and clear comments in this file
 *		- Document your design (how you implemented the solution, and why) in the report
 *
 ********************************************************************************************************/

// Stub so that the code compiles/runs - This will be removed and replaced by your code!

// variables to hold graph data
int distance[graph_size][graph_size];
int distances_set = 0;


double MiniMax(double gr[graph_size][4], int path[1][2], double minmax_cost[size_X][size_Y], int cat_loc[10][2], int cats, int cheese_loc[10][2], int cheeses, int mouse_loc[1][2], int mode, double (*utility)(int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, int depth, double gr[graph_size][4]), int agentId, int depth, int maxDepth, double alpha, double beta)
{

	if (!distances_set) {
		set_distances(gr);
		distances_set = 1;
	}

	// if terminal node
	if (checkForTerminal(mouse_loc, cat_loc, cheese_loc, cats, cheeses) > 0 || depth >= maxDepth) {
		//int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, int depth, double gr[graph_size][4]
		// return the nodes utility
		return utility(cat_loc, cheese_loc, mouse_loc, cats, cheeses, depth, gr);
	}

    // loop agent to switch back to mouses turn
	if (agentId > cats) {
		agentId = 0;
	} 

	// values for calculating min and max and for returning
	double ret = 0;
	double min = INFINITY;
	double max = -INFINITY;

	// temporary variables and their initializiation to keep track of agent locations
	int temp_mouse_loc[1][2];
	int temp_cat_loc[10][2];

	temp_mouse_loc[0][0] = mouse_loc[0][0];
	temp_mouse_loc[0][1] = mouse_loc[0][1];

	for (int i = 0; i < cats; i++) {
		temp_cat_loc[i][0] = cat_loc[i][0];
		temp_cat_loc[i][1] = cat_loc[i][1];
	}

	// keep track of where the current agent's turn is
	int curr_loc = 0;

	if (agentId == 0) {
		curr_loc = TO_INDEX(mouse_loc[0][0], mouse_loc[0][1]);
	} else {
		curr_loc = TO_INDEX(cat_loc[agentId-1][0], cat_loc[agentId-1][1]);
	}

	for (int i = 0; i < 4; i ++) {

		if (gr[curr_loc][i]) {

			// set the variables for the simulation of the agents action
			int child = connected_index(curr_loc, i);

			int child_x = X_VALUE(child);
			int child_y = Y_VALUE(child);

			if (agentId == 0) {
				temp_mouse_loc[0][0] = child_x;
				temp_mouse_loc[0][1] = child_y;
			} else {
				temp_cat_loc[agentId-1][0] = child_x;
				temp_cat_loc[agentId-1][1] = child_y;
			}

			// recursive call for minimax
			double u = MiniMax(gr, path, minmax_cost, temp_cat_loc, cats, cheese_loc, cheeses, temp_mouse_loc, mode, utility, agentId + 1, depth + 1, maxDepth, alpha, beta);
		
			// max node
			if (agentId == 0) {

				// update minimax cost for this child node
				minmax_cost[child_x][child_y] = u;

				if (u > max) {
					max = u;
					if (depth == 0) {
						path[0][0] = child_x;
					    path[0][1] = child_y;
					}
					
				}

				// using a-b pruning
				if (mode) {
					if (u > alpha) {
						alpha = u;
						if (alpha >= beta) {
							return u;
						}
					}
				}
				
				
				ret = max;

			// min node
			} else {

				// min node a-b pruning
				if (mode) {
					if (u < beta) {
						beta = u;
						if (beta <= alpha) {
							return u;
						}
					}
				}
				
				if (u < min) {
					min = u;
				}
				ret = min;
			}
		}
	}
	return ret;
}

double utility(int cat_loc[10][2], int cheese_loc[10][2], int mouse_loc[1][2], int cats, int cheeses, int depth, double gr[graph_size][4])
{
 /*
	This function computes and returns the utility value for a given game configuration.
	As discussed in lecture, this should return a positive value for configurations that are 'good'
	for the mouse, and a negative value for locations that are 'bad' for the mouse.

	How to define 'good' and 'bad' is up to you. Note that you can write a utility function
	that favours your mouse or favours the cats, but that would be a bad idea... (why?)

	Input arguments:

		cat_loc - Cat locations
		cheese_loc - Cheese locations
		mouse_loc - Mouse location
		cats - # of cats
		cheeses - # of cheeses
		depth - current search depth
		gr - The graph's adjacency list for the maze

		These arguments are as described in A1. Do have a look at your solution!
 */

   int mouse_index = TO_INDEX(mouse_loc[0][0], mouse_loc[0][1]);

   int cat_dist = 0;
   for (int i = 0; i < cats; i ++ ) {
	   int cat_index = TO_INDEX(cat_loc[i][0], cat_loc[i][1]);
	   int d =  distance[mouse_index][cat_index];
   }

   // pick the closest cheese to minimize the distance of
   float cheese_dist = INFINITY;
   for (int i = 0; i < cheeses; i ++ ) {
	   int cheese_index = TO_INDEX(cheese_loc[i][0], cheese_loc[i][1]);
	   int new_dist = distance[mouse_index][cheese_index];
	   if (new_dist < cheese_dist) {
		   cheese_dist = new_dist;
	   }
   	}

	// middle node or terminal node?

	int node_type = checkForTerminal(mouse_loc, cat_loc, cheese_loc, cats, cheeses);

	// cats win
	if (node_type == 1) {
		return -32;
	} else if (node_type == 2) { // mouse wins or
		return 32;
	} else { // non terminal node
		// return cat_dist - cheese_dist;
		return  cat_dist - cheese_dist;// 32 - cheese_dist - cat_dist;
	}
}

// edited, so that nodes where cats win return 1, mouse wins returns 2
int checkForTerminal(int mouse_loc[1][2],int cat_loc[10][2],int cheese_loc[10][2],int cats,int cheeses)
{
 /* 
   This function determines whether a given configuration constitutes a terminal node.
   Terminal nodes are those for which:
     - A cat eats the mouse
     or
     - The mouse eats a cheese
   
   If the node is a terminal, the function returns 1, else it returns 0
 */

 // Check for cats having lunch
 for (int i=0; i<cats; i++)
  if (mouse_loc[0][0]==cat_loc[i][0]&&mouse_loc[0][1]==cat_loc[i][1]) return(1);

 // Check for mouse having lunch
 for (int i=0; i<cheeses; i++)
  if (mouse_loc[0][0]==cheese_loc[i][0]&&mouse_loc[0][1]==cheese_loc[i][1]) return(2);

 return(0);

}

int connected_index(int index, int direction) {
    int x = X_VALUE(index);
    int y = Y_VALUE(index);
    if (direction == 0) {
        y --;
    } else if (direction == 1) {
        x ++;
    } else if (direction == 2) {
        y ++;
    } else if (direction == 3) {
        x --;
    }

    if (x < 0 || y < 0 || x >= size_X || y >= size_Y) {
        printf("incorrect value of (%d, %d) at index %d in direction %d\n", x, y, index, direction);
        exit(1);
    }

    return TO_INDEX(x, y);
}

// a very similar copy of BFS that finds and sets the distance for all values in the graph using the distance array.
void set_distances(double graph[graph_size][4]) {
    

	for (int j = 0; j < graph_size; j++)
	{
		/* code */
		int priority_queue[graph_size][2];
		init_queue(priority_queue);

		int seen[graph_size];
		init_seen(seen);

		update_queue(priority_queue, j, 0);

		while (!queue_is_empty(priority_queue)) {
			// get next node u from pq
			int u = get_next(priority_queue);
			// mark u as seen
			add_to_set(seen, u);

			for (int i = 0; i < 4; i ++) {
				if (graph[u][i]) {
					int v = connected_index(u, i);
					if (!set_contains(seen, v)) {
						// add the value to queue
						update_queue(priority_queue, v, 0);
						// mark seen
						add_to_set(seen, v);
						// set distance
						distance[j][v] = distance[j][u] + 1;
					}
				}
			}
		}

	}
}

void init_seen(int seen[graph_size]) {
    for (int i = 0; i < graph_size; i++) 
    {
        seen[i] = -1;
    }
}

void init_queue(int q[][2]) {
    for (int i = 0; i < queue_size; i ++) 
    {
        q[i][0] = -1;
        q[i][1] = graph_size + 1;
    }
}

void update_queue(int q[][2], int value, int priority) {
	int free_spot = -1;
	for (int i = 0; i < queue_size; i++) {
		if (q[i][0] == value) {
			if (q[i][1] > priority) {
				q[i][1] = priority;
			}
			return;
		} else if (free_spot == -1 && q[i][0] == -1) {
			free_spot = i;
		}
	}
	// not in queue so update
	q[free_spot][0] = value;
	q[free_spot][1] = priority;
}

void add_to_set(int s[set_size], int value) {
    for (int i = 0; i < set_size; i ++) {
        if (s[i] == value) {
            return;
        } else if (s[i] == -1) {
            s[i] = value;
            return;
        }
    }
}

int queue_is_empty(int q[][2]) {
    for (int i = 0; i < queue_size; i ++)
    {
        if (q[i][0] > -1) {
            return 0;
        }
    }
    return 1;
}

int set_contains(int s[set_size], int value) {
    for (int i = 0; i < set_size; i ++) {
        if (s[i] == value) {
            return 1;
        }
    }
    return 0;
}

int get_next(int q[][2]){
	int minimum_priority = graph_size + 1;
	int index = -1;
	for (int i = 0; i < queue_size; i++) {
		// spot is not empty and smallest priority
		if (q[i][0] > -1 && q[i][1] < minimum_priority) {
			minimum_priority = q[i][1];
			index = i;
		}
	}
	if (index < 0) {
		return -1;
	}
	int ret_index = q[index][0];
	q[index][0] = -2; // spot taken, but not valid, necesarry for normal queue behaviour
	q[index][1] = graph_size + 1;
	return ret_index;;
}


