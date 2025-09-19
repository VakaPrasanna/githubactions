import yaml
import json
from datetime import datetime, timedelta
import random

class SimpleWorkflowMetricsGenerator:
    def __init__(self, workflow_yaml_path: str = None, workflow_yaml_content: str = None):
        if workflow_yaml_content:
            self.workflow_data = yaml.safe_load(workflow_yaml_content)
        elif workflow_yaml_path:
            with open(workflow_yaml_path, 'r') as file:
                self.workflow_data = yaml.safe_load(file)
        else:
            raise ValueError("Either workflow_yaml_path or workflow_yaml_content must be provided")
        
        self.base_timestamp = datetime.now()
    
    def _extract_commands_from_step(self, step):
        """Extract commands from a step"""
        commands = []
        if 'run' in step:
            run_script = step['run'].strip()
            lines = run_script.split('\n')
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    commands.append(line)
        elif 'uses' in step:
            commands.append(f"uses: {step['uses']}")
        return commands
    
    def _generate_step_output(self, commands, status):
        """Generate realistic step output with timestamps"""
        timestamp_base = self.base_timestamp + timedelta(seconds=random.randint(0, 300))
        output_lines = []
        
        # Generate timestamps
        for i, cmd in enumerate(commands):
            ts = (timestamp_base + timedelta(milliseconds=i*50)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            output_lines.append(f"{ts} {cmd}")
        
        # Add shell info
        ts_shell = (timestamp_base + timedelta(milliseconds=len(commands)*50)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        output_lines.append(f"{ts_shell} shell: /usr/bin/bash -e {{0}}")
        
        # Add command outputs
        for cmd in commands:
            ts_out = (timestamp_base + timedelta(milliseconds=(len(commands)+1)*50)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
            if 'echo' in cmd.lower():
                # Extract echo content
                import re
                match = re.search(r'echo\s+["\']?([^"\']+)["\']?', cmd)
                if match:
                    output_lines.append(f"{ts_out} {match.group(1)}")
            elif any(keyword in cmd.lower() for keyword in ['build', 'test', 'deploy']):
                output_lines.append(f"{ts_out} {cmd.split()[0]} logic")
        
        return output_lines
    
    def generate_metrics(self):
        """Generate metrics matching the screenshot format"""
        jobs = self.workflow_data.get('jobs', {})
        result = {}
        
        for job_name, job_config in jobs.items():
            # Generate job-level data
            job_start = self.base_timestamp + timedelta(minutes=random.randint(0, 10))
            job_duration = random.randint(60, 300) # 1-5 minutes
            job_end = job_start + timedelta(seconds=job_duration)
            
            # Determine job status (85% success rate)
            job_status = "success" if random.random() > 0.15 else "failure"
            
            job_data = {
                "data": {
                    "Job URL": f"https://gh.asml.com/repos/asml-gh/lc09-obi-actions-common/actions/runs/{random.randint(1000000, 9999999)}",
                    "Start Time": job_start.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "End Time": job_end.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "Duration": f"{job_duration}s",
                    "Status": job_status
                },
                "stderr": {
                    "file": f"logs/{job_name}.txt",
                    "errors": []
                },
                "stdout": {}
            }
            
            # Add error if job failed
            if job_status == "failure":
                error_ts = (job_end - timedelta(seconds=10)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                job_data["stderr"]["errors"].append(f"{error_ts} ##[error]Process completed with exit code 1.")
            
            # Process steps
            steps = job_config.get('steps', [])
            for step_idx, step in enumerate(steps):
                step_name = step.get('name', f'Step {step_idx + 1}')
                step_key = step_name.lower().replace(' ', '').replace('-', '').replace('&', '')
                
                # Extract commands
                commands = self._extract_commands_from_step(step)
                
                # Generate step status (most steps succeed)
                step_status = "success" if job_status == "success" and random.random() > 0.1 else "failure"
                
                # Generate output
                output_lines = self._generate_step_output(commands, step_status)
                
                # Add to stdout
                job_data["stdout"][step_key] = {
                    "steps": [
                        {
                            "cmds": commands
                        }
                    ],
                    "output": output_lines
                }
            
            result[job_name] = job_data
        
        return result
    
    def export_to_json(self, filename=None):
        """Export metrics to JSON file"""
        if filename is None:
            filename = f"workflow_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        metrics = self.generate_metrics()
        
        with open(filename, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        return filename
    
    def print_metrics(self):
        """Print metrics in JSON format"""
        metrics = self.generate_metrics()
        print(json.dumps(metrics, indent=2))

# Quick usage functions
def generate_metrics_from_file(workflow_file_path: str):
    """Generate metrics from workflow file"""
    try:
        generator = SimpleWorkflowMetricsGenerator(workflow_yaml_path=workflow_file_path)
        
        # Print to console
        print("Generated Workflow Metrics:")
        print("=" * 50)
        generator.print_metrics()
        
        # Export to file
        json_file = generator.export_to_json()
        print(f"\n✅ Metrics exported to: {json_file}")
        
        return generator.generate_metrics()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def generate_metrics_from_yaml(yaml_content: str):
    """Generate metrics from YAML content"""
    try:
        generator = SimpleWorkflowMetricsGenerator(workflow_yaml_content=yaml_content)
        
        # Print to console
        print("Generated Workflow Metrics:")
        print("=" * 50)
        generator.print_metrics()
        
        # Export to file
        json_file = generator.export_to_json()
        print(f"\n✅ Metrics exported to: {json_file}")
        
        return generator.generate_metrics()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

if __name__ == "__main__":
    # Example usage - change the path to your workflow file
    workflow_file = ".github/workflows/ci.yml"
    
    print("🚀 Generating simple workflow metrics...")
    metrics = generate_metrics_from_file(workflow_file)
    
    if metrics:
        print(f"\n📊 Generated metrics for {len(metrics)} jobs")
        for job_name in metrics.keys():
            print(f" - {job_name}")
