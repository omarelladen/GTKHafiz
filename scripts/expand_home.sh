expand_home()
{
    _PATH="$1"

    case "$_PATH" in
        "~"|"~"/*)
            _PATH="/home/${SUDO_USER:-$USER}${_PATH#\~}" ;;
    esac

    echo "$_PATH"
}
