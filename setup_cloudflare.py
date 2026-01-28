#!/usr/bin/env python3
import os
import sys
import json
import urllib.request
import urllib.error

# Configuration
REPO_OWNER = "wmoore012"
REPO_NAME = "links-perdaycatalog"
PROJECT_NAME = "links-perdaycatalog"
ENV_FILE = ".env"

def load_env():
    """Load CACHE_API_TOKEN from .env file manually to avoid dependencies."""
    if not os.path.exists(ENV_FILE):
        print(f"❌ Error: {ENV_FILE} not found in current directory.")
        return None
    
    token = None
    with open(ENV_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('CLOUDFLARE_API_TOKEN='):
                token = line.split('=', 1)[1].strip('"').strip("'")
                # Remove any trailing comments or whitespace
                token = token.split()[0]
                break
    return token

def make_request(url, method='GET', data=None, token=None):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, method=method, headers=headers)
    
    if data:
        json_data = json.dumps(data).encode('utf-8')
        req.data = json_data
        
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP Error {e.code}: {e.reason}")
        try:
            error_body = e.read().decode('utf-8')
            print(f"Details: {error_body}")
        except:
            pass
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def main():
    print("🔍 Checking Environment...")
    token = load_env()
    if not token:
        print("❌ CLOUDFLARE_API_TOKEN not found in .env")
        sys.exit(1)
    
    print("✅ Token loaded (hidden)")
    
    # 1. Get Account ID
    print("\n☁️  Verifying Cloudflare Access...")
    accounts_url = "https://api.cloudflare.com/client/v4/accounts"
    accounts_resp = make_request(accounts_url, token=token)
    
    if not accounts_resp or not accounts_resp.get('success'):
        print("❌ Failed to list accounts. Check your token permissions.")
        sys.exit(1)
        
    accounts = accounts_resp.get('result', [])
    if not accounts:
        print("❌ No Cloudflare accounts found.")
        sys.exit(1)
        
    account_id = accounts[0]['id']
    account_name = accounts[0]['name']
    print(f"✅ Using Account: {account_name} ({account_id})")
    
    # 2. Check if Project Exists
    print(f"\nExample: Checking for existing project '{PROJECT_NAME}'...")
    project_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects/{PROJECT_NAME}"
    
    # Note: API returns 404 if not found, so we expect an error if it's new
    # But urllib raises exception on 404, so we handle it gracefully inside make_request? 
    # Actually make_request prints error. Let's suppress for 404 check or just list all projects.
    # Listing is safer.
    
    projects_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
    projects_resp = make_request(projects_url, token=token)
    
    project_exists = False
    if projects_resp and projects_resp.get('success'):
        for p in projects_resp.get('result', []):
            if p['name'] == PROJECT_NAME:
                project_exists = True
                print(f"ℹ️  Project '{PROJECT_NAME}' already exists.")
                print(f"   URL: {p.get('subdomain')}")
                break
    
    if project_exists:
        print("\n✅ Project already setup. Setup complete.")
        return

    # 3. Create Project
    print(f"\n🚀 Creating Pages project '{PROJECT_NAME}' linked to {REPO_OWNER}/{REPO_NAME}...")
    
    create_url = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/pages/projects"
    payload = {
        "name": PROJECT_NAME,
        "production_branch": "main",
        "source": {
            "type": "github",
            "config": {
                "owner": REPO_OWNER,
                "repo": REPO_NAME,
                "production_branch": "main",
                "pr_comments_enabled": True,
                "deployments_enabled": True
            }
        },
        "build_config": {
            "build_command": "npm run build",
            "destination_dir": "dist",
            "root_dir": "linktree-pages" 
        }
    }
    
    # NOTE: user has linktree-pages/ folder, so root_dir should probably be "linktree-pages"
    # and build command "npm run build" inside it.
    
    create_resp = make_request(create_url, method='POST', data=payload, token=token)
    
    if create_resp and create_resp.get('success'):
        result = create_resp['result']
        print("✅ Project created successfully!")
        print(f"   Name: {result['name']}")
        print(f"   Subdomain: {result['subdomain']}")
        print("\n⚠️  IMPORTANT: You may need to trigger the first deployment manually via git push or dashboard.")
    else:
        print("\n❌ Failed to create project.")

if __name__ == "__main__":
    main()
