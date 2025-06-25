# Can we fool LLMs? Investigating Prosody-Driven Semantic Disambiguation in Spoken Inputs

## Table of Contents

- [Problem Statement](#problem-statement)
- [File Structure](#file-structure)
- [Usage](#usage)
- [Pending Tasks](#pending-tasks)
- [References](#references)

## Problem Statement

Prosody—intonation, stress, and rhythm—can significantly alter the meaning of spoken sentences, even when the textual content remains identical, e.g., *“He went to school.”* vs *“He went to school?”*. 
While LLMs excel at text-based understanding, their ability to interpret **prosody-driven semantic variations** remains unclear. This project investigates:

1. **LLM Sensitivity to Prosody:** Evaluate whether speech-enabled LLMs or speech-to-text pipelines can distinguish between prosodically distinct utterances with identical text.

2. **Failure Case Analysis:** Identify scenarios where models fail to disambiguate meaning based on prosody and analyze their underlying limitations.

