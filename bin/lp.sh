#!/bin/bash

exit_if_err() {
	if [ "$?" != "0" ]
	then
		if ! [[ -n "${IGNORE_ERRORS:-}" ]]
	        then
	       		exit 1
		fi
	fi
}

PROJECT=${PWD##*/}
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

while getopts ":lbip:" opt; do
  case $opt in
    l)
      LOG=true
      ;;
    b)
      BUILD=true
      ;;
    i)
      IGNORE_ERRORS=true
      ;;
    p)
      PROJECT=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [[ -n "${BUILD:-}" ]]
then
	printf "\n"
	printf "#############################################\n"
	printf " ${RED}run${NC} > ${GREEN}mvn clean install${NC}\n"
	printf "#############################################\n"
	printf "\n"
  mvn --version
	mvn clean install
	exit_if_err
fi

printf "\n"
printf "#############################################\n"
printf " ${RED}run${NC} > ${GREEN}docker compose rm -s -f${NC}\n"
printf "#############################################\n"
printf "\n"

docker compose rm -s -f
exit_if_err

printf "\n"
printf "#############################################\n"
printf " ${RED}run${NC} > ${GREEN}docker rmi ${PROJECT}${NC}\n"
printf "#############################################\n"
printf "\n"

docker rmi ${PROJECT}
exit_if_err

printf "\n"
printf "#############################################\n"
printf " ${RED}run${NC} > ${GREEN}docker compose up --build -d${NC}\n"
printf "#############################################\n"
printf "\n"
docker compose up --build -d
exit_if_err

if [[ -n "${LOG:-}" ]]
then
        printf "\n"
        printf "#############################################\n"
        printf " ${RED}run${NC} > ${GREEN}docker logs ${PROJECT} -n 10 -f${NC}\n"
        printf "#############################################\n"
        printf "\n"

	docker logs ${PROJECT} -n 10 -f
	exit_if_err
fi
