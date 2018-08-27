
#ifndef PRIORITYQ_H_
#define PRIORITYQ_H_

typedef struct _TokenList
{
        uint8_t port;
        uint8_t priority;
        struct _TokenList *next;
}TokenList;


void pushQ(TokenList *list, uint8_t port,uint8_t port_priority);
uint8_t popQ(TokenList *);

#endif /* PRIORITYQ_H_ */
