#!/bin/env bash

picom --fading --fade-delta=5 --inactive-opacity=1.0 --inactive-dim=0.05 &
conky &
