package executor

import (
	"fmt"
	"io"
	"net/http"
	"time"
)

type JupiterClient struct {
	BaseURL    string
	HTTPClient *http.Client
}

func NewJupiterClient() *JupiterClient {
	return &JupiterClient{
		BaseURL:    "https://quote-api.jup.ag/v6",
		HTTPClient: &http.Client{Timeout: 10 * time.Second},
	}
}

func (c *JupiterClient) GetQuote(inputMint, outputMint string, amount int64) ([]byte, error) {
	url := fmt.Sprintf("%s/quote?inputMint=%s&outputMint=%s&amount=%d", c.BaseURL, inputMint, outputMint, amount)
	
	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	return io.ReadAll(resp.Body)
}
