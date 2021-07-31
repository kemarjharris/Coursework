/*
	CSC D84 - Unit 3 - Reinforcement Learning
	
	This file contains stubs for implementing the Q-Learning method
	for reinforcement learning as discussed in lecture. You have to
	complete two versions of Q-Learning.
	
	* Standard Q-Learning, based on a full-state representation and
	  a large Q-Table
	* Feature based Q-Learning to handle problems too big to allow
	  for a full-state representation
	    
	Read the assignment handout carefully, then implement the
	required functions below. Sections where you have to add code
	are marked

	**************
	*** TO DO:
	**************

	If you add any helper functions, make sure you document them
	properly and indicate in the report.txt file what you added.
	
	Have fun!

	DO NOT FORGET TO 'valgrind' YOUR CODE - We will check for pointer
	management being done properly, and for memory leaks.#define TO_STATE(mouse_x, mouse_y, cat_x, cat_y, cheese_x, cheese_y, size_X, graph_size) (mouse_x+(mouse_y*size_X)) + ((cat_x+(cat_y*size_X))*graph_size) + ((cheese_x+(cheese_y*size_X))*graph_size*graph_size) 
#define TO_INDEX(x, y, size_X) (x + ((y)*size_X))
#define X_VALUE(index, size_X) ((index) % size_X)
#define Y_VALUE(index, size_X) ((index) / size_X);



	Starter code: F.J.E. Jan. 16
*/

#include "QLearn.h"


 /*
   This function implementes the Q-Learning update as stated in Lecture. It 
   receives as input a <s,a,r,s'> tuple, and updates the Q-table accordingly.
   
   Your work here is to calculate the required update for the Q-table entry
   for state s, and apply it to the Q-table
     
   The update involves two constants, alpha and lambda, which are defined in QLearn.h - you should not 
   have to change their values. Use them as they are.
     
   Details on how states are used for indexing into the QTable are shown
   below, in the comments for QLearn_action. Be sure to read those as well!
 */
 
  /***********************************************************************************************
   * TO DO: Complete this function
   ***********************************************************************************************/
int my_graph_size = 0;
int queue_size = 0;
int set_size = 0;
// variables to hold graph data
int distance[max_graph_size][max_graph_size];
int distances_set = 0;
int my_size_X = 0;
int seeded = 0;


void QLearn_update(int s, int a, double r, int s_new, double *QTable)
{

  double max = -INFINITY;
  double c;
  for (int i = 0; i < 4; i ++) {
    c = *(QTable+ (4*s_new)+i);
    if (c > max) {
      max = c;
    }
  }

  *(QTable+(4*s)+a) =  *(QTable+(4*s)+a) +  alpha * (r + lambda*(max) - *(QTable+(4*s)+a) );
}

/*
     This function decides the action the mouse will take. It receives as inputs
     - The graph - so you can check for walls! The mouse must never move through walls
     - The mouse position
     - The cat position
     - The chees position
     - A 'pct' value in [0,1] indicating the amount of time the mouse uses the QTable to decide its action,
       for example, if pct=.25, then 25% of the time the mouse uses the QTable to choose its action,
       the remaining 75% of the time it chooses randomly among the available actions.
       
     Remember that the training process involves random exploration initially, but as training
     proceeds we use the QTable more and more, in order to improve our QTable values around promising
     actions.
     
     The value of pct is controlled by QLearn_core_GL, and increases with each round of training.
     
     This function *must return* an action index in [0,3] where
        0 - move up
        1 - move right
        2 - move down
        3 - move left
        
     QLearn_core_GL will print a warning if your action makes the mouse cross a wall, or if it makes
     the mouse leave the map - this should not happen. If you see a warning, fix the code in this
     function!
     
   The Q-table has been pre-allocated and initialized to 0. The Q-table has
   a size of
   
        graph_size^3 x 4
        
   This is because the table requires one entry for each possible state, and
   the state is comprised of the position of the mouse, cat, and cheese. 
   Since each of these agents can be in one of graph_size positions, all
   possible combinations yield graph_size^3 states.
   
   Now, for each state, the mouse has up to 4 possible moves (up, right,
   down, and left). We ignore here the fact that some moves are not possible
   from some states (due to walls) - it is up to the QLearn_action() function
   to make sure the mouse never crosses a wall. 
   
   So all in all, you have a big table.
        
   For example, on an 8x8 maze, the Q-table will have a size of
   
       64^3 x 4  entries
       
       with 
       
       size_X = 8		<--- size of one side of the maze
       graph_size = 64		<--- Total number of nodes in the graph
       
   Indexing within the Q-table works as follows:
   
     say the mouse is at   i,j
         the cat is at     k,l
         the cheese is at  m,n
         
     state = (i+(j*size_X)) + ((k+(l*size_X))*graph_size) + ((m+(n*size_X))*graph_size*graph_size)
     ** Make sure you undestand the state encoding above!
     
     Entries in the Q-table for this state are

     *(QTable+(4*state)+a)      <-- here a is the action in [0,3]
     
     (yes, it's a linear array, no shorcuts with brackets!)
     
     NOTE: There is only one cat and once cheese, so you only need to use cats[0][:] and cheeses[0][:]
   */
  
