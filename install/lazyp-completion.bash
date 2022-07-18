#/usr/bin/env bash

_lazyp_version_completions()
{
    local VERSION_OPTS="--help --path"

    COMPREPLY=($(compgen -W "$VERSION_OPTS" -- $cur))
}

_lazyp_find_dependency_completions()
{
    local VERSION_OPTS="--help --path --art-id --group"

    COMPREPLY=($(compgen -W "$VERSION_OPTS" -- $cur))
}

_lazyp_completions()
{
    local COMMANDS="--help --version dependency publish version check-dependency m2-installed find-dependency"

    local cur prev words cword
    _init_completion || return

    case "$prev" in
        lazyp)
            COMPREPLY=($(compgen -W "$COMMANDS" -- $cur))
            ;;
        version)
            _lazyp_version_completions
            ;;
        find-dependency)
            _lazyp_find_dependency_completions
            ;;
    esac
}

complete -F _lazyp_completions lazyp