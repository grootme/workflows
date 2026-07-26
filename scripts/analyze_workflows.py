#!/usr/bin/env python3
"""
Analyze all n8n workflow JSON files to:
1. Parse metadata (name, nodes, connections, tags)
2. Extract node types and categorize workflows
3. Identify duplications and similarities
4. Generate consolidated catalog with best practices
5. Output results as JSON for the web app
"""

import json
import os
import glob
import hashlib
import re
from collections import defaultdict
from difflib import SequenceMatcher

UPLOAD_DIR = "/home/z/my-project/upload"
OUTPUT_DIR = "/home/z/my-project/download"
SCRIPTS_DIR = "/home/z/my-project/scripts"

def normalize_name(name):
    """Normalize workflow name for comparison"""
    if not name:
        return ""
    # Remove common suffixes/prefixes
    name = re.sub(r'_Josema_Fernandez$', '', name)
    name = re.sub(r'_JosemaFernandez$', '', name)
    name = re.sub(r'__Josema_Fernandez$', '', name)
    name = re.sub(r'\s*\(\d+\)\s*$', '', name)
    name = re.sub(r'_v\d+$', '', name)
    name = name.strip().lower()
    # Replace underscores and special chars with spaces
    name = re.sub(r'[_\-\s]+', ' ', name)
    return name

def get_node_types(nodes):
    """Extract unique node types from a workflow"""
    if not nodes:
        return []
    types = []
    for node in nodes:
        if isinstance(node, dict) and 'type' in node:
            types.append(node['type'])
    return sorted(set(types))

def get_node_names(nodes):
    """Extract node names"""
    if not nodes:
        return []
    names = []
    for node in nodes:
        if isinstance(node, dict) and 'name' in node:
            names.append(node['name'])
    return names

def get_connection_count(connections):
    """Count total connections in a workflow"""
    if not connections or not isinstance(connections, dict):
        return 0
    count = 0
    for source, targets in connections.items():
        if isinstance(targets, dict):
            for target_list in targets.values():
                if isinstance(target_list, list):
                    for conn in target_list:
                        if isinstance(conn, list):
                            count += len(conn)
                        else:
                            count += 1
        elif isinstance(targets, list):
            count += len(targets)
    return count