int QLearn_action(double gr[max_graph_size][4], int mouse_pos[1][2], int cats[5][2], int cheeses[5][2], double pct, double *QTable, int size_X, int graph_size)
{
  int a = random_action(gr, mouse_pos, pct, size_X);
   if (a > -1) {
     return a;
     
   } else {
      // current optimal action
      int s = TO_STATE(mouse_pos[0][0], mouse_pos[0][1], cats[0][0], cats[0][1], cheeses[0][0], cheeses[0][1], size_X, graph_size);
      int index = TO_INDEX(mouse_pos[0][0], mouse_pos[0][1], size_X);
      double max = -INFINITY;
      double c;
      int optimal_action = -1;
      for (int i = 0; i < 4; i ++) {
        if (gr[index][i]) {
          c = *(QTable+ (4*s)+i);
          if (c > max) {
            max = c;
            optimal_action = i;
          }
        } 
      }
      return optimal_action;
   }
}

double QLearn_reward(double gr[max_graph_size][4], int mouse_loc[1][2], int cat_loc[5][2], int cheese_loc[5][2], int size_X, int graph_size)
{

  if (distances_set == 0) {
    my_graph_size = graph_size;
    queue_size = graph_size;
    set_size = graph_size;
    my_size_X = size_X; 
    set_distances(gr);
    distances_set = 1;
  }

  int ret_min =0;
  int ret_max = 0;
  double min = 0;
  double max = 0;

  int cat_dist = 0;
  float cheese_dist = INFINITY;
  int dead_end = 4;
  double distance_from_center = 0;
  /*
    This function computes and returns a reward for the state represented by the input mouse, cat, and
    cheese position. 
    
    You can make this function as simple or as complex as you like. But it should return positive values
    for states that are favorable to the mouse, and negative values for states that are bad for the 
    mouse.
    
    I am providing you with the graph, in case you want to do some processing on the maze in order to
    decide the reward. 
        
    This function should return a maximim/minimum reward when the mouse eats/gets eaten respectively.      
   */

   /***********************************************************************************************
   * TO DO: Complete this function
   ***********************************************************************************************/ 
   // Check for cats having lunch
   int cats = 1;
   int cheeses = 1;
    for (int i=0; i<cats; i++)
      if (mouse_loc[0][0]==cat_loc[i][0]&&mouse_loc[0][1]==cat_loc[i][1]) ret_min = 1;

    // Check for mouse having lunch
    for (int i=0; i<cheeses; i++)
      if (mouse_loc[0][0]==cheese_loc[i][0]&&mouse_loc[0][1]==cheese_loc[i][1]) ret_max = 1;

    // reward processing
    if (!ret_min && !ret_max) {
          int mouse_index = TO_INDEX(mouse_loc[0][0], mouse_loc[0][1], size_X);
      
    for (int i = 0; i < cats; i ++ ) {
      int cat_index = TO_INDEX(cat_loc[i][0], cat_loc[i][1], size_X);
      cat_dist += distance[mouse_index][cat_index];
    }

    // pick the closest cheese to minimize the distance of
    for (int i = 0; i < cheeses; i ++ ) {
      int cheese_index = TO_INDEX(cheese_loc[i][0], cheese_loc[i][1],size_X);
      int new_dist = distance[mouse_index][cheese_index];
      if (new_dist < cheese_dist) {
        cheese_dist = new_dist;
      }
      }

      dead_end = 4;
      for (int i = 0; i < 4; i ++) {
        dead_end -= gr[mouse_index][i];
      }

      // optional scaling value for dead end value
      // the higher the value, the less options the mouse has for escape
      dead_end *= size_X;
    }

    
    distance_from_center = euclidian_distance(mouse_loc[0][0], mouse_loc[0][1], size_X/2, size_X/2);
    // distance_from_center *= size_X;

    

    double reward = 0;

    // 83% success rate 
    // reward = cat_dist - (cheese_dist + 1) - dead_end;
    // min= -graph_size  -1 - 4*size_X
    // max= graph_size
    
    // 91% success rate 
    // reward = cat_dist - (cheese_dist + 1);
    // min= -graph_size -1;
    // max= graph_size;

		// 94% sucess rate
     //reward = (graph_size * (cat_dist / cheese_dist)) - dead_end;
     // min = 0;
     // max = graph_size * graph_size;

     // 94% sucess rate
     reward = (graph_size * (cat_dist / cheese_dist)) - dead_end - distance_from_center;
     min = -graph_size;
     max = graph_size * graph_size * graph_size;

     // 93% sucess rate
     // reward = (graph_size * ((cat_dist + 1) / cheese_dist)) - dead_end;
     // min = 0;
     // max = graph_size * graph_size;

     // 93% sucess rate
     // reward = (graph_size * (cat_dist / (cheese_dist + 1))) - dead_end;
     // min = 0;
     // max = graph_size * graph_size;

    // 86% success rate
    // reward = (graph_size - (cheese_dist * 1.1)) + cat_dist;
    // min = -graph_size
    // max = graph_size * 2

    // printf("mouse_loc (%d, %d) cat_loc(%d, %d) cheese_loc(%d, %d), reward %f\n", mouse_loc[0][0], mouse_loc[0][1], cat_loc[0][0], cat_loc[0][1], cheese_loc[0][0], cheese_loc[0][1], reward);
    // printf("%f ", cheese_dist);
    // printf("reward: %f\n", reward);
    if (ret_max) {
      return max;
    } else if (ret_min) {
      return min;
    } 

    return reward;
}

