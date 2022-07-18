# Lazy Publish
v0.1.3

**Why?**\
Because I'm lazy

**What?**\
Java Maven project utilities.
1. `lazyp publish` - build maven project, build docker image and run container:
    - Build Maven project *(OPTIONAL)*\
      `mvn clean install`
    - Stop and remove docker container\
      `docker compose rm -s -f`
    - Remove docker image\
      `docker rmi <IMAGE>`
    - Build and up docker image from Dockerfile\
     `docker compose up --build -d`
    - Start watching logs *(OPTIONAL)*\
     `docker logs <IMAGE> -n 10 -f`
2. `lazyp version` - show maven project version from pom.xml\
   ```
   user@host:~/my-project$ lazyp version
   1.0.4
   ```
3. `lazyp dependency` - show maven project dependencies
   ```
   user@host:~/my-project$ lazyp dependency
   org.projectlombok.lombok: Unknown
   org.postgresql.postgresql: 1.16.3
   org.modelmapper.modelmapper: 3.1.0
   org.mycorp.core.core-root-starter: 1.5.1
   org.mycorp.core.core-std-starter: 1.5.1
   org.mycorp.core.core-redis-starter: 1.5.1
   org.mycorp.core.core-jpa-starter: 1.5.1
   org.mycorp.cmn-gate.cmn-gate-cbonds-api: 1.0.3
   org.springframework.boot.spring-boot-starter-web: Unknown
   org.springframework.boot.spring-boot-starter-data-jpa: Unknown
   org.springframework.boot.spring-boot-starter-actuator: Unknown
   org.springframework.boot.spring-boot-configuration-processor: Unknown
   ```
4. `lazyp check-dependency` - check maven project dependencies
   ```
   user@host:~/my-project$ lazyp check-dependency
   org.projectlombok             lombok                                         in use: Unknown; current: Unknown
   org.postgresql                postgresql                                     in use: 1.16.3; current: Unknown
   org.modelmapper               modelmapper                                    in use: 3.1.0; current: Unknown
   ru.spb.core                   core-root-starter                              in use: 1.5.1; current: 1.5.9
   ru.spb.core                   core-std-starter                               in use: 1.5.1; current: 1.5.9
   ru.spb.core                   core-redis-starter                             in use: 1.5.1; current: 1.5.9
   ru.spb.core                   core-jpa-starter                               in use: 1.5.1; current: 1.5.9
   ru.spb.cmn-gate               cmn-gate-cbonds-api                            1.0.3
   cmn-quotes                    cmn-quotes-raw-saver-api                       in use: 1.0.1; current: 1.1.0
   cmn-quotes                    cmn-quotes-starter                             in use: 1.0.2; current: 1.1.0
   org.springframework.boot      spring-boot-starter-web                        in use: Unknown; current: Unknown
   org.springframework.boot      spring-boot-starter-data-jpa                   in use: Unknown; current: Unknown
   org.springframework.boot      spring-boot-starter-actuator                   in use: Unknown; current: Unknown
   org.springframework.boot      spring-boot-configuration-processor            in use: Unknown; current: Unknown
   ```
   
**Install**
1. Clone git repo and install script:
   ```
   cd <WORK_DIR>
   git clone https://github.com/peyba/lazy-publish.git
   cd lazy-publish/install
   sudo ./install.sh
   ```
2. Set LAZYP_HOME variable on your lazy-publish directory:
   ```
   LAZYP_HOME=<WORK_DIR>/lazy-publish
   export LAZYP_HOME
   ```
   For constant result add this rows to your ~/.profile and run `source ~/.profile`

**Use**\
At your project directory:\
`lp.sz` - run 2 - 4 items from the list. Your project name will be used curren directory name.\
For example, in case: `user@desktop:~/worl/my_project$ lp.sh` **project** will be used as my_your project name.

**Options and flags**
- for `lazyp publish`
  - `-b` flag run `mvn clean install`
  - `-l` flag run `docker logs <IMAGE> -n 10 -f`
  - `-p <IMAGE>` changes the default project name value to the specified one
  - `-i` ignore errors and go on
- for `lazyp version`
  - `--path <path>` change target directory from current to <path>
- for `lazyp dependency`
   - `--path <path>` change target directory from current to <path>
- for `lazyp check-dependency`
   - `--path <path>` change target directory from current to <path>

For more information user --help