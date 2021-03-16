from pefesens.pefesens_cfg import *
from pefesens.helpers import exec_command_ssh


def pfctlKill(target):
    _, stderr = exec_command_ssh(
        PFSENSE_HOST, PFSENSE_USER, f"pfctl -k {target}"
    )
    # byte object with eol
    return "\n".join(stderr).strip()


def gatewayStatus(gw):
    # lee el socket del dpinger
    if gw == "WANGW":
        gw_sock = PFSENSE_WANGW_SOCK
    elif gw == "SCPCGW":
        gw_sock = PFSENSE_SCPCGW_SOCK
    else:
        return {"rtt": -1, "rttsd": -1, "loss": -1}
    stdout, _ = exec_command_ssh(PFSENSE_HOST, PFSENSE_USER, f"cat {gw_sock}")
    # ej: SCPCGW 570624 5415 0
    _, rtt, rttsd, loss = stdout[0].strip().split()
    return {"rtt": int(rtt) / 1e3, "rttsd": int(rttsd) / 1e3, "loss": int(loss)}


def gatewayLog(gw, nlines=30):
    stdout, _ = exec_command_ssh(
        PFSENSE_HOST,
        PFSENSE_USER,
        f"clog {PFSENSE_GATEWAY_LOGFILE} | grep {gw}| tail -{nlines}",
    )
    return [l.strip() for l in stdout]