/*
    This function performs the Q-learning adjustment to all the weights associated with your
    features. Unlike standard Q-learning, you don't receive a <s,a,r,s'> tuple, instead,
    you receive the current state (mouse, cats, and cheese potisions), and the reward 
    associated with this action (this is called immediately after the mouse makes a move,
    so implicit in this is the mouse having selected some action)
    
    Your code must then evaluate the update and apply it to the weights in the weight array.    
   */
void feat_QLearn_update(double gr[max_graph_size][4], double weights[25], double reward, int mouse_pos[1][2], int cats[5][2], int cheeses[5][2], int size_X, int graph_size)
{
   double features[25];
  evaluateFeatures(gr, features, mouse_pos, cats, cheeses, size_X, graph_size);
  int qsa = Qsa(weights, features);
  int maxA = 0;
  double maxU = 0;
  maxQsa(gr, weights, mouse_pos, cats, cheeses, size_X, graph_size, &maxU, &maxA);
  for (int i = 0; i < numFeatures; i ++) {
    weights[i] += alpha * ((reward + lambda * (maxU) - qsa))* features[i];
    // printf("w[%d], %f \t", i, weights[i]);
  }
  // printf("\n");
}

  /*
    Similar to its counterpart for standard Q-learning, this function returns the index of the next
    action to be taken by the mouse.
    
    Once more, the 'pct' value controls the percent of time that the function chooses an optimal
    action given the current policy.
    
    E.g. if 'pct' is .15, then 15% of the time the function uses the current weights and chooses
    the optimal action. The remaining 85% of the time, a random action is chosen.
    
    As before, the mouse must never select an action that causes it to walk through walls or leave
    the maze.    
   */  
