package executor

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

type OKXClient struct {
	APIKey     string
	SecretKey  string
	Passphrase string
	BaseURL    string
	HTTPClient *http.Client
}

type OKXTickerResponse struct {
	Code string `json:"code"`
	Msg  string `json:"msg"`
	Data []struct {
		Last string `json:"last"`
	} `json:"data"`
}

func NewOKXClient() *OKXClient {
	return &OKXClient{
		APIKey:     os.Getenv("OKX_API_KEY"),
		SecretKey:  os.Getenv("OKX_API_SECRET"),
		Passphrase: os.Getenv("OKX_PASSPHRASE"),
		BaseURL:    "https://www.okx.com",
		HTTPClient: &http.Client{Timeout: 10 * time.Second},
	}
}

func (c *OKXClient) Sign(method, requestPath, body, timestamp string) string {
	message := timestamp + method + requestPath + body
	h := hmac.New(sha256.New, []byte(c.SecretKey))
	h.Write([]byte(message))
	return base64.StdEncoding.EncodeToString(h.Sum(nil))
}

func (c *OKXClient) Request(method, path, body string) ([]byte, error) {
	if c.APIKey == "" {
		return nil, fmt.Errorf("OKX credentials missing")
	}

	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05.000Z")
	url := c.BaseURL + path
	
	req, err := http.NewRequest(method, url, nil)
	if err != nil {
		return nil, err
	}

	if body != "" {
		// handle body reader if needed
	}

	signature := c.Sign(method, path, body, timestamp)

	req.Header.Set("OK-ACCESS-KEY", c.APIKey)
	req.Header.Set("OK-ACCESS-SIGN", signature)
	req.Header.Set("OK-ACCESS-TIMESTAMP", timestamp)
	req.Header.Set("OK-ACCESS-PASSPHRASE", c.Passphrase)
	req.Header.Set("Content-Type", "application/json")

	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	return io.ReadAll(resp.Body)
}

func (c *OKXClient) GetTicker(instId string) (float64, error) {
	path := fmt.Sprintf("/api/v5/market/ticker?instId=%s", instId)
	url := c.BaseURL + path

	resp, err := c.HTTPClient.Get(url)
	if err != nil {
		return 0, err
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return 0, err
	}

	var tickerResp OKXTickerResponse
	if err := json.Unmarshal(body, &tickerResp); err != nil {
		return 0, err
	}

	if tickerResp.Code != "0" || len(tickerResp.Data) == 0 {
		return 0, fmt.Errorf("OKX error: %s", tickerResp.Msg)
	}

	var price float64
	fmt.Sscanf(tickerResp.Data[0].Last, "%f", &price)
	return price, nil
}

func (c *OKXClient) GetOrderbook(instId string) (map[string]interface{}, error) {
	// Mock/Simple implementation for now as per Issue 009 requirements
	// Real implementation would parse JSON and calculate slippage
	return nil, nil
}
