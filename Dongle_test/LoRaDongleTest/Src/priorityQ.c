#include <stdio.h>
#include <stdlib.h>
#include "priorityQ.h"

void pushQ(TokenList *list, uint8_t port,uint8_t port_priority)
{
        TokenList *tmp,*rpointer,*lpointer;
        rpointer = list->next;
        lpointer = list;

        tmp=(TokenList*)malloc(sizeof(TokenList));

        tmp->port = port;
        tmp->priority = port_priority;

        while(rpointer != NULL){
                if(rpointer->priority <= port_priority)
                {
                        lpointer = rpointer;
                        rpointer = rpointer->next;
                }
                else
                        break;
        }
        lpointer->next = tmp;
        tmp->next = rpointer;
}

uint8_t popQ(TokenList *list)
{
        uint8_t prt;
        TokenList* tmp=list->next;
        prt=tmp->port;
        list->next=tmp->next;
        free(tmp);
        return prt;
}


//void pushQ(TokenList *list, uint8_t port,uint8_t port_priority)
//{
//	TokenList *tmp,*rpointer,*lpointer;
//	rpointer = list->next;
//	lpointer = list;
//
//	tmp=(TokenList*)malloc(sizeof(TokenList));
//
//	tmp->port = port;
//	tmp->priority = port_priority;
//
//	while(rpointer != NULL){
//		if(rpointer->priority <= port_priority)
//		{
//			lpointer = rpointer;
//			rpointer = rpointer->next;
//		}
//		else
//			break;
//	}
//	lpointer->next = tmp;
//	tmp->next = rpointer;
//}
//
//uint8_t popQ(TokenList **list)
//{
//	uint8_t prt;
//	TokenList* tmp=*list;
//	prt=tmp->port;
//	*list=tmp->next;
//	free(tmp);
//	return prt;
//}

//void del(TokenList *list){


/*
void display(TokenList *list){

while (list != NULL){
	printf("%d\n", list->port);
	list = list->next;
	}
} */

/*
void main(){

	TokenList *list =(TokenList *)malloc(sizeof(TokenList));
	list->next = NULL;
	list->priority = 0;
	list->port = 10;
	pushQ(list, 23,5);

	pushQ(list, 2, 2);

	pushQ(list, 24, 3);
	pushQ(list, 42, 1);

	display(list);

	printf("\n\n");

	printf("Popped first %d \n", popQ(&list));
        printf("Popped next %d \n", popQ(&list));


	display(list);
}*/
