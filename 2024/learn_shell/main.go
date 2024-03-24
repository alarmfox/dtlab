package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"path/filepath"

	"github.com/fsnotify/fsnotify"
)

func main() {
	// Setup game environment
	setupGameEnvironment()

	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		fmt.Println("ERROR", err)
		return
	}
	defer watcher.Close()

	done := make(chan bool)

	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				handleEvent(event)

			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				fmt.Println("ERROR", err)
			}
		}
	}()

	// Add game_data directory to the watcher
	err = watcher.Add("game_data")
	if err != nil {
		fmt.Println("ERROR", err)
		return
	}
	fmt.Println("Game started. Follow the instructions in game_data/instructions.txt.")

	<-done // Run until the program is terminated
}

func handleEvent(event fsnotify.Event) {
	// Check for specific events here, e.g., file created, modified, etc.
	if event.Op&fsnotify.Create == fsnotify.Create {
		fmt.Println("Detected creation:", event.Name)
		// Verify task completion and generate token if successful
		if filepath.Base(event.Name) == "level1" || filepath.Base(event.Name) == "task.txt" {
			token := generateToken()
			fmt.Printf("Task completed! Your token: %s\n", token)
		}
	}
	// Add more conditions as needed for different tasks
}

func generateToken() string {
	byteArray := make([]byte, 10) // generates a token of 20 characters
	_, err := rand.Read(byteArray)
	if err != nil {
		fmt.Println("ERROR generating token:", err)
		return ""
	}
	return hex.EncodeToString(byteArray)
}

func setupGameEnvironment() error {
    // Create a game_data directory
    dirPath := "game_data"
    if err := os.Mkdir(dirPath, 0755); err != nil {
        return err
    }

    // Create an instructions file with initial tasks
    instructions := `Welcome to the Shell Game!
Your tasks:
1. Create a directory inside game_data named 'level1'.
2. Inside 'level1', create a file named 'task.txt' and write 'Shell Game' in it.
3. Change the permissions of 'task.txt' to read-only.
4. Find the hidden message in '.secret' and write it to 'secret_message.txt' in 'game_data'.

Good luck!
`
    if err := os.WriteFile(fmt.Sprintf("%s/instructions.txt", dirPath), []byte(instructions), 0644); err != nil {
        return err
    }

    // Create a hidden file with a secret message
    secretMessage := "The secret of the shell is exploration."
    if err := os.WriteFile(fmt.Sprintf("%s/.secret", dirPath), []byte(secretMessage), 0644); err != nil {
        return err
    }

    return nil
}