def categorize_workflow(node_types, name):
    """Categorize workflow based on node types and name"""
    categories = []
    name_lower = name.lower() if name else ""
    
    # Category detection based on node types
    type_set = set(node_types)
    
    # AI/LLM related
    ai_types = {'n8n-nodes-base.openAi', '@n8n/n8n-nodes-langchain.lmChatOpenAi',
                '@n8n/n8n-nodes-langchain.lmChatAnthropic', 'n8n-nodes-base.googleGemini',
                '@n8n/n8n-nodes-langchain.agent', '@n8n/n8n-nodes-langchain.tool',
                '@n8n/n8n-nodes-langchain.memoryBufferWindow'}
    if type_set.intersection(ai_types) or any(kw in name_lower for kw in ['ai', 'ia', 'agent', 'gpt', 'openai', 'llm', 'gemini', 'claude']):
        categories.append('IA & Agentes')
    
    # RAG related
    if any(kw in name_lower for kw in ['rag', 'vector', 'embedding', 'qdrant', 'milvus', 'knowledge', 'reranker', 'cohere']):
        categories.append('RAG & Vector Store')
    
    # Chat/Messaging
    chat_types = {'n8n-nodes-base.telegram', 'n8n-nodes-base.telegramTrigger',
                  'n8n-nodes-base.slack', 'n8n-nodes-base.slackTrigger',
                  'n8n-nodes-base.discord', 'n8n-nodes-base.whatsApp'}
    if type_set.intersection(chat_types) or any(kw in name_lower for kw in ['chat', 'telegram', 'whatsapp', 'slack', 'chatbot', 'chatwoot', 'bot']):
        categories.append('Chat & Mensajería')
    
    # Email
    email_types = {'n8n-nodes-base.emailSend', 'n8n-nodes-base.emailRead',
                   'n8n-nodes-base.gmail', 'n8n-nodes-base.gmailTrigger',
                   'n8n-nodes-base.gmailRead', 'n8n-nodes-base.gmailSend'}
    if type_set.intersection(email_types) or any(kw in name_lower for kw in ['email', 'gmail', 'correo', 'newsletter']):
        categories.append('Email & Comunicación')
    
    # Social Media
    if any(kw in name_lower for kw in ['social', 'linkedin', 'instagram', 'tiktok', 'youtube', 'facebook', 'twitter', 'x', 'post', 'video', 'media']):
        categories.append('Social Media & Contenido')
    
    # E-Commerce
    if any(kw in name_lower for kw in ['shopify', 'ecommerce', 'e-commerce', 'producto', 'venta', 'store', 'banana', 'nano']):
        categories.append('E-Commerce & Ventas')
    
    # Marketing
    if any(kw in name_lower for kw in ['marketing', 'leads', 'seo', 'scrap', 'scraper', 'scrapp', 'branding', 'blog']):
        categories.append('Marketing & Leads')
    
    # HR/Recruitment
    if any(kw in name_lower for kw in ['hr', 'resume', 'cv', 'candidate', 'recruitment', 'interview', 'screening', 'onboarding', 'employee']):
        categories.append('RRHH & Selección')
    
    # Calendar/Scheduling
    if any(kw in name_lower for kw in ['calendar', 'calendario', 'agenda', 'scheduling', 'agendamiento', 'appointment']):
        categories.append('Calendario & Agenda')
    
    # Voice/Transcription
    if any(kw in name_lower for kw in ['voz', 'voice', 'transcripcion', 'transcription', 'elevenlabs', 'audio']):
        categories.append('Voz & Transcripción')
    
    # Scraping/Data extraction
    scraping_types = {'n8n-nodes-base.httpRequest', '@n8n/n8n-nodes-langchain.toolHttpRequest'}
    if any(kw in name_lower for kw in ['scrap', 'extract', 'scrapp', 'scrape', 'firecrawl', 'apify', 'bright data']):
        categories.append('Scraping & Extracción')
    
    # Documents/PDF
    if any(kw in name_lower for kw in ['pdf', 'documento', 'document', 'cotizacion', 'report']):
        categories.append('Documentos & PDF')
    
    # Database
    db_types = {'n8n-nodes-base.postgres', 'n8n-nodes-base.mongoDb', 'n8n-nodes-base.supabase',
               'n8n-nodes-base.mysql', 'n8n-nodes-base.redis'}
    if type_set.intersection(db_types) or any(kw in name_lower for kw in ['supabase', 'sql', 'database', 'mongo', 'redis', 'postgres']):
        categories.append('Base de Datos')
    
    # MCP
    if any(kw in name_lower for kw in ['mcp']):
        categories.append('MCP Tools')
    
    # Flowise
    if any(kw in name_lower for kw in ['flowise']):
        categories.append('Flowise Integration')
    
    # Dashboard
    if any(kw in name_lower for kw in ['dashboard', 'table', 'data']):
        categories.append('Dashboard & Datos')
    
    # Automation/Utility
    if any(kw in name_lower for kw in ['trucos', 'trick', 'error', 'backup', 'github', 'respaldar']):
        categories.append('Utilidades & DevOps')
    
    if not categories:
        categories.append('General')
    
    return categories

def compute_similarity(wf1, wf2):
    """Compute similarity score between two workflows"""
    score = 0
    max_score = 100
    
    # Name similarity (30 points)
    name1 = normalize_name(wf1.get('name', '') or os.path.basename(wf1.get('file_path', '')))
    name2 = normalize_name(wf2.get('name', '') or os.path.basename(wf2.get('file_path', '')))
    name_sim = SequenceMatcher(None, name1, name2).ratio()
    score += name_sim * 30
    
    # Node type overlap (40 points)
    types1 = set(wf1.get('node_types', []))
    types2 = set(wf2.get('node_types', []))
    if types1 and types2:
        overlap = types1.intersection(types2)
        union = types1.union(types2)
        jaccard = len(overlap) / len(union) if union else 0
        score += jaccard * 40
    
    # Category overlap (20 points)
    cats1 = set(wf1.get('categories', []))
    cats2 = set(wf2.get('categories', []))
    if cats1 and cats2:
        cat_overlap = cats1.intersection(cats2)
        cat_union = cats1.union(cats2)
        cat_jaccard = len(cat_overlap) / len(cat_union) if cat_union else 0
        score += cat_jaccard * 20
    
    # Node count similarity (10 points)
    nc1 = wf1.get('node_count', 0)
    nc2 = wf2.get('node_count', 0)
    if nc1 and nc2:
        count_sim = 1 - abs(nc1 - nc2) / max(nc1, nc2)
        score += count_sim * 10
    
    return round(score, 2)