int feat_QLearn_action(double gr[max_graph_size][4],double weights[25], int mouse_pos[1][2], int cats[5][2], int cheeses[5][2], double pct, int size_X, int graph_size)
{
  int a = random_action(gr, mouse_pos, pct, size_X);
   if (a > -1) {
     return a;
   } else {
      // current optimal action
      double maxU = 0;
      int maxA =-1;
      maxQsa(gr, weights, mouse_pos, cats, cheeses, size_X, graph_size, &maxU, &maxA);
      // printf("The max action is %d\n", maxA);
      return maxA;
   }
}

void evaluateFeatures(double gr[max_graph_size][4],double features[25], int mouse_loc[1][2], int cat_loc[5][2], int cheese_loc[5][2], int size_X, int graph_size)
{
  /*
   This function evaluates all the features you defined for the game configuration given by the input
   mouse, cats, and cheese positions. You are free to define up to 25 features. This function will
   evaluate each, and return all the feature values in the features[] array.
   
   Take some time to think about what features would be useful to have, the better your features, the
   smarter your mouse!
   
   Note that instead of passing down the number of cats and the number of cheese chunks (too many parms!)
   the arrays themselves will tell you what are valid cat/cheese locations.
   
   You can have up to 5 cats and up to 5 cheese chunks, and array entries for the remaining cats/cheese
   will have a value of -1 - check this when evaluating your features!
  */


  if (distances_set == 0) {
    my_graph_size = graph_size;
    queue_size = graph_size;
    set_size = graph_size;
    my_size_X = size_X; 
    set_distances(gr);
    distances_set = 1;
  }

  int cat_dist = 0;
  float cheese_dist = INFINITY;
  int dead_end = 4;
  double distance_from_center = 0;

   int cats = 5;
   int cheeses = 5;

    int mouse_index = TO_INDEX(mouse_loc[0][0], mouse_loc[0][1], size_X);
      
    int num_cats = 0;
    for (int i = 0; i < cats && cat_loc[i][0] != -1; i ++ ) {
      int cat_index = TO_INDEX(cat_loc[i][0], cat_loc[i][1], size_X);
      cat_dist += distance[mouse_index][cat_index];
      num_cats ++;
    }


    // pick the closest cheese to minimize the distance of
    for (int i = 0; i < cheeses && cheese_loc[i][0] != -1; i ++ ) {
      int cheese_index = TO_INDEX(cheese_loc[i][0], cheese_loc[i][1],size_X);
      int new_dist = distance[mouse_index][cheese_index];
      if (new_dist < cheese_dist) {
        cheese_dist = new_dist;
      }
    }

    for (int i = 0; i < 4; i ++) {
      dead_end -= gr[mouse_index][i];
    }
    // optional scaling value for dead end value
    // the higher the value, the less options the mouse has for escape
    
    distance_from_center = euclidian_distance(mouse_loc[0][0], mouse_loc[0][1], size_X/2, size_X/2);
    // distance_from_center *= size_X;

    // to break deadlocks
    double randomness = rand() % 100;
    if (rand() % 2) { // coin flip, flip value 
      randomness *= 1;
    }

    features[0] = cheese_dist / graph_size;
    features[1] = cat_dist / (num_cats * graph_size);
    features[2] = dead_end / 4;
    features[3] = distance_from_center / ((graph_size /2) + 1);
    features[4] = ((rand() % 100) / 100);

}

double Qsa(double weights[25], double features[25])
{
  /*
    Compute and return the Qsa value given the input features and current weights
   */

  /***********************************************************************************************
  * TO DO: Complete this function
  ***********************************************************************************************/  
  double sum = 0;
  for (int i = 0; i < numFeatures; i++){
    sum += weights[i]*features[i];
  }

  // printf("za sum is... %f", sum);
  //printf("the sum is %f", sum);
  return(sum);		// <--- stub! compute and return the Qsa value
}

 /*
   Given the state represented by the input positions for mouse, cats, and cheese, this function evaluates
   the Q-value at all possible neighbour states and returns the max. The maximum value is returned in maxU
   and the index of the action corresponding to this value is returned in maxA.
   
   You should make sure the function does not evaluate moves that would make the mouse walk through a
   wall. 
  */
