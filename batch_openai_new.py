# Laterality Prompt Evaluation

Utilities for evaluating anatomical laterality classification with:

- LM Studio or older OpenAI-compatible chat-completions endpoints
- newer OpenAI models via the Responses API
- batch runs over a folder tree
- single-image reruns
- original vs horizontally flipped comparisons
- three prompt variants with `unable_to_determine` preserved
- per-run raw-output artifacts and aggregate CSV summaries

## Repository layout

```text
scripts/
  batch_lmstudio.py
  batch_openai_new.py
  rerun_single_lmstudio.py
  rerun_single_openai_new.py
prompts/
  prompts.json
requirements.txt
.gitignore
```

## Install

```bash
python -m pip install -r requirements.txt
```

## Prompts

The repository uses three prompts:

1. `p1_landmark_justified`
2. `p2_clinician_oneword`
3. `p3_minimal_oneword`

They are stored in `prompts/prompts.json` and duplicated inside the scripts so each script is self-contained.

## Labels

Primary labels:

- `left`
- `right`
- `unable_to_determine`

Internal diagnostic buckets:

- `other` for malformed but non-empty outputs
- `empty` for empty visible output
- `timeout` for request timeout / manual interruption in LM Studio scripts

## Scripts

### 1. Batch LM Studio / older OpenAI-compatible

```bash
python scripts/batch_lmstudio.py
```

Edit these config values first:

- `BASE_URL`
- `API_KEY`
- `MODEL`
- `INPUT_ROOT`
- `OUTPUT_ROOT`

This script uses `chat.completions`, supports sampling controls, walks all images in a folder tree, and tests original + flipped images.

### 2. Batch newer OpenAI

```bash
python scripts/batch_openai_new.py
```

Edit these config values first:

- `MODEL`
- `INPUT_ROOT`
- `OUTPUT_ROOT`

Set the API key in your shell before running:

```bash
export OPENAI_API_KEY=your_key_here
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

### 3. Single-image LM Studio rerun

```bash
python scripts/rerun_single_lmstudio.py
```

Set `IMAGE_PATH` and LM Studio config at the top of the file.

### 4. Single-image newer OpenAI rerun

```bash
python scripts/rerun_single_openai_new.py
```

Set `IMAGE_PATH` and model at the top of the file.

## Outputs

Each session creates a timestamped directory with:

- `session_meta.json`
- `runs.csv`
- `aggregate.csv`
- one directory per image and prompt
- per-run JSON artifacts for original and flipped conditions
- `summary.json` per prompt

Typical layout:

```text
<output_root>/<timestamp>/
  session_meta.json
  runs.csv
  aggregate.csv
  subfolder/
    image_name/
      p1_landmark_justified/
        original/
          001_left.json
        flipped/
          001_right.json
        summary.json
```

## Notes

- Prompt 1 is the most fragile for local VLMs because it asks for a label plus a justification.
- The LM Studio scripts include request timeout handling and incremental row persistence.
- The newer OpenAI scripts use the Responses API with JSON schema output.
- If you see many `empty` outputs, increase the token budget or simplify the prompt.


## Image descriptions

The repository now includes example image descriptions under `data/image_descriptions/` in both CSV and JSON formats:

- `data/image_descriptions/image_descriptions.csv`
- `data/image_descriptions/image_descriptions.json`

These are dataset metadata for organization and review. They should not be supplied to the model during image-only laterality evaluation.
