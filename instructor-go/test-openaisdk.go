package main

import (
	"context"
	"encoding/base64"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"

	"github.com/joho/godotenv"

	openai "github.com/sashabaranov/go-openai"
)

func ImageToBase64(url string) (string, error) {
	resp, err := http.Get(url)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	data, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	return "data:" + resp.Header.Get("Content-Type") + ";base64," + base64.StdEncoding.EncodeToString(data), nil
}

func test() {
	err := godotenv.Load()
	if err != nil {
		panic(err)
	}
	client := openai.NewClient(os.Getenv("OPENAI_API_KEY"))
	image_url := "https://utfs.io/f/5b079e4a-4d4f-4481-823d-86834d8db4bc-6bhxt2.webp"
	resp, err := client.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model: openai.GPT4VisionPreview,
			Messages: []openai.ChatCompletionMessage{
				{
					Role: openai.ChatMessageRoleUser,
					MultiContent: []openai.ChatMessagePart{
						{
							Type: "image_url",
							ImageURL: &openai.ChatMessageImageURL{
								URL: image_url,
							},
						},
					},
				},
			},
		},
	)

	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Printf("Response: %s\n", resp.Choices[0].Message.Content)
}
