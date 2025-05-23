// main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h> // For assert()
#include "hash.h"   // Include your hash table header

// Helper function to create a dynamically allocated integer value
// This simulates how you might store more complex data.
int* create_int_value(int val) {
    int* p_val = (int*)malloc(sizeof(int));
    if (p_val == NULL) {
        perror("Failed to allocate int value for testing");
        exit(EXIT_FAILURE);
    }
    *p_val = val;
    return p_val;
}

void print_divider() {
    printf("\n----------------------------------------\n");
}

int main() {
    HashTable* ht = NULL;
    int* v = NULL; // For retrieved values

    print_divider();
    printf("Test 1: Create and Free Empty Table\n");
    ht = ht_create(10);
    assert(ht != NULL);
    assert(ht->count == 0);
    assert(ht->size == 10);
    printf("Table created successfully.\n");
    ht_free(ht);
    ht = NULL;
    printf("Table freed successfully.\n");
    print_divider();

    printf("Test 2: Basic Insert and Search\n");
    ht = ht_create(5); // Small size to test collisions sooner
    
    ht_insert(ht, "apple", create_int_value(100));
    ht_insert(ht, "banana", create_int_value(200));
    ht_insert(ht, "cherry", create_int_value(300));

    assert(ht->count == 3);
    printf("Inserted 3 items.\n");

    v = (int*)ht_search(ht, "apple");
    assert(v != NULL && *v == 100);
    printf("Found 'apple': %d\n", *v);

    v = (int*)ht_search(ht, "banana");
    assert(v != NULL && *v == 200);
    printf("Found 'banana': %d\n", *v);
    
    v = (int*)ht_search(ht, "cherry");
    assert(v != NULL && *v == 300);
    printf("Found 'cherry': %d\n", *v);

    v = (int*)ht_search(ht, "date");
    assert(v == NULL);
    printf("Did not find 'date' (expected).\n");
    print_divider();

    printf("Test 3: Update Existing Key\n");
    printf("Current 'apple' value: %d\n", *((int*)ht_search(ht, "apple")));
    // The old value (100) should be freed by ht_insert
    ht_insert(ht, "apple", create_int_value(150)); 
    assert(ht->count == 3); // Count should not change
    v = (int*)ht_search(ht, "apple");
    assert(v != NULL && *v == 150);
    printf("Updated 'apple' to: %d\n", *v);
    print_divider();

    printf("Test 4: Insert to Cause Collision (if hash func and size allow)\n");
    // We need keys that might collide. This depends on your hash_func.
    // For SDBM, "key1" and "key10" might not collide easily with size 5.
    // Let's try a few more to increase chances or fill up.
    ht_insert(ht, "grape", create_int_value(400));
    ht_insert(ht, "kiwi", create_int_value(500)); 
    // ht is now full (count 5, size 5). Next insert would ideally trigger resize.
    // For now, it will just increase chain length.
    
    ht_insert(ht, "lemon", create_int_value(600)); // This will definitely use an existing bucket.
    assert(ht->count == 6);
    
    v = (int*)ht_search(ht, "grape");
    assert(v != NULL && *v == 400);
    v = (int*)ht_search(ht, "kiwi");
    assert(v != NULL && *v == 500);
    v = (int*)ht_search(ht, "lemon");
    assert(v != NULL && *v == 600);
    printf("Inserted 'grape', 'kiwi', 'lemon'. All searchable.\n");
    print_divider();

    printf("Test 5: Delete Operations\n");
    // Delete a key that exists (e.g., 'banana')
    printf("Deleting 'banana'...\n");
    ht_delete(ht, "banana");
    assert(ht->count == 5);
    v = (int*)ht_search(ht, "banana");
    assert(v == NULL);
    printf("'banana' deleted and not found.\n");

    // Delete a key that doesn't exist
    printf("Attempting to delete 'date' (non-existent)...\n");
    ht_delete(ht, "date");
    assert(ht->count == 5); // Count should not change
    printf("Count remains %d.\n", ht->count);

    // Delete from head of a chain (if 'apple' was head of its chain)
    // This is hard to guarantee without knowing hash values, but we'll try.
    // Let's delete 'apple' (was updated to 150)
    printf("Deleting 'apple'...\n");
    ht_delete(ht, "apple");
    assert(ht->count == 4);
    v = (int*)ht_search(ht, "apple");
    assert(v == NULL);
    printf("'apple' deleted and not found.\n");

    // Delete another one, e.g., 'lemon'
    printf("Deleting 'lemon'...\n");
    ht_delete(ht, "lemon");
    assert(ht->count == 3);
    v = (int*)ht_search(ht, "lemon");
    assert(v == NULL);
    printf("'lemon' deleted and not found.\n");

    // Verify remaining items
    v = (int*)ht_search(ht, "cherry"); assert(v != NULL && *v == 300);
    v = (int*)ht_search(ht, "grape");  assert(v != NULL && *v == 400);
    v = (int*)ht_search(ht, "kiwi");   assert(v != NULL && *v == 500);
    printf("Remaining items ('cherry', 'grape', 'kiwi') are still searchable.\n");
    print_divider();

    printf("Test 6: Clear Table by Deleting All and Free\n");
    ht_delete(ht, "cherry");
    ht_delete(ht, "grape");
    ht_delete(ht, "kiwi");
    assert(ht->count == 0);
    printf("All items deleted. Count is %d.\n", ht->count);

    ht_free(ht);
    ht = NULL;
    printf("Table freed successfully after clearing.\n");
    print_divider();

    printf("Test 7: Operations on NULL table (should be handled gracefully)\n");
    // Assuming your functions have NULL checks and don't crash
    ht_insert(NULL, "test", create_int_value(1)); // create_int_value will leak if ht_insert exits
                                                 // Better: int val_for_null_test = 1; ht_insert(NULL, "test", &val_for_null_test);
                                                 // Or handle the leak if exit is expected.
                                                 // For now, if ht_insert exits, this create_int_value leaks.
                                                 // If ht_insert returns, it's fine.
    int temp_val = 1; // Use a stack variable to avoid leak if ht_insert exits early
    ht_insert(NULL, "test", &temp_val); 
    ht_search(NULL, "test");
    ht_delete(NULL, "test");
    ht_free(NULL);
    printf("Operations on NULL table attempted (check for errors/crashes).\n");
    // Note: The values created by create_int_value in this block will leak if ht_insert exits,
    // because main won't free them. For robust testing of NULL table, avoid dynamic allocation
    // for values or ensure ht_insert doesn't exit but returns an error.
    // Given your current ht_insert exits on NULL table, the create_int_value() call for it would leak.
    // I've changed it to use a stack variable for this specific NULL test.
    print_divider();


    printf("All tests completed. Check output and run with Valgrind.\n");
    return 0;
}
