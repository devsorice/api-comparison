#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void flush_and_print(const char *message) {
    printf("%s\n", message);
    fflush(stdout);
}

int main() {
    extern char **environ;

    flush_and_print("Starting the environment variable extraction program...");

    // Open the file for reading the current content
    FILE *fp_read = fopen("/var/www/localhost/htdocs/js/sidebar.js", "r");
    if (fp_read == NULL) {
        perror("Failed to open file for reading");
        flush_and_print("Proceeding to start lighttpd...");
        char *args[] = {"/bin/lighttpd", "-D", "-f", "/lighttpd.conf", NULL};
        execv(args[0], args);
        perror("execv failed");
        return 1;
    }

    // Read the current content into a buffer
    fseek(fp_read, 0, SEEK_END);
    long file_size = ftell(fp_read);
    fseek(fp_read, 0, SEEK_SET);
    char *buffer = malloc(file_size + 1);
    if (buffer == NULL) {
        perror("Failed to allocate memory");
        fclose(fp_read);
        flush_and_print("Proceeding to start lighttpd...");
        char *args[] = {"/bin/lighttpd", "-D", "-f", "/lighttpd.conf", NULL};
        execv(args[0], args);
        perror("execv failed");
        return 1;
    }
    fread(buffer, 1, file_size, fp_read);
    buffer[file_size] = '\0';
    fclose(fp_read);

    flush_and_print("Opened /var/www/localhost/htdocs/js/sidebar.js for reading.");

    // Find the position of /*CRUD*/ in the buffer
    char *crud_pos = strstr(buffer, "/*CRUD*/");
    if (crud_pos == NULL) {
        flush_and_print("/*CRUD*/ not found in the file. File will not be edited.");
        free(buffer);
        flush_and_print("Proceeding to start lighttpd...");
        char *args[] = {"/bin/lighttpd", "-D", "-f", "/lighttpd.conf", NULL};
        execv(args[0], args);
        perror("execv failed");
        return 1;
    }

    flush_and_print("Found /*CRUD*/ in the file.");

    // Open the file for writing the new content
    FILE *fp_write = fopen("/var/www/localhost/htdocs/js/sidebar.js", "w");
    if (fp_write == NULL) {
        perror("Failed to open file for writing");
        free(buffer);
        flush_and_print("Proceeding to start lighttpd...");
        char *args[] = {"/bin/lighttpd", "-D", "-f", "/lighttpd.conf", NULL};
        execv(args[0], args);
        perror("execv failed");
        return 1;
    }

    flush_and_print("Opened /var/www/localhost/htdocs/js/sidebar.js for writing.");

    // Write the environment variables to the file
    for (char **env = environ; *env != 0; env++) {
        char *current = *env;
        if (strncmp(current, "APP_", 4) == 0) {
            char *value = strchr(current, '=');
            if (value != NULL) {
                *value = '\0'; // Null-terminate the variable name
                value++; // Move to the start of the variable value
                fprintf(fp_write, "const %s = \"%s\";\n", current, value);
                flush_and_print("Wrote environment variable to sidebar.js.");
            }
        }
    }

    // Write the remaining content after /*CRUD*/
    fprintf(fp_write, "%s", crud_pos);
    free(buffer);

    fclose(fp_write);
    flush_and_print("Finished writing environment variables to sidebar.js.");

    // Start lighttpd
    flush_and_print("Starting lighttpd...");
    char *args[] = {"/bin/lighttpd", "-D", "-f", "/lighttpd.conf", NULL};
    execv(args[0], args);
    perror("execv failed");
    return 1;
}
