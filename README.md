# talk_cancer
LLM RAG project to provide a conversational interface to support information for people [in Northern Ireland/Ireland/UK] affected by a cancer diagnosis

---

## Test Coverage

```
================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.2-final-0 _______________

Name                                Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------------
app/__init__.py                         0      0      0      0   100%
app/assistant_service.py               10      0      0      0   100%
app/cli.py                             23      1      6      1    93%
app/llm_base.py                        10      0      0      0   100%
app/llm_ollama.py                      35      1      8      2    93%
tests/test_cli.py                      74      2      0      0    97%
tests/test_ollama_chat_model.py        48      2      2      1    94%
tests/test_story_1_1_assistant.py      31      0      0      0   100%
---------------------------------------------------------------------
TOTAL                                 231      6     16      4    96%
============================== 7 passed in 0.13s ===============================
```