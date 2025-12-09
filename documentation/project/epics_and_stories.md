# Epic 1 – General cancer information & Q&A

## Story 1.1 – Ask free-form questions
As a person affected by cancer (P1/P2)
I want to ask free-form questions about symptoms, treatments and side effects in my own words
so that I can get information that fits my situation, without needing medical jargon.
### Acceptance criteria:
User can type any question in a text box and submit.
The system replies in plain English within a few seconds.
Long questions still work (e.g. a few paragraphs).

## Story 1.2 – Understand symptoms in context of cancer
As a person with cancer (P1)
I want to describe a new or worrying symptom and get general information on what it might mean and what sensible next steps are
so that I can decide whether I should contact my cancer team, GP, or seek urgent help.
### Acceptance criteria:
The answer does not diagnose.
The answer explains common possibilities in broad terms.
The answer suggests appropriate next steps (e.g. “contact your team”, “urgent help if X/Y”).

## Story 1.3 – Understand treatments and procedures
As a person affected by cancer (P1/P2)
I want to ask what a test, scan, or treatment involves (e.g. chemo, radiotherapy, surgery)
so that I know what to expect and feel less anxious.
### Acceptance criteria:
Treatments are explained in simple terms.
Common experiences (time taken, pain/discomfort, side effects) are described.
Clear that details vary per person and the hospital/doctor remains the authority.

## Story 1.4 – Everyday life with cancer
As a person affected by cancer (P1/P2)
I want to ask about day-to-day issues (work, fatigue, mood, relationships, money, childcare, etc.)
so that I can get practical ideas and know what support exists.
Acceptance criteria:
Answers include practical suggestions (not just medical).
The system may signpost to benefits/financial support and emotional support services.
Tone is supportive and non-judgemental.

----

# Epic 2 – Child / young person questions

## Story 2.1 – Explain cancer simply
As a child or teenager with a parent who has cancer (P3)
I want simple explanations of what cancer is and what treatment does
so that I can understand what’s happening without being overwhelmed.

### Acceptance criteria:
Uses simpler language and shorter sentences.
Avoids graphic or needlessly frightening details.
Encourages the child to talk to a trusted adult and/or the clinical team.

## Story 2.2 – “Does chemo hurt?” / “Will it change Mum’s mood?”
As a child or teenager with a parent on treatment (P3)
I want answers to questions like “does chemo hurt?” or “will it change my mum’s mood?”
so that I can prepare myself and feel less scared.
### Acceptance criteria:
Acknowledges feelings (“It’s understandable to worry about this”).
Gives honest but gentle explanations about pain/discomfort and mood changes.
Suggests asking the parent’s nurse/doctor, as they know the exact drugs and doses.

----
# Epic 3 – Local support & signposting (NI first, then Ireland / UK)

## Story 3.1 – NI-specific information first
As a person affected by cancer in Northern Ireland (P1/P2/P3)
I want the tool to show me support and information relevant to Northern Ireland first
so that I can find services and advice that actually apply to where I live.
### Acceptance criteria:
When services are mentioned, NI options are prioritised (HSC NI, NI Direct, PHA NI, Cancer Focus NI, Action Cancer, etc.).
If no NI-specific service exists, the answer clearly says this and offers Ireland/UK options.

## Story 3.2 – Helplines and support services
As a person affected by cancer (P1/P2/P3)
I want to be signposted to trusted helplines, support centres, and online resources
so that I can get human support and more detailed, up-to-date information.
### Acceptance criteria:
Only reputable services are suggested (e.g. Cancer Focus NI, Irish Cancer Society, Macmillan, CRUK).
The answer briefly explains what each service offers (e.g. nurse helpline, information centre, counselling).
No made-up phone numbers or organisations.

## Story 3.3 – Cross-border options (Ireland / UK-wide)
As someone in NI who is close to the border or has family elsewhere (P1/P2)
I want to see relevant Ireland and UK-wide services when NI options are limited
so that I still get practical support even if a local service does not exist.
### Acceptance criteria:
The tool can recommend Irish Cancer Society and UK-wide resources where appropriate.
It explains why a non-NI service is suggested (“this is Ireland-wide, not NI-specific, but may still help”).

----

# Epic 4 – Safety, risk and escalation

## Story 4.1 – Highlight emergencies
As a person with cancer or their carer (P1/P2)
I want the tool to tell me clearly when my description sounds like it might be an emergency
so that I know I should seek urgent medical help immediately.
### Acceptance criteria:
For red-flag symptoms (e.g. difficulty breathing, chest pain, heavy bleeding, signs of sepsis), the answer:
Clearly states that it could be serious.
Advises calling 999 or going to A&E in NI/UK and/or using the cancer team’s emergency number.
The tool never tells someone to “wait and see” in a high-risk scenario.

## Story 4.2 – Default to “check with the clinical team”
As a person with cancer (P1)
I want the tool to remind me to discuss personal medical decisions with my own doctors/nurses
so that I don’t make treatment decisions based on a chatbot.
### Acceptance criteria:
For clinical questions (dose changes, stopping treatment, alternative therapies), the answer:
Refuses to give direct medical instructions.
Encourages discussion with oncologist/GP/clinical nurse specialist.
Clear statement that the tool is not a replacement for professional medical advice.

