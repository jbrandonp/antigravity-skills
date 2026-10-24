# Workflow SOP: [Task Name]

## Objective
[Clear 1-sentence description of the final result]

## Inputs
- [Input 1]: Description
- [Input 2]: Description

## Execution Tools
- `tools/[tool_script].py`: Does [action]

## Step-by-Step Procedure
1. Run `python tools/[tool_1].py [args]`
2. Inspect output in `work/[slug]_[output].json`
3. If error condition X occurs: run fallback Y
4. Produce deliverable in `output/[filename]`

## Quality Gate & Verification
- Check condition A
- Confirm zero errors