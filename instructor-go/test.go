package main

import (
	"context"
	"fmt"
	"os"

	"github.com/joho/godotenv"

	"github.com/instructor-ai/instructor-go/pkg/instructor"
	openai "github.com/sashabaranov/go-openai"
)

type Person struct {
	Name  string `json:"name"          jsonschema:"title=the name,description=The name of the person,example=joe,example=lucy"`
	Age   int    `json:"age,omitempty" jsonschema:"title=the age,description=The age of the person,example=25,example=67"`
	Adult bool   `json:"adult"         jsonschema:"title=is adult,description=Is the person an adult"`
}

// Method to return the person's details as a string
func (p *Person) String() string {
	return fmt.Sprintf("Name: %s, Age: %d", p.Name, p.Age)
}

// Method to check if the person is an adult
func (p *Person) IsAdult() bool {
	return p.Age >= 50
}

func main() {
	ctx := context.Background()
	err := godotenv.Load()
	if err != nil {
		panic(err)
	}

	// print functions on Person Schema

	client, err := instructor.FromOpenAI[Person](
		openai.NewClient(os.Getenv("OPENAI_API_KEY")),
		instructor.WithMode(instructor.ModeToolCall),
		instructor.WithMaxRetries(5),
	)
	if err != nil {
		panic(err)
	}

	for _, function := range client.Schema.Functions {
		fmt.Printf("Function Name: %s, Description: %s\n", function.Name, function.Description)
	}
	person, err := client.CreateChatCompletion(
		ctx,
		instructor.Request{
			Model: openai.GPT4Turbo20240409,
			Messages: []instructor.Message{
				{
					Role:    instructor.RoleUser,
					Content: "Robby is 22 years old, extract if he is an adult, name and age",
				},
			},
		},
	)
	if err != nil {
		panic(err)
	}

	fmt.Printf(`
Name: %s
Age:  %d
Adult: %t
`, person.Name, person.Age, person.Adult)
	/*
	   Name: Robby
	   Age:  22
	*/
}
