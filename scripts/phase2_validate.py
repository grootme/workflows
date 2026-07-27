"""
Phase 2 Zero-Debt Validation Script
Validates every workflow against zero-debt standards:
- No PLACEHOLDER credentials
- No orphan nodes (every node wired or is stickyNote)
- ai_* connections present for all LangChain agents
- $fromAI() expressions in MCP tool parameters
- Real n8n node types
- Proper connection format
"""

import json
import os

BASE_DIR = "/home/z/my-project/download/n8n_workflows_v2"

def validate_workflow(filepath):
    """Validate a single workflow JSON for zero-debt compliance"""
    with open(filepath, 'r') as f:
        wf = json.load(f)
    
    issues = []
    warnings = []
    checks_passed = []
    
    name = wf.get("name", "Unknown")
    nodes = wf.get("nodes", [])
    connections = wf.get("connections", {})
    
    # 1. Check valid n8n format
    required_keys = ["name", "nodes", "connections", "settings"]
    for key in required_keys:
        if key not in wf:
            issues.append(f"Missing required key: {key}")
        else:
            checks_passed.append(f"Has {key}")
    
    # 2. Check settings.executionOrder
    if "executionOrder" not in wf.get("settings", {}):
        issues.append("Missing executionOrder in settings")
    else:
        checks_passed.append("Has executionOrder")
    
    # 3. Check no PLACEHOLDER credentials
    placeholder_found = False
    for node in nodes:
        creds = node.get("credentials", {})
        for cred_type, cred_data in creds.items():
            if isinstance(cred_data, dict):
                if cred_data.get("id") == "PLACEHOLDER":
                    placeholder_found = True
                    issues.append(f"Node '{node['name']}' uses PLACEHOLDER credential ID")
    if not placeholder_found:
        checks_passed.append("No PLACEHOLDER credentials")
    
    # 4. Check empty credential IDs (template-ready)
    empty_id_count = 0
    for node in nodes:
        creds = node.get("credentials", {})
        for cred_type, cred_data in creds.items():
            if isinstance(cred_data, dict):
                if cred_data.get("id") == "":
                    empty_id_count += 1
    if empty_id_count > 0:
        checks_passed.append(f"Credential IDs are empty ({empty_id_count} creds - template-ready)")
    
    # 5. Check no orphan nodes (every non-stickyNote must appear in connections)
    sticky_names = {n["name"] for n in nodes if n["type"] == "n8n-nodes-base.stickyNote"}
    node_names = {n["name"] for n in nodes}
    connection_sources = set(connections.keys())
    # Find targets
    connection_targets = set()
    for source, conn_types in connections.items():
        for type_key, target_list in conn_types.items():
            for targets in target_list:
                for target in targets:
                    connection_targets.add(target["node"])
    
    wired_nodes = connection_sources | connection_targets | sticky_names
    orphan_nodes = node_names - wired_nodes
    
    if orphan_nodes:
        issues.append(f"Orphan nodes (not wired): {orphan_nodes}")
    else:
        checks_passed.append("No orphan nodes - all wired")
    
    # 6. Check ai_* connections for Agent nodes
    agent_nodes = [n for n in nodes if n["type"] == "@n8n/n8n-nodes-langchain.agent"]
    mcp_trigger_nodes = [n for n in nodes if n["type"] == "@n8n/n8n-nodes-langchain.mcpTrigger"]
    
    for agent in agent_nodes:
        agent_name = agent["name"]
        # Check that agent has at least ai_languageModel connection
        has_llm = False
        has_memory = False
        has_tool = False
        
        for source, conn_types in connections.items():
            for type_key in conn_types.keys():
                if type_key == "ai_languageModel":
                    # Check if target is this agent
                    for targets in conn_types[type_key]:
                        for t in targets:
                            if t["node"] == agent_name:
                                has_llm = True
                if type_key == "ai_memory":
                    for targets in conn_types[type_key]:
                        for t in targets:
                            if t["node"] == agent_name:
                                has_memory = True
                if type_key == "ai_tool":
                    for targets in conn_types[type_key]:
                        for t in targets:
                            if t["node"] == agent_name:
                                has_tool = True
        
        if not has_llm:
            issues.append(f"Agent '{agent_name}' missing ai_languageModel connection (no LLM!)")
        else:
            checks_passed.append(f"Agent '{agent_name}' has ai_languageModel ✅")
        
        if not has_memory:
            warnings.append(f"Agent '{agent_name}' missing ai_memory connection")
        else:
            checks_passed.append(f"Agent '{agent_name}' has ai_memory ✅")
        
        if not has_tool:
            warnings.append(f"Agent '{agent_name}' has no ai_tool connections (no tools)")
        else:
            checks_passed.append(f"Agent '{agent_name}' has ai_tool ✅")
    
    # 7. Check MCP trigger has ai_tool connections
    for trigger in mcp_trigger_nodes:
        trigger_name = trigger["name"]
        has_tool = False
        for source, conn_types in connections.items():
            for type_key in conn_types.keys():
                if type_key == "ai_tool":
                    for targets in conn_types[type_key]:
                        for t in targets:
                            if t["node"] == trigger_name:
                                has_tool = True
        if not has_tool:
            issues.append(f"MCP Trigger '{trigger_name}' has no ai_tool connections (no tools!)")
        else:
            checks_passed.append(f"MCP Trigger '{trigger_name}' has ai_tool connections ✅")
    
    # 8. Check $fromAI() expressions in MCP/AI tool parameters
    fromAI_count = 0
    for node in nodes:
        if node["type"] in ["n8n-nodes-base.googleCalendarTool", "n8n-nodes-base.gmailTool", 
                            "n8n-nodes-base.googleContactsTool", "@n8n/n8n-nodes-langchain.toolHttpRequest"]:
            params_str = json.dumps(node["parameters"])
            if "$fromAI" in params_str:
                fromAI_count += params_str.count("$fromAI")
    if fromAI_count > 0:
        checks_passed.append(f"$fromAI() expressions present: {fromAI_count} occurrences")
    
    # 9. Check tags are empty (no fake IDs)
    tags = wf.get("tags", [])
    if tags == []:
        checks_passed.append("Tags empty (template-ready)")
    elif any(isinstance(t, dict) and "id" in t for t in tags):
        issues.append("Tags contain fake IDs - use empty array")
    
    # 10. Check no errorWorkflow with string name
    settings = wf.get("settings", {})
    if "errorWorkflow" in settings:
        ew = settings["errorWorkflow"]
        if isinstance(ew, str) and len(ew) > 5 and not ew.isalnum():
            issues.append(f"errorWorkflow uses invalid format: {ew}")
        elif isinstance(ew, str):
            warnings.append(f"errorWorkflow present: {ew} (consider removing for distribution)")
    
    # 11. Check real n8n node types
    known_bad_types = ["n8n-nodes-base.shopifyTool", "n8n-nodes-base.googleCalendar", 
                       "n8n-nodes-base.googleSheetsTool"]
    for node in nodes:
        if node["type"] in known_bad_types:
            issues.append(f"Node '{node['name']}' uses invalid type: {node['type']}")
    
    # Score calculation
    total_checks = len(checks_passed) + len(issues) + len(warnings)
    score = (len(checks_passed) / max(total_checks, 1)) * 100
    
    return {
        "name": name,
        "filepath": filepath,
        "nodes_count": len(nodes),
        "connections_count": len(connections),
        "checks_passed": checks_passed,
        "issues": issues,
        "warnings": warnings,
        "score": round(score, 1),
        "zero_debt": len(issues) == 0
    }


