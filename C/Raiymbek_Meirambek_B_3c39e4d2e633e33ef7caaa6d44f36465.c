#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <dirent.h>

#define MAX_FILENAME_LENGTH 100
#define MAX_LINE_LENGTH 512
#define SEARCH_STRING_1 "CSCI332"
#define SEARCH_STRING_2 "OS"

// To store thread-specific information
struct ThreadData
{
    char filename[MAX_FILENAME_LENGTH];
};

// Function created to search for a string
void *strSearch(void *arg)
{
    struct ThreadData *threadData = (struct ThreadData *)arg;

    FILE *file = fopen(threadData->filename, "r");
    if (file == NULL)
    {
        perror("Opening file failure!");
        pthread_exit(NULL);
    }

    char line[MAX_LINE_LENGTH];
    int lineNumber = 1;

    // String search
    while (fgets(line, sizeof(line), file) != NULL)
    {
        if (strstr(line, SEARCH_STRING_1) != NULL)
        {
            // Process when string is found
            printf("Thread found '%s' in file: %s at line: %d\n", SEARCH_STRING_1, threadData->filename, lineNumber);
	    //Close
            fclose(file);
	    //and Exit
            pthread_exit(NULL);
        }
	lineNumber++;
    }

    // Reset the pointer
    rewind(file);
    lineNumber = 0;

    // Search for the second string
    while (fgets(line, sizeof(line), file) != NULL)
    {
        lineNumber++;
        if (strstr(line, SEARCH_STRING_2) != NULL)
        {
            // Second string found
            printf("Thread found '%s' in file: %s at line: %d\n", SEARCH_STRING_2, threadData->filename, lineNumber);
        }
    }

    fclose(file);
    pthread_exit(NULL);
}

int main()
{
    // Locating 'my_files' as a directory
    const char *directory = "my_files";

    // Open the directory
    DIR *dir = opendir(directory);
    //Error message
    if (!dir)
    {
        perror("Error opening directory");
        exit(EXIT_FAILURE);
    }

    struct dirent *entry;

    // Iterating through files
    while (!((entry = readdir(dir)) == NULL))
    {
        if (entry->d_type == DT_REG)
        { 
            pthread_t threadID;
            struct ThreadData threadData;

            // Constructing path for the file
            snprintf(threadData.filename, MAX_FILENAME_LENGTH, "%s/%s", directory, entry->d_name);

            // Creating a thread 
            if (!(pthread_create(&threadID, NULL, strSearch, (void *)&threadData) == 0))
            {
		//Error message
                perror("Failure of creating thread");
                closedir(dir);
                exit(EXIT_FAILURE);
		//Closing and exiting
            }

            // Waiting for the thread to finish
            pthread_join(threadID, NULL);

	    //Cleanup
	    cleanupThread(threadID);
        }
    }

    closedir(dir);
    //Close the directory

    return 0;
}