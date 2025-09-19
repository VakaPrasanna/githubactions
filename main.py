
#!/usr/bin/env python3
"""
Enhanced Jenkins Declarative Pipeline -> GitHub Actions converter

"""

import sys
import re
import yaml
from pathlib import Path
from typing import List, Dict, Any
from converter import convert_jenkins_to_gha
from report_generator import generate_conversion_report
# from enhanced_report_generator import generate_enhanced_conversion_report


def cleanup_generated_actions(output_dir: Path):
    """Clean up generated actions by removing duplicates and fixing variables"""
    actions_dir = output_dir / ".github" / "actions"
    if not actions_dir.exists():
        return
    
    for action_dir in actions_dir.iterdir():
        if action_dir.is_dir():
            action_file = action_dir / "action.yml"
            if action_file.exists():
                with action_file.open('r') as f:
                    content = f.read()
                
                # Fix variable references
                fixes = [
                    (r'\$\{\{\s*inputs\.APP_NAME\s*\}\}', '${{ inputs.app-name }}'),
                    (r'\$\{\{\s*inputs\.DEPLOY_ENV\s*\}\}', '${{ inputs.deploy-env }}'),
                    (r'\$\{\{\s*inputs\.KCONFIG\s*\}\}', '${{ inputs.kubeconfig }}'),
                ]
                
                for pattern, replacement in fixes:
                    content = re.sub(pattern, replacement, content)
                
                with action_file.open('w') as f:
                    f.write(content)


def interactive_mode():
    """Interactive mode for easier conversion"""
    print("🔧 Interactive Jenkins to GitHub Actions Converter")
    print("=" * 50)
    
    # Get input source
    while True:
        source = input("\n📁 Enter Jenkins file/directory path (or 'q' to quit): ").strip()
        if source.lower() == 'q':
            sys.exit(0)
        if Path(source).exists():
            break
        print("❌ Path not found. Please try again.")
    
    # Get output directory
    output = input("📂 Output directory (press Enter for current): ").strip() or "."
    
    # Get options
    print("\n⚙️  Options:")
    cleanup = input("Clean existing output? (y/N): ").lower().startswith('y')
    
    return [source], Path(output), cleanup


