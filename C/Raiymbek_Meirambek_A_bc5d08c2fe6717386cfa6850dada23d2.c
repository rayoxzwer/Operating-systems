#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

#define MAX_COMMAND_LENGTH 100

int runCommand(char *command)
{
    // This is a function to execute a command in a child process
    // Implemented using system() function
    int res = system(command);
    return res;
}
void removeLeadingWhitespace(char **tok) {
    // To remove leading whitespaces from a string
    while (isspace(**tok)) {
        (*tok)++;
    }
}

int main()
{
    while (1)
    {
        // Asking user to enter commands
        printf("Enter commands separated by comma: ");
        char input[MAX_COMMAND_LENGTH];
        fgets(input, sizeof(input), stdin);

        // Separation of commands
        char *tok = strtok(input, ",");
        while (tok != NULL)
        {
            // Creating child process and execute commands
	    // Removing leading Whitespaces
            removeLeadingWhitespace(&tok);

            pid_t pid = fork();

            if (pid < 0)
	    {
                // Error message
                perror("Fork failure");
                exit(EXIT_FAILURE);
            }
	    else if (pid == 0)
            {
                // Child process
                int res = runCommand(tok);
                exit(res);
            }
            
            tok = strtok(NULL, ",");
        }

        // Parent process waits for child processes to finish
        int status;
        while (wait(&status) > 0);
           

        // Check if all commands executed successfully/returned to 0 or failed
        if (WIFEXITED(status) && WEXITSTATUS(status) == 0)
        {
            printf("All commands returned to 0.\n");
        }
        else
        {
            printf("Failure detected of some commands.\n");
        }
    }

    return 0;
}