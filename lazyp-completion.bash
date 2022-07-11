#/usr/bin/env bash

_lazyp_version_completions()
{
    local VERSION_OPTS="--help --path"

    COMPREPLY=($(compgen -W "$VERSION_OPTS" -- $cur))
}

_lazyp_completions()
{
    local COMMANDS="--help --version dependency publish version check-dependency"

    local cur prev words cword
    _init_completion || return

    case "$prev" in
        lazyp)
            COMPREPLY=($(compgen -W "$COMMANDS" -- $cur))
            ;;
        version)
            _lazyp_version_completions
            ;;
    esac
}

complete -F _lazyp_completions lazyp