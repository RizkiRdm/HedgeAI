package executor

import (
	"context"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"time"

	pb "cryptohedge/go_engine/proto"
)

type ExecutionService struct {
	pb.UnimplementedExecutionEngineServer
	OKX     *OKXClient
	Jupiter *JupiterClient
}

func NewExecutionService() *ExecutionService {
	return &ExecutionService{
		OKX:     NewOKXClient(),
		Jupiter: NewJupiterClient(),
	}
}

func (s *ExecutionService) DryRunSwap(ctx context.Context, req *pb.SwapRequest) (*pb.DryRunResult, error) {
	log.Printf("DryRunSwap: %s %.2f on %s", req.Ticker, req.SizeUsd, req.Exchange)
	
	var estSlippage float64 = 0.005 // Default 0.5%
	var priceImpact float64 = 0.002
	var estOutput float64 = req.SizeUsd

	if req.Exchange == "okx" {
		price, err := s.OKX.GetTicker(req.Ticker)
		if err == nil {
			// Simulate slight slippage based on size (simplified)
			estSlippage = 0.001 + (req.SizeUsd / 100000.0)
			estOutput = (req.SizeUsd / price) * (1.0 - estSlippage) * price
		} else {
			log.Printf("Warning: OKX price fetch failed for DryRun: %v", err)
		}
	} else if req.Exchange == "jupiter" {
		// Mock mint addresses if not provided (for simulation)
		quote, err := s.Jupiter.GetQuote("EPjFW3F2Tz2S6KVcyP56XRLsgZ4cyWq6wGV36nKSvS8", "So11111111111111111111111111111111111111112", int64(req.SizeUsd*1000000))
		if err == nil {
			impact, _ := strconv.ParseFloat(quote.PriceImpactPct, 64)
			priceImpact = impact / 100.0
			estSlippage = float64(quote.SlippageBps) / 10000.0
			outAmt, _ := strconv.ParseFloat(quote.OutAmount, 64)
			estOutput = outAmt / 1000000000.0 // Assuming SOL decimals for out
		} else {
			log.Printf("Warning: Jupiter quote fetch failed for DryRun: %v", err)
		}
	}
	
	isSafe := estSlippage < 0.02
	
	return &pb.DryRunResult{
		EstimatedSlippage: estSlippage,
		PriceImpact:       priceImpact,
		EstimatedOutput:   estOutput,
		IsSafe:            isSafe,
		RejectionReason:   "",
	}, nil
}

func (s *ExecutionService) ExecuteSwap(ctx context.Context, req *pb.SwapRequest) (*pb.SwapResult, error) {
	log.Printf("ExecuteSwap: %s %.2f on %s", req.Ticker, req.SizeUsd, req.Exchange)

	paperTrading := os.Getenv("PAPER_TRADING") != "false" // Default to true for safety
	
	if paperTrading {
		// Simulate latency: 500ms to 2000ms
		latency := 500 + rand.Intn(1500)
		time.Sleep(time.Duration(latency) * time.Millisecond)

		txHash := ""
		if req.Exchange == "jupiter" {
			txHash = "sol_paper_" + fmt.Sprint(time.Now().UnixNano())
		} else {
			txHash = "okx_paper_" + fmt.Sprint(time.Now().UnixNano())
		}

		return &pb.SwapResult{
			Success:        true,
			TxHash:         txHash,
			ExecutedPrice:  100.0, // Should ideally fetch real price here too
			ActualSlippage: 0.005 + (rand.Float64() * 0.002),
		}, nil
	}

	// Real execution logic with 30s timeout
	execCtx, cancel := context.WithTimeout(ctx, 30*time.Second)
	defer cancel()

	errChan := make(chan error, 1)

	go func() {
		// Real API call here
		if req.Exchange == "okx" {
			errChan <- fmt.Errorf("Real execution not fully implemented without secure vault")
		} else {
			errChan <- fmt.Errorf("Exchange %s real execution not implemented", req.Exchange)
		}
	}()

	select {
	case err := <-errChan:
		return &pb.SwapResult{
			Success:      false,
			ErrorMessage: err.Error(),
		}, nil
	case <-execCtx.Done():
		return &pb.SwapResult{
			Success:      false,
			ErrorMessage: "timeout after 30 seconds",
		}, nil
	}
}

func (s *ExecutionService) GetPortfolio(ctx context.Context, req *pb.Empty) (*pb.PortfolioState, error) {
	// Simple mock for skeleton - in Task 4 this should read from DB/Exchange
	return &pb.PortfolioState{
		TotalCapital:     1000.0,
		AvailableCapital: 800.0,
		Positions: []*pb.Position{
			{Ticker: "SOL/USDC", Size: 2.0, EntryPrice: 100.0, CurrentPrice: 105.0, UnrealizedPnl: 10.0},
		},
	}, nil
}

func (s *ExecutionService) Liquidate(ctx context.Context, req *pb.LiquidateRequest) (*pb.LiquidateResult, error) {
	return &pb.LiquidateResult{
		Success:         true,
		PositionsClosed: 1,
		TotalPnl:        10.0,
	}, nil
}

func (s *ExecutionService) HealthCheck(ctx context.Context, req *pb.Empty) (*pb.HealthResponse, error) {
	return &pb.HealthResponse{
		Ok:      true,
		Version: "0.1.1",
	}, nil
}
