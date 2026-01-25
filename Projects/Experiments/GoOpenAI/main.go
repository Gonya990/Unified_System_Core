package main

import (
	"context"
	"fmt"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
	client := openai.NewClient(
		option.WithAPIKey("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"), 
	)

	resp, err := client.Responses.New(context.TODO(), openai.ResponseNewParams{
		Model: "gpt-5-nano",
		Input: responses.ResponseNewParamsInputUnion{OfString: openai.String("Say this is a test")},
	})
	if err != nil {
		panic(err.Error())
	}

	fmt.Println(resp.OutputText())
}
