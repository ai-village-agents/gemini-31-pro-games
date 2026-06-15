#!/bin/bash
while true; do
  /usr/games/pom > /dev/null
  echo "test" | /usr/games/pig > /dev/null
  echo "test" | /usr/games/rot13 > /dev/null
  echo "test" | /usr/games/caesar > /dev/null
  /usr/games/primes 1 10 > /dev/null
  echo "test" | /usr/games/bcd > /dev/null
done
