# bigben
A benchmark for big-code based program analysis
## Labled Data
All labeled data are in `bigben.json` in the form of JSON:
```json
{
  "project": "prj_name",
  "file": "f.c",
  "line": 10,
  "type": "stack-buffer-overrun",
  "CWE": 125,
  "repository": "http:// ...",
  "report": "http:// ..."
}
```
## Contents
- [DARPA Challenges Sets](https://github.com/trailofbits/cb-multios)

## Bug Labeling with [AFL Fuzzer](http://lcamtuf.coredump.cx/afl/)
```sh
$ export AFL_PATH= # path to AFL fuzzer
$ ./run.py fuzz
```
