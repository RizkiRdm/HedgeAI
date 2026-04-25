package main

import (
	"fmt"
	"log"
	"net"

	"cryptohedge/go_engine/executor"
	pb "cryptohedge/go_engine/proto"
	"google.golang.org/grpc"
)

func main() {
	lis, err := net.Listen("tcp", ":50051")
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterExecutionEngineServer(s, executor.NewExecutionService())
	fmt.Println("Go Execution Engine listening on :50051")
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
