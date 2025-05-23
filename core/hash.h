#ifndef HASH_H
#define HASH_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct HashNode {
    char* key;
    void* value;
    struct HashNode* next;
} HashNode;

typedef struct HashTable {
    HashNode** buckets;
    int size;
    int count;
} HashTable;

HashTable* ht_create(int initial_size);

void ht_free(HashTable* table);

unsigned long hash_func(const char* key);

void ht_insert(HashTable* table, const char* key, void* value);

void* ht_search(HashTable* table, const char* key);

void ht_delete(HashTable* table, const char* key); 

#endif // HASH_H
