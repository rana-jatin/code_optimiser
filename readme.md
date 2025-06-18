# 🐛 AI-Powered Python Debugger

A comprehensive debugging framework that uses Groq's language models to analyze Python errors, suggest intelligent fixes, and generate detailed reports with automatic code patching capabilities.

## ✨ Features

### 🤖 AI-Powered Analysis
- **Intelligent Error Analysis**: Uses Groq's advanced language models to understand and analyze Python errors
- **Automatic Fix Suggestions**: Provides detailed explanations and code fixes for common errors
- **Pattern Recognition**: Identifies error patterns and applies specific fixing strategies
- **Confidence Scoring**: AI provides confidence levels for suggested fixes

### 🔧 Error Handling Capabilities
- **Undefined Variables**: Automatic variable definition suggestions
- **Zero Division Errors**: Safe division with error handling
- **Syntax Errors**: Common syntax fix patterns
- **Index Errors**: Bounds checking implementation
- **Attribute Errors**: hasattr validation checks
- **Import Errors**: Module dependency analysis
- **Type Errors**: Type validation suggestions

### 📊 Comprehensive Reporting
- **JSON Export**: Detailed structured reports for each debugging session
- **Session History**: Track all debugging sessions with timestamps
- **Code Context**: Capture surrounding code and variables for better analysis
- **Modification Tracking**: Document all applied fixes with before/after comparisons

### 🛠️ Multiple Usage Patterns
- **Decorators**: Automatic function debugging with `@debug_decorator`
- **Context Managers**: Code block debugging with `with debug_context:`
- **Static Analysis**: Analyze code without execution
- **Direct Integration**: Manual error capturing and analysis

## 🚀 Installation

### Prerequisites
```bash
pip install groq
```

### Optional Dependencies
For Jupyter/Colab environments:
```bash
pip install nest-asyncio
```

## ⚙️ Configuration

### API Key Setup
```python
import os
os.environ["GROQ_API_KEY"] = "your-groq-api-key-here"

# Or pass directly to the debugger
debugger = GroqDebugger("your-groq-api-key-here")
```

Get your API key from: [https://console.groq.com/keys](https://console.groq.com/keys)

### Model Configuration
```python
# Default model
debugger = GroqDebugger(api_key, model="meta-llama/llama-4-maverick-17b-128e-instruct")

# Custom model
debugger = GroqDebugger(api_key, model="your-preferred-model")
```

## 📚 Usage Examples

### Basic Usage

```python
from groq_debugger import GroqDebugger

# Initialize debugger
debugger = GroqDebugger("your-groq-api-key")

# Static code analysis
problematic_code = """
def divide_numbers(a, b):
    result = a / b  # Potential division by zero
    return result

print(undefined_variable)  # NameError
"""

# Analyze and get suggestions
json_file = debugger.debug_code_static(problematic_code, "example.py")
print(f"Analysis saved to: {json_file}")
```

### Using Decorators

```python
from groq_debugger import GroqDebugger, DebugDecorator

debugger = GroqDebugger("your-api-key")
debug_decorator = DebugDecorator(debugger)

@debug_decorator
def buggy_function(x, y):
    if x > 0:
        return y / x  # Will fail if x is 0
    else:
        return undefined_var  # NameError

# This will automatically capture and analyze any errors
try:
    result = buggy_function(0, 10)
except Exception:
    print("Error captured and analyzed!")
```

### Using Context Managers

```python
from groq_debugger import GroqDebugger, DebugContext

debugger = GroqDebugger("your-api-key")
debug_context = DebugContext(debugger)

try:
    with debug_context:
        numbers = [1, 2, 3]
        print(numbers[10])  # IndexError - will be analyzed
except Exception:
    print("Error analyzed and suggestions provided!")
```

### Runtime Error Handling

```python
import sys
from groq_debugger import GroqDebugger

debugger = GroqDebugger("your-api-key")

try:
    # Your potentially buggy code here
    result = risky_operation()
except Exception:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    debug_info = debugger.capture_error_context(exc_type, exc_value, exc_traceback)
    json_file = debugger.debug_with_json_output(debug_info)
    print(f"Debug session saved to: {json_file}")
```

## 📖 Core Classes

### DebugInfo
Stores comprehensive error information:
```python
@dataclass
class DebugInfo:
    error_type: str           # Exception type name
    error_message: str        # Exception message  
    traceback_info: str       # Full traceback
    code_context: str         # Surrounding code lines
    line_number: int          # Error line number
    file_name: str           # Source file name
    function_name: str       # Function where error occurred
    variables: Dict[str, Any] # Local variables at error time
    timestamp: str           # When error occurred
    original_code: str       # Complete source code
```

### DebugSuggestion
AI-generated debugging suggestions:
```python
@dataclass
class DebugSuggestion:
    analysis: str                    # AI's error analysis
    suggested_fix: str              # Proposed code fix
    explanation: str                # Why error occurred and how fix works
    confidence: float               # AI confidence (0.0-1.0)
    alternative_solutions: List[str] # Other possible solutions
    fixed_code: str                 # Automatically patched code
    patch_applied: bool             # Whether patch was successfully applied
```

### DebugSession
Complete debugging session record:
```python
@dataclass
class DebugSession:
    session_id: str              # Unique session identifier
    timestamp: str              # Session timestamp
    debug_info: DebugInfo       # Error details
    suggestion: DebugSuggestion # AI suggestions and fixes
    status: str                 # Session status
    notes: str                  # Additional notes
```

## 🔍 Analysis Capabilities

### Code Analysis
- **Syntax Validation**: Check for Python syntax errors
- **Pattern Recognition**: Identify common error patterns
- **Complexity Analysis**: Assess code complexity metrics
- **Variable Tracking**: Capture local variables at error time

### Code Smells Detection
- Long lines (>100 characters)
- Nested loops (performance issues)
- Global variables (maintainability issues)
- Magic numbers (readability issues)

### Automatic Fixes
- **Variable Definition**: Add missing variable declarations
- **Zero Division Protection**: Implement safe division checks
- **Bounds Checking**: Add index validation for lists/arrays
- **Attribute Validation**: Use hasattr() for safe attribute access
- **Generic Fixes**: Apply AI-suggested improvements

## 📁 Output Structure

### JSON Report Format
```json
{
  "session_info": {
    "session_id": "20231215_143022_001",
    "timestamp": "2023-12-15T14:30:22",
    "status": "completed",
    "notes": "AI confidence: 85%"
  },
  "error_details": {
    "error_type": "NameError",
    "error_message": "name 'undefined_variable' is not defined",
    "line_number": 5,
    "file_name": "example.py",
    "variables": {...},
    "code_context": "...",
    "original_code": "..."
  },
  "ai_analysis": {
    "analysis": "The error occurs because...",
    "suggested_fix": "```python\n# Fixed code here\n```",
    "explanation": "This error happened because...",
    "confidence": 0.85,
    "alternative_solutions": ["Solution 1", "Solution 2"],
    "patch_applied": true
  },
  "code_changes": {
    "original_code": "...",
    "fixed_code": "...",
    "has_fix": true
  }
}
```

### File Organization
```
debug_output/
├── debug_session_20231215_143022_001.json
├── debug_session_20231215_143023_002.json
├── debug_summary.json
└── ...
```

## 🎛️ Advanced Configuration

### Custom Output Directory
```python
debugger = GroqDebugger(
    api_key="your-key",
    output_dir="custom_debug_reports"
)
```

### Model Parameters
```python
# Custom model with specific parameters
debugger = GroqDebugger(
    api_key="your-key", 
    model="llama-3.1-70b-versatile"
)
```

### Debugging History
```python
# Access debugging history
for session in debugger.debug_history:
    print(f"Session {session.session_id}: {session.debug_info.error_type}")

