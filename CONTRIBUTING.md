# Contributing to Greptile Code Review Automation

First off, thank you for considering contributing! This project aims to make code reviews faster and more accessible for all developers.

## 🚀 Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/greptile-skill.git`
3. Install the pre-commit hook: `./install-pre-commit.sh .`
4. Create a branch: `git checkout -b feature/amazing-feature`
5. Make your changes
6. Commit (the hook will review your code!)
7. Push and create a Pull Request

## 📝 Development Setup

```bash
# Clone the repo
git clone https://github.com/bigph00t/greptile-skill.git
cd greptile-skill

# Install dependencies
pip install -r requirements.txt

# Set up pre-commit hook (yes, we eat our own dog food)
./install-pre-commit.sh .

# Run tests
python -m pytest tests/
```

## 🎯 What We're Looking For

### Priority Areas

1. **Language Support** - Extend beyond Python/JavaScript
2. **Performance** - Make reviews even faster
3. **Integration** - VS Code, Vim, other editors
4. **Security Rules** - More comprehensive security checks

### Good First Issues

- Add support for configuration files (`.greptilerc`)
- Improve error messages
- Add more examples
- Enhance documentation

## 💻 Code Standards

### Python Style
- Follow PEP 8
- Use type hints where possible
- Document all public functions

### Commit Messages
```
feat: Add support for Ruby files
fix: Handle API timeout gracefully
docs: Update installation guide
test: Add tests for branch detection
```

### Code Review (Automated!)

Your code will be automatically reviewed by Greptile when you commit. The hook will check for:
- Security vulnerabilities
- Code quality issues
- Missing error handling
- Performance problems

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_api.py

# Run with coverage
pytest --cov=greptile_skill tests/
```

## 📦 Pull Request Process

1. **Update Documentation** - If you've added functionality
2. **Add Tests** - Maintain or increase coverage
3. **Pass Pre-commit** - Fix any issues caught by the hook
4. **Update README** - If needed
5. **Small PRs** - Easier to review and merge

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] Added new tests
- [ ] Pre-commit hook passes

## Screenshots (if applicable)
```

## 🐛 Reporting Issues

### Security Issues
Please email security issues directly rather than creating public issues.

### Bug Reports
Include:
- Python version
- OS
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

## 💡 Feature Requests

Open an issue with:
- Use case description
- Proposed solution
- Alternative approaches considered
- Examples if possible

## 🏗️ Architecture Decisions

### Why These Design Choices?

1. **Separate CLI tools** - Modularity and flexibility
2. **Query API approach** - Works without GitHub App setup
3. **Python-first** - Easy integration with AI/ML workflows
4. **Git hooks** - Shift-left security approach

## 🙏 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive criticism
- Assume positive intent

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🚀 Getting Help

- Open an issue for bugs/features
- Check existing issues first
- Join discussions in issues/PRs

---

**Remember**: The pre-commit hook is your friend! It catches issues before they become PRs. 🖤