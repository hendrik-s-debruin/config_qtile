#!/bin/env bash

picom --fading --fade-delta=5 --inactive-opacity=1.0 --inactive-dim=0.05 --menu-opacity=1.0 --opacity-rule 90:'name *= "qutebrowser"' &
# conky &
