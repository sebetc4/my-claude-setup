# Benchmark: writing-notes, iteration-1

Model and effort as the iteration sets them: claude-sonnet-5-5 at xhigh; 3 runs per case and configuration; cases: decision-note, nothing-follows.
12 runs counted, 0 left out. Cost of the counted runs: $0.375; of their grading: $0.342.

## Summary

| Metric | with_skill | without_skill | Delta |
|---|---|---|---|
| Pass rate | 100% ± 0% (100% to 100%) | 28% ± 14% (0% to 33%) | +72 pts |
| Duration | 9.2 s ± 2.2 s (7.7 s to 13.4 s) | 13.5 s ± 3.2 s (10.4 s to 18.7 s) | -4.3 s |
| Fresh input | 6 ± 0 (6 to 6) | 7 ± 1 (6 to 8) | -1 |
| Cache reads | 26,878 ± 83 (26,799 to 26,976) | 31,398 ± 5,587 (26,293 to 36,526) | -4,520 |
| Cache writes | 4,277 ± 191 (4,074 to 4,550) | 3,971 ± 153 (3,772 to 4,170) | +306 |
| Output | 836 ± 200 (645 to 1,125) | 952 ± 113 (851 to 1,137) | -115 |
| Cost | $0.031 ± $0.003 ($0.028 to $0.035) | $0.032 ± $0.002 ($0.029 to $0.035) | -$0.001 |

## Pass Rate By Case

| Case | with_skill | without_skill | Delta |
|---|---|---|---|
| decision-note | 100% ± 0% (100% to 100%) | 33% ± 0% (33% to 33%) | +67 pts |
| nothing-follows | 100% ± 0% (100% to 100%) | 22% ± 19% (0% to 33%) | +78 pts |

## Runs

| Run | Assertions | Duration | Output | Cost | Models | Efforts |
|---|---|---|---|---|---|---|
| decision-note/with_skill/run-1 | 3/3 | 13.4 s | 1,125 | $0.035 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| decision-note/with_skill/run-2 | 3/3 | 9.7 s | 886 | $0.031 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| decision-note/with_skill/run-3 | 3/3 | 8.7 s | 1,001 | $0.033 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| decision-note/without_skill/run-1 | 1/3 | 11.1 s | 1,029 | $0.031 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| decision-note/without_skill/run-2 | 1/3 | 10.4 s | 858 | $0.029 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| decision-note/without_skill/run-3 | 1/3 | 18.7 s | 851 | $0.029 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| nothing-follows/with_skill/run-1 | 3/3 | 8.0 s | 705 | $0.029 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| nothing-follows/with_skill/run-2 | 3/3 | 7.7 s | 656 | $0.028 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| nothing-follows/with_skill/run-3 | 3/3 | 7.7 s | 645 | $0.028 | claude-sonnet-5-5 ×3 | xhigh ×3 |
| nothing-follows/without_skill/run-1 | 1/3 | 11.5 s | 883 | $0.032 | claude-sonnet-5-5 ×4 | xhigh ×4 |
| nothing-follows/without_skill/run-2 | 1/3 | 13.6 s | 1,137 | $0.035 | claude-sonnet-5-5 ×4 | xhigh ×4 |
| nothing-follows/without_skill/run-3 | 0/3 | 15.6 s | 951 | $0.033 | claude-sonnet-5-5 ×4 | xhigh ×4 |

## Notes

- with_skill against without_skill: pass rate +72 pts, cost -$0.001 a run (-3%), duration -4.3 s a run.
- decision-note, assertion 1 ("The note is a file under notes/ named YYYY-MM-DD-<slug>.md, the slug three words at most"): passed in every run of both configurations; it does not tell them apart.
- nothing-follows, assertion 1 ("The note is a file under notes/ named YYYY-MM-DD-<slug>.md, the slug three words at most"): passed in 2 of 3 without_skill runs.
- nothing-follows, assertion 1 ("The note is a file under notes/ named YYYY-MM-DD-<slug>.md, the slug three words at most"): named weak by the grader in 2 of 6 runs: It only requires the YYYY-MM-DD-<slug> pattern and a slug of at most three words. It never requires the date to be today's, so a note dated 2025-01-01 would pass although the expected output says <today>.