def main():
    # Check for interactive mode
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ['-i', '--interactive']):
        if len(sys.argv) == 1:
            print("Enhanced Jenkins to GitHub Actions Converter")
            print("Usage: python main.py <jenkinsfile1|directory> [jenkinsfile2] ... [output_directory]")
            print("       python main.py -i  (interactive mode)")
            print("\nFeatures:")
            print("  - Multiple Jenkins file and directory support")
            print("  - Interactive mode for guided conversion")
            print("  - Comprehensive Jenkins feature support")
            print("  - Automatic variable conversion and cleanup")
            sys.exit(1)
        else:
            args, output_dir, cleanup = interactive_mode()
            if cleanup and output_dir.exists():
                import shutil
                shutil.rmtree(output_dir / ".github", ignore_errors=True)
                for f in output_dir.glob("CONVERSION_REPORT.*"):
                    f.unlink()
    else:
        args = sys.argv[1:]

    # Parse arguments and find Jenkins files
    jenkinsfiles = []
    if 'output_dir' not in locals():
        output_dir = Path(".")
    
    # Separate directories, files, and output directory
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            # Find Jenkins files in directory
            jenkins_patterns = ['*.Jenkinsfile', '*jenkinsfile*', 'Jenkinsfile*']
            found_files = []
            for pattern in jenkins_patterns:
                found_files.extend(path.glob(pattern))
            
            if found_files:
                jenkinsfiles.extend(found_files)
                print(f"Found {len(found_files)} Jenkins file(s) in {path}")
            else:
                print(f"No Jenkins files found in directory: {path}")
        elif path.exists():
            jenkinsfiles.append(path)
        elif not path.exists() and len(args) > 1 and arg == args[-1]:
            # Last argument that doesn't exist - treat as output directory
            output_dir = path
        else:
            print(f"Error: File not found: {path}")
            sys.exit(1)
    
    if not jenkinsfiles:
        print("Error: No Jenkins files found to convert")
        sys.exit(1)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Converting {len(jenkinsfiles)} Jenkins file(s) to GitHub Actions...")
    
    workflows_dir = output_dir / ".github" / "workflows"
    workflows_dir.mkdir(parents=True, exist_ok=True)
    
    all_action_paths = []
    successful_conversions = 0
    
    try:
        for i, jenkinsfile in enumerate(jenkinsfiles):
            print(f"\n📁 Processing {jenkinsfile.name} ({i+1}/{len(jenkinsfiles)})...")
            
            try:
                jenkins_text = jenkinsfile.read_text(encoding="utf-8")
                print("Analyzing pipeline structure and features...")
                
                # Perform the conversion
                gha, action_paths = convert_jenkins_to_gha(jenkins_text, output_dir)
                
                # Generate workflow filename
                workflow_name = jenkinsfile.stem.replace('.', '-').lower()
                if workflow_name == 'jenkinsfile':
                    workflow_name = 'ci'
                workflow_path = workflows_dir / f"{workflow_name}.yml"
                
                # Save workflow file
                print(f"Generating workflow file: {workflow_path.name}")
                with workflow_path.open("w", encoding="utf-8") as f:
                    yaml.dump(gha, f, sort_keys=False, width=1000, default_flow_style=False, allow_unicode=True)
                
                print(f"✅ Workflow saved to: {workflow_path}")
                all_action_paths.extend(action_paths)
                successful_conversions += 1
                
            except Exception as e:
                print(f"❌ Failed to convert {jenkinsfile.name}: {e}")
                continue
        
        if successful_conversions == 0:
            print("❌ No files were successfully converted")
            sys.exit(1)
        
        # Clean up generated actions
        print("\nCleaning up generated actions...")
        cleanup_generated_actions(output_dir)
        
        # Generate comprehensive conversion reports
        print("Generating conversion reports...")
        
        # Generate combined report for all conversions
        html_report_path = output_dir / "CONVERSION_REPORT.html"
        md_report_path = output_dir / "CONVERSION_REPORT.md"
        
        # Use the first successful conversion for report generation
        sample_jenkins_text = jenkinsfiles[0].read_text(encoding="utf-8") if jenkinsfiles else ""
        
        html_report = generate_conversion_report(all_action_paths, sample_jenkins_text)
        with html_report_path.open("w", encoding="utf-8") as f:
            f.write(html_report)
        
        md_report = generate_simple_markdown_report(all_action_paths, sample_jenkins_text)
        with md_report_path.open("w", encoding="utf-8") as f:
            f.write(md_report)
        
        print(f"✅ Conversion reports generated:")
        print(f"   - Interactive HTML: {html_report_path}")
        
        # Display summary of generated files
        print("\n📁 Generated files:")
        for workflow_file in workflows_dir.glob("*.yml"):
            print(f"   - {workflow_file.relative_to(output_dir)} (Workflow)")
        print(f"   - {html_report_path.relative_to(output_dir)} (Report)")
        print(f"   - {md_report_path.relative_to(output_dir)} (Report)")
        
        # List generated composite actions
        actions_dir = output_dir / ".github" / "actions"
        action_count = 0
        if actions_dir.exists():
            for action_dir in actions_dir.iterdir():
                if action_dir.is_dir():
                    action_file = action_dir / "action.yml"
                    if action_file.exists():
                        print(f"   - {action_file.relative_to(output_dir)}")
                        action_count += 1
        
        # Display conversion summary
        print(f"\n📊 Conversion Summary:")
        print(f"   - Jenkins files processed: {successful_conversions}/{len(jenkinsfiles)}")
        print(f"   - Total stages converted: {len(all_action_paths)}")
        print(f"   - Composite actions created: {action_count}")
        
        # Check for manual conversion requirements
        manual_items = sum(len(a.get("manual_conversion_needed", [])) for a in all_action_paths)
        if manual_items > 0:
            print(f"   - Manual items requiring attention: {manual_items}")
            print("   ⚠️  Review generated actions for manual conversion notes")
        else:
            print("   ✅ No manual conversion required")
        
        # Check for credentials
        all_credentials = set()
        for action in all_action_paths:
            all_credentials.update(action.get("credentials", []))
        
        if all_credentials:
            print(f"   - GitHub Secrets to configure: {len(all_credentials)}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Review generated workflow files in .github/workflows/")
        print(f"   2. Configure GitHub Secrets as needed")
        print(f"   3. Test workflows incrementally")
        print(f"   4. Open {html_report_path.name} for detailed conversion report")
        
        print(f"\n✨ Conversion completed successfully!")
        print(f"📋 {successful_conversions} Jenkins file(s) converted to GitHub Actions!")
        
    except Exception as e:
        print(f"❌ Conversion Error: {e}")
        if successful_conversions > 0:
            print(f"\n✅ {successful_conversions} file(s) were successfully converted")
            print("Check the generated workflows and reports")
        else:
            print("\nNo files were successfully converted. Please check:")
            print("  - Files are valid Jenkins declarative pipelines")
            print("  - File paths are correct")
            print("  - Files are readable")
            sys.exit(1)
        
    except FileNotFoundError as e:
        print(f"❌ File Error: {e}")
        print("Please check the file path and try again.")
        sys.exit(1)
        
    except PermissionError as e:
        print(f"❌ Permission Error: {e}")
        print("Please check file permissions and try again.")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print("\nDebug Information:")
        import traceback
        traceback.print_exc()
        print(f"\nPlease report this issue with:")
        print(f"  - The error message above")
        print(f"  - Your Jenkinsfile content (sanitized)")
        print(f"  - Python version: {sys.version}")
        sys.exit(1)