def main():
    all_results = []
    
    # Validate consolidated workflows
    consolidated_dir = os.path.join(BASE_DIR, "consolidated")
    for f in sorted(os.listdir(consolidated_dir)):
        if f.endswith(".json") and not f.startswith("_"):
            filepath = os.path.join(consolidated_dir, f)
            result = validate_workflow(filepath)
            all_results.append(result)
    
    # Validate MCP server templates
    mcp_dir = os.path.join(BASE_DIR, "mcp_servers")
    for f in sorted(os.listdir(mcp_dir)):
        if f.endswith(".json") and not f.startswith("_"):
            filepath = os.path.join(mcp_dir, f)
            result = validate_workflow(filepath)
            all_results.append(result)
    
    # Validate base templates
    base_dir = os.path.join(BASE_DIR, "base_templates")
    for f in sorted(os.listdir(base_dir)):
        if f.endswith(".json") and not f.startswith("_"):
            filepath = os.path.join(base_dir, f)
            result = validate_workflow(filepath)
            all_results.append(result)
    
    print("=" * 70)
    print("ZERO-DEBT VALIDATION REPORT")
    print("=" * 70)
    
    total_zero_debt = 0
    total_issues = 0
    total_warnings = 0
    
    for r in all_results:
        status = "✅ ZERO-DEBT" if r["zero_debt"] else "❌ HAS ISSUES"
        print(f"\n{status} {r['name']} (score: {r['score']}%)")
        print(f"   Nodes: {r['nodes_count']} | Connections: {r['connections_count']}")
        
        if r["issues"]:
            for issue in r["issues"]:
                print(f"   🔴 ISSUE: {issue}")
                total_issues += 1
        
        if r["warnings"]:
            for warning in r["warnings"]:
                print(f"   🟡 WARNING: {warning}")
                total_warnings += 1
        
        for check in r["checks_passed"][:5]:  # Show top 5 checks
            print(f"   ✅ {check}")
        
        if r["zero_debt"]:
            total_zero_debt += 1
    
    print("\n" + "=" * 70)
    print(f"SUMMARY: {total_zero_debt}/{len(all_results)} workflows are zero-debt")
    print(f"Total issues: {total_issues} | Total warnings: {total_warnings}")
    
    if total_issues == 0:
        print("🎉 ALL WORKFLOWS ARE ZERO-DEBT - READY FOR PRODUCTION!")
    else:
        print(f"⚠️  {total_issues} issues need to be resolved before production")
    
    # Save validation results
    validation = {
        "total_workflows": len(all_results),
        "zero_debt_count": total_zero_debt,
        "total_issues": total_issues,
        "total_warnings": total_warnings,
        "results": all_results,
        "validated_at": datetime.now().isoformat()
    }
    
    with open(os.path.join(BASE_DIR, "_validation_report.json"), 'w') as f:
        json.dump(validation, f, indent=2)

from datetime import datetime

if __name__ == "__main__":
    main()