def find_duplications(workflows):
    """Find potential duplications and similarities"""
    duplications = []
    similarities = []
    
    # Group by normalized name first
    name_groups = defaultdict(list)
    for wf in workflows:
        norm_name = normalize_name(wf.get('name', '') or os.path.basename(wf.get('file_path', '')))
        name_groups[norm_name].append(wf)
    
    # Exact name matches -> duplications
    for norm_name, group in name_groups.items():
        if len(group) > 1:
            # Check if they're actual duplicates (same node types)
            for i in range(len(group)):
                for j in range(i+1, len(group)):
                    sim = compute_similarity(group[i], group[j])
                    if sim >= 70:
                        duplications.append({
                            'workflow_1': group[i]['id'],
                            'workflow_2': group[j]['id'],
                            'name_1': group[i].get('name', ''),
                            'name_2': group[j].get('name', ''),
                            'similarity': sim,
                            'type': 'duplicate',
                            'reason': f'Nombres muy similares: "{group[i].get("name","")}" y "{group[j].get("name","")}"'
                        })
                    elif sim >= 40:
                        similarities.append({
                            'workflow_1': group[i]['id'],
                            'workflow_2': group[j]['id'],
                            'name_1': group[i].get('name', ''),
                            'name_2': group[j].get('name', ''),
                            'similarity': sim,
                            'type': 'similar',
                            'reason': f'Funcionalidad similar con nombres parecidos'
                        })
    
    # Cross-group similarity check (sample based for efficiency)
    all_ids = list(range(len(workflows)))
    # Check workflows within same category
    category_groups = defaultdict(list)
    for wf in workflows:
        for cat in wf.get('categories', []):
            category_groups[cat].append(wf)
    
    for cat, cat_wfs in category_groups.items():
        for i in range(len(cat_wfs)):
            for j in range(i+1, len(cat_wfs)):
                norm1 = normalize_name(cat_wfs[i].get('name', '') or '')
                norm2 = normalize_name(cat_wfs[j].get('name', '') or '')
                # Skip if already found as duplicate
                if norm1 == norm2:
                    continue
                sim = compute_similarity(cat_wfs[i], cat_wfs[j])
                if sim >= 60 and not any(
                    (d['workflow_1'] == cat_wfs[i]['id'] and d['workflow_2'] == cat_wfs[j]['id']) or
                    (d['workflow_1'] == cat_wfs[j]['id'] and d['workflow_2'] == cat_wfs[i]['id'])
                    for d in duplications + similarities
                ):
                    similarities.append({
                        'workflow_1': cat_wfs[i]['id'],
                        'workflow_2': cat_wfs[j]['id'],
                        'name_1': cat_wfs[i].get('name', ''),
                        'name_2': cat_wfs[j].get('name', ''),
                        'similarity': sim,
                        'type': 'similar',
                        'reason': f'Misma categoría "{cat}" con {sim}% de similitud'
                    })
    
    return duplications, similarities

def analyze_best_practices(workflows):
    """Identify best practices and anti-patterns"""
    practices = {
        'good': [],
        'warnings': [],
        'recommendations': []
    }
    
    # Analyze node usage patterns
    all_node_types = defaultdict(int)
    for wf in workflows:
        for nt in wf.get('node_types', []):
            all_node_types[nt] += 1
    
    # Good practices detected
    error_handler_count = sum(1 for wf in workflows if 'n8n-nodes-base.errorTrigger' in wf.get('node_types', []) or 
                              'n8n-nodes-base.if' in wf.get('node_types', []))
    
    has_sticky_notes = sum(1 for wf in workflows if any(
        n.get('type') == 'n8n-nodes-base.stickyNote' for n in (wf.get('raw_nodes') or [])
    ))
    
    # Check for common patterns
    mcp_usage = sum(1 for wf in workflows if any('mcp' in nt.lower() for nt in wf.get('node_types', [])))
    langchain_usage = sum(1 for wf in workflows if any('langchain' in nt.lower() for nt in wf.get('node_types', [])))
    
    practices['good'].append({
        'title': 'Uso de LangChain nodes',
        'description': f'{langchain_usage} workflows utilizan nodes LangChain de n8n para agentes IA, lo cual es la práctica recomendada para construir agentes con memoria y herramientas.',
        'impact': 'high'
    })
    
    practices['good'].append({
        'title': 'Uso de MCP (Model Context Protocol)',
        'description': f'{mcp_usage} workflows implementan MCP para conectar agentes con herramientas externas (Calendar, Gmail, Contactos). MCP es el estándar emergente para integración de agentes.',
        'impact': 'medium'
    })
    
    practices['good'].append({
        'title': 'Notas Sticky en workflows',
        'description': f'{has_sticky_notes} workflows incluyen notas sticky para documentación visual, facilitando la comprensión del flujo.',
        'impact': 'low'
    })
    
    # Warnings/Anti-patterns
    duplicate_count = 0  # Will be filled after duplication analysis
    
    workflows_no_name = sum(1 for wf in workflows if not wf.get('name') or wf.get('name') == '')
    large_workflows = sum(1 for wf in workflows if wf.get('node_count', 0) > 30)
    
    practices['warnings'].append({
        'title': 'Workflows sin nombre descriptivo',
        'description': f'{workflows_no_name} workflows carecen de nombre descriptivo, lo que dificulta su identificación y mantenimiento.',
        'impact': 'medium'
    })
    
    practices['warnings'].append({
        'title': 'Workflows muy complejos',
        'description': f'{large_workflows} workflows tienen más de 30 nodos. Workflows complejos son más difíciles de mantener y depurar. Considerar dividir en sub-workflows.',
        'impact': 'high'
    })
    
    # Recommendations
    practices['recommendations'].append({
        'title': 'Consolidar automatizaciones duplicadas',
        'description': 'Identificar y merge workflows con funcionalidad similar en una versión consolidada y parametrizable, reduciendo mantenimiento y errores.',
        'impact': 'critical'
    })
    
    practices['recommendations'].append({
        'title': 'Implementar Error Handling',
        'description': f'Agregar nodos de Error Trigger y manejo de errores en workflows críticos. Solo {error_handler_count} workflows tienen manejo de errores explícito.',
        'impact': 'high'
    })
    
    practices['recommendations'].append({
        'title': 'Usar Sub-workflows',
        'description': 'Para workflows con más de 20 nodos, considerar usar Execute Workflow nodes para modularizar lógica reutilizable.',
        'impact': 'medium'
    })
    
    practices['recommendations'].append({
        'title': 'Documentar con Sticky Notes',
        'description': 'Agregar notas sticky en cada workflow para describir su propósito, inputs, outputs, y decisiones clave de diseño.',
        'impact': 'low'
    })
    
    practices['recommendations'].append({
        'title': 'Versionar workflows',
        'description': 'Implementar un sistema de versiones para workflows (v1, v2, etc.) y mantener un changelog. Evitar múltiples versiones similares como se observa en los eCommerce agents.',
        'impact': 'medium'
    })
    
    practices['recommendations'].append({
        'title': 'Usar credenciales centralizadas',
        'description': 'Definir credenciales globales en n8n y reutilizarlas, evitando hardcodear API keys en nodos individuales.',
        'impact': 'critical'
    })
    
    practices['recommendations'].append({
        'title': 'Implementar testing automático',
        'description': 'Crear workflows de test que validen outputs esperados antes de activar automatizaciones en producción.',
        'impact': 'high'
    })
    
    return practices

