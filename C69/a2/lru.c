#include <stdio.h>
#include <assert.h>
#include <unistd.h>
#include <getopt.h>
#include <stdlib.h>
#include "pagetable.h"


extern int memsize;

extern int debug;

extern struct frame *coremap;

// Node 
typedef struct node { 
    int data; 
  
    // current frame number 
    int pageFrameNumber; 
  
    struct node* next; 
  
} Node; 

Node* head;
Node* curr;

/* Page to evict is chosen using the accurate LRU algorithm.
 * Returns the page frame number (which is also the index in the coremap)
 * for the page that is to be evicted.
 */

int lru_evict() {
	int frame;

	//gets rid of head of the list and makes new head
	assert(head != NULL);
	frame = (*head).pageFrameNumber;

	Node* temp = (*head).next;
	free(head);
	head = temp;

	return frame;
}

/* This function is called on each access to a page to update any information
 * needed by the lru algorithm.
 * Input: The page table entry for the page that is being accessed.
 */
void lru_ref(pgtbl_entry_t *p) {

	int frame = (*p).frame >> PAGE_SHIFT;
	
	Node* temp = head;	
	Node* last = NULL;
	//finds the value to place at the end of the and gets
	while ((*temp).pageFrameNumber != frame && temp != curr) {
		last = temp;
		temp = (*temp).next;
	}

	//given last node and the node to replace we can now move the 
	//node to the curr position, and remove pointers to it from previous
	//case where we are moving the head to the end
	if ((*last).next != NULL) {
		//head is now the next item in the list
		head = (*temp).next;
	} //situation where its in the middle of the list
	else {
		//last on now points to the next of the node to replace
		(*last).next = (*temp).next;
	} 

	//the next item at the end of the list
	(*curr).next = temp;
	//replace the pointer of the new end of the list
	(*temp).next = NULL;
	//make the new end of the list
	curr = temp;
	free(temp);
}


/* Initialize any data structures needed for this 
 * replacement algorithm 
 */
void lru_init() {
	head = NULL;
	curr = NULL;
}
