package asb.rag

default allow = false

# 允许访问的条件：
# - 操作为 RAG 查询
# - 用户部门为 engineering
# - 候选文档中不存在 sensitivity = "secret"
allow {
  input.operation.category == "rag_search"
  input.subject.user.attributes.department == "engineering"
  not contains_secret_docs
}

contains_secret_docs {
  some i
  cand := input.resource.rag.candidates[i]
  cand.metadata.sensitivity == "secret"
}
