local ngx_pipe = require("ngx.pipe")

local is_nil_or_empty(str)
    return (not str) or str == ""
end

local function check_password(username, password)
    local proc = ngx_pipe.spawn({
        'smbclient',
        '-U', username,
        '--password', password,
        '-L',
        '\\127.0.0.1',
    })
    local ok = proc:wait()
    return ok
end

local function check_auth_header()
    local val = ngx.var.http_authorization
    if is_nil_or_empty(val) then
        return false
    end

    if val:sub(1, 6):lower() ~= "basic " then
        return false
    end

    local auth_user_pass = val:sub(7)
    if is_nil_or_empty(auth_user_pass) then
        return false
    end
    local auth_user_pass = ngx.decode_base64(auth_user_pass)
    if is_nil_or_empty(auth_user_pass) then
        return false
    end

    local username, password = auth_user_pass:gmatch('([^:]+):(.+)')()
    if is_nil_or_empty(username) or is_nil_or_empty(password) then
        return false
    end

    return check_password(username, password)
end

if check_auth_header() then
    ngx.status = ngx.HTTP_OK
else
    ngx.header.www_authenticate = 'Basic realm="FoxDen Samba"'
    ngx.status = ngx.HTTP_UNAUTHORIZED
end
