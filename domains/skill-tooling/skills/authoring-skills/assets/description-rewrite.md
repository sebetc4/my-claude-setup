# Rewrite A Skill's Description

A skill is a folder of instructions that an agent loads when a request needs it. The
agent sees every skill's name and description at every turn and decides from them alone
whether to load one; it reads a skill's body only once it has chosen the skill. Write a
new description for the skill below: one that makes an agent load the skill for the
requests it serves, and leave it for the others.

Below are the skill's body, the description to rewrite with the queries it got wrong,
and the earlier descriptions with their results. Other queries, which are not shown
here, decide which description is kept: a description that lists the queries it was
shown fits those and fails the others. Generalize from each failure to the intent behind
it — what the user wants done, in the words users say —, never to the query's wording.
Notes from the skill's author, when present, give the skill's intent and the user's
feedback: follow them.

Rules for the description:

1. What the skill does, in one clause that names its operations or its outputs; then
   when to use it: the key use case first, then the situations in the users' words —
   keywords, synonyms, symptoms, error messages, file types, tool names.
2. No sequence of steps: an agent that finds the workflow in the description follows it
   and skips the body.
3. An exclusion ("Not for …") only against a false trigger the results show, and in
   general terms.
4. Third person; no model named.
5. 1,024 characters at most, the key use case in the first sentence: listings cut long
   descriptions short.
6. A skill that triggers too rarely widens its situations; one that triggers too often
   narrows them first, then gains exclusions.
7. When earlier descriptions failed, try another structure rather than a variation of
   the same one.

Answer with the new description alone, as one paragraph without quotes around it,
between `<new_description>` and `</new_description>`.
