#!/bin/sh

ssh -C lvuser@roborio-3636.local "rm -r /home/lvuser/py"
scp -r -C ./ lvuser@roborio-3636.local:/home/lvuser/py
ssh -C lvuser@roborio-3636.local "env PATH=/usr/local/natinst/bin:/usr/bin:/bin /usr/local/frc/bin/frcKillRobot.sh -t -r"
