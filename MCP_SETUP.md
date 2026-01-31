# Greptile MCP Server Setup

This implements Greptile functionality as an MCP (Model Context Protocol) server, allowing AI assistants like Claude Desktop to directly trigger code reviews.

## What is MCP?

Model Context Protocol (MCP) is a standard protocol that enables AI assistants to interact with external tools and services. When Greptile mentioned they have an MCP server with `trigger_code_review`, they're referring to this protocol.

## Installation

1. **Install MCP package:**
   ```bash
   pip install mcp
   ```

2. **Install Greptile dependencies:**
   ```bash
   cd ~/greptile-skill
   pip install -r requirements.txt
   ```

## Running the MCP Server

### Option 1: Standalone Mode
```bash
cd ~/greptile-skill
python greptile_mcp_server.py
```

### Option 2: With Claude Desktop

1. Edit Claude Desktop's config file:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add the Greptile MCP server:
   ```json
   {
     "mcpServers": {
       "greptile": {
         "command": "python",
         "args": ["/path/to/greptile-skill/greptile_mcp_server.py"],
         "env": {
           "GREPTILE_API_KEY": "your-api-key-here"
         }
       }
     }
   }
   ```

3. Restart Claude Desktop

## Available MCP Tools

Once connected, Claude can use these tools:

### 1. enable_repository
Enable a repo for Greptile analysis:
```
Use the enable_repository tool with repository "owner/repo"
```

### 2. trigger_code_review
Get a code review on a PR:
```
Use the trigger_code_review tool with pr_url "https://github.com/owner/repo/pull/123"
```
Add `post_comment: true` to post the review as a PR comment.

### 3. check_repository_status
Check if a repo is indexed:
```
Use the check_repository_status tool with repository "owner/repo"
```

### 4. query_repository
Ask questions about code:
```
Use the query_repository tool with repository "owner/repo" and query "How does authentication work?"
```

## Benefits of MCP Approach

1. **Direct Integration** - Claude can trigger reviews without you running commands
2. **Automatic Setup** - No manual command execution needed
3. **Resource Access** - Claude can read past reviews stored locally
4. **Native Experience** - Tools appear in Claude's UI

## Example Workflow

1. **In Claude Desktop:**
   "Enable the bigph00t/my-app repository for code reviews"
   
2. **Claude uses MCP:**
   → Calls `enable_repository` tool
   → Waits for indexing
   → Confirms completion

3. **Request review:**
   "Review the PR at https://github.com/bigph00t/my-app/pull/1 and post your feedback"
   
4. **Claude uses MCP:**
   → Calls `trigger_code_review` with `post_comment: true`
   → Gets review
   → Posts to GitHub
   → Shows you the review

## Troubleshooting

### "MCP package not installed"
```bash
pip install mcp
```

### "Cannot connect to MCP server"
- Check Claude Desktop config path is correct
- Ensure Python path is absolute
- Check API key is set in environment

### "Repository not found"
- Verify Greptile API key has access
- Check repository exists and is accessible

## Alternative: Direct API Usage

If MCP setup is complex, you can still use the simple commands:
```bash
python greptile_simple.py enable owner/repo
python greptile_simple.py review-post <pr-url>
```

The MCP approach just makes it more seamless within Claude Desktop!