def parse_workflow_json(filepath):
    """Parse a single n8n workflow JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                data = json.load(f)
        except:
            return None
    
    # Handle different n8n JSON formats
    nodes = data.get('nodes', [])
    connections = data.get('connections', {})
    name = data.get('name', '') or os.path.splitext(os.path.basename(filepath))[0]
    
    # Some workflows have different structures
    if not nodes and 'workflow' in data:
        inner = data['workflow']
        nodes = inner.get('nodes', [])
        connections = inner.get('connections', {})
        name = inner.get('name', name)
    
    node_types = get_node_types(nodes)
    node_names = get_node_names(nodes)
    node_count = len(nodes) if nodes else 0
    connection_count = get_connection_count(connections)
    
    # Extract tags
    tags = data.get('tags', [])
    if isinstance(tags, list):
        tag_names = [t.get('name', str(t)) if isinstance(t, dict) else str(t) for t in tags]
    else:
        tag_names = []
    
    # Extract source folder to determine origin
    path_parts = filepath.split('/')
    source = 'unknown'
    if 'Materiales comunidad whatsapp' in filepath:
        source = 'Materiales Comunidad WhatsApp'
    elif 'Plantillas GRATIS JosemaFernandez' in filepath:
        source = 'Plantillas JosemaFernandez'
    elif 'Sistema Agentes Marketing' in filepath:
        source = 'Sistema Agentes Marketing - Víctor Pérez'
    elif 'upload' in path_parts and filepath.endswith('.json'):
        # Root level files
        basename = os.path.basename(filepath)
        if basename == 'n8n.json':
            source = 'n8n (archivo root)'
        elif basename == 'Milvus_vs_Supabase.json':
            source = 'Milvus vs Supabase'
        elif basename == 'My_workflow_8.json':
            source = 'My Workflow 8'
    
    # Get specific folder category
    folder_category = ''
    for part in path_parts:
        if part not in ['upload', 'extracted', 'json de workflows n8n (Compilation)'] and len(part) > 3:
            if part != os.path.basename(filepath).replace('.json', ''):
                folder_category = part
    
    categories = categorize_workflow(node_types, name)
    
    # Create unique ID based on filepath hash
    wf_id = hashlib.md5(filepath.encode()).hexdigest()[:12]
    
    # Extract active status
    active = data.get('active', False)
    
    # Extract settings
    settings = data.get('settings', {})
    
    # Extract description/comments from sticky notes
    descriptions = []
    for node in (nodes or []):
        if isinstance(node, dict) and node.get('type') == 'n8n-nodes-base.stickyNote':
            content = node.get('parameters', {}).get('content', '')
            if content:
                descriptions.append(content)
    
    workflow = {
        'id': wf_id,
        'name': name,
        'file_path': filepath,
        'file_name': os.path.basename(filepath),
        'source': source,
        'folder_category': folder_category,
        'node_count': node_count,
        'connection_count': connection_count,
        'node_types': node_types,
        'node_names': node_names,
        'categories': categories,
        'tags': tag_names,
        'active': active,
        'descriptions': descriptions,
        'raw_nodes': nodes,  # Keep for further analysis
    }
    
    return workflow

def main():
    print("=" * 60)
    print("ANÁLISIS DE CATÁLOGO DE AUTOMATIZACIONES n8n")
    print("=" * 60)
    
    # Collect all JSON files
    all_json_files = []
    
    # Root level files
    for f in glob.glob(os.path.join(UPLOAD_DIR, "*.json")):
        all_json_files.append(f)
    
    # Extracted files
    for f in glob.glob(os.path.join(UPLOAD_DIR, "extracted", "**", "*.json"), recursive=True):
        all_json_files.append(f)
    
    print(f"\nTotal archivos JSON encontrados: {len(all_json_files)}")
    
    # Parse all workflows
    workflows = []
    errors = []
    for filepath in all_json_files:
        wf = parse_workflow_json(filepath)
        if wf:
            workflows.append(wf)
        else:
            errors.append(filepath)
    
    print(f"Workflows parseados exitosamente: {len(workflows)}")
    print(f"Errores de parseo: {len(errors)}")
    
    # Find duplications and similarities
    print("\nBuscando duplicaciones y similitudes...")
    duplications, similarities = find_duplications(workflows)
    
    print(f"Duplicaciones encontradas: {len(duplications)}")
    print(f"Similitudes encontradas: {len(similarities)}")
    
    # Analyze best practices
    print("\nAnalizando buenas prácticas...")
    practices = analyze_best_practices(workflows)
    
    # Update practices with duplication info
    practices['warnings'].append({
        'title': 'Workflows duplicados',
        'description': f'Se encontraron {len(duplications)} duplicaciones exactas y {len(similarities)} similitudes entre workflows. Esto genera mantenimiento redundante y inconsistencias.',
        'impact': 'critical'
    })
    
    # Generate statistics
    stats = {
        'total_workflows': len(workflows),
        'total_node_types': len(set(nt for wf in workflows for nt in wf.get('node_types', []))),
        'avg_node_count': round(sum(wf.get('node_count', 0) for wf in workflows) / len(workflows), 1) if workflows else 0,
        'max_node_count': max(wf.get('node_count', 0) for wf in workflows) if workflows else 0,
        'min_node_count': min(wf.get('node_count', 0) for wf in workflows) if workflows else 0,
        'duplications_count': len(duplications),
        'similarities_count': len(similarities),
        'categories_distribution': defaultdict(int),
        'sources_distribution': defaultdict(int),
        'node_type_frequency': defaultdict(int),
        'top_node_types': [],
    }
    
    for wf in workflows:
        for cat in wf.get('categories', []):
            stats['categories_distribution'][cat] += 1
        stats['sources_distribution'][wf.get('source', 'unknown')] += 1
        for nt in wf.get('node_types', []):
            stats['node_type_frequency'][nt] += 1
    
    # Top node types
    sorted_types = sorted(stats['node_type_frequency'].items(), key=lambda x: x[1], reverse=True)
    stats['top_node_types'] = [{'type': t, 'count': c} for t, c in sorted_types[:20]]
    
    # Convert defaultdicts to regular dicts
    stats['categories_distribution'] = dict(stats['categories_distribution'])
    stats['sources_distribution'] = dict(stats['sources_distribution'])
    stats['node_type_frequency'] = dict(stats['node_type_frequency'])
    
    # Create consolidated catalog - group by category
    catalog_by_category = defaultdict(list)
    for wf in workflows:
        primary_cat = wf.get('categories', ['General'])[0]
        wf_copy = {k: v for k, v in wf.items() if k != 'raw_nodes'}
        catalog_by_category[primary_cat].append(wf_copy)
    
    # Create consolidation suggestions
    consolidation_suggestions = []
    
    # Group similar workflows for consolidation
    processed_pairs = set()
    for sim in similarities + duplications:
        pair_key = (sim['workflow_1'], sim['workflow_2'])
        if pair_key in processed_pairs:
            continue
        processed_pairs.add(pair_key)
        
        # Find the workflows
        wf1 = next((w for w in workflows if w['id'] == sim['workflow_1']), None)
        wf2 = next((w for w in workflows if w['id'] == sim['workflow_2']), None)
        
        if wf1 and wf2:
            suggestion = {
                'group_name': normalize_name(wf1.get('name', '')),
                'workflows': [
                    {'id': wf1['id'], 'name': wf1.get('name', ''), 'source': wf1.get('source', ''), 'node_count': wf1.get('node_count', 0)},
                    {'id': wf2['id'], 'name': wf2.get('name', ''), 'source': wf2.get('source', ''), 'node_count': wf2.get('node_count', 0)},
                ],
                'similarity': sim['similarity'],
                'type': sim['type'],
                'suggestion': f'Consolidar en un workflow parametrizado que cubra ambas funcionalidades',
                'categories': list(set(wf1.get('categories', []) + wf2.get('categories', [])))
            }
            consolidation_suggestions.append(suggestion)
    
    # Build final output
    output = {
        'metadata': {
            'analysis_date': '2026-07-27',
            'total_files_analyzed': len(all_json_files),
            'total_workflows_parsed': len(workflows),
            'parse_errors': len(errors),
        },
        'stats': stats,
        'workflows': [{k: v for k, v in wf.items() if k != 'raw_nodes'} for wf in workflows],
        'catalog_by_category': dict(catalog_by_category),
        'duplications': duplications,
        'similarities': similarities,
        'consolidation_suggestions': consolidation_suggestions,
        'best_practices': practices,
    }
    
    # Save output
    output_path = os.path.join(OUTPUT_DIR, 'automation_catalog_analysis.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Análisis guardado en: {output_path}")
    print(f"\n--- RESUMEN ---")
    print(f"Total workflows: {len(workflows)}")
    print(f"Duplicaciones: {len(duplications)}")
    print(f"Similitudes: {len(similarities)}")
    print(f"Sugerencias de consolidación: {len(consolidation_suggestions)}")
    print(f"Categorías: {len(stats['categories_distribution'])}")
    
    print("\n--- DISTRIBUCIÓN POR CATEGORÍA ---")
    for cat, count in sorted(stats['categories_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count} workflows")
    
    print("\n--- DISTRIBUCIÓN POR FUENTE ---")
    for source, count in sorted(stats['sources_distribution'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} workflows")
    
    print("\n--- TOP 10 NODE TYPES ---")
    for item in stats['top_node_types'][:10]:
        print(f"  {item['type']}: {item['count']} usos")
    
    print("\n--- DUPLICACIONES ---")
    for d in duplications[:10]:
        print(f"  [{d['type']}] {d['name_1']} <-> {d['name_2']} (sim: {d['similarity']}%)")
    
    print("\n--- SIMILITUDES ---")
    for s in similarities[:10]:
        print(f"  [{s['type']}] {s['name_1']} <-> {s['name_2']} (sim: {s['similarity']}%)")
    
    return output

if __name__ == '__main__':
    result = main()
