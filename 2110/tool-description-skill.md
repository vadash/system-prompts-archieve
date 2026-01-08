<!--
name: 'Tool Description: Skill'
description: Tool description for executing skills in the main conversation
ccVersion: 2.0.77
variables:
  - FORMAT_SKILLS_AS_XML_FN
  - LIMITED_COMMANDS
-->
Execute a skill within the main conversation.

Skills provide specialized capabilities. When users reference "/<something>" (e.g., "/commit"), use this tool to invoke the corresponding skill.

Invoke with skill name: `skill: "pdf"` or `skill: "commit"`.

If you see a <${FORMAT_SKILLS_AS_XML_FN}> tag in the current turn, the skill is already loaded - follow its instructions directly.

Available skills:
${LIMITED_COMMANDS}
