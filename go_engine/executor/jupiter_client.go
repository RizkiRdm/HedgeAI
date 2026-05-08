package executor

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"
)

type JupiterClient struct {
	BaseURL    string
	HTTPClient *http.Client
}

type JupiterQuoteResponse struct {
	InputMint            string `json:"inputMint"`
	OutputMint           string `json:"outputMint"`
	InAmount             string `json:"inAmount"`
	OutAmount            string `json:"outAmount"`
	PriceImpactPct       string `json:"priceImpactPct"`
	SlippageBps          int    `json:"slippageBps"`
}

func NewJupiterClient() *JupiterClient {
	return &JupiterClient{
		BaseURL:    "https://quote-api.jup.ag/v6",
		HTTPClient: &http.Client{Timeout: 10 * time.Second},
	}
}

func (c *JupiterClient) GetQuote(inputMint, outputMint string, amount int64) (*JupiterQuoteResponse, error) {
	url := fmt.Sprintf("%s/quote?inputMint=%s&outputMint=%s&amount=%d", c.BaseURL, inputMint, outputMint, amount)
	
	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var quoteResp JupiterQuoteResponse
	if err := json.Unmarshal(body, &quoteResp); err != nil {
		return nil, err
	}

	return &quoteResp, nil
}
