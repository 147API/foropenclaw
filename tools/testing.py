"""
OpenClaw Agent Testing Utilities

Test your agents before deploying to production.

Features:
- Mock tool responses
- Simulate failures
- Measure performance
- Validate outputs
"""

import time
import json
from typing import Dict, List, Callable, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TestResult:
    """Test execution result."""
    name: str
    passed: bool
    duration_ms: float
    error: str = None
    output: Any = None

class AgentTester:
    """
    Test harness for OpenClaw agents.
    
    Example:
        tester = AgentTester()
        
        @tester.test("Health check returns 200")
        def test_health_check():
            result = agent.check_health()
            assert result["status"] == "healthy"
        
        tester.run_all()
    """
    
    def __init__(self):
        self.tests: List[Callable] = []
        self.results: List[TestResult] = []
    
    def test(self, name: str):
        """Decorator to register a test."""
        def decorator(func: Callable):
            self.tests.append((name, func))
            return func
        return decorator
    
    def run_all(self) -> Dict:
        """
        Run all registered tests.
        
        Returns:
            Summary with pass/fail counts and details
        """
        print(f"\n🧪 Running {len(self.tests)} tests...\n")
        
        self.results = []
        passed = 0
        failed = 0
        
        for name, test_func in self.tests:
            result = self._run_test(name, test_func)
            self.results.append(result)
            
            if result.passed:
                passed += 1
                print(f"✅ {name} ({result.duration_ms:.0f}ms)")
            else:
                failed += 1
                print(f"❌ {name}")
                print(f"   Error: {result.error}")
        
        print(f"\n{'='*50}")
        print(f"Results: {passed} passed, {failed} failed")
        print(f"{'='*50}\n")
        
        return {
            "total": len(self.tests),
            "passed": passed,
            "failed": failed,
            "results": [vars(r) for r in self.results]
        }
    
    def _run_test(self, name: str, test_func: Callable) -> TestResult:
        """Run a single test and capture result."""
        start = time.time()
        
        try:
            output = test_func()
            duration_ms = (time.time() - start) * 1000
            return TestResult(
                name=name,
                passed=True,
                duration_ms=duration_ms,
                output=output
            )
        except AssertionError as e:
            duration_ms = (time.time() - start) * 1000
            return TestResult(
                name=name,
                passed=False,
                duration_ms=duration_ms,
                error=str(e)
            )
        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            return TestResult(
                name=name,
                passed=False,
                duration_ms=duration_ms,
                error=f"Unexpected error: {str(e)}"
            )


class MockTool:
    """
    Mock OpenClaw tools for testing.
    
    Example:
        mock_exec = MockTool("exec")
        mock_exec.set_response("ls -la", "file1.txt\nfile2.txt")
        
        result = mock_exec.call("ls -la")
        assert "file1.txt" in result
    """
    
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.responses: Dict[str, Any] = {}
        self.call_history: List[Dict] = []
    
    def set_response(self, input_key: str, response: Any):
        """Set mock response for specific input."""
        self.responses[input_key] = response
    
    def call(self, *args, **kwargs) -> Any:
        """Call the mock tool and return response."""
        # Record call
        self.call_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "args": args,
            "kwargs": kwargs
        })
        
        # Find matching response
        key = str(args) + str(kwargs)
        if key in self.responses:
            return self.responses[key]
        
        # Default response
        return {"status": "ok", "mock": True}
    
    def assert_called(self, times: int = None):
        """Assert tool was called specific number of times."""
        if times is not None:
            assert len(self.call_history) == times, \
                f"Expected {times} calls, got {len(self.call_history)}"
        else:
            assert len(self.call_history) > 0, "Tool was never called"
    
    def reset(self):
        """Reset call history."""
        self.call_history = []


class PerformanceTester:
    """
    Measure agent performance.
    
    Example:
        perf = PerformanceTester()
        
        with perf.measure("API call"):
            result = api.call()
        
        perf.report()
    """
    
    def __init__(self):
        self.measurements: List[Dict] = []
    
    def measure(self, name: str):
        """Context manager to measure execution time."""
        class MeasureContext:
            def __init__(self, tester, name):
                self.tester = tester
                self.name = name
                self.start = None
            
            def __enter__(self):
                self.start = time.time()
                return self
            
            def __exit__(self, *args):
                duration_ms = (time.time() - self.start) * 1000
                self.tester.measurements.append({
                    "name": self.name,
                    "duration_ms": duration_ms,
                    "timestamp": datetime.utcnow().isoformat()
                })
        
        return MeasureContext(self, name)
    
    def report(self):
        """Print performance report."""
        if not self.measurements:
            print("No measurements recorded")
            return
        
        print("\n⚡ Performance Report\n")
        print(f"{'Operation':<30} {'Duration':<15}")
        print("=" * 45)
        
        for m in self.measurements:
            print(f"{m['name']:<30} {m['duration_ms']:>10.2f}ms")
        
        total = sum(m['duration_ms'] for m in self.measurements)
        print("=" * 45)
        print(f"{'Total':<30} {total:>10.2f}ms\n")


# Example usage
if __name__ == "__main__":
    # 1. Basic testing
    tester = AgentTester()
    
    @tester.test("Simple assertion")
    def test_simple():
        assert 1 + 1 == 2
    
    @tester.test("String contains")
    def test_string():
        result = "hello world"
        assert "world" in result
    
    @tester.test("This will fail")
    def test_failure():
        assert False, "Expected failure"
    
    results = tester.run_all()
    
    # 2. Mock tools
    print("\n📦 Testing with mocks\n")
    
    mock_exec = MockTool("exec")
    mock_exec.set_response("ls", "file1.txt\nfile2.txt")
    
    result = mock_exec.call("ls")
    print(f"Mock result: {result}")
    
    mock_exec.assert_called(times=1)
    print("✅ Mock assertions passed")
    
    # 3. Performance testing
    print("\n⚡ Performance testing\n")
    
    perf = PerformanceTester()
    
    with perf.measure("Fast operation"):
        time.sleep(0.01)
    
    with perf.measure("Slow operation"):
        time.sleep(0.1)
    
    perf.report()