## Story 4.3 – Handle emotional distress and self-harm concerns
As a distressed person affected by cancer (P1/P2/P3)
I want the tool to respond sensitively if I express distress, hopelessness or thoughts of self-harm
so that I feel heard and am guided to safe, human support.
Acceptance criteria:
The tool acknowledges feelings in a calm, compassionate way.
Encourages contacting a trusted person and/or crisis support (following UK/NI norms).
Does not provide instructions for self-harm and does not minimise risk.

----

# Epic 5 – Tone, language and accessibility

## Story 5.1 – Plain language only
As any user (P1/P2/P3)
I want answers written in plain, everyday English
so that I can understand them even when I am tired, stressed, or have no medical background.
### Acceptance criteria:
Medical jargon is avoided, or explained when used.
Long answers are broken into short paragraphs or bullet points.
No reading level that assumes clinical training.

## Story 5.2 – Kind and non-judgemental tone
As a person affected by cancer (P1/P2/P3)
I want the tool to be kind and non-judgemental
so that I feel safe asking any question, even if I feel it is “silly”.
### Acceptance criteria:
Responses acknowledge emotions and worries.
No blaming language (e.g. for lifestyle, previous choices).
No shaming around treatment choices.

----

# Epic 6 – Transparency and limitations

## Story 6.1 – Clear about what it can’t do
As any user (P1–P3)
I want the tool to be honest about what it does not know or cannot safely answer
so that I don’t get a false sense of certainty.
### Acceptance criteria:
When information is uncertain or absent, the answer admits uncertainty.
The tool explicitly avoids making up details (e.g. local clinic names, phone numbers).
The tool suggests practical next steps instead of guessing.

## Story 6.2 – Clear about data use
As a privacy-conscious user (P1–P3)
I want to know how my questions and answers are handled and stored
so that I can decide what I am comfortable sharing.
### Acceptance criteria:
The UI (not necessarily the model) explains that:
Logs may be anonymised.
It is not for emergencies.
It is not a replacement for a doctor.
Sensitive data is not echoed back unnecessarily.

----

# Epic 7 – Admin / content and RAG management (internal)
## Story 7.1 – Curated content sources
As a product owner (P5)
I want to maintain a curated list of trusted NI, Ireland, and UK cancer information sources
so that the RAG layer uses high-quality, up-to-date information.
### Acceptance criteria:
There is a defined list of domains/organisations allowed into the corpus.
Each document is tagged with source, date, geography (NI / Ireland / UK), and intended audience (adult/child/carer).
Only these tagged sources are used for retrieval.

## Story 7.2 – Update content easily
As a product owner (P5)
I want to update or add new documents to the information corpus with a simple process
so that the tool stays accurate as guidelines and services change.
### Acceptance criteria:
There is a documented pipeline/script to:
Add or update documents.
Re-chunk and re-embed them.
Old versions can be retired cleanly.

## Story 7.3 – Traceability of answers
As a product owner or reviewer (P5/P4)
I want to see which sources were used for a given answer
so that I can audit and improve the system over time.
### Acceptance criteria:
Each answer internally records which documents/snippets were retrieved.
The user can see, at least at a basic level, which organisations the info comes from (e.g. “Based on information from Cancer Research UK and Cancer Focus NI”).

----

# Epic 8 – Technical, safety and quality (non-functional)
## Story 8.1 – Low hallucination, RAG-first behaviour
As a product owner (P5)
I want the LLM to rely on retrieved sources first and minimise invented facts
so that medical information is as accurate and safe as possible.
### Acceptance criteria:
Prompting instructs the model to quote/summarise retrieved text first.
When no relevant retrievable content exists, the model is encouraged to say “I’m not sure” and signpost rather than invent.

## Story 8.2 – Robustness and testing
As a product owner/engineer (P5)
I want a suite of scenario tests for key question types and safety cases
so that I can catch regressions when I change prompts, models, or content.
### Acceptance criteria:
There are representative test conversations (unit/integration style) for:
Common symptom queries.
Child questions about chemo and mood.
Red-flag symptom descriptions.
Extreme or adversarial inputs.
Tests can be run automatically against the deployed model and produce measurable results (e.g. checking for certain phrases, presence of escalation guidance).

## Story 8.3 – Privacy and logging
As a product owner (P5)
I want to log enough information for debugging and safety monitoring, without storing identifiable medical data
so that I meet privacy expectations while still improving the service.
### Acceptance criteria:
Logs strip or mask obvious identifiers where possible.
Logs store model version, prompt template version, and high-level intention of queries (e.g. symptom vs emotional vs practical).
Access to logs is restricted and audited.

## Story 8.4 – Performance and availability
As a user (P1–P3)
I want answers to arrive within a reasonable time and the service to be available when I need it
so that I don’t give up in frustration.
### Acceptance criteria:
Typical response time target is set (e.g. < 10 seconds end-to-end for a standard-length question).
Basic monitoring/alerting on uptime and latency is in place.