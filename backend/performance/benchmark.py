"""
Performance benchmarks for API endpoints.
"""
import time
import asyncio
import aiohttp
import requests
import statistics
from typing import List, Dict, Tuple
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BenchmarkResult:
    """Represents the result of a performance benchmark."""
    endpoint: str
    method: str
    num_requests: int
    total_time: float
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    response_times: List[float]
    success_rate: float
    timestamp: datetime


class APIClient:
    """Simple API client for testing."""
    def __init__(self, base_url: str, auth_token: str = None):
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.session = requests.Session()

        if auth_token:
            self.session.headers.update({
                'Authorization': f'Bearer {auth_token}',
                'Content-Type': 'application/json'
            })

    def get(self, endpoint: str) -> requests.Response:
        """Make a GET request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url)

    def post(self, endpoint: str, data: dict = None) -> requests.Response:
        """Make a POST request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data)

    def put(self, endpoint: str, data: dict = None) -> requests.Response:
        """Make a PUT request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.put(url, json=data)

    def delete(self, endpoint: str) -> requests.Response:
        """Make a DELETE request."""
        url = f"{self.base_url}{endpoint}"
        return self.session.delete(url)


class PerformanceBenchmark:
    """Performance benchmarking tool for API endpoints."""
    def __init__(self, base_url: str, auth_token: str = None):
        self.client = APIClient(base_url, auth_token)
        self.results = []

    def benchmark_endpoint(
        self,
        method: str,
        endpoint: str,
        num_requests: int = 100,
        payload: dict = None
    ) -> BenchmarkResult:
        """
        Benchmark a specific endpoint with multiple requests.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint to test
            num_requests: Number of requests to make
            payload: Payload to send with POST/PUT requests

        Returns:
            BenchmarkResult containing performance metrics
        """
        print(f"Benchmarking {method} {endpoint} with {num_requests} requests...")

        response_times = []
        successful_requests = 0

        for i in range(num_requests):
            start_time = time.perf_counter()

            try:
                if method.upper() == 'GET':
                    response = self.client.get(endpoint)
                elif method.upper() == 'POST':
                    response = self.client.post(endpoint, payload)
                elif method.upper() == 'PUT':
                    response = self.client.put(endpoint, payload)
                elif method.upper() == 'DELETE':
                    response = self.client.delete(endpoint)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                if response.status_code in [200, 201, 204]:
                    successful_requests += 1

            except Exception as e:
                print(f"Request {i+1} failed: {e}")

            end_time = time.perf_counter()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            response_times.append(response_time)

            # Small delay to avoid overwhelming the server
            time.sleep(0.01)

        total_time = sum(response_times)
        avg_response_time = statistics.mean(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        success_rate = successful_requests / num_requests if num_requests > 0 else 0

        result = BenchmarkResult(
            endpoint=endpoint,
            method=method,
            num_requests=num_requests,
            total_time=total_time,
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            response_times=response_times,
            success_rate=success_rate,
            timestamp=datetime.utcnow()
        )

        self.results.append(result)

        print(f"Completed benchmark for {method} {endpoint}")
        print(f"  Average response time: {avg_response_time:.2f} ms")
        print(f"  Success rate: {success_rate:.2%}")
        print(f"  Min/Max: {min_response_time:.2f}/{max_response_time:.2f} ms")
        print()

        return result

    def run_comprehensive_benchmark(self) -> List[BenchmarkResult]:
        """
        Run comprehensive benchmarking of all major API endpoints.

        Returns:
            List of BenchmarkResult objects
        """
        endpoints_to_test = [
            ('GET', '/health', None),
            ('GET', '/api/tasks', None),
            ('POST', '/api/tasks', {"title": "Benchmark Task", "description": "Task for benchmarking"}),
            ('GET', '/api/tasks', None),
        ]

        print("Starting comprehensive API benchmarking...")
        print("=" * 60)

        for method, endpoint, payload in endpoints_to_test:
            self.benchmark_endpoint(method, endpoint, num_requests=50, payload=payload)

        print("=" * 60)
        print("Comprehensive benchmarking completed!")
        print()

        return self.results

    def print_summary(self):
        """Print a summary of all benchmark results."""
        if not self.results:
            print("No benchmark results to display.")
            return

        print("BENCHMARK SUMMARY")
        print("=" * 60)

        for result in self.results:
            print(f"Endpoint: {result.method} {result.endpoint}")
            print(f"  Requests: {result.num_requests}")
            print(f"  Avg Response Time: {result.avg_response_time:.2f} ms")
            print(f"  Success Rate: {result.success_rate:.2%}")
            print(f"  Min/Max: {result.min_response_time:.2f}/{result.max_response_time:.2f} ms")
            print(f"  Total Time: {result.total_time:.2f} ms")
            print("-" * 40)

    def generate_report(self) -> str:
        """
        Generate a text report of the benchmark results.

        Returns:
            Formatted report string
        """
        if not self.results:
            return "No benchmark results available."

        report_lines = [
            "API PERFORMANCE BENCHMARK REPORT",
            "=" * 50,
            f"Generated: {datetime.utcnow().isoformat()}",
            ""
        ]

        for result in self.results:
            report_lines.extend([
                f"Endpoint: {result.method} {result.endpoint}",
                f"  Total Requests: {result.num_requests}",
                f"  Successful: {int(result.success_rate * result.num_requests)}",
                f"  Failed: {result.num_requests - int(result.success_rate * result.num_requests)}",
                f"  Success Rate: {result.success_rate:.2%}",
                f"  Average Response Time: {result.avg_response_time:.2f} ms",
                f"  Median Response Time: {statistics.median(result.response_times):.2f} ms" if result.response_times else "",
                f"  Min Response Time: {result.min_response_time:.2f} ms",
                f"  Max Response Time: {result.max_response_time:.2f} ms",
                f"  95th Percentile: {np.percentile(result.response_times, 95):.2f} ms" if result.response_times else "",
                f"  99th Percentile: {np.percentile(result.response_times, 99):.2f} ms" if result.response_times else "",
                ""
            ])

        return "\n".join(report_lines)


def run_performance_benchmarks():
    """Run the performance benchmarks."""
    print("Setting up performance benchmarks...")

    # Use a placeholder URL - in real usage, this would be the actual API URL
    base_url = "http://localhost:8000"  # Default development URL

    # Placeholder token for testing
    auth_token = "placeholder_token_for_testing"

    benchmark = PerformanceBenchmark(base_url, auth_token)

    print("Starting API performance benchmarks...")
    results = benchmark.run_comprehensive_benchmark()

    # Print summary
    benchmark.print_summary()

    # Generate report
    report = benchmark.generate_report()

    # Save report to file
    with open('performance_benchmark_report.txt', 'w') as f:
        f.write(report)

    print("Performance benchmark report saved to 'performance_benchmark_report.txt'")

    return results


if __name__ == "__main__":
    run_performance_benchmarks()