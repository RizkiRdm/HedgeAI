package executor

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
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

func (c *OKXClient) GetOrderbook(instId string) (map[string]interface{}, error) {
	// Mock/Simple implementation for now as per Issue 009 requirements
	// Real implementation would parse JSON and calculate slippage
	return nil, nil
}