def generate_simple_markdown_report(action_paths: List[Dict[str, Any]], pipeline_text: str) -> str:
    """Generate a simple markdown report for compatibility"""
    
    from datetime import datetime
    from utils import analyze_pipeline_complexity, validate_conversion_feasibility
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    complexity_analysis = analyze_pipeline_complexity(pipeline_text)
    feasibility_analysis = validate_conversion_feasibility(pipeline_text)
    
    report = [
        "# Jenkins to GitHub Actions Conversion Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Pipeline Complexity:** {complexity_analysis['complexity_level']} ({complexity_analysis['complexity_score']} points)",
        f"**Conversion Feasibility:** {feasibility_analysis['confidence']}",
        "",
        "## Conversion Summary",
        f"- **Stages converted**: {len(action_paths)}",
        f"- **Manual items**: {sum(len(a.get('manual_conversion_needed', [])) for a in action_paths)}",
        f"- **Approval gates**: {len([a for a in action_paths if a.get('approval_environment')])}",
        "",
        "## Interactive Report Available",
        "📱 **Open CONVERSION_REPORT.html in your browser for an interactive experience with:**",
        "- Clickable statistics that show detailed stage information",
        "- Expandable stage details with full conversion data",
        "- Interactive secrets and credentials configuration",
        "- Step-by-step implementation guidance",
        "",
        "## Quick Stage Overview",
        ""
    ]
    
    for i, action in enumerate(action_paths, 1):
        features = []
        if action.get("has_docker"):
            features.append("Docker")
        if action.get("has_kubectl"):
            features.append("K8s")
        if action.get("has_sonarqube"):
            features.append("SonarQube")
        if action.get("approval_environment"):
            features.append("Approval")
        
        manual_count = len(action.get("manual_conversion_needed", []))
        status = "⚠️ Manual" if manual_count > 0 else "✅ Ready"
        features_str = f"({', '.join(features)})" if features else ""
        
        report.append(f"{i}. **{action['name']}** {features_str} - {status}")
    
    report.extend([
        "",
        "## Next Steps",
        "1. **Open the interactive HTML report** for detailed guidance",
        "2. **Configure GitHub repository secrets**",
        "3. **Set up environments for approval gates**",
        "4. **Test the generated workflow**",
        "",
        "---",
        "*For the full interactive experience with clickable elements and detailed breakdowns, open CONVERSION_REPORT.html in your web browser.*"
    ])
    
    return "\n".join(report)


if __name__ == "__main__":
    main()
