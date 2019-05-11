#!/bin/bash

hostname -I
bootnode --genkey=boot.key
bootnode --nodekey=boot.key
