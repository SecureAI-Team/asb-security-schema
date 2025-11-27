package asb.prompt

default allow = true

# 顶层导出：是否允许该 prompt
allow {
  not is_suspicious_prompt
}

# 如果 user 消息中包含特定模式，则认为可疑
is_suspicious_prompt {
  some i
  msg := input.resource.llm.messages[i]
  msg.role == "user"
  lower(msg.content) == "ignore previous instructions"
}
