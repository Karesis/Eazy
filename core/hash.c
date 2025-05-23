#include "hash.h"

static void free_bucket_chain(HashNode* head);
static size_t get_hash(const char* key, int size);
static HashNode* hn_create(const char* key_original, void* value_ptr);


HashTable* ht_create(int initial_size)
{
    if (initial_size <= 0) {
        fprintf(stderr, "ht_create: initial_size must be positive.\n");
        return NULL;
    }

    HashTable* new_table = (HashTable*)malloc(sizeof(HashTable));
    if (new_table == NULL) {
        perror("ht_create: Failed to malloc HashTable");
        exit(EXIT_FAILURE);
    }
    new_table->count = 0;
    new_table->size = initial_size;
    new_table->buckets = (HashNode**)calloc(initial_size, sizeof(HashNode*));
    if (new_table->buckets == NULL) {
        perror("ht_create: Failed to calloc buckets");
        free(new_table);
        exit(EXIT_FAILURE);
    }
    
    return new_table;
}

void ht_free(HashTable* table)
{
    if (table == NULL) return;
    for (int i = 0; i < table->size; i ++)
        free_bucket_chain(table->buckets[i]);
    free(table->buckets);
    free(table);
}

static void free_bucket_chain(HashNode* head)
{
    HashNode* current = head;
    HashNode* next_node;
    while (current != NULL) {
        next_node = current->next;
        free(current->key);
        free(current->value);
        free(current); 
        current = next_node;
    }
}

unsigned long hash_func(const char* key)
{
    unsigned long hash = 0;
    int c;

    while ((c = *key++)) {
        hash = c + (hash << 6) + (hash << 16) - hash;
    }
    return hash;
}

static size_t get_hash(const char* key, int size)
{
    if (size <= 0) {
        fprintf(stderr, "get_hash: invalid table size %d\n", size);
        return 0; 
    }
    return hash_func(key) % size;
}

void ht_insert(HashTable* table, const char* key, void* value)
{
    if (table == NULL || key == NULL) {
        fprintf(stderr, "ht_insert: NULL table or key\n");
        exit(EXIT_FAILURE); 
    }

    size_t index = get_hash(key, table->size);
    HashNode* current = table->buckets[index];
    while (current != NULL) {
        if (!strcmp(current->key, key)) {
            if (current->value != NULL && current->value != value) {
                free(current->value);
            }
            current->value = value;
            return;
        }
        current = current->next;
    }

    HashNode* new_node = hn_create(key, value);
    new_node->next = table->buckets[index];
    table->buckets[index] = new_node;    
    
    table->count++;
}

static HashNode* hn_create(const char* key_original, void* value_ptr)
{
    HashNode* new_node = (HashNode*)malloc(sizeof(HashNode));
    if (new_node == NULL) {
        perror("hn_create: Failed to malloc HashNode");
        exit(EXIT_FAILURE); 
    }

    new_node->key = strdup(key_original);
    if (new_node->key == NULL) { 
        perror("hn_create: Failed to strdup key");
        free(new_node); 
        exit(EXIT_FAILURE); 
    }
    new_node->value = value_ptr;
    new_node->next = NULL;

    return new_node;
}

void* ht_search(HashTable* table, const char* key)
{
    if (table == NULL || key == NULL) {
        fprintf(stderr, "ht_insert: NULL table or key\n");
        exit(EXIT_FAILURE); 
    }

    size_t index = get_hash(key, table->size);
    HashNode* current = table->buckets[index];
    while (current != NULL) {
        if (!strcmp(current->key, key)) 
            return current->value;
        current = current->next;
    }
    return NULL;
}

void ht_delete(HashTable* table, const char* key)
{
    if (table == NULL || key == NULL) return;

    size_t index = get_hash(key, table->size);
    HashNode* current = table->buckets[index];
    HashNode* prev = NULL;

    while (current != NULL) {
        if (!strcmp(current->key, key)) {
            if (prev == NULL) {
                table->buckets[index] = current->next;
            } else {
                prev->next = current->next;
            }
            free(current->key);

            if (current->value != NULL)
                free(current->value); 

            free(current);
            table->count--;
            return;
        }
        prev = current;
        current = current->next;
    }
}
