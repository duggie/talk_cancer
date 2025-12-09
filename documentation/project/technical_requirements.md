# Technical Requirements

1. Local development environment, for speed of addressing feedback and minimal costs.
1.1 latest python 3.14 (correct December 2025)
1.2 use an efficient LLM for performance reasons - results are not being critiqued
1.3 TDD matters
1.4 IaC matters

2. Model training environment - runs locally and on (say) AWS
2.1 results matter here

3. CLI interface is optional but useful for local development

4. Web interface offers a more polished experience for demos and thinking about production use
4.1 Use [FastAPI](https://fastapi.tiangolo.com) framework because it is fit for purpose and I want some exposure to the framework

5. Mobile app is - probably - another production interface

6. Security is a first class citizen

7. Log usage to help with model training
7.1 keep it anonymous - protect users

8. Enrich responses from LLM with data from trusted, authoritative sources

9. I will never know less about a project or subject than I do at the start. Make decisions which will result in less refactoring in the future. Don't be afraid to make mistakes.