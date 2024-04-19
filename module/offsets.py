# Offsets dumped by: https://github.com/a2x/cs2-dumper

from requests import get

class Offsets:
    try:
        offset = get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json").json()
        client = get("https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client.dll.json").json()

        dwEntityList = offset["client.dll"]["dwEntityList"]
        dwViewMatrix = offset["client.dll"]["dwViewMatrix"]
        dwLocalPlayerPawn = offset["client.dll"]["dwLocalPlayerPawn"]
        dwLocalPlayerController = offset["client.dll"]["dwLocalPlayerController"]
        m_iszPlayerName = client["client.dll"]["classes"]["CBasePlayerController"]["fields"]["m_iszPlayerName"]
        m_iHealth = client["client.dll"]["classes"]["C_BaseEntity"]["fields"]["m_iHealth"]
        m_iTeamNum = client["client.dll"]["classes"]["C_BaseEntity"]["fields"]["m_iTeamNum"]
        m_vOldOrigin = client["client.dll"]["classes"]["C_BasePlayerPawn"]["fields"]["m_vOldOrigin"]
        m_pGameSceneNode = client["client.dll"]["classes"]["C_BaseEntity"]["fields"]["m_pGameSceneNode"]
        m_hPlayerPawn = client["client.dll"]["classes"]["CCSPlayerController"]["fields"]["m_hPlayerPawn"]
        m_iIDEntIndex = client["client.dll"]["classes"]["C_CSPlayerPawnBase"]["fields"]["m_iIDEntIndex"]
    except:
        exit("Error: Invalid offsets, wait for an update")