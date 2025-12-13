# How to use the proxy server

## Register
- whitelist a non DND phone number and get Auth token

## Makefile and Postman
- Query the call server for actions and info
- Postman Documentation - https://documenter.getpostman.com/view/29008927/2sB3dSQUQE

## Important
- The post call evaluation json has to be of a specific format
- system tools available (end_call and session_notes) that cna we called via the tool names in respetive json. dont forget to pass required keys
- various vad settings you cna test out
## Timing Comparison

| Engine    | Start   | End   | Character         |
| --------- | ------- | ----- | ----------------- |
| LOKEN     | instant | 100ms | Responsive        |
| KAAN      | 50ms    | 550ms | Aggressive        |
| POLUX     | 128ms   | 160ms | Balanced          |
| ANCHORITE | 200ms   | 800ms | Patient           |
| CALGAR    | 50ms    | 400ms | Fast-in, slow-out |
| VALDOR    | 50ms    | 400ms | Fast-in, slow-out |
| CAWL      | 50ms    | 400ms | Fast-in, slow-out |

## When to Use What

| Engine        | Use Case                                        |
| ------------- | ----------------------------------------------- |
| **LOKEN**     | Testing, baseline, clean audio                  |
| **KAAN**      | Need fastest response, accept false triggers    |
| **POLUX**     | Noisy environment, need stability               |
| **ANCHORITE** | Very conservative, minimize interruptions       |
| **CALGAR**    | Good all-rounder for telephony (no native deps) |
| **VALDOR**    | **Production default** - best balance           |
| **CAWL**      | Maximum performance, have native libs           |