# Generate summary report
summary_file = debugger.save_summary_report()
print(f"Summary saved to: {summary_file}")
```

## 🔧 Error Handling

### API Errors
```python
try:
    result = debugger.debug_code_static(code)
except Exception as e:
    print(f"Debugger error: {e}")
    # Fallback to manual debugging
```

### Invalid Code
```python
# The framework handles syntax errors gracefully
invalid_code = "def broken_function( syntax error here"
result = debugger.debug_code_static(invalid_code)
# Will return analysis indicating syntax issues
```

## 📊 Performance Metrics

### Analysis Speed
- **Static Analysis**: ~1-2 seconds per file
- **Runtime Error**: ~2-3 seconds including API call
- **Code Patching**: ~100ms for pattern-based fixes

### Memory Usage
- **Base Framework**: ~10MB
- **Per Session**: ~1-5MB depending on code size
- **JSON Reports**: ~10-100KB per session

## 🤝 Contributing

### Development Setup
```bash
git clone https://github.com/your-repo/groq-debugger
cd groq-debugger
pip install -r requirements.txt
```

### Adding New Error Patterns
```python
class CustomCodePatcher(CodePatcher):
    def __init__(self):
        super().__init__()
        self.patch_strategies['custom_error'] = self._fix_custom_error
    
    def _fix_custom_error(self, original_code, debug_info, suggestion):
        # Implement custom fix logic
        return fixed_code
```

### Testing
```bash
python -m pytest tests/
python examples/test_all_examples.py
```

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

### Common Issues

**Q: "ModuleNotFoundError: No module named 'groq'"**
A: Install the Groq package: `pip install groq`

**Q: "API key not working"**
A: Verify your API key at [console.groq.com](https://console.groq.com/keys)

**Q: "Jupyter notebook async issues"**
A: Install nest-asyncio: `pip install nest-asyncio`

### Getting Help
- 📧 Email: support@your-domain.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-repo/issues)
- 📖 Documentation: [Full Docs](https://your-docs-site.com)

## 🚀 Roadmap

### Upcoming Features
- [ ] **IDE Integration**: VS Code and PyCharm plugins
- [ ] **Team Collaboration**: Shared debugging sessions
- [ ] **Advanced Analytics**: Error pattern trends
- [ ] **Custom Models**: Fine-tuned debugging models
- [ ] **Real-time Monitoring**: Production error tracking
- [ ] **Multi-language Support**: JavaScript, Java, C++ debugging

### Version History
- **v1.0.0**: Initial release with basic debugging
- **v1.1.0**: Added context managers and decorators  
- **v1.2.0**: JSON export and session history
- **v1.3.0**: Automatic code patching
- **v1.4.0**: Static code analysis

---

**Built with ❤️ using Groq's powerful language models**
