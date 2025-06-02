rm src/claw/frontend/Nyan*
rm -rf src/claw/frontend/__pycache__

antlr4 -Dlanguage=Python3 -o src/claw/frontend -lib grammar -package claw.frontend -Xexact-output-dir grammar/NyanLexer.g4
antlr4 -Dlanguage=Python3 -visitor -no-listener -o src/claw/frontend -lib grammar -package claw.frontend -Xexact-output-dir grammar/Nyan.g4
