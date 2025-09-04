
"""
Interactive HTML conversion report generation with clickable elements
"""

import re
from typing import List, Dict, Any
from datetime import datetime
from utils import (
    extract_unsupported_features, analyze_pipeline_complexity, 
    validate_conversion_feasibility, detect_languages, detect_tools,
    extract_all_credentials
)


def generate_conversion_report(action_paths: List[Dict[str, Any]], pipeline_text: str) -> str:
    """Generate an interactive HTML conversion report"""
    
    # Generate report timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Analyze the pipeline
    complexity_analysis = analyze_pipeline_complexity(pipeline_text)
    feasibility_analysis = validate_conversion_feasibility(pipeline_text)
    unsupported_features = extract_unsupported_features(pipeline_text)
    languages = detect_languages(pipeline_text)
    tools = detect_tools(pipeline_text)
    all_credentials = extract_all_credentials(pipeline_text)
    
    # Generate HTML report
    html_content = generate_interactive_html_report(
        action_paths, pipeline_text, timestamp, complexity_analysis,
        feasibility_analysis, unsupported_features, languages, tools, all_credentials
    )
    
    return html_content


def generate_interactive_html_report(
    action_paths: List[Dict[str, Any]], 
    pipeline_text: str, 
    timestamp: str,
    complexity_analysis: Dict[str, Any],
    feasibility_analysis: Dict[str, Any],
    unsupported_features: List[Dict[str, str]],
    languages: List[str],
    tools: List[str],
    all_credentials: set
) -> str:
    """Generate complete interactive HTML report"""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins to GitHub Actions Conversion Report</title>
    <style>
        {get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🚀 Jenkins to GitHub Actions Conversion Dashboard</h1>
            <div class="header-info">
                <span><strong>Generated:</strong> {timestamp}</span>
                <span><strong>Pipeline Complexity:</strong> {complexity_analysis['complexity_level']} ({complexity_analysis['complexity_score']} points)</span>
                <span><strong>Conversion Feasibility:</strong> {feasibility_analysis['confidence']}</span>
            </div>
        </header>

        <div class="status-section">
            <h2>📊 Conversion Status Overview</h2>
            <div class="badges">
                {generate_status_badges_html(action_paths, feasibility_analysis, complexity_analysis)}
            </div>
        </div>

        <div class="stats-section">
            <h2>📈 Quick Statistics</h2>
            <div class="stats-grid">
                {generate_interactive_stats_grid(action_paths, pipeline_text, complexity_analysis)}
            </div>
        </div>

        <div class="section">
            <h2>🛠️ Technology Stack Detected</h2>
            {generate_technology_stack_html(languages, tools)}
        </div>

        {generate_secrets_section_html(all_credentials, action_paths)}

        <div class="section">
            <h2>📋 Stage Conversion Details</h2>
            {generate_interactive_stages_html(action_paths)}
        </div>

        {generate_manual_conversion_section_html(action_paths, unsupported_features)}

        {generate_next_steps_html(action_paths, all_credentials, feasibility_analysis)}

        <div class="section">
            <h2>📁 Generated Files Structure</h2>
            {generate_file_structure_html(action_paths)}
        </div>
    </div>

    <script>
        {get_javascript_code()}
    </script>
</body>
</html>"""
    
    return html


def get_css_styles() -> str:
    """Generate CSS styles for the interactive report"""
    return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f7fa;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 15px;
        }

        .header-info {
            display: flex;
            justify-content: center;
            gap: 30px;
            font-size: 0.9em;
            flex-wrap: wrap;
        }

        .section {
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 10px;
        }

        .badges {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }

        .badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            color: white;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .badge:hover {
            transform: scale(1.05);
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }

        .badge-blue { background: #3182ce; }
        .badge-green { background: #38a169; }
        .badge-yellow { background: #d69e2e; }
        .badge-red { background: #e53e3e; }
        .badge-orange { background: #dd6b20; }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }

        .stat-card {
            background: #f7fafc;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }

        .stat-card.clickable:hover {
            background: #edf2f7;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #4a5568;
            font-size: 0.9em;
        }

        .stat-description {
            color: #718096;
            font-size: 0.8em;
            margin-top: 5px;
        }

        .collapsible {
            background: #f1f5f9;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin: 10px 0;
        }

        .collapsible-header {
            background: #e2e8f0;
            padding: 15px;
            cursor: pointer;
            font-weight: bold;
            border-radius: 7px 7px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .collapsible-header:hover {
            background: #cbd5e0;
        }

        .collapsible-content {
            padding: 20px;
            display: none;
            border-top: 1px solid #e2e8f0;
        }

        .collapsible-content.show {
            display: block;
        }

        .stage-card {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin: 10px 0;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .stage-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }

        .stage-header {
            background: #f8f9fa;
            padding: 15px;
            cursor: pointer;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s ease;
        }

        .stage-header:hover {
            background: #e9ecef;
        }

        .stage-content {
            padding: 20px;
            display: none;
            background: #fafbfc;
            animation: slideDown 0.3s ease;
        }

        .stage-content.show {
            display: block;
        }

        @keyframes slideDown {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .stage-info {
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
        }

        .stage-tag {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .stage-tag:hover {
            transform: scale(1.1);
        }

        .tag-docker { background: #0066cc; }
        .tag-k8s { background: #326ce5; }
        .tag-sonar { background: #4e9bcd; }
        .tag-approval { background: #f56500; }
        .tag-post { background: #6f42c1; }

        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px;
            border-radius: 6px;
            font-family: 'Monaco', 'Consolas', monospace;
            font-size: 0.9em;
            overflow-x: auto;
            margin: 10px 0;
            position: relative;
        }

        .copy-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            background: #4a5568;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.8em;
        }

        .copy-btn:hover {
            background: #2d3748;
        }

        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 10px 0;
        }

        .tech-tag {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .tech-tag:hover {
            background: #5a67d8;
            transform: scale(1.05);
        }

        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .modal-content {
            background-color: white;
            margin: 5% auto;
            padding: 30px;
            border-radius: 12px;
            width: 90%;
            max-width: 800px;
            max-height: 80vh;
            overflow-y: auto;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from { transform: translateY(-50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
            cursor: pointer;
            transition: color 0.3s ease;
        }

        .close:hover {
            color: #000;
        }

        .arrow {
            transition: transform 0.3s ease;
            font-size: 1.2em;
        }

        .arrow.rotated {
            transform: rotate(90deg);
        }

        .stages-list {
            max-height: 400px;
            overflow-y: auto;
        }

        .stage-summary {
            padding: 15px;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            margin: 10px 0;
            background: #f8f9fa;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .stage-summary:hover {
            background: #e9ecef;
            transform: translateX(5px);
        }

        .breadcrumb {
            background: #f1f5f9;
            padding: 10px 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 0.9em;
            color: #4a5568;
        }

        .breadcrumb a {
            color: #667eea;
            text-decoration: none;
            cursor: pointer;
        }

        .breadcrumb a:hover {
            text-decoration: underline;
        }

        .quick-nav {
            position: fixed;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 15px;
            z-index: 100;
        }

        .quick-nav h4 {
            margin-bottom: 10px;
            color: #2d3748;
            font-size: 0.9em;
        }

        .quick-nav ul {
            list-style: none;
            padding: 0;
        }

        .quick-nav li {
            margin: 5px 0;
        }

        .quick-nav a {
            color: #667eea;
            text-decoration: none;
            font-size: 0.8em;
            display: block;
            padding: 5px;
            border-radius: 4px;
            transition: background 0.3s ease;
        }

        .quick-nav a:hover {
            background: #edf2f7;
        }

        @media (max-width: 768px) {
            .header-info {
                flex-direction: column;
                gap: 10px;
            }
            
            .stats-grid {
                grid-template-columns: 1fr;
            }

            .quick-nav {
                display: none;
            }

            .stage-info {
                flex-direction: column;
                gap: 10px;
            }
        }
    """


def get_javascript_code() -> str:
    """Generate JavaScript code for interactivity"""
    return """
        // Global state for navigation
        let currentView = 'overview';
        let stageData = {};

        // Toggle collapsible sections with animation
        function toggleCollapsible(element) {
            const content = element.nextElementSibling;
            const arrow = element.querySelector('.arrow');
            
            if (content.classList.contains('show')) {
                content.classList.remove('show');
                arrow.classList.remove('rotated');
            } else {
                // Close other open sections in the same container
                const container = element.closest('.section');
                if (container) {
                    container.querySelectorAll('.collapsible-content.show').forEach(openContent => {
                        if (openContent !== content) {
                            openContent.classList.remove('show');
                            const openArrow = openContent.previousElementSibling.querySelector('.arrow');
                            if (openArrow) openArrow.classList.remove('rotated');
                        }
                    });
                }
                
                content.classList.add('show');
                arrow.classList.add('rotated');
            }
        }

        // Enhanced stage navigation
        function showStagesList() {
            const modal = document.getElementById('contentModal');
            const modalTitle = document.getElementById('contentModalTitle');
            const modalBody = document.getElementById('contentModalBody');
            
            modalTitle.innerHTML = '📋 All Converted Stages <span style="font-size: 0.8em; color: #666;">(Click on any stage to see details)</span>';
            
            let stagesHtml = '<div class="stages-navigation">';
            
            // Get all stages from the page
            const stageCards = document.querySelectorAll('.stage-card');
            stageCards.forEach((card, index) => {
                const stageName = card.querySelector('.stage-header strong').textContent;
                const tags = Array.from(card.querySelectorAll('.stage-tag')).map(tag => tag.outerHTML).join('');
                const status = card.querySelector('.stage-header').textContent.includes('Manual') ? '⚠️ Manual' : '✅ Ready';
                
                stagesHtml += `
                    <div class="stage-summary" onclick="showStageDetails('${stageName}', ${index})">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <strong>${stageName}</strong>
                            <span>${status}</span>
                        </div>
                        <div style="margin: 8px 0;">${tags}</div>
                        <div style="font-size: 0.9em; color: #666;">Click to view detailed conversion information</div>
                    </div>
                `;
            });
            
            stagesHtml += '</div>';
            modalBody.innerHTML = stagesHtml;
            modal.style.display = 'block';
        }

        // Show individual stage details
        function showStageDetails(stageName, stageIndex) {
            const modal = document.getElementById('contentModal');
            const modalTitle = document.getElementById('contentModalTitle');
            const modalBody = document.getElementById('contentModalBody');
            
            // Get stage content from the page
            const stageCards = document.querySelectorAll('.stage-card');
            const stageCard = stageCards[stageIndex];
            const stageContent = stageCard.querySelector('.stage-content');
            
            modalTitle.innerHTML = `
                <div class="breadcrumb">
                    <a onclick="showStagesList()">← All Stages</a> / ${stageName}
                </div>
            `;
            
            let detailsHtml = `
                <div class="stage-details-view">
                    <h3>${stageName}</h3>
                    ${stageContent.innerHTML}
                    
                    <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                        <h4>Quick Actions</h4>
                        <button onclick="copyStageInfo('${stageName}')" class="copy-btn" style="position: static; margin: 5px;">Copy Stage Info</button>
                        <button onclick="showStagesList()" class="copy-btn" style="position: static; margin: 5px; background: #667eea;">Back to All Stages</button>
                    </div>
                </div>
            `;
            
            modalBody.innerHTML = detailsHtml;
        }

        // Copy stage information to clipboard
        function copyStageInfo(stageName) {
            const stageCards = document.querySelectorAll('.stage-card');
            let stageInfo = '';
            
            stageCards.forEach(card => {
                const cardStageName = card.querySelector('.stage-header strong').textContent;
                if (cardStageName === stageName) {
                    const content = card.querySelector('.stage-content');
                    stageInfo = `Stage: ${stageName}\n${content.textContent}`;
                }
            });
            
            navigator.clipboard.writeText(stageInfo).then(() => {
                showNotification('Stage information copied to clipboard!');
            });
        }

        // Show notification
        function showNotification(message) {
            const notification = document.createElement('div');
            notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #38a169;
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                z-index: 2000;
                animation: slideIn 0.3s ease;
            `;
            notification.textContent = message;
            document.body.appendChild(notification);
            
            setTimeout(() => {
                notification.remove();
            }, 3000);
        }

        // Enhanced clickable content with better navigation
        function showClickableContent(type, data) {
            const modal = document.getElementById('contentModal');
            const modalTitle = document.getElementById('contentModalTitle');
            const modalBody = document.getElementById('contentModalBody');
            
            modalTitle.textContent = type;
            
            // Special handling for stages converted
            if (type === 'Total Stages Converted') {
                showStagesList();
                return;
            }
            
            modalBody.innerHTML = data;
            modal.style.display = 'block';
        }

        // Close modal
        function closeModal() {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                modal.style.display = 'none';
            });
        }

        // Smooth scroll to section
        function scrollToSection(sectionId) {
            const section = document.getElementById(sectionId);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth' });
            }
        }

        // Filter stages by type
        function filterStages(filterType) {
            const stageCards = document.querySelectorAll('.stage-card');
            
            stageCards.forEach(card => {
                const tags = card.querySelectorAll('.stage-tag');
                let shouldShow = filterType === 'all';
                
                if (!shouldShow) {
                    tags.forEach(tag => {
                        if (tag.textContent.toLowerCase().includes(filterType.toLowerCase())) {
                            shouldShow = true;
                        }
                    });
                }
                
                card.style.display = shouldShow ? 'block' : 'none';
            });
        }

        // Search functionality
        function searchStages(searchTerm) {
            const stageCards = document.querySelectorAll('.stage-card');
            const term = searchTerm.toLowerCase();
            
            stageCards.forEach(card => {
                const stageName = card.querySelector('.stage-header strong').textContent.toLowerCase();
                const stageContent = card.querySelector('.stage-content').textContent.toLowerCase();
                
                const matches = stageName.includes(term) || stageContent.includes(term);
                card.style.display = matches ? 'block' : 'none';
            });
        }

        // Switch between tabs in stage details
        function switchTab(stageIndex, tabIndex) {
            const tabHeaders = document.querySelectorAll(`#stage-tabs-${stageIndex} .tab-header`);
            const tabPanes = document.querySelectorAll(`#stage-tabs-${stageIndex} .tab-pane`);
            
            // Update headers
            tabHeaders.forEach((header, i) => {
                if (i === tabIndex) {
                    header.style.background = '#667eea';
                    header.style.color = 'white';
                } else {
                    header.style.background = '#f8f9fa';
                    header.style.color = '#666';
                }
            });
            
            // Update panes
            tabPanes.forEach((pane, i) => {
                pane.style.display = i === tabIndex ? 'block' : 'none';
            });
        }

        // Initialize page with enhanced functionality
        document.addEventListener('DOMContentLoaded', function() {
            // Close modals when clicking outside
            window.onclick = function(event) {
                const modals = document.querySelectorAll('.modal');
                modals.forEach(modal => {
                    if (event.target === modal) {
                        modal.style.display = 'none';
                    }
                });
            }

            // Add click handlers for stat cards
            document.querySelectorAll('.stat-card.clickable').forEach(card => {
                card.addEventListener('click', function() {
                    const type = this.dataset.type;
                    const content = this.dataset.content;
                    showClickableContent(type, content);
                });
            });

            // Add click handlers for badges
            document.querySelectorAll('.badge').forEach(badge => {
                badge.addEventListener('click', function() {
                    const text = this.textContent;
                    if (text.includes('Stages Converted')) {
                        showStagesList();
                    } else if (text.includes('Manual Required')) {
                        filterStages('manual');
                        scrollToSection('stages-section');
                    }
                });
            });

            // Add click handlers for filter buttons
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.addEventListener('click', function() {
                    // Update button styles
                    document.querySelectorAll('.filter-btn').forEach(b => {
                        b.style.background = 'white';
                        b.style.color = '#333';
                        b.style.border = '1px solid #e2e8f0';
                    });
                    
                    this.style.background = '#667eea';
                    this.style.color = 'white';
                    this.style.border = '1px solid #667eea';
                });
            });

            // Add search functionality
            const searchInput = document.createElement('input');
            searchInput.type = 'text';
            searchInput.placeholder = 'Search stages...';
            searchInput.style.cssText = `
                width: 100%;
                padding: 10px;
                margin-bottom: 20px;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                font-size: 0.9em;
            `;
            
            searchInput.addEventListener('input', function() {
                searchStages(this.value);
            });
            
            const stagesSection = document.querySelector('.section h2');
            if (stagesSection && stagesSection.textContent.includes('Stage Conversion')) {
                stagesSection.parentNode.insertBefore(searchInput, stagesSection.nextSibling);
            }

            // Add keyboard shortcuts
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape') {
                    closeModal();
                }
                if (e.ctrlKey && e.key === 'f') {
                    e.preventDefault();
                    searchInput.focus();
                }
            });

            // Add copy buttons to code blocks
            document.querySelectorAll('.code-block').forEach(block => {
                const copyBtn = document.createElement('button');
                copyBtn.className = 'copy-btn';
                copyBtn.textContent = 'Copy';
                copyBtn.onclick = function() {
                    navigator.clipboard.writeText(block.textContent).then(() => {
                        this.textContent = 'Copied!';
                        setTimeout(() => {
                            this.textContent = 'Copy';
                        }, 2000);
                    });
                };
                block.style.position = 'relative';
                block.appendChild(copyBtn);
            });

            // Add quick navigation
            createQuickNavigation();

            // Initialize filter buttons
            const allBtn = document.querySelector('.filter-btn');
            if (allBtn) {
                allBtn.style.background = '#667eea';
                allBtn.style.color = 'white';
                allBtn.style.border = '1px solid #667eea';
            }
        });

        // Create quick navigation panel
        function createQuickNavigation() {
            const quickNav = document.createElement('div');
            quickNav.className = 'quick-nav';
            quickNav.innerHTML = `
                <h4>Quick Navigation</h4>
                <ul>
                    <li><a onclick="scrollToSection('overview')">Overview</a></li>
                    <li><a onclick="scrollToSection('stats')">Statistics</a></li>
                    <li><a onclick="scrollToSection('stages')">Stages</a></li>
                    <li><a onclick="showStagesList()">All Stages</a></li>
                    <li><a onclick="filterStages('docker')">Docker Stages</a></li>
                    <li><a onclick="filterStages('k8s')">K8s Stages</a></li>
                    <li><a onclick="filterStages('all')">Show All</a></li>
                </ul>
            `;
            document.body.appendChild(quickNav);
        }
    """


def generate_status_badges_html(action_paths: List[Dict[str, Any]], feasibility: Dict[str, Any], complexity: Dict[str, Any]) -> str:
    """Generate HTML status badges with click functionality"""
    total_stages = len(action_paths)
    manual_stages = len([a for a in action_paths if a.get("manual_conversion_needed")])
    
    feasibility_color = {"High": "badge-green", "Medium": "badge-yellow", "Low": "badge-red"}.get(feasibility["confidence"], "badge-red")
    complexity_color = {"Low": "badge-green", "Medium": "badge-yellow", "High": "badge-orange", "Very High": "badge-red"}.get(complexity["complexity_level"], "badge-red")
    
    return f"""
        <div class="badge badge-blue" onclick="showStagesList()" title="Click to see all converted stages">
            📋 Stages Converted: {total_stages}
        </div>
        <div class="badge badge-orange" onclick="filterStages('manual'); scrollToSection('stages-section')" title="Click to see stages requiring manual work">
            ⚠️ Manual Required: {manual_stages}
        </div>
        <div class="badge {feasibility_color}" title="Conversion feasibility assessment">
            🎯 Feasibility: {feasibility["confidence"]}
        </div>
        <div class="badge {complexity_color}" title="Pipeline complexity level">
            📊 Complexity: {complexity["complexity_level"]}
        </div>
    """


def generate_interactive_stats_grid(action_paths: List[Dict[str, Any]], pipeline_text: str, complexity: Dict[str, Any]) -> str:
    """Generate interactive statistics grid with clickable elements"""
    total_stages = len(action_paths)
    docker_stages = [a for a in action_paths if a.get("has_docker")]
    k8s_stages = [a for a in action_paths if a.get("has_kubectl")]
    sonar_stages = [a for a in action_paths if a.get("has_sonarqube")]
    approval_stages = [a for a in action_paths if a.get("approval_environment")]
    post_action_stages = [a for a in action_paths if a.get("has_post_actions")]
    manual_stages = [a for a in action_paths if a.get("manual_conversion_needed")]
    
    # Generate detailed content for each stat
    stages_detail = generate_stages_detail_html(action_paths)
    docker_detail = generate_feature_detail_html("Docker Operations", docker_stages)
    k8s_detail = generate_feature_detail_html("Kubernetes Operations", k8s_stages)
    sonar_detail = generate_feature_detail_html("SonarQube Integration", sonar_stages)
    approval_detail = generate_feature_detail_html("Approval Gates", approval_stages)
    post_detail = generate_feature_detail_html("Post-Action Stages", post_action_stages)
    manual_detail = generate_manual_detail_html(manual_stages)
    
    return f"""
        <div class="stat-card clickable" data-type="Total Stages Converted" data-content='{stages_detail}'>
            <div class="stat-value">{total_stages}</div>
            <div class="stat-label">Total Stages</div>
            <div class="stat-description">Click to see all converted stages</div>
        </div>
        <div class="stat-card clickable" data-type="Docker Operations" data-content='{docker_detail}'>
            <div class="stat-value">{len(docker_stages)}</div>
            <div class="stat-label">Docker Stages</div>
            <div class="stat-description">Stages with Docker build/push operations</div>
        </div>
        <div class="stat-card clickable" data-type="Kubernetes Operations" data-content='{k8s_detail}'>
            <div class="stat-value">{len(k8s_stages)}</div>
            <div class="stat-label">Kubernetes Stages</div>
            <div class="stat-description">Stages with kubectl/helm commands</div>
        </div>
        <div class="stat-card clickable" data-type="SonarQube Integration" data-content='{sonar_detail}'>
            <div class="stat-value">{len(sonar_stages)}</div>
            <div class="stat-label">SonarQube Stages</div>
            <div class="stat-description">Stages with code quality scanning</div>
        </div>
        <div class="stat-card clickable" data-type="Approval Gates" data-content='{approval_detail}'>
            <div class="stat-value">{len(approval_stages)}</div>
            <div class="stat-label">Approval Gates</div>
            <div class="stat-description">Stages requiring manual approval</div>
        </div>
        <div class="stat-card clickable" data-type="Post-Action Handling" data-content='{post_detail}'>
            <div class="stat-value">{len(post_action_stages)}</div>
            <div class="stat-label">Post-Actions</div>
            <div class="stat-description">Stages with post-execution actions</div>
        </div>
        <div class="stat-card clickable" data-type="Manual Conversion Required" data-content='{manual_detail}'>
            <div class="stat-value">{len(manual_stages)}</div>
            <div class="stat-label">Manual Items</div>
            <div class="stat-description">Stages needing manual attention</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{complexity['complexity_score']}</div>
            <div class="stat-label">Complexity Score</div>
            <div class="stat-description">Overall pipeline complexity rating</div>
        </div>
    """


def generate_stages_detail_html(action_paths: List[Dict[str, Any]]) -> str:
    """Generate detailed HTML for all stages"""
    stages_html = "<h3>All Converted Stages</h3><div class='stages-list'>"
    
    for i, action in enumerate(action_paths, 1):
        features = []
        if action.get("has_docker"):
            features.append("<span class='stage-tag tag-docker'>Docker</span>")
        if action.get("has_kubectl"):
            features.append("<span class='stage-tag tag-k8s'>K8s</span>")
        if action.get("has_sonarqube"):
            features.append("<span class='stage-tag tag-sonar'>SonarQube</span>")
        if action.get("approval_environment"):
            features.append("<span class='stage-tag tag-approval'>Approval</span>")
        if action.get("has_post_actions"):
            features.append("<span class='stage-tag tag-post'>Post-Actions</span>")
        
        complexity = action.get("complexity_score", 0)
        complexity_level = "Low" if complexity < 10 else "Medium" if complexity < 25 else "High"
        
        stages_html += f"""
            <div class='stage-summary'>
                <strong>{i}. {action['name']}</strong>
                <div style='margin: 5px 0;'>{"".join(features)}</div>
                <div style='font-size: 0.9em; color: #666;'>
                    Complexity: {complexity_level} ({complexity}) | 
                    Action Path: {action['path']}
                </div>
            </div>
        """
    
    stages_html += "</div>"
    return stages_html.replace("'", "\\'")


def generate_feature_detail_html(feature_name: str, stages: List[Dict[str, Any]]) -> str:
    """Generate detailed HTML for stages with specific features"""
    if not stages:
        return f"<h3>{feature_name}</h3><p>No stages found with this feature.</p>"
    
    detail_html = f"<h3>{feature_name}</h3><div class='feature-stages'>"
    
    for stage in stages:
        detail_html += f"""
            <div class='feature-stage'>
                <strong>{stage['name']}</strong>
                <div style='margin: 5px 0; font-size: 0.9em; color: #666;'>
                    Path: {stage['path']}
                </div>
            </div>
        """
    
    detail_html += "</div>"
    return detail_html.replace("'", "\\'")


def generate_manual_detail_html(manual_stages: List[Dict[str, Any]]) -> str:
    """Generate detailed HTML for stages requiring manual conversion"""
    if not manual_stages:
        return "<h3>Manual Conversion Required</h3><p>All stages converted successfully!</p>"
    
    detail_html = "<h3>Stages Requiring Manual Attention</h3><div class='manual-stages'>"
    
    for stage in manual_stages:
        manual_items = stage.get("manual_conversion_needed", [])
        detail_html += f"""
            <div class='manual-stage'>
                <strong>{stage['name']}</strong>
                <ul style='margin: 10px 0; padding-left: 20px;'>
        """
        
        for item in manual_items:
            detail_html += f"<li>{item}</li>"
        
        detail_html += """
                </ul>
            </div>
        """
    
    detail_html += "</div>"
    return detail_html.replace("'", "\\'")


def generate_technology_stack_html(languages: List[str], tools: List[str]) -> str:
    """Generate HTML for technology stack"""
    html = ""
    
    if languages:
        html += "<h4>Languages/Frameworks</h4><div class='tech-tags'>"
        for lang in languages:
            html += f"<span class='tech-tag'>{lang}</span>"
        html += "</div>"
    
    if tools:
        html += "<h4>Tools & Technologies</h4><div class='tech-tags'>"
        for tool in tools:
            html += f"<span class='tech-tag'>{tool}</span>"
        html += "</div>"
    
    return html if html else "<p>No specific technologies detected</p>"


def generate_secrets_section_html(all_credentials: set, action_paths: List[Dict[str, Any]]) -> str:
    """Generate HTML for secrets configuration section"""
    if not all_credentials:
        return ""
    
    html = """
        <div class="section">
            <h2>🔐 Required GitHub Secrets Configuration</h2>
            <div class="collapsible">
                <div class="collapsible-header" onclick="toggleCollapsible(this)">
                    <span>Secret Configuration Details</span>
                    <span class="arrow">▶</span>
                </div>
                <div class="collapsible-content">
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #f8f9fa;">
                                <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Secret Name</th>
                                <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Purpose</th>
                                <th style="padding: 10px; text-align: left; border: 1px solid #dee2e6;">Type</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    # Process credentials
    for cred in sorted(all_credentials):
        secret_name = cred.upper().replace("-", "_").replace(".", "_")
        purpose = get_credential_purpose(cred)
        cred_type = detect_credential_type(cred)
        
        html += f"""
                            <tr>
                                <td style="padding: 10px; border: 1px solid #dee2e6;"><code>{secret_name}</code></td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">{purpose}</td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">{cred_type}</td>
                            </tr>
        """
    
    # Add common secrets
    if any(a.get("has_docker") for a in action_paths):
        html += """
                            <tr>
                                <td style="padding: 10px; border: 1px solid #dee2e6;"><code>DOCKER_USERNAME</code></td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">Docker registry authentication</td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">Username</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #dee2e6;"><code>DOCKER_PASSWORD</code></td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">Docker registry authentication</td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">Password/Token</td>
                            </tr>
        """
    
    if any(a.get("has_sonarqube") for a in action_paths):
        html += """
                            <tr>
                                <td style="padding: 10px; border: 1px solid #dee2e6;"><code>SONAR_TOKEN</code></td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">SonarQube server authentication</td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">Token</td>
                            </tr>
                            <tr>
                                <td style="padding: 10px; border: 1px solid #dee2e6;"><code>SONAR_HOST_URL</code></td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">SonarQube server URL</td>
                                <td style="padding: 10px; border: 1px solid #dee2e6;">URL</td>
                            </tr>
        """
    
    html += """
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    """
    
    return html


def generate_interactive_stages_html(action_paths: List[Dict[str, Any]]) -> str:
    """Generate interactive HTML for stage details with enhanced navigation"""
    html = f"""
        <div id="stages-section">
            <div style="margin-bottom: 20px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
                <button onclick="filterStages('all')" class="filter-btn" style="padding: 8px 15px; border: 1px solid #e2e8f0; background: white; border-radius: 6px; cursor: pointer;">All Stages</button>
                <button onclick="filterStages('docker')" class="filter-btn" style="padding: 8px 15px; border: 1px solid #0066cc; background: #0066cc; color: white; border-radius: 6px; cursor: pointer;">Docker</button>
                <button onclick="filterStages('k8s')" class="filter-btn" style="padding: 8px 15px; border: 1px solid #326ce5; background: #326ce5; color: white; border-radius: 6px; cursor: pointer;">Kubernetes</button>
                <button onclick="filterStages('sonar')" class="filter-btn" style="padding: 8px 15px; border: 1px solid #4e9bcd; background: #4e9bcd; color: white; border-radius: 6px; cursor: pointer;">SonarQube</button>
                <button onclick="filterStages('manual')" class="filter-btn" style="padding: 8px 15px; border: 1px solid #f56500; background: #f56500; color: white; border-radius: 6px; cursor: pointer;">Manual Required</button>
            </div>
    """
    
    for i, action in enumerate(action_paths):
        stage_name = action["name"]
        complexity = action.get("complexity_score", 0)
        complexity_level = "Low" if complexity < 10 else "Medium" if complexity < 25 else "High"
        complexity_color = "#38a169" if complexity < 10 else "#d69e2e" if complexity < 25 else "#e53e3e"
        
        # Generate stage tags with click functionality
        tags = []
        if action.get("has_docker"):
            tags.append("<span class='stage-tag tag-docker' onclick='filterStages(\"docker\")' title='Click to filter Docker stages'>🐳 Docker</span>")
        if action.get("has_kubectl"):
            tags.append("<span class='stage-tag tag-k8s' onclick='filterStages(\"k8s\")' title='Click to filter Kubernetes stages'>☸️ K8s</span>")
        if action.get("has_sonarqube"):
            tags.append("<span class='stage-tag tag-sonar' onclick='filterStages(\"sonar\")' title='Click to filter SonarQube stages'>🔍 SonarQube</span>")
        if action.get("approval_environment"):
            tags.append("<span class='stage-tag tag-approval' onclick='filterStages(\"approval\")' title='Click to filter approval stages'>✋ Approval</span>")
        if action.get("has_post_actions"):
            tags.append("<span class='stage-tag tag-post' onclick='filterStages(\"post\")' title='Click to filter post-action stages'>📋 Post-Actions</span>")
        
        manual_items = action.get("manual_conversion_needed", [])
        status_icon = "⚠️" if manual_items else "✅"
        status_text = "Manual Required" if manual_items else "Ready to Deploy"
        status_class = "manual-required" if manual_items else "ready"
        
        # Add data attributes for filtering
        filter_classes = []
        if action.get("has_docker"): filter_classes.append("docker")
        if action.get("has_kubectl"): filter_classes.append("k8s")
        if action.get("has_sonarqube"): filter_classes.append("sonar")
        if action.get("approval_environment"): filter_classes.append("approval")
        if action.get("has_post_actions"): filter_classes.append("post")
        if manual_items: filter_classes.append("manual")
        
        html += f"""
            <div class="stage-card {' '.join(filter_classes)}" data-stage-index="{i}">
                <div class="stage-header" onclick="toggleCollapsible(this)">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                            <strong style="font-size: 1.1em;">{stage_name}</strong>
                            <span style="background: {complexity_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">
                                {complexity_level}
                            </span>
                        </div>
                        <div style="margin-bottom: 8px;">{"".join(tags)}</div>
                        <div style="font-size: 0.9em; color: #666;">
                            📁 {action['path']} | 🔑 {len(action.get('credentials', []))} credentials
                        </div>
                    </div>
                    <div style="display: flex; flex-direction: column; align-items: center; gap: 5px;">
                        <span class="{status_class}" style="font-size: 0.9em; font-weight: bold;">
                            {status_icon} {status_text}
                        </span>
                        <span class="arrow">▶</span>
                    </div>
                </div>
                <div class="stage-content">
                    <div class="stage-info">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px;">
                            <div>
                                <strong>📊 Complexity Score:</strong><br>
                                <span style="color: {complexity_color}; font-weight: bold;">{complexity_level} ({complexity} points)</span>
                            </div>
                            <div>
                                <strong>📂 Action Path:</strong><br>
                                <code style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px;">{action['path']}</code>
                            </div>
                            <div>
                                <strong>🔐 Credentials Required:</strong><br>
                                <span style="color: #667eea; font-weight: bold;">{len(action.get('credentials', []))} items</span>
                            </div>
                        </div>
                    </div>
                    
                    {generate_enhanced_stage_details_content(action, i)}
                    
                    <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;">
                        <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                            <button onclick="copyStageInfo('{stage_name}')" class="copy-btn" style="position: static; margin: 0;">📋 Copy Stage Info</button>
                            <button onclick="showStageDetails('{stage_name}', {i})" class="copy-btn" style="position: static; margin: 0; background: #667eea;">🔍 View Details</button>
                        </div>
                    </div>
                </div>
            </div>
        """
    
    html += "</div>"
    return html


def generate_stage_details_content(action: Dict[str, Any]) -> str:
    """Generate detailed content for a specific stage"""
    html = ""
    
    # Environment variables
    if action.get("env"):
        html += "<h4>Environment Variables</h4>"
        html += "<div class='code-block'>"
        for key, value in action["env"].items():
            html += f"{key}={value}<br>"
        html += "</div>"
    
    # Credentials
    if action.get("credentials"):
        html += "<h4>Required Credentials</h4><ul>"
        for cred in action["credentials"]:
            html += f"<li><code>{cred}</code></li>"
        html += "</ul>"
    
    # Manual conversion items
    if action.get("manual_conversion_needed"):
        html += "<h4>Manual Conversion Required</h4><ul>"
        for item in action["manual_conversion_needed"]:
            html += f"<li>{item}</li>"
        html += "</ul>"
    
    # Post-action types
    if action.get("post_action_types"):
        html += "<h4>Post-Action Types</h4><ul>"
        for post_type in action["post_action_types"]:
            html += f"<li>{post_type}</li>"
        html += "</ul>"
    
    # Plugin dependencies
    if action.get("plugin_dependencies"):
        html += "<h4>Plugin Dependencies</h4><ul>"
        for plugin in action["plugin_dependencies"]:
            html += f"<li>{plugin}</li>"
        html += "</ul>"
    
    return html


def generate_enhanced_stage_details_content(action: Dict[str, Any], stage_index: int) -> str:
    """Generate enhanced detailed content for a specific stage with better formatting"""
    html = ""
    
    # Create tabbed interface for different types of information
    tabs = []
    tab_contents = []
    
    # Environment variables tab
    if action.get("env"):
        tabs.append("Environment")
        env_content = "<div class='tab-content'><h4>🌍 Environment Variables</h4>"
        env_content += "<div class='code-block' style='position: relative;'>"
        for key, value in action["env"].items():
            env_content += f"{key}={value}\n"
        env_content += "</div></div>"
        tab_contents.append(env_content)
    
    # Credentials tab
    if action.get("credentials"):
        tabs.append("Credentials")
        cred_content = "<div class='tab-content'><h4>🔐 Required Credentials</h4>"
        cred_content += "<div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 10px;'>"
        for cred in action["credentials"]:
            cred_type = detect_credential_type(cred)
            cred_content += f"""
                <div style='padding: 10px; background: #f8f9fa; border-radius: 6px; border-left: 3px solid #667eea;'>
                    <code style='font-weight: bold;'>{cred}</code><br>
                    <small style='color: #666;'>{cred_type}</small>
                </div>
            """
        cred_content += "</div></div>"
        tab_contents.append(cred_content)
    
    # Manual conversion tab
    if action.get("manual_conversion_needed"):
        tabs.append("Manual Tasks")
        manual_content = "<div class='tab-content'><h4>⚠️ Manual Conversion Required</h4>"
        manual_content += "<div style='background: #fef5e7; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b;'>"
        manual_content += "<ul style='margin: 0; padding-left: 20px;'>"
        for item in action["manual_conversion_needed"]:
            manual_content += f"<li style='margin: 8px 0;'>{item}</li>"
        manual_content += "</ul></div></div>"
        tab_contents.append(manual_content)
    
    # Technical details tab
    tech_details = []
    if action.get("post_action_types"):
        tech_details.append(("Post-Action Types", action["post_action_types"]))
    if action.get("plugin_dependencies"):
        tech_details.append(("Plugin Dependencies", action["plugin_dependencies"]))
    
    if tech_details:
        tabs.append("Technical")
        tech_content = "<div class='tab-content'><h4>🔧 Technical Details</h4>"
        for title, items in tech_details:
            tech_content += f"<h5>{title}</h5><ul>"
            for item in items:
                tech_content += f"<li>{item}</li>"
            tech_content += "</ul>"
        tech_content += "</div>"
        tab_contents.append(tech_content)
    
    # Generate tabbed interface if there are tabs
    if tabs:
        html += f"""
            <div class="stage-tabs" id="stage-tabs-{stage_index}">
                <div class="tab-headers" style="display: flex; gap: 5px; margin-bottom: 15px; border-bottom: 1px solid #e2e8f0;">
        """
        
        for i, tab in enumerate(tabs):
            active_class = "active" if i == 0 else ""
            html += f"""
                <button class="tab-header {active_class}" onclick="switchTab({stage_index}, {i})" 
                        style="padding: 8px 15px; border: none; background: {'#667eea' if i == 0 else '#f8f9fa'}; 
                               color: {'white' if i == 0 else '#666'}; border-radius: 6px 6px 0 0; cursor: pointer; 
                               transition: all 0.3s ease;">
                    {tab}
                </button>
            """
        
        html += "</div><div class='tab-contents'>"
        
        for i, content in enumerate(tab_contents):
            display_style = "block" if i == 0 else "none"
            html += f"<div class='tab-pane' id='tab-{stage_index}-{i}' style='display: {display_style};'>{content}</div>"
        
        html += "</div></div>"
    
    return html


def generate_manual_conversion_section_html(action_paths: List[Dict[str, Any]], unsupported_features: List[Dict[str, str]]) -> str:
    """Generate HTML for manual conversion requirements"""
    manual_stages = [a for a in action_paths if a.get("manual_conversion_needed")]
    
    if not manual_stages and not unsupported_features:
        return ""
    
    html = """
        <div class="section">
            <h2>🔧 Manual Conversion Required</h2>
    """
    
    if manual_stages:
        html += """
            <div class="collapsible">
                <div class="collapsible-header" onclick="toggleCollapsible(this)">
                    <span>Stage-Level Manual Items</span>
                    <span class="arrow">▶</span>
                </div>
                <div class="collapsible-content">
        """
        
        for stage in manual_stages:
            html += f"""
                <div style="margin-bottom: 20px; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px;">
                    <h4>{stage['name']}</h4>
                    <ul>
            """
            for item in stage.get("manual_conversion_needed", []):
                html += f"<li>{item}</li>"
            html += "</ul></div>"
        
        html += "</div></div>"
    
    if unsupported_features:
        html += """
            <div class="collapsible">
                <div class="collapsible-header" onclick="toggleCollapsible(this)">
                    <span>Pipeline-Level Unsupported Features</span>
                    <span class="arrow">▶</span>
                </div>
                <div class="collapsible-content">
        """
        
        for feature in unsupported_features:
            html += f"""
                <div style="margin-bottom: 15px; padding: 10px; background: #fef5e7; border-left: 4px solid #f59e0b; border-radius: 4px;">
                    <strong>{feature['feature']}</strong><br>
                    <span style="color: #92400e; font-size: 0.9em;">{feature['manual_action']}</span>
                </div>
            """
        
        html += "</div></div>"
    
    html += "</div>"
    return html


def generate_next_steps_html(action_paths: List[Dict[str, Any]], all_credentials: set, feasibility_analysis: Dict[str, Any]) -> str:
    """Generate HTML for next steps checklist"""
    html = """
        <div class="section">
            <h2>✅ Next Steps Checklist</h2>
            <div class="collapsible">
                <div class="collapsible-header" onclick="toggleCollapsible(this)">
                    <span>Implementation Checklist</span>
                    <span class="arrow">▶</span>
                </div>
                <div class="collapsible-content">
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
    """
    
    # Repository setup
    html += """
                        <div>
                            <h4>Repository Setup</h4>
                            <div style="font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 4px;">
                                ☐ Review generated workflow file<br>
                                ☐ Configure repository secrets<br>
                                ☐ Set up environments (if needed)<br>
                                ☐ Test with sample commit
                            </div>
                        </div>
    """
    
    # Service setup
    services_needed = []
    if any(a.get("has_sonarqube") for a in action_paths):
        services_needed.append("☐ Configure SonarQube integration")
    if any(a.get("has_docker") for a in action_paths):
        services_needed.append("☐ Set up Docker registry auth")
    if any(a.get("has_kubectl") for a in action_paths):
        services_needed.append("☐ Configure Kubernetes access")
    
    if services_needed:
        html += """
                        <div>
                            <h4>Service Integration</h4>
                            <div style="font-family: monospace; background: #f8f9fa; padding: 10px; border-radius: 4px;">
        """
        for service in services_needed:
            html += f"{service}<br>"
        html += "</div></div>"
    
    # Manual conversion
    manual_count = sum(len(a.get("manual_conversion_needed", [])) for a in action_paths)
    if manual_count > 0:
        html += f"""
                        <div>
                            <h4>Manual Tasks</h4>
                            <div style="font-family: monospace; background: #fef5e7; padding: 10px; border-radius: 4px;">
                                ☐ Address {manual_count} manual items<br>
                                ☐ Test complex script blocks<br>
                                ☐ Verify plugin replacements
                            </div>
                        </div>
        """
    
    html += """
                    </div>
                </div>
            </div>
        </div>
    """
    
    return html


def generate_file_structure_html(action_paths: List[Dict[str, Any]]) -> str:
    """Generate HTML for file structure display"""
    html = """
        <div class="code-block" style="font-family: monospace; white-space: pre;">
.github/
├── workflows/
│   └── ci.yml                 # Main workflow file
└── actions/
    """
    
    for i, action in enumerate(action_paths):
        action_name = action["name"].lower().replace(" ", "-").replace("/", "-")
        is_last = i == len(action_paths) - 1
        prefix = "└──" if is_last else "├──"
        
        html += f"""{prefix} {action_name}/
{"    " if is_last else "│   "}└── action.yml
"""
    
    html += """
CONVERSION_REPORT.html         # This interactive report
    </div>"""
    
    return html


def detect_credential_type(cred_id: str) -> str:
    """Detect the type of credential based on its ID"""
    cred_lower = cred_id.lower()
    if "ssh" in cred_lower:
        return "SSH Key"
    elif any(x in cred_lower for x in ["token", "api", "key"]):
        return "Token/API Key"
    elif any(x in cred_lower for x in ["password", "pwd"]):
        return "Password"
    elif any(x in cred_lower for x in ["username", "user"]):
        return "Username"
    elif "kubeconfig" in cred_lower:
        return "File (Kubeconfig)"
    elif any(x in cred_lower for x in ["cert", "certificate", "pem"]):
        return "Certificate"
    else:
        return "Credential"


def get_credential_purpose(cred_id: str) -> str:
    """Get the purpose description for a credential"""
    cred_lower = cred_id.lower()
    if "docker" in cred_lower:
        return "Docker registry authentication"
    elif "git" in cred_lower or "github" in cred_lower:
        return "Git repository access"
    elif "sonar" in cred_lower:
        return "SonarQube server authentication"
    elif "kubeconfig" in cred_lower or "k8s" in cred_lower:
        return "Kubernetes cluster access"
    elif "aws" in cred_lower:
        return "AWS service authentication"
    elif "ssh" in cred_lower:
        return "SSH server access"
    else:
        return f"Authentication for {cred_id}"


# Add modals to the HTML template
def add_modals_to_html() -> str:
    """Generate modal HTML for interactive content"""
    return """
    <!-- Stage Details Modal -->
    <div id="stageModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2 id="modalTitle"></h2>
            <div id="modalBody"></div>
        </div>
    </div>

    <!-- Content Details Modal -->
    <div id="contentModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="document.getElementById('contentModal').style.display='none'">&times;</span>
            <h2 id="contentModalTitle"></h2>
            <div id="contentModalBody"></div>
        </div>
    </div>
    """


def generate_interactive_html_report(
    action_paths: List[Dict[str, Any]], 
    pipeline_text: str, 
    timestamp: str,
    complexity_analysis: Dict[str, Any],
    feasibility_analysis: Dict[str, Any],
    unsupported_features: List[Dict[str, str]],
    languages: List[str],
    tools: List[str],
    all_credentials: set
) -> str:
    """Generate complete interactive HTML report"""
    
    # Generate all HTML sections
    status_badges = generate_status_badges_html(action_paths, feasibility_analysis, complexity_analysis)
    stats_grid = generate_interactive_stats_grid(action_paths, pipeline_text, complexity_analysis)
    tech_stack = generate_technology_stack_html(languages, tools)
    secrets_section = generate_secrets_section_html(all_credentials, action_paths)
    stages_section = generate_interactive_stages_html(action_paths)
    manual_section = generate_manual_conversion_section_html(action_paths, unsupported_features)
    next_steps = generate_next_steps_html(action_paths, all_credentials, feasibility_analysis)
    file_structure = generate_file_structure_html(action_paths)
    modals = add_modals_to_html()
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Jenkins to GitHub Actions Conversion Report</title>
    <style>
        {get_css_styles()}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>🚀 Jenkins to GitHub Actions Conversion Dashboard</h1>
            <div class="header-info">
                <span><strong>Generated:</strong> {timestamp}</span>
                <span><strong>Pipeline Complexity:</strong> {complexity_analysis['complexity_level']} ({complexity_analysis['complexity_score']} points)</span>
                <span><strong>Conversion Feasibility:</strong> {feasibility_analysis['confidence']}</span>
            </div>
        </header>

        <div class="section status-section">
            <h2>📊 Conversion Status Overview</h2>
            <div class="badges">
                {status_badges}
            </div>
        </div>

        <div class="section stats-section">
            <h2>📈 Interactive Statistics</h2>
            <p style="color: #666; margin-bottom: 20px;">Click on any statistic below to see detailed information</p>
            <div class="stats-grid">
                {stats_grid}
            </div>
        </div>

        <div class="section">
            <h2>🛠️ Technology Stack Detected</h2>
            {tech_stack}
        </div>

        {secrets_section}

        <div class="section">
            <h2>📋 Stage Conversion Details</h2>
            <p style="color: #666; margin-bottom: 20px;">Click on any stage to expand and see detailed conversion information</p>
            {stages_section}
        </div>

        {manual_section}

        {next_steps}

        <div class="section">
            <h2>📁 Generated Files Structure</h2>
            {file_structure}
        </div>
    </div>

    {modals}

    <script>
        {get_javascript_code()}
    </script>
</body>
</html>"""
    
    return html
