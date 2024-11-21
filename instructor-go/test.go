// package main

// import (
// 	"context"
// 	"fmt"
// 	"os"

// 	"github.com/joho/godotenv"
// 	"github.com/liushuangls/go-anthropic/v2"

// 	"github.com/instructor-ai/instructor-go/pkg/instructor"
// )

// type Person struct {
// 	Name  string `json:"name"          jsonschema:"title=the name,description=The name of the person,example=joe,example=lucy"`
// 	Age   int    `json:"age,omitempty" jsonschema:"title=the age,description=The age of the person,example=25,example=67"`
// 	Adult bool   `json:"adult"         jsonschema:"title=is adult,description=Is the person an adult"`
// }

// // Method to return the person's details as a string
// func (p *Person) String() string {
// 	return fmt.Sprintf("Name: %s, Age: %d", p.Name, p.Age)
// }

// // Method to check if the person is an adult
// func (p *Person) IsAdult() bool {
// 	return p.Age >= 50
// }

// func test() {
// 	ctx := context.Background()
// 	err := godotenv.Load()
// 	if err != nil {
// 		panic(err)
// 	}

// 	// print functions on Person Schema

// 	client, err := instructor.FromAnthropic[Person](
// 		anthropic.NewClient(os.Getenv("ANTHROPIC_API_KEY")),
// 		instructor.WithMode(instructor.ModeJSONSchema),
// 		instructor.WithMaxRetries(5),
// 	)
// 	if err != nil {
// 		panic(err)
// 	}

// 	person, err := client.CreateChatCompletion(
// 		ctx,
// 		instructor.Request{
// 			Model: "claude-3-haiku-20240307",
// 			Messages: []instructor.Message{
// 				{
// 					Role:    instructor.RoleUser,
// 					Content: "Hello, I am a human",
// 				},
// 				{
// 					Role:    instructor.RoleAssistant,
// 					Content: "Hello, I am a machine",
// 				},
// 				{
// 					Role:    instructor.RoleUser,
// 					Content: "Robby is 22 years old, extract if he is an adult, name and age",
// 				},
// 			},
// 		},
// 	)
// 	if err != nil {
// 		panic(err)
// 	}

// 	fmt.Printf(`
// Name: %s
// Age:  %d
// Adult: %t
// `, person.Name, person.Age, person.Adult)
// 	/*
// 	   Name: Robby
// 	   Age:  22
// 	*/
// }
