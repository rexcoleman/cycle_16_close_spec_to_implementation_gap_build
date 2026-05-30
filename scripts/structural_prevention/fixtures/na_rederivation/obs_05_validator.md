# Validator obligation: number-tagging gate

Every reported number in a verdict MUST be tagged measured/heuristic/inherited. The
number_tagging_gate MUST validate the verdict file and MUST refuse (exit nonzero) when an
untagged number appears in a verdict context. It emits a fire event per check. This is a
runtime-observable enforcement obligation.
