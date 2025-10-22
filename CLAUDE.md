# Use of examples
Use examples located in ../swf-testbed/example_agents/. Suggest the use lof logging
utilities used in these source files.

# agent_name and agent_type patterns

```
username = getpass.getuser()
agent_id = self.get_next_agent_id()
self.agent_name = f"{self.agent_type.lower()}-agent-{username}-{agent_id}"
```

# Message types

'run_imminent', 'start_run', 'pause_run', 'resume_run', 'end_run', 'stf_gen', 'data_ready'
