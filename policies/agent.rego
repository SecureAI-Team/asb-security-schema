package asb.agent

default allow = false

# 支持工程师可以调用 update_ticket，
# 但不能将 "critical" 优先级工单改为 "resolved"。
allow {
  input.operation.category == "agent_tool"
  input.resource.agent_tool.tool_name == "update_ticket"
  input.subject.user.roles[_] == "support_engineer"
  not is_critical_resolution
}

is_critical_resolution {
  input.resource.agent_tool.args.priority == "critical"
  input.resource.agent_tool.args.status == "resolved"
}