void maxQsa(double gr[max_graph_size][4],double weights[25],int mouse_pos[1][2], int cats[5][2], int cheeses[5][2], int size_X, int graph_size, double *maxU, int *maxA)
{
 
  double max = -INFINITY;
  double features[25];
  int mouse_index = TO_INDEX(mouse_pos[0][0], mouse_pos[0][1], size_X);
  int temp_mouse[1][2];
  
  // for the current state s
  for (int i = 0; i < 4; i ++) {
    
    // for each action i
    if (gr[mouse_index][i]) {
      temp_mouse[0][0] = mouse_pos[0][0];
      temp_mouse[0][1] = mouse_pos[0][1];

      if (i == 0) {
        temp_mouse[0][1] -= 1;
      } else if (i == 1) {
        temp_mouse[0][0] += 1;
      } else if (i == 2) {
        temp_mouse[0][1] += 1;
      } else if (i == 3) {
        temp_mouse[0][0] -= 1;
      } 

      // compute the feature values after the action has been taken
      evaluateFeatures(gr, features, temp_mouse, cats, cheeses, size_X, graph_size);
      // compute q(s_i) - the resulting state after s_i
      double q_si = Qsa(weights, features);
      // choose the s_i that results in the maximal q(s_i)

      
      if (max == -INFINITY || q_si >= max) {
        max = q_si;
        *maxU = max;
        *maxA = i;
      }
    }
  }

  // printf("the v of max q_si is %f\n", *maxU);
  // printf("the v of maxA is %d\n", *maxA);

  return;
}

int random_action(double gr[max_graph_size][4], int mouse_pos[1][2], double pct, int size_X) {

  if (!seeded) {
    time_t t;

     /* Intializes random number generator */
     srand((unsigned) time(&t));
    seeded = 1;
  }
  
   int c = rand() % 100;   
   int index = TO_INDEX(mouse_pos[0][0], mouse_pos[0][1], size_X);
   if ( c >= pct * 100) {
     
     // random action
     while (1) {
       int action;
       action = rand() % 4;
       if (gr[index][action]) {
         return action;
       }
     }
   } 
   return -1;


}

int euclidian_distance(int x1, int y1, int x2, int y2) {
    double x = x2 - x1;
    double y = y2 - y1;
    double d = sqrt( pow(x, 2) + pow(y, 2));
    d = floor(d);
    int ret = d;
    return ret;
}


int connected_index(int index, int direction) {
    int x = X_VALUE(index, my_size_X);
    int y = Y_VALUE(index, my_size_X);
    if (direction == 0) {
        y --;
    } else if (direction == 1) {
        x ++;
    } else if (direction == 2) {
        y ++;
    } else if (direction == 3) {
        x --;
    }

    if (x < 0 || y < 0 || x >= my_size_X || y >= my_size_X) {
        printf("incorrect value of (%d, %d) at index %d in direction %d\n", x, y, index, direction);
        exit(1);
    }

    return TO_INDEX(x, y, my_size_X);
}

// a very similar copy of BFS that finds and sets the distance for all values in the graph using the distance array.
void set_distances(double graph[][4]) {
    

	for (int j = 0; j < my_graph_size; j++)
	{
		/* code */
		int priority_queue[max_graph_size][2];
		init_queue(priority_queue);

		int seen[max_graph_size];
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

void init_seen(int *seen) {
    for (int i = 0; i < my_graph_size; i++) 
    {
        seen[i] = -1;
    }
}

void init_queue(int q[][2]) {
    for (int i = 0; i < queue_size; i ++) 
    {
        q[i][0] = -1;
        q[i][1] = my_graph_size + 1;
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

void add_to_set(int *s, int value) {
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

int set_contains(int *s, int value) {
    for (int i = 0; i < set_size; i ++) {
        if (s[i] == value) {
            return 1;
        }
    }
    return 0;
}

int get_next(int q[][2]){
	int minimum_priority = my_graph_size + 1;
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
	q[index][1] = my_graph_size + 1;
	return ret_index;;
}


/***************************************************************************************************
 *  Add any functions needed to compute your features below 
 *                 ---->  THIS BOX <-----
 * *************************************************************************************************/
