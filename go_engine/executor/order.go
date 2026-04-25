package executor

import (
	"context"
	"fmt"
	"log"
	"os"
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
	
	// Implementation for Issue 009: 
	// 1. Fetch current orderbook (mocked for now, real logic would call OKX/Jupiter)
	// 2. Calculate slippage
	
	// Mock safe result for dev
	estSlippage := 0.005 // 0.5%
	isSafe := estSlippage < 0.02
	
	return &pb.DryRunResult{
		EstimatedSlippage: estSlippage,
		PriceImpact:       0.002,
		EstimatedOutput:   req.SizeUsd * (1.0 - estSlippage),
		IsSafe:            isSafe,
		RejectionReason:   "",
	}, nil
}

func (s *ExecutionService) ExecuteSwap(ctx context.Context, req *pb.SwapRequest) (*pb.SwapResult, error) {
	log.Printf("ExecuteSwap: %s %.2f on %s", req.Ticker, req.SizeUsd, req.Exchange)

	paperTrading := os.Getenv("PAPER_TRADING") == "true"
	
	if paperTrading {
		time.Sleep(500 * time.Millisecond)
		return &pb.SwapResult{
			Success:        true,
			TxHash:         "0xpaper_mock_hash_" + fmt.Sprint(time.Now().Unix()),
			ExecutedPrice:  100.0,
			ActualSlippage: 0.005,
		}, nil
	}

	// Real execution logic with 30s timeout
	execCtx, cancel := context.WithTimeout(ctx, 30*time.Second)
	defer cancel()

	done := make(chan *pb.SwapResult, 1)
	errChan := make(chan error, 1)

	go func() {
		// Real API call here
		// For now, returning error because credentials aren't set
		if req.Exchange == "okx" {
			// res, err := s.OKX.Request("POST", "/api/v5/trade/order", body)
			errChan <- fmt.Errorf("Real execution not fully implemented without secure vault")
		} else {
			errChan <- fmt.Errorf("Exchange %s not supported", req.Exchange)
		}
	}()

	select {
	case res := <-done:
		return res, nil
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
	// Simple mock for skeleton
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
		Version: "0.1.0",
	}, nil
}
