#!/bin/sh
find ./ -name '*.fio' -print | xargs -0 -d '\n' -I % fio --output "%.report"  %
