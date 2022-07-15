#!/bin/bash

cp lazyp-completion.bash /etc/bash_completion.d/lazyp-completion.bash
chmod 644 /etc/bash_completion.d/lazyp-completion.bash
install ../bin/lazyp /bin/lazyp
