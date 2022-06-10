# lazy-publish

**Why?**\
Because I'm lazy

**What?**\
Java Maven project docker publisher.
1. Build Maven project *(OPTIONAL)*\
`mvn clean install`
2. Stop and remove docker container\
`docker compose rm -s -f`
3. Remove docker image\
`docker rmi <IMAGE>`
4. Build and up docker image from Dockerfile\
`docker compose up --build -d`
5. Start watching logs *(OPTIONAL)*\
`docker logs <IMAGE> -n 10 -f`

**Install**
```
cd <WORK_DIR>
git clone https://github.com/peyba/lazy-publish.git
sudo cp pl.sh /bin
```

**Use**
At your project directory:\
`lp.sz` - run 2 - 4 items from the list. Your project name will be used curren directory name.\
For example, in case: `user@desktop:~/worl/my_project$ lp.sh` **project** will be used as my_your project name.

**Options**\
- `-b` flag run `mvn clean install`
- `-l` flag run `docker logs <IMAGE> -n 10 -f`
- `-p <IMAGE>` changes the default project name value to the specified